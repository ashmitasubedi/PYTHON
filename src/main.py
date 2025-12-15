from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import os
from student import Student
from train import train
from FaceRecognization import FaceRecognitionSystem
import tkinter.messagebox
import tkinter.messagebox as messagebox
from help import Help
from time import strftime
from datetime import datetime

class Face_Recognition_System:
    def __init__(self, root):#CONSTUUCTOR CALLED root represents the main Tkinter window
        self.root = root
        self.root.geometry("1530x790+0+0")#SETTING THE GEOMETRY OF THE WINDOW
        self.root.title("Face Recognition Attendance System")
        self.root.configure(bg="#0a0e27")
        
        # Color scheme
        self.colors = {# Custom color palette aafaile create gareko colors 
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

        # Create main canvas for gradient background A Canvas is used to draw shapes / lines.
        self.canvas = Canvas(self.root, width=1530, height=790, 
                           bg=self.colors['bg_dark'], highlightthickness=0)#
        self.canvas.place(x=0, y=0)
        
        # Create gradient background
        self.create_gradient_bg()
        
        header_frame = Frame(self.root, bg="#1a1f3a", height=100)
        header_frame.place(x=0, y=0, width=1530, height=100)

        # Add shadow effect to header
        shadow = Frame(self.root, bg="#000000", height=3)
        shadow.place(x=0, y=100, width=1530, height=3)

        # Title container (LEFT SIDE)
        title_frame = Frame(header_frame, bg="#1a1f3a")
        title_frame.place(x=50, y=20)  # Changed to absolute positioning

        # Main Title
        title_lbl = Label(
            title_frame,
            text="🎯 FACE RECOGNITION ATTENDANCE SYSTEM",
            font=("Segoe UI", 36, "bold"),
            bg="#1a1f3a",
            fg="#ffffff"
        )
        title_lbl.pack()

        # Subtitle
        subtitle_lbl = Label(
            title_frame,
            text="Advanced AI-Powered Recognition & Tracking",
            font=("Segoe UI", 12),
            bg="#1a1f3a",
            fg="#b8bcc8"
        )
        subtitle_lbl.pack()

        # CLOCK SECTION (RIGHT SIDE) -
        # Create clock frame
        clock_frame = Frame(header_frame, bg="#2a3f5a", bd=2, relief=RIDGE)
        clock_frame.place(x=1150, y=20, width=220, height=60)

        # Time label
        self.time_label = Label(
            clock_frame,
            text="00:00:00 AM",
            font=("Digital-7", 18, "bold"),  # Digital font style
            bg="#2a3f5a",
            fg="#00ff00"  # Bright green like digital clock
        )
        self.time_label.pack(pady=2)

        # Date label
        self.date_label = Label(
            clock_frame,
            text="01-01-2025",
            font=("Segoe UI", 10),
            bg="#2a3f5a",
            fg="#ffffff"
        )
        self.date_label.pack()

        # Clock update function
        def update_clock():
            time_string = strftime('%I:%M:%S %p')
            date_string = strftime('%d-%m-%Y')
            self.time_label.config(text=time_string)
            self.date_label.config(text=date_string)
            self.time_label.after(1000, update_clock)

        # Start the clock
        update_clock()
            # ========= Main Content Area =========
        #All the big modern buttons appear inside this frame.
        content_frame = Frame(self.root, bg=self.colors['bg_dark'])
        content_frame.place(x=50, y=100, width=1330, height=600)

        # Button data with colors
        self.buttons_data = [
            {
                'text': 'STUDENT DETAILS',
                'icon': '👥',
                'color': '#4a90e2',
                'hover': '#357abd',
                'command': self.student_details,
                'row': 0, 'col': 0
            },
            {
                'text': 'FACE RECOGNITION',
                'icon': '🎭',
                'color': '#9b59b6',
                'hover': '#8e44ad',
                'command': self.face_recognition,
                'row': 0, 'col': 1
            },
            {
                'text': 'ATTENDANCE',
                'icon': '📋',
                'color': '#2ecc71',
                'hover': '#27ae60',
                'command': self.attendance,
                'row': 0, 'col': 2
            },
            {
                'text': 'HELP DESK',
                'icon': '💬',
                'color': '#f39c12',
                'hover': '#e67e22',
                'command': self.help_desk,
                'row': 0, 'col': 3
            },
            {
                'text': 'TRAIN DATA',
                'icon': '🧠',
                'color': '#1abc9c',
                'hover': '#16a085',
                'command': self.train_data,
                'row': 1, 'col': 0
            },
            {
                'text': 'PHOTOS',
                'icon': '📸',
                'color': '#e91e63',
                'hover': '#c2185b',
                'command': lambda: self.open_img("data", 1),
                'row': 1, 'col': 1
            },
            {
                'text': 'DEVELOPER',
                'icon': '👨‍💻',
                'color': '#607d8b',
                'hover': '#455a64',
                'command': self.developer,
                'row': 1, 'col': 2
            },
            {
                'text': 'EXIT',
                'icon': '🚪',
                'color': '#e74c3c',
                'hover': '#c0392b',
                'command': self.exit_app,
                'row': 1, 'col': 3
            }
        ]

        # Create modern card-style buttons Each button gets passed to a function that builds a “card-style UI”.
        for btn_data in self.buttons_data:
            self.create_modern_button(content_frame, btn_data)

        # ========= Footer =========
        footer = Label(self.root,
                      text="© 2025 Face Recognition System | Powered by Advanced AI Technology ",
                      font=("Segoe UI", 10),
                      bg=self.colors['bg_dark'],
                      fg=self.colors['text_secondary'])
        footer.place(x=0, y=90, width=1530, height=40)

    def create_gradient_bg(self):
        """Create a gradient background effect"""
        for i in range(790):
            r = int(10 + (26 - 10) * i / 790)
            g = int(14 + (30 - 14) * i / 790)
            b = int(39 + (55 - 39) * i / 790)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, 1530, i, fill=color)
            #This draws 790 horizontal colored lines (one for each pixel row).

    def create_modern_button(self, parent, btn_data):
        """Create a modern card-style button with hover effects"""
        row, col = btn_data['row'], btn_data['col']
        
        # Calculate position
        x = col * 320 + 25
        y = row * 280 + 20
        
        # Card container
        card = Frame(parent, bg=self.colors['bg_card'], 
                    highlightbackground=btn_data['color'],
                    highlightthickness=0)
        card.place(x=x, y=y, width=280, height=240)#This creates a rectangular card.
        
        # Icon and text frame large icon and text inside the card
        content = Frame(card, bg=self.colors['bg_card'])
        content.place(relx=0.5, rely=0.4, anchor=CENTER)
        
        # Icon label
        icon_lbl = Label(content,
                        text=btn_data['icon'],
                        font=("Segoe UI Emoji", 60),
                        bg=self.colors['bg_card'],
                        fg=btn_data['color'])
        icon_lbl.pack(pady=10)
        
        # Button title
        title_lbl = Label(content,
                         text=btn_data['text'],
                         font=("Segoe UI", 14, "bold"),
                         bg=self.colors['bg_card'],
                         fg=self.colors['text_light'])
        title_lbl.pack()
        
        # Action button
        action_btn = Button(card,
                           text="Open →",
                           font=("Segoe UI", 11, "bold"),
                           bg=btn_data['color'],
                           fg="white",
                           activebackground=btn_data['hover'],
                           activeforeground="white",
                           border=0,
                           cursor="hand2",
                           command=btn_data['command'],
                           relief=FLAT,
                           padx=20,
                           pady=8)
        action_btn.place(relx=0.5, rely=0.85, anchor=CENTER)
        
        # Hover effects
        def on_enter(e):
            card.configure(highlightthickness=2)
            action_btn.configure(bg=btn_data['hover'])
            
        def on_leave(e):
            card.configure(highlightthickness=0)
            action_btn.configure(bg=btn_data['color'])
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        icon_lbl.bind("<Enter>", on_enter)
        icon_lbl.bind("<Leave>", on_leave)
        title_lbl.bind("<Enter>", on_enter)
        title_lbl.bind("<Leave>", on_leave)
        content.bind("<Enter>", on_enter)
        content.bind("<Leave>", on_leave)
        
        # Make card clickable
        for widget in [card, content, icon_lbl, title_lbl]:
            widget.bind("<Button-1>", lambda e: btn_data['command']())

    def show_notification(self, message, color):
        """Show a temporary notification"""
        notif = Frame(self.root, bg=color, highlightbackground="#ffffff",
                     highlightthickness=1)
        notif.place(relx=0.5, y=120, anchor=N, width=400, height=60)
        
        Label(notif, text=message, font=("Segoe UI", 12, "bold"),
              bg=color, fg="white").place(relx=0.5, rely=0.5, anchor=CENTER)
        
        # Auto-hide after 2 seconds
        self.root.after(2000, notif.destroy)

    # ========= Button Functions =========
    def student_details(self):
        self.__new__window=Toplevel(self.root)
        self.app=Student(self.__new__window)    
        self.show_notification("Opening Student Details...", "#4a90e2")
        print("Student Details clicked")    

    def face_recognition(self):
        self.__new__window=Toplevel(self.root)
        self.app= FaceRecognitionSystem(self.__new__window)    
        self.show_notification("Opening  face recognization...", "#4a90e2")
        print("Student Details clicked")    

    def attendance(self):
        self.show_notification("Loading Attendance Records...", "#2ecc71")
        print("Attendance clicked")

    def help_desk(self):
        self.__new__window=Toplevel(self.root)
        self.app=Help(self.__new__window)
        

    def train_data(self):
        self.__new__window=Toplevel(self.root)
        self.app=train(self.__new__window)
        print("Train Data clicked")


    def developer(self):
        self.show_notification("Developer Information...", "#607d8b")
        print("Developer clicked")

    def exit_app(self):
        self.iExit= tkinter.messagebox.askyesno("Face Recognition","Are you sure you want to exit",parent=self.root)
        if self.iExit>0:
            self.root.destroy()
        else:
            return
#IMAGES 
    def open_img(self, path, size=None):
     os.startfile(path)
    

# Run program
if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()