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
        self.CONFIDENCE_THRESHOLD = 86  # Increased from 50 to 70 for better accuracy
        
        # ====== FIXED: Get absolute paths ======
        # Get the directory where this script is located
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        
        # File paths - now using absolute paths
        self.HAARCASCADE_PATH = os.path.join(self.BASE_DIR, "haarcascade_frontalface_default.xml")
        self.CLASSIFIER_PATH = os.path.join(self.BASE_DIR, "classifier.xml")
        self.ATTENDANCE_PATH = os.path.join(self.BASE_DIR, "attendance.csv")
        
        # Print paths for debugging
        print("=" * 60)
        print("FILE PATHS:")
        print(f"Base Directory: {self.BASE_DIR}")
        print(f"Haarcascade: {self.HAARCASCADE_PATH}")
        print(f"Classifier: {self.CLASSIFIER_PATH}")
        print(f"Attendance: {self.ATTENDANCE_PATH}")
        print("=" * 60)
        
        # Check if files exist
        print("\nFILE STATUS:")
        print(f"Haarcascade exists: {os.path.exists(self.HAARCASCADE_PATH)}")
        print(f"Classifier exists: {os.path.exists(self.CLASSIFIER_PATH)}")
        print("=" * 60)
        
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
        self._create_debug_info()
    
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
        self.info_label.place(x=50, y=630, width=1430, height=60)
    
    def _create_debug_info(self):
        """Create debug information panel"""
        debug_text = f"Working Directory: {os.getcwd()}\n"
        debug_text += f"Script Directory: {self.BASE_DIR}\n"
        debug_text += f"Haarcascade: {'✓ Found' if os.path.exists(self.HAARCASCADE_PATH) else '✗ Missing'}\n"
        debug_text += f"Classifier: {'✓ Found' if os.path.exists(self.CLASSIFIER_PATH) else '✗ Missing - Train model first'}"
        
        self.debug_label = Label(
            self.root,
            text=debug_text,
            font=("Courier", 9),
            bg="#0a0e27",
            fg="#888888",
            justify="left"
        )
        self.debug_label.place(x=50, y=695, width=1430, height=60)
    
    def _create_buttons(self):
        """Create control buttons"""
        button_frame = Frame(self.root, bg="#0a0e27")
        button_frame.place(x=350, y=580, width=850, height=50)
        
        # Start button
        self.btn_start = Button(
            button_frame,
            text="▶ Start Recognition",
            command=self.start_face_recognition,
            cursor="hand2",
            font=("Times New Roman", 14, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#1e8449",
            activeforeground="white"
        )
        self.btn_start.pack(side="left", padx=8, ipadx=15, ipady=5)
        
        # Stop button
        self.btn_stop = Button(
            button_frame,
            text="⬛ Stop Recognition",
            command=self.stop_face_recognition,
            cursor="hand2",
            font=("Times New Roman", 14, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            state="disabled"
        )
        self.btn_stop.pack(side="left", padx=8, ipadx=15, ipady=5)
        
        # Check Files button
        self.btn_check = Button(
            button_frame,
            text="🔍 Check Files",
            command=self.check_files,
            cursor="hand2",
            font=("Times New Roman", 14, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white"
        )
        self.btn_check.pack(side="left", padx=8, ipadx=15, ipady=5)
        
        # Settings button
        self.btn_settings = Button(
            button_frame,
            text="⚙ Settings",
            command=self.show_settings,
            cursor="hand2",
            font=("Times New Roman", 14, "bold"),
            bg="#9b59b6",
            fg="white",
            activebackground="#8e44ad",
            activeforeground="white"
        )
        self.btn_settings.pack(side="left", padx=8, ipadx=15, ipady=5)
    
    def check_files(self):
        """Check if required files exist and show detailed info"""
        message = "FILE CHECK RESULTS:\n\n"
        
        # Check haarcascade
        if os.path.exists(self.HAARCASCADE_PATH):
            message += f"✓ Haarcascade file found\n  Path: {self.HAARCASCADE_PATH}\n\n"
        else:
            message += f"✗ Haarcascade file NOT FOUND\n  Expected path: {self.HAARCASCADE_PATH}\n"
            message += f"  Download from: https://github.com/opencv/opencv/tree/master/data/haarcascades\n\n"
        
        # Check classifier
        if os.path.exists(self.CLASSIFIER_PATH):
            message += f"✓ Classifier file found\n  Path: {self.CLASSIFIER_PATH}\n\n"
        else:
            message += f"✗ Classifier file NOT FOUND\n  Expected path: {self.CLASSIFIER_PATH}\n"
            message += f"  You need to train the model first using the training module\n\n"
        
        # Check current directory contents
        message += f"\nFILES IN CURRENT DIRECTORY ({self.BASE_DIR}):\n"
        try:
            files = os.listdir(self.BASE_DIR)
            xml_files = [f for f in files if f.endswith('.xml')]
            if xml_files:
                message += "XML Files found:\n"
                for f in xml_files:
                    message += f"  - {f}\n"
            else:
                message += "  No XML files found in this directory\n"
        except Exception as e:
            message += f"  Error reading directory: {e}\n"
        
        messagebox.showinfo("File Check", message, parent=self.root)
    
    def show_settings(self):
        """Show settings dialog to adjust confidence threshold"""
        from tkinter import Toplevel, Scale, HORIZONTAL
        
        settings_window = Toplevel(self.root)
        settings_window.title("Recognition Settings")
        settings_window.geometry("500x300+500+300")
        settings_window.configure(bg="#1a1e37")
        settings_window.resizable(False, False)
        
        # Title
        title = Label(
            settings_window,
            text="⚙ Recognition Settings",
            font=("Arial", 18, "bold"),
            bg="#1a1e37",
            fg="white"
        )
        title.pack(pady=20)
        
        # Info label
        info = Label(
            settings_window,
            text="Adjust the confidence threshold to improve accuracy\n\n"
                 "Higher values = More strict (fewer false positives)\n"
                 "Lower values = More lenient (may recognize wrong faces)",
            font=("Arial", 10),
            bg="#1a1e37",
            fg="#cccccc",
            justify="left"
        )
        info.pack(pady=10)
        
        # Current threshold label
        current_label = Label(
            settings_window,
            text=f"Current Threshold: {self.CONFIDENCE_THRESHOLD}%",
            font=("Arial", 12, "bold"),
            bg="#1a1e37",
            fg="#4ae24a"
        )
        current_label.pack(pady=10)
        
        # Slider
        def update_threshold(val):
            self.CONFIDENCE_THRESHOLD = int(val)
            current_label.config(text=f"Current Threshold: {self.CONFIDENCE_THRESHOLD}%")
            
            # Visual feedback
            if int(val) < 60:
                current_label.config(fg="#e74c3c")  # Red - too lenient
                recommendation.config(text="⚠ Warning: Low threshold may cause false recognitions")
            elif int(val) < 75:
                current_label.config(fg="#f39c12")  # Orange - moderate
                recommendation.config(text="✓ Moderate threshold - balanced accuracy")
            else:
                current_label.config(fg="#4ae24a")  # Green - strict
                recommendation.config(text="✓ High threshold - strict recognition")
        
        slider = Scale(
            settings_window,
            from_=30,
            to=95,
            orient=HORIZONTAL,
            command=update_threshold,
            length=350,
            bg="#1a1e37",
            fg="white",
            troughcolor="#0a0e27",
            highlightthickness=0,
            font=("Arial", 10)
        )
        slider.set(self.CONFIDENCE_THRESHOLD)
        slider.pack(pady=10)
        
        # Recommendation label
        recommendation = Label(
            settings_window,
            text="✓ High threshold - strict recognition",
            font=("Arial", 9, "italic"),
            bg="#1a1e37",
            fg="#4ae24a"
        )
        recommendation.pack(pady=5)
        
        # Close button
        close_btn = Button(
            settings_window,
            text="Save & Close",
            command=settings_window.destroy,
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            activebackground="#1e8449"
        )
        close_btn.pack(pady=15, ipadx=20, ipady=5)
    
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
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
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
                    face_roi = gray_image[y:y + h, x:x + w]
 
                    # LBPH predict() returns (label, distance)
                    # LOWER distance = BETTER match  (0 = perfect, 100+ = poor)
                    # FIXED: removed broken formula (1 - prediction/300)
                    student_id, prediction = clf.predict(face_roi)
 
                    print(f"Face detected - ID: {student_id}, LBPH Distance: {prediction:.1f}")
 
                    if prediction < 50:
                        # ✅ HIGH CONFIDENCE — strict match, mark attendance
                        confidence = int(100 * (1 - prediction / 100))
                        student_info = self._fetch_student_info(student_id)
 
                        if student_info:
                            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                            text_y_start = y + h + 25
                            self._draw_text(img, f"Name: {student_info['name']}",       x, text_y_start)
                            self._draw_text(img, f"Roll: {student_info['roll_no']}",    x, text_y_start + 25)
                            self._draw_text(img, f"Dept: {student_info['department']}", x, text_y_start + 50)
                            self._draw_text(img, f"Confidence: {confidence}%",          x, text_y_start + 75)
                            self.mark_attendence(
                                student_id,
                                student_info['roll_no'],
                                student_info['department'],
                                student_info['name']
                            )
                            detection_info.append(
                                f"✓ Recognized: {student_info['name']} "
                                f"(ID: {student_id}, Distance: {prediction:.1f})"
                            )
                        else:
                            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 165, 255), 3)
                            text_y_start = y + h + 25
                            self._draw_text(img, f"ID {student_id} Not in DB", x, text_y_start)
                            self._draw_text(img, f"Distance: {prediction:.1f}",  x, text_y_start + 25)
                            detection_info.append(
                                f"⚠ Face detected (ID: {student_id}) but not in database"
                            )
 
                    elif prediction < 80:
                        # ⚠ UNCERTAIN — possible match, not confident enough
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 165, 255), 3)
                        text_y_start = y + h + 25
                        self._draw_text(img, "Uncertain Match",             x, text_y_start)
                        self._draw_text(img, f"Distance: {prediction:.1f}", x, text_y_start + 25)
                        detection_info.append(
                            f"⚠ Uncertain: Distance {prediction:.1f} (need < 50 to recognize)"
                        )
 
                    else:
                        # ✗ UNKNOWN FACE — too different from any trained face
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                        text_y_start = y + h + 25
                        self._draw_text(img, "Unknown Face",                x, text_y_start)
                        self._draw_text(img, f"Distance: {prediction:.1f}", x, text_y_start + 25)
                        detection_info.append(
                            f"✗ Unknown face: Distance {prediction:.1f} (too high)"
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
                f"Haar Cascade file not found!\n\n"
                f"Expected location:\n{self.HAARCASCADE_PATH}\n\n"
                f"Current directory:\n{os.getcwd()}\n\n"
                f"Please ensure the file is in the same directory as this script.\n\n"
                f"Download from:\nhttps://github.com/opencv/opencv/tree/master/data/haarcascades",
                parent=self.root
            )
            return
        
        if not os.path.exists(self.CLASSIFIER_PATH):
            messagebox.showerror(
                "File Not Found",
                f"Classifier file not found!\n\n"
                f"Expected location:\n{self.CLASSIFIER_PATH}\n\n"
                "You need to train the model first before running face recognition.\n"
                "Please run the training module to generate classifier.xml",
                parent=self.root
            )
            return
        
        try:
            # Load the Haar Cascade classifier for face detection
            self.face_cascade = cv2.CascadeClassifier(self.HAARCASCADE_PATH)
            
            if self.face_cascade.empty():
                messagebox.showerror(
                    "Classifier Error",
                    "Failed to load Haar Cascade classifier. File may be corrupted.\n"
                    "Try re-downloading the file.",
                    parent=self.root
                )
                return
            
            # Load the trained LBPH face recognizer
            self.clf = cv2.face.LBPHFaceRecognizer_create()
            self.clf.read(self.CLASSIFIER_PATH)
            
            # Initialize webcam (0 is default camera)
            self.video_capture = cv2.VideoCapture(0)
            
            if not self.video_capture.isOpened():
                messagebox.showerror("Camera Error", "Could not access the camera", parent=self.root)
                return
            
            # Update status
            self.is_running = True
            self.status_label.configure(text="Status: Camera Active - Recognizing Faces", fg="#4ae24a")
            self.btn_start.configure(state="disabled")
            self.btn_stop.configure(state="normal")
            self.btn_check.configure(state="disabled")
            
            # Start processing in a separate thread
            self.processing_thread = threading.Thread(target=self._process_frame, daemon=True)
            self.processing_thread.start()
            
            print("Face recognition started.")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during initialization:\n\n{str(e)}", parent=self.root)
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
        self.btn_check.configure(state="normal")
        
        print("Face recognition stopped.")

    def mark_attendence(self, student_id, roll, department, name):
        """Mark student attendance in CSV file"""
        # FIXED: header ends with \n so first data row is not glued to it
        if not os.path.exists(self.ATTENDANCE_PATH):
            with open(self.ATTENDANCE_PATH, "w") as f:
                f.write("StudentID,Name,Roll,Department,Time,Date,Status\n")
 
        # FIXED: use set() for O(1) duplicate lookup
        existing = set()
        with open(self.ATTENDANCE_PATH, "r") as f:
            lines = f.readlines()
            for line in lines[1:]:   # skip header
                values = line.strip().split(",")
                if len(values) >= 6:
                    existing.add((values[0], values[5]))  # (student_id, date)
 
        now        = datetime.now()
        date_today = now.strftime("%d/%m/%Y")
        time_now   = now.strftime("%H:%M:%S")
 
        if (str(student_id), date_today) in existing:
            print(f"Attendance already marked today for ID: {student_id}")
            return
 
        # FIXED: \n at END of line, not beginning
        with open(self.ATTENDANCE_PATH, "a") as f:
            f.write(f"{student_id},{name},{roll},{department},{time_now},{date_today},Present\n")
 
        print(f"✓ Attendance marked: {student_id} - {name} at {time_now}")

def main():
    """Main entry point for the application"""
    root = Tk()
    app = FaceRecognitionSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()