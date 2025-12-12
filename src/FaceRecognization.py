"""
Face Recognition Attendance System - WITH LIVE CAMERA FEED IN GUI
A GUI application for real-time face detection and recognition using OpenCV and MySQL
"""

import os
from tkinter import Tk, Label, Button, Frame
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import threading
from datetime import datetime
import mysql.connector
from contextlib import contextmanager
from time import strftime, localtime


class FaceRecognitionSystem:
    """Main class for Face Recognition Attendance System"""
    
    def __init__(self, root):
        """
        Initialize the Face Recognition System GUI
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self._setup_window()
        
        # Configuration constants
        self.DB_CONFIG = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'face_recognizer'
        }
        
        # Face detection parameters
        self.SCALE_FACTOR = 1.1
        self.MIN_NEIGHBORS = 5
        self.CONFIDENCE_THRESHOLD = 50
        
        # File paths
        self.HAARCASCADE_PATH = "haarcascade_frontalface_default.xml"
        self.CLASSIFIER_PATH = "classifier.xml"
        
        # Camera variables
        self.video_capture = None
        self.is_running = False
        self.face_cascade = None
        self.clf = None
        
        # Error tracking
        self.last_error_time = 0
        self.ERROR_COOLDOWN = 5
        
        # Setup UI after variables are initialized
        self._setup_ui()
    
    def _setup_window(self):
        """Configure the main window properties"""
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition Attendance System")
        self.root.configure(bg="#0a0e27")
    
    def _setup_ui(self):
        """Setup all UI components"""
        self._create_title()
        self._create_video_panel()
        self._create_buttons()
    
    def _create_title(self):
        """Create and place the title label"""
        title_lbl = Label(
            self.root,
            text="FACE RECOGNITION ATTENDANCE SYSTEM",
            font=("Times New Roman", 35, "bold"),
            bg="#0a0e27",
            fg="white"
        )
        title_lbl.place(x=0, y=0, width=1530, height=45)
    
    def _create_video_panel(self):
        """Create the main video display panel"""
        # Create a frame for the video
        self.video_frame = Frame(self.root, bg="#1a1e37")
        self.video_frame.place(x=50, y=70, width=1430, height=500)
        
        # Create label to display video feed
        self.video_label = Label(
            self.video_frame,
            bg="#1a1e37",
            text="Camera feed will appear here\n\nClick 'Start Recognition' to begin",
            fg="white",
            font=("Arial", 20)
        )
        self.video_label.pack(fill="both", expand=True)
        
        # Create status label
        self.status_label = Label(
            self.root,
            text="Status: Camera Off",
            font=("Arial", 14),
            bg="#0a0e27",
            fg="#4a90e2"
        )
        self.status_label.place(x=50, y=590, width=400, height=30)
        
        # Create info panel
        self.info_label = Label(
            self.root,
            text="Ready to start",
            font=("Arial", 12),
            bg="#0a0e27",
            fg="white",
            justify="left"
        )
        self.info_label.place(x=50, y=630, width=1430, height=100)
    
    def _create_buttons(self):
        """Create control buttons"""
        button_y = 500
        
        # Start button
        self.btn_start = Button(
            self.root,
            text="Start Recognition",
            command=self.start_face_recognition,
            cursor="hand2",
            font=("Times New Roman", 16, "bold"),
            bg="#4a90e2",
            fg="white",
            activebackground="#357abd",
            activeforeground="white"
        )
        self.btn_start.place(x=500, y=button_y, width=200, height=40)
        
        # Stop button
        self.btn_stop = Button(
            self.root,
            text="Stop Recognition",
            command=self.stop_face_recognition,
            cursor="hand2",
            font=("Times New Roman", 16, "bold"),
            bg="#e24a4a",
            fg="white",
            activebackground="#bd3737",
            activeforeground="white",
            state="disabled"
        )
        self.btn_stop.place(x=720, y=button_y, width=200, height=40)
    
    @contextmanager
    def _get_db_connection(self):
        """
        Context manager for database connections
        Ensures proper connection cleanup
        
        Yields:
            tuple: (connection, cursor) objects
        """
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.DB_CONFIG)
            cursor = conn.cursor()
            yield conn, cursor
        except mysql.connector.Error as e:
            print(f"Database connection error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def _show_error_throttled(self, title, message):
        """
        Show error message with cooldown to prevent spam
        
        Args:
            title: Error dialog title
            message: Error message
        """
        import time
        current_time = time.time()
        
        if current_time - self.last_error_time > self.ERROR_COOLDOWN:
            messagebox.showerror(title, message)
            self.last_error_time = current_time
        else:
            print(f"{title}: {message}")
    
    def _fetch_student_info(self, student_id):
        """
        Fetch student information from database
        
        Args:
            student_id: The student's ID number
            
        Returns:
            dict: Student information (name, roll_no, department) or None if not found
        """
        try:
            with self._get_db_connection() as (conn, cursor):
                query = """
                    SELECT name, roll_no, department 
                    FROM student 
                    WHERE student_id = %s
                """
                cursor.execute(query, (student_id,))
                result = cursor.fetchone()
                
                if result:
                    return {
                        'name': result[0],
                        'roll_no': result[1],
                        'department': result[2]
                    }
                return None
        except Exception as e:
            print(f"Error fetching student info: {e}")
            return None
    
    def _draw_face_boundary(self, img, classifier, clf):
        """
        Detect faces and draw bounding boxes with student information
        
        Args:
            img: Input image frame
            classifier: Haar Cascade classifier for face detection
            clf: LBPH face recognizer
            
        Returns:
            tuple: (processed_image, detection_info_text)
        """
        detection_info = []
        
        try:
            # Convert to grayscale for better face detection
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Detect faces in the image
            faces = classifier.detectMultiScale(
                gray_image,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            if len(faces) > 0:
                detection_info.append(f"✓ Detected {len(faces)} face(s)")
            
            for (x, y, w, h) in faces:
                try:
                    # Extract face region for recognition
                    face_roi = gray_image[y:y + h, x:x + w]
                    
                    # Predict the face ID and confidence
                    student_id, prediction = clf.predict(face_roi)
                    
                    # Calculate confidence percentage (higher is better)
                    confidence = int(100 * (1 - prediction / 300))
                    
                    # Check if confidence meets threshold
                    if confidence > self.CONFIDENCE_THRESHOLD:
                        # Fetch student information from database
                        student_info = self._fetch_student_info(student_id)
                        
                        if student_info:
                            # Draw green rectangle for recognized face
                            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                            
                            # Display student information above the face
                            self._draw_text(img, f"Name: {student_info['name']}", x, y - 75)
                            self._draw_text(img, f"Roll: {student_info['roll_no']}", x, y - 55)
                            self._draw_text(img, f"Dept: {student_info['department']}", x, y - 35)
                            self._draw_text(img, f"Confidence: {confidence}%", x, y - 15)
                            self.mark_attendence(student_id, student_info['roll_no'], student_info['department'], student_info['name'])

                            
                            detection_info.append(
                                f"✓ Recognized: {student_info['name']} "
                                f"(ID: {student_id}, Confidence: {confidence}%)"
                            )
                        else:
                            # Student ID not found in database
                            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 165, 255), 3)
                            self._draw_text(img, f"ID {student_id} Not in DB", x, y - 35)
                            self._draw_text(img, f"Confidence: {confidence}%", x, y - 15)
                           
                            
                            detection_info.append(
                                f"⚠ Face detected (ID: {student_id}) but not in database"
                            )
                    else:
                        # Low confidence - unknown face
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                        self._draw_text(img, "Unknown Face", x, y - 55)
                        self._draw_text(img, f"ID: {student_id}", x, y - 35)
                        self._draw_text(img, f"Confidence: {confidence}%", x, y - 15)
                        
                        detection_info.append(
                            f"✗ Low confidence: {confidence}% (threshold: {self.CONFIDENCE_THRESHOLD}%)"
                        )
                
                except Exception as e:
                    print(f"Error processing face at ({x}, {y}): {e}")
                    continue
            
            info_text = "\n".join(detection_info) if detection_info else "No faces detected"
            return img, info_text
            
        except Exception as e:
            print(f"Error in face boundary detection: {e}")
            return img, f"Error: {str(e)}"
    
    def _draw_text(self, img, text, x, y):
        """
        Helper method to draw text with consistent styling
        
        Args:
            img: Image to draw on
            text: Text to display
            x, y: Position coordinates
        """
        cv2.putText(
            img, 
            text, 
            (x, y), 
            cv2.FONT_HERSHEY_COMPLEX, 
            0.8, 
            (255, 255, 255), 
            2
        )
    
    def _process_frame(self):
        """Process video frames continuously"""
        while self.is_running:
            try:
                ret, frame = self.video_capture.read()
                
                if not ret:
                    print("Failed to grab frame")
                    break
                
                # Process frame for face recognition
                processed_frame, info_text = self._draw_face_boundary(
                    frame, 
                    self.face_cascade, 
                    self.clf
                )
                
                # Convert to RGB for tkinter
                frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                
                # Resize to fit the display area (1430x500)
                frame_resized = cv2.resize(frame_rgb, (1430, 500))
                
                # Convert to PhotoImage
                img = Image.fromarray(frame_resized)
                imgtk = ImageTk.PhotoImage(image=img)
                
                # Update the video label
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk, text="")
                
                # Update info label
                self.info_label.configure(text=info_text)
                
            except Exception as e:
                print(f"Error in frame processing: {e}")
                break
    
    def start_face_recognition(self):
        """Start the face recognition process using webcam"""
        # Verify required files exist
        if not os.path.exists(self.HAARCASCADE_PATH):
            messagebox.showerror(
                "File Not Found",
                f"Haar Cascade file not found: {self.HAARCASCADE_PATH}\n\n"
                f"Please download it from OpenCV GitHub repository."
            )
            return
        
        if not os.path.exists(self.CLASSIFIER_PATH):
            messagebox.showerror(
                "File Not Found",
                f"Classifier file not found: {self.CLASSIFIER_PATH}\n"
                "Please train the model first."
            )
            return
        
        try:
            # Load the Haar Cascade classifier for face detection
            self.face_cascade = cv2.CascadeClassifier(self.HAARCASCADE_PATH)
            
            if self.face_cascade.empty():
                messagebox.showerror(
                    "Classifier Error",
                    "Failed to load Haar Cascade classifier. File may be corrupted."
                )
                return
            
            # Load the trained LBPH face recognizer
            self.clf = cv2.face.LBPHFaceRecognizer_create()
            self.clf.read(self.CLASSIFIER_PATH)
            
            # Initialize webcam (0 is default camera)
            self.video_capture = cv2.VideoCapture(0)
            
            if not self.video_capture.isOpened():
                messagebox.showerror("Camera Error", "Could not access the camera")
                return
            
            # Update status
            self.is_running = True
            self.status_label.configure(text="Status: Camera Active - Recognizing Faces", fg="#4ae24a")
            self.btn_start.configure(state="disabled")
            self.btn_stop.configure(state="normal")
            
            # Start processing in a separate thread
            self.processing_thread = threading.Thread(target=self._process_frame, daemon=True)
            self.processing_thread.start()
            
            print("Face recognition started.")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during initialization: {str(e)}")
            print(f"Error details: {e}")
    
    def stop_face_recognition(self):
        """Stop the face recognition process"""
        self.is_running = False
        
        if self.video_capture is not None:
            self.video_capture.release()
        
        # Reset video label
        self.video_label.configure(
            image="",
            text="Camera Stopped\n\nClick 'Start Recognition' to begin again"
        )
        
        # Update status
        self.status_label.configure(text="Status: Camera Off", fg="#4a90e2")
        self.info_label.configure(text="Ready to start")
        
        # Update buttons
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")
        
        print("Face recognition stopped.")

    def mark_attendence(self, student_id, roll, department, name):
       

        file_path = "attendance.csv"

        # Create file if missing
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write("StudentID,Name,Roll,Department,Time,Date,Status")

        # Read existing attendance
        with open(file_path, "r") as f:
            data = f.readlines()
            existing = []
            for line in data:
                values = line.strip().split(",")
                if len(values) >= 6:
                    existing.append((values[0], values[5]))  # (student_id, date)

        now = datetime.now()
        date_today = now.strftime("%d/%m/%Y")
        time_now = now.strftime("%H:%M:%S")

        # Check duplicate attendance
        if (str(student_id), date_today) in existing:
            print(f"Attendance already marked today for ID: {student_id}")
            return

        # Append attendance
        with open(file_path, "a") as f:
            f.write(f"\n{student_id},{name},{roll},{department},{time_now},{date_today},Present")

        print(f"Attendance marked: {student_id} - {name}")





def main():
    """Main entry point for the application"""
    root = Tk()
    app = FaceRecognitionSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()