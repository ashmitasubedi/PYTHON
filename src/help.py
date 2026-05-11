from tkinter import *
from tkinter import messagebox
import os
import tkinter.messagebox
from tkinter import ttk
import tkinter
import mysql.connector
import cv2
from PIL import Image, ImageTk

class Help:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Help Desk")
        
        # Color scheme
        self.colors = {
            'bg_dark': '#0a0e27',
            'bg_card': '#1a1f3a',
            'primary': '#4a90e2',
            'primary_hover': '#357abd',
            'accent': '#e74c3c',
            'text_light': '#ffffff',
            'text_secondary': '#b8bcc8',
            'success': '#2ecc71',
            'warning': '#f39c12'
        }
        
        # Title
        title_lbl = Label(self.root, text="HELP DESK", font=(
            "times new roman", 35, "bold"), bg="white", fg="blue")
        title_lbl.place(x=0, y=0, width=1530, height=45)
        
        # Main frame with background
        main_frame = Frame(self.root, bg="white")
        main_frame.place(x=0, y=55, width=1530, height=735)
        
        # Try to load background image, if not available use solid color
        try:
            img_top = Image.open("photos/help.jpg")
            img_top = img_top.resize((1530, 735), Image.LANCZOS)
            self.photoimg_top = ImageTk.PhotoImage(img_top)
            bg_lbl = Label(main_frame, image=self.photoimg_top)
            bg_lbl.place(x=0, y=0, width=1530, height=735)
        except:
            main_frame.config(bg=self.colors['bg_dark'])
        
        # Help content frame
        content_frame = Frame(main_frame, bg="white", bd=2, relief=RIDGE)
        content_frame.place(x=100, y=50, width=1330, height=630)
        
        # Help heading
        help_title = Label(content_frame, text="How Can We Help You?", 
                          font=("times new roman", 28, "bold"), 
                          bg="white", fg=self.colors['primary'])
        help_title.pack(pady=20)
        
        # Info frame with scrollbar
        info_frame = Frame(content_frame, bg="white")
        info_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = Scrollbar(info_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Text widget for help content
        help_text = Text(info_frame, font=("times new roman", 12), 
                        bg="white", fg="black", wrap=WORD, 
                        yscrollcommand=scrollbar.set, spacing1=5, spacing3=5)
        help_text.pack(fill=BOTH, expand=True)
        scrollbar.config(command=help_text.yview)
        
        # Help content
        help_content = """
        WELCOME TO THE HELP DESK
        
        This application provides comprehensive support for face recognition system management.
        
        📋 KEY FEATURES:
        
        • Student Management: Add, update, and delete student records with photo capture
        • Face Recognition: Real-time face detection and recognition system
        • Attendance Tracking: Automated attendance marking with timestamp
        • Train Data: Train the face recognition model with collected photos
        • Photo Management: Organize and manage student photo database
        
        🔧 HOW TO USE:
        
        1. STUDENT DETAILS:
           - Navigate to Student Details section
           - Fill in all required information (Department, Course, Year, etc.)
           - Click 'Take Photo Sample' to capture student photos
           - Save the information to database
        
        2. TRAIN DATA:
           - After adding students, go to Train Data section
           - Click 'Train Data' button to train the face recognition model
           - Wait for training completion message
        
        3. FACE RECOGNITION:
           - Open Face Recognition section
           - The system will automatically detect and recognize faces
           - Press 'q' to exit the recognition window
        
        4. ATTENDANCE:
           - View and export attendance records
           - Data is stored with date and time stamps
           - Export to CSV for external analysis
        
        ⚙️ SYSTEM REQUIREMENTS:
        
        • Python 3.7 or higher
        • OpenCV library (cv2)
        • MySQL database
        • PIL (Python Imaging Library)
        • Tkinter (usually comes with Python)
        
        📞 SUPPORT:
        
        For technical support or inquiries, please contact:
        Email: subediashmita848@gmail.com
        
        💡 TIPS:
        
        • Ensure good lighting when capturing photos
        • Take multiple photos from different angles
        • Keep the database regularly updated
        • Train the model after adding new students
        • Backup your database periodically
        
        🔒 SECURITY:
        
        • All data is stored securely in MySQL database
        • Face recognition uses advanced algorithms
        • Attendance records are timestamped and cannot be modified manually
        
        Thank you for using our Face Recognition Attendance System!
        """
        
        help_text.insert(1.0, help_content)
        help_text.config(state=DISABLED)  # Make text read-only
        
        # Contact information at bottom
        contact_frame = Frame(main_frame, bg=self.colors['primary'], bd=2, relief=RAISED)
        contact_frame.place(x=100, y=680, width=1330, height=50)
        
        contact_label = Label(contact_frame, 
                            text="📧 Contact: subediashmita848@gmail.com | 💬 Need assistance? We're here to help!", 
                            font=("times new roman", 14, "bold"), 
                            bg=self.colors['primary'], 
                            fg="white")
        contact_label.pack(pady=12)

if __name__ == "__main__":
    root = Tk()
    obj = Help(root)
    root.mainloop()