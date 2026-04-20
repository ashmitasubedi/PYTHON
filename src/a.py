import os
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from PIL import Image, ImageTk, ImageDraw, ImageFilter
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import cv2
import numpy as np


class train:
    def __init__(self, root):  # CONSTRUCTOR CALLED root represents the main Tkinter window
        self.root = root
        self.root.geometry("1530x790+0+0")  # SETTING THE GEOMETRY OF THE WINDOW
        self.root.title("Face Recognition Attendance System")
        self.root.configure(bg="#0a0e27")
        # TITLE LABEL
        title_lbl = Label(
            self.root,
            text="TRAIN DATA SET",
            font=("times new roman", 35, "bold"),
            bg="#130303",
            fg="red",
        )
        title_lbl.place(x=0, y=0, width=1530, height=45)

        img_top = Image.open(r"..\photos\facw2.png")
        img_top = img_top.resize((1530, 325), Image.LANCZOS)  
        self.photoimg_top = ImageTk.PhotoImage(img_top)

        f_lbl = Label(self.root, image=self.photoimg_top)
        f_lbl.place(x=0, y=55, width=1530, height=325)
        # TRAIN BUTTON
        b1_1 = Button(
            self.root,
            text="TRAIN DATA",
            command=self.train_classifier,
            cursor="hand2",
            font=("times new roman", 30, "bold"),
            bg="#0a0e27",
            fg="white",
        )
        b1_1.place(x=0, y=380, width=1530, height=60)

        
        
        img_button = Image.open(r"..\photos\face.png")
        img_button = img_button.resize((1530, 325), Image.LANCZOS)  
        self.photoimg_top = ImageTk.PhotoImage(img_button)
        f_lbl = Label(self.root, image=self.photoimg_top)
        f_lbl.place(x=0, y=440, width=1530, height=325)

        
    def train_classifier(self):
        data_dir = ("data")#DIRECTORY WHERE IMAGES ARE STORED
        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]#list comprehension to get image paths

        faces = []
        ids = []#eauta manxe ko lagi eauta id assigned garya hunxa

        for image in path:
            img = Image.open(image).convert("L")  # CONVERTING IMAGE TO GRAYSCALE
            imageNp = np.array(img, "uint8")#grid ma convert garna ko lagi numpy uint8m is data type
            id = int(os.path.split(image)[1].split(".")[1])#getting id from image name 
            #splitting path to get file name and then splitting by . to get id part
            faces.append(imageNp)
            ids.append(id)
            cv2.imshow("Training", imageNp)
            cv2.waitKey(1) == 13

        ids = np.array(ids)#converting ids list to numpy array

        # TRAIN THE CLASSIFIER AND SAVE
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("classifier.xml")
        cv2.destroyAllWindows()
        messagebox.showinfo(
            "Result", "Training Dataset Completed!", parent=self.root
        )


# =========================== RUN APP ============================
if __name__ == "__main__":
    root = Tk()
    obj = train(root)
    root.mainloop()
from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector

class Register:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Register Desk")

        # Frame
        frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        frame.place(x=500, y=100, width=500, height=600)

        register_lbl = Label(self.root, text="REGISTER HERE", font=("times new roman", 35, "bold"), bg="white", fg="blue")
        register_lbl.place(x=0, y=0, width=1530, height=45)

        # Form Fields
        labels = ["First Name", "Last Name", "Email", "Password", "Confirm Password",
                  "Contact Number", "Select Security Question", "Security Answer"]
        y_positions = [50, 120, 190, 260, 330, 400, 470, 540]

        self.entries = {}

        for i, text in enumerate(labels):
            lbl = Label(frame, text=text, font=("times new roman", 15, "bold"), bg="white", fg="black")
            lbl.place(x=50, y=y_positions[i])

        self.fname_entry = ttk.Entry(frame, font=("times new roman", 15, "bold"))
        self.fname_entry.place(x=50, y=80, width=400)

        self.lname_entry = ttk.Entry(frame, font=("times new roman", 15, "bold"))
        self.lname_entry.place(x=50, y=150, width=400)

        self.email_entry = ttk.Entry(frame, font=("times new roman", 15, "bold"))
        self.email_entry.place(x=50, y=220, width=400)

        self.password_entry = ttk.Entry(frame, font=("times new roman", 15, "bold"), show="*")
        self.password_entry.place(x=50, y=290, width=400)

        self.confirm_password_entry = ttk.Entry(frame, font=("times new roman", 15, "bold"), show="*")
        self.confirm_password_entry.place(x=50, y=360, width=400)

        self.contact_entry = ttk.Entry(frame, font=("times new roman", 15, "bold"))
        self.contact_entry.place(x=50, y=430, width=400)

        self.security_combo = ttk.Combobox(frame, font=("times new roman", 15, "bold"), state="readonly")
        self.security_combo['values'] = ("Select", "Your Birth Place", "Your Best Friend Name", "Your Pet Name")
        self.security_combo.place(x=50, y=500, width=400)
        self.security_combo.current(0)

        self.security_answer_entry = ttk.Entry(frame, font=("times new roman", 15, "bold"))
        self.security_answer_entry.place(x=50, y=570, width=400)

        # Register Button
        register_btn = Button(frame, text="Register", font=("times new roman", 15, "bold"), bd=3, relief=RIDGE,
                              fg="white", bg="green", activeforeground="white", activebackground="green",
                              command=self.register_user)
        register_btn.place(x=200, y=620, width=100, height=35)

    def register_user(self):
        if (self.fname_entry.get() == "" or self.lname_entry.get() == "" or self.email_entry.get() == "" or
                self.password_entry.get() == "" or self.confirm_password_entry.get() == "" or
                self.contact_entry.get() == "" or self.security_combo.get() == "Select" or
                self.security_answer_entry.get() == ""):
            messagebox.showerror("Error", "All fields are required")
        elif self.password_entry.get() != self.confirm_password_entry.get():
            messagebox.showerror("Error", "Passwords do not match")
        else:
            conn = mysql.connector.connect(host="localhost", username="root", password="", database="face_recognizer")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT * FROM register WHERE email=%s", (self.email_entry.get(),))
            row = my_cursor.fetchone()
            if row is not None:
                messagebox.showerror("Error", "User already exists")
            else:
                my_cursor.execute("INSERT INTO register (fname, lname, email, password, contact, securityQ, securityA) VALUES (%s,%s,%s,%s,%s,%s,%s)", (
                    self.fname_entry.get(),
                    self.lname_entry.get(),
                    self.email_entry.get(),
                    self.password_entry.get(),
                    self.contact_entry.get(),
                    self.security_combo.get(),
                    self.security_answer_entry.get()
                ))
                conn.commit()
                messagebox.showinfo("Success", "Registration Successful")
            conn.close()


if __name__ == "__main__":
    root = Tk()
    app = Register(root)
    root.mainloop()
from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector

class Register:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Register Desk")

        # Frame
        frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        frame.place(x=500, y=100, width=500, height=600)

        register_lbl = Label(self.root, text="REGISTER HERE", font=("times new roman", 35, "bold"), bg="white", fg="blue")
        register_lbl.place(x=0, y=0, width=1530, height=45)

        # Form Fields
        labels = ["First Name", "Last Name", "Email", "Password", "Confirm Password",
                  "Contact Number", "Select Security Question", "Security Answer"]
        y_positions = [50, 120, 190, 260, 330, 400, 470, 540]

        self.entries = {}

        for i, text in enumerate(labels):
            lbl = Label(frame, text=text, font=("times new roman", 15, "bold"), bg="white", fg="black")
            lbl.place(x=50, y=y_positions[i])

        self.fname_entry = ttk.Entry(frame, font=("times new roman", 15, "bold"))
        self.fname_entry.place(x=50, y=80, width=400)

        self.lname_entry = ttk.Entry(frame, font=("times new roman", 15, "bold"))
        self.lname_entry.place(x=50, y=150, width=400)

        self.email_entry = ttk.Entry(frame, font=("times new roman", 15, "bold"))
        self.email_entry.place(x=50, y=220, width=400)

        self.password_entry = ttk.Entry(frame, font=("times new roman", 15, "bold"), show="*")
        self.password_entry.place(x=50, y=290, width=400)

        self.confirm_password_entry = ttk.Entry(frame, font=("times new roman", 15, "bold"), show="*")
        self.confirm_password_entry.place(x=50, y=360, width=400)

        self.contact_entry = ttk.Entry(frame, font=("times new roman", 15, "bold"))
        self.contact_entry.place(x=50, y=430, width=400)

        self.security_combo = ttk.Combobox(frame, font=("times new roman", 15, "bold"), state="readonly")
        self.security_combo['values'] = ("Select", "Your Birth Place", "Your Best Friend Name", "Your Pet Name")
        self.security_combo.place(x=50, y=500, width=400)
        self.security_combo.current(0)

        self.security_answer_entry = ttk.Entry(frame, font=("times new roman", 15, "bold"))
        self.security_answer_entry.place(x=50, y=570, width=400)

        # Register Button
        register_btn = Button(frame, text="Register", font=("times new roman", 15, "bold"), bd=3, relief=RIDGE,
                              fg="white", bg="green", activeforeground="white", activebackground="green",
                              command=self.register_user)
        register_btn.place(x=200, y=620, width=100, height=35)

    def register_user(self):
        if (self.fname_entry.get() == "" or self.lname_entry.get() == "" or self.email_entry.get() == "" or
                self.password_entry.get() == "" or self.confirm_password_entry.get() == "" or
                self.contact_entry.get() == "" or self.security_combo.get() == "Select" or
                self.security_answer_entry.get() == ""):
            messagebox.showerror("Error", "All fields are required")
        elif self.password_entry.get() != self.confirm_password_entry.get():
            messagebox.showerror("Error", "Passwords do not match")
        else:
            conn = mysql.connector.connect(host="localhost", username="root", password="", database="face_recognizer")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT * FROM register WHERE email=%s", (self.email_entry.get(),))
            row = my_cursor.fetchone()
            if row is not None:
                messagebox.showerror("Error", "User already exists")
            else:
                my_cursor.execute("INSERT INTO register (fname, lname, email, password, contact, securityQ, securityA) VALUES (%s,%s,%s,%s,%s,%s,%s)", (
                    self.fname_entry.get(),
                    self.lname_entry.get(),
                    self.email_entry.get(),
                    self.password_entry.get(),
                    self.contact_entry.get(),
                    self.security_combo.get(),
                    self.security_answer_entry.get()
                ))
                conn.commit()
                messagebox.showinfo("Success", "Registration Successful")
            conn.close()


if __name__ == "__main__":
    root = Tk()
    app = Register(root)
    root.mainloop()
  def create_gradient_background(self):
        self.canvas = Canvas(
            self.root,
            width=1400,
            height=800,
            bg="#0f0f1e",
            highlightthickness=0
        )
        self.canvas.place(x=0, y=0)

        self.bg_shapes = []

        self.bg_shapes.append({
            "id": self.canvas.create_oval(-150, -150, 650, 650, fill="#1a1a3e", outline=""),
            "dx": 0.3, "dy": 0.2
        })

        self.bg_shapes.append({
            "id": self.canvas.create_oval(750, 150, 1650, 1050, fill="#16213e", outline=""),
            "dx": -0.25, "dy": 0.15
        })

        self.bg_shapes.append({
            "id": self.canvas.create_oval(250, 450, 1150, 1250, fill="#0f3460", outline=""),
            "dx": 0.2, "dy": -0.25
        })

        # Accent glow circles
        self.glow1 = self.canvas.create_oval(90, 40, 260, 210, fill="#e94560", outline="")
        self.glow2 = self.canvas.create_oval(1180, 580, 1380, 780, fill="#533483", outline="")

        self.animate_background()
    def animate_background(self):
        for shape in self.bg_shapes:
            self.canvas.move(shape["id"], shape["dx"], shape["dy"])

            x1, y1, x2, y2 = self.canvas.coords(shape["id"])

            # Bounce effect
            if x1 < -300 or x2 > 1800:
                shape["dx"] *= -1
            if y1 < -300 or y2 > 1200:
                shape["dy"] *= -1

        # Glow pulse
        self.pulse_glow(self.glow1)
        self.pulse_glow(self.glow2)

        self.root.after(30, self.animate_background)
    def pulse_glow(self, item):
        x1, y1, x2, y2 = self.canvas.coords(item)
        expand = 0.6

        self.canvas.coords(
            item,
            x1 - expand,
            y1 - expand,
            x2 + expand,
            y2 + expand
        )


        from tkinter import*
from tkinter import messagebox
from tkinter import ttk
import os
import mysql.connector
import cv2
from PIL import Image, ImageTk
class Login_window:
    def__init__(self,root):
      self.root=root
     self.root.title("Login")
     self.root.goemetry("1530x790+0+0")
     self.bg=ImageTk.PhotoImage(file=r"photos\login.jpg")
        lbl_bg=Label(self.root,image=self.bg)
        lbl_bg.place(x=0,y=0,relwidth=1,relheight=1)
        frame=Frame(self.root,bg="black")
        frame.place(x=610,y=170,width=340,height=450)
        img1=Image.open(r"photos\loginicon.png")
        img1=img1.resize((100,100),Image.LANCZOS)
        self.photoimage1=ImageTk.PhotoImage(img1)
        lblimg1=Label(image=self.photoimage1,bg="black",borderwidth=0)
        lblimg1.place(x=730,y=175,width=100,height=100)
        get_str=Label(frame,text="Get Started",font=("times new roman",20,"bold"),fg="white",bg="black")
        get_str.place(x=95,y=100)
        #label
        username_lbl=Label(frame,text="Username",font=("times new roman",15,"bold"),fg="white",bg="black")
        username.place(x=70,y=155)
        self.txtuser=ttk.Entry(frame,font=("times new roman",15,"bold"))
        self.txtuser.place(x=40,y=180,width=270)
        password_lbl=Label(frame,text="Password",font=("times new roman",15,"bold"),fg="white",bg="black")
        password.place(x=70,y=225)
        self.txtpass=ttk.Entry(frame,font=("times new roman",15,"bold"),show="*")
        self.txtpass.place(x=40,y=250,width=270)
        
        #login button
        loginbtn=Button(frame,command=self.login,text="Login",font=("times new roman",15,"bold"),bd=3,relief=RIDGE,fg="white",bg="red",activeforeground="white",activebackground="red")
        loginbtn.place(x=110,y=300,width=120,height=35)
       registerbtn=Button(frame,text="Register New User",font=("times new roman",10,"bold"),borderwidth=0,fg="white",bg="black",activeforeground="white",activebackground="black")
        registerbtn.place(x=15,y=350,width=160),height=25)
        forgetbtn=Button(frame,text="Forget Password",font=("times new roman",10,"bold"),borderwidth=0,fg="white",bg="black",activeforeground="white",activebackground="black") 
        forgetbtn.place(x=10,y=370,width=160),height=25)
    
    
    def login(self):
        if self.txtuser.get()=="" or self.txtpass.get()=="":
            messagebox.showerror("Error","All fields are required")
        elif self.txtuser.get()=="ash" and self.txtpass.get()=="1234":
            messagebox.showinfo("Success","Welcome to Face Recognition System")
        else:
            conn=mysql.connector.connect(host="localhost",username="root",password="",database="face_recognizer")
            my_cursor=conn.cursor()
            my_cursor.execute("select * from register where email=%s and password=%s",(
                self.txtuser.get(),
                self.txtpass.get()
            ))
            row=my_cursor.fetchone()
            if row==None:
                messagebox.showerror("Error","Invalid Username and Password")
            else:
                conn.close()
                self.root.destroy()
                self.root2=Toplevel()
                self.root2.title("Forget Password")
                self.root2.geometry("400x400+610+170")

                l=label(self.root2,text="Reset Password",font=("times new roman",20,"bold"),fg="red")
                l.place(x=100,y=50)
                security_ques_lbl=Label(self.root2,text="Select Security Question",font=("times new roman",15,"bold"),fg="black")
                security_ques_lbl.place(x=50,y=100)
                self.security_combo=ttk.Combobox(self.root2,font=("times new roman",15,"bold"),state="readonly")
                self.security_combo['values']=("Select","Your Birth Place","Your Best Friend Name","Your Pet Name")
                self.security_combo.place(x=50,y=130,width=250)
                security_answer_lbl=Label(self.root2,text="Security Answer",font=("times new roman",15,"bold"),fg="black")
                security_answer_lbl.place(x=50,y=170)
                self.security_answer_entry=ttk.Entry(self.root2,font=("times new roman",15,"bold"))
                self.security_answer_entry.place(x=50,y=200,width=250)
                new_password_lbl=Label(self.root2,text="New Password",font=("times new roman",15,"bold"),fg="black")
                new_password_lbl.place(x=50,y=240)
                self.new_password_entry=ttk.Entry(self.root2,font=("times new roman",15,"bold"))
                self.new_password_entry.place(x=50,y=270,width=250)
                resetbtn=Button(self.root2,command=self.reset_password,text="Reset",font=("times new roman",15,"bold"),bd=3,relief=RIDGE,fg="white",bg="green",activeforeground="white",activebackground="green")
                resetbtn.place(x=150,y=320,width=100,height=35)
    def reset_password(self):
        if self.security_combo.get()=="Select" or self.security_answer_entry.get()=="" or self.new_password_entry.get()=="":
            messagebox.showerror("Error","All fields are required")
        else:
            conn=mysql.connector.connect(host="localhost",username="root",password="",database="face_recognizer")
            my_cursor=conn.cursor()
            query=("select * from register where email=%s and securityQ=%s and securityA=%s")
            value=(self.txtuser.get(),self.security_combo.get(),self.security_answer_entry.get())
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            if row==None:
                messagebox.showerror("Error","Please select the correct security question and answer")
            else:
                query=("update register set password=%s where email=%s")
                value=(self.new_password_entry.get(),self.txtuser.get())
                my_cursor.execute(query,value)
                messagebox.showinfo("Success","Your password has been reset successfully")
                        
            conn.commit()
            conn.close()


            
    
if __name__ == "__main__":
    root=Tk()
    app=Login_window(root)
    root.mainloop()
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
        self.CONFIDENCE_THRESHOLD = 86
        
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
        self.marked_today = set()

        # FIX 1: confirmation counter - face must match N consecutive frames before marking
        self._confirm_counts = {}   # {student_id: int}
        self.CONFIRM_FRAMES  = 8   # change this to make it stricter or faster

        # FIX 2: load who was already marked today from CSV so restart doesn't double-mark
        self._load_marked_today()
        
        # Setup UI after variables are initialized
        self._setup_ui()

    # ── FIX 2 helper ─────────────────────────────────────────
    def _load_marked_today(self):
        """On startup, read CSV and remember IDs already marked today."""
        if not os.path.exists(os.path.join(self.BASE_DIR, "attendance.csv")):
            return
        today = datetime.now().strftime("%d/%m/%Y")
        try:
            with open(os.path.join(self.BASE_DIR, "attendance.csv"), "r") as f:
                for line in f.readlines()[1:]:
                    parts = line.strip().split(",")
                    if len(parts) >= 6 and parts[5] == today:
                        self.marked_today.add(str(parts[0]))
            print(f"Already marked today: {self.marked_today}")
        except Exception as e:
            print(f"Could not load today attendance: {e}")
    
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
        debug_text += f"Haarcascade: {'Found' if os.path.exists(self.HAARCASCADE_PATH) else 'Missing'}\n"
        debug_text += f"Classifier: {'Found' if os.path.exists(self.CLASSIFIER_PATH) else 'Missing - Train model first'}"
        
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
            text="Stop Recognition",
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
            text="Check Files",
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
            text="Settings",
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
            message += f"Haarcascade file found\n  Path: {self.HAARCASCADE_PATH}\n\n"
        else:
            message += f"Haarcascade file NOT FOUND\n  Expected path: {self.HAARCASCADE_PATH}\n"
            message += f"  Download from: https://github.com/opencv/opencv/tree/master/data/haarcascades\n\n"
        
        # Check classifier
        if os.path.exists(self.CLASSIFIER_PATH):
            message += f"Classifier file found\n  Path: {self.CLASSIFIER_PATH}\n\n"
        else:
            message += f"Classifier file NOT FOUND\n  Expected path: {self.CLASSIFIER_PATH}\n"
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
            text="Recognition Settings",
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
                current_label.config(fg="#e74c3c")
                recommendation.config(text="Warning: Low threshold may cause false recognitions")
            elif int(val) < 75:
                current_label.config(fg="#f39c12")
                recommendation.config(text="Moderate threshold - balanced accuracy")
            else:
                current_label.config(fg="#4ae24a")
                recommendation.config(text="High threshold - strict recognition")
        
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
            text="High threshold - strict recognition",
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
            self._show_error_throttled("Database Error", str(e))
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

            # FIX 3: equalise histogram for better detection in varied lighting
            gray_image = cv2.equalizeHist(gray_image)
 
            faces = classifier.detectMultiScale(
                gray_image,
                scaleFactor=1.1,
                minNeighbors=6,
                minSize=(100, 100)
             )

            # track which IDs appeared this frame to reset missing ones
            seen_ids = set()
            
            if len(faces) > 0:
                detection_info.append(f"Detected {len(faces)} face(s)")
 
            for (x, y, w, h) in faces:
                try:
                    face_roi = gray_image[y:y + h, x:x + w]
                    student_id, prediction = clf.predict(face_roi)

                    print(f"Face detected - ID: {student_id}, LBPH Distance: {prediction:.1f}")
                    seen_ids.add(student_id)
 
                    if prediction < 60:
                        # HIGH CONFIDENCE
                        # FIX 1: increment confirmation counter
                        self._confirm_counts[student_id] = self._confirm_counts.get(student_id, 0) + 1
                        count = self._confirm_counts[student_id]

                        confidence = max(0, min(100, int(100 - prediction)))
                        student_info = self._fetch_student_info(student_id)
 
                        if student_info and prediction < 70:
                            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                            text_y_start = y + h + 25
                            self._draw_text(img, f"Name: {student_info['name']}",       x, text_y_start)
                            self._draw_text(img, f"Roll: {student_info['roll_no']}",    x, text_y_start + 25)
                            self._draw_text(img, f"Dept: {student_info['department']}", x, text_y_start + 50)
                            self._draw_text(img, f"Confidence: {confidence}%",          x, text_y_start + 75)
                            self._draw_text(img, f"Confirm: {count}/{self.CONFIRM_FRAMES}", x, text_y_start + 100)

                            # FIX 1: only mark after CONFIRM_FRAMES consecutive matches
                            if count >= self.CONFIRM_FRAMES:
                                self.mark_attendence(
                                    student_id,
                                    student_info['roll_no'],
                                    student_info['department'],
                                    student_info['name']
                                )
                            detection_info.append(
                                f"Recognised: {student_info['name']} "
                                f"(ID: {student_id}, Distance: {prediction:.1f}, {count}/{self.CONFIRM_FRAMES})"
                            )
                        else:
                            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 165, 255), 3)
                            text_y_start = y + h + 25
                            self._draw_text(img, f"ID {student_id} Not in DB", x, text_y_start)
                            self._draw_text(img, f"Distance: {prediction:.1f}",  x, text_y_start + 25)
                            detection_info.append(
                                f"Face detected (ID: {student_id}) but not in database"
                            )
 
                    elif 60 <= prediction < 80:
                        # UNCERTAIN — reset confirmation, don't mark
                        self._confirm_counts.pop(student_id, None)

                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 165, 255), 3)
                        text_y_start = y + h + 25
                        self._draw_text(img, "Uncertain Match",             x, text_y_start)
                        self._draw_text(img, f"Distance: {prediction:.1f}", x, text_y_start + 25)
                        detection_info.append(
                            f"Uncertain: Distance {prediction:.1f}"
                        )
 
                    else:
                        # UNKNOWN FACE — reset confirmation
                        self._confirm_counts.pop(student_id, None)

                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                        text_y_start = y + h + 25
                        self._draw_text(img, "Unknown Face",                x, text_y_start)
                        self._draw_text(img, f"Distance: {prediction:.1f}", x, text_y_start + 25)
                        detection_info.append(
                            f"Unknown face: Distance {prediction:.1f}"
                        )
 
                except Exception as e:
                    print(f"Error processing face at ({x}, {y}): {e}")
                    continue

            # FIX 1: reset counters for IDs not seen this frame
            for sid in list(self._confirm_counts.keys()):
                if sid not in seen_ids:
                    self._confirm_counts.pop(sid)
 
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
                self.video_label.imgtk = imgtk  # Keep reference to avoid garbage collection

                # FIX 4: capture loop variables in lambda defaults to avoid closure bug
                self.root.after(0, lambda i=imgtk, t=info_text: (
                    self.video_label.configure(image=i, text=""),
                    self.info_label.configure(text=t)
                ))
                
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
            self._confirm_counts.clear()  # reset on every fresh start

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
            cv2.destroyAllWindows()
        
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

        self._confirm_counts.clear()
        print("Face recognition stopped.")

    def mark_attendence(self, student_id, roll, department, name):
        """Mark student attendance in CSV file"""
        import time
        current_time = time.time()

        # Throttle per student_id
        last_time = self.last_mark_time.get(str(student_id), 0)
        if current_time - last_time < 5:
            return

        self.last_mark_time[str(student_id)] = current_time

        # Create file with header if it doesn't exist
        if not os.path.exists(self.ATTENDANCE_PATH):
            with open(self.ATTENDANCE_PATH, "w") as f:
                f.write("StudentID,Name,Roll,Department,Time,Date,Status\n")

        existing = set()
        with open(self.ATTENDANCE_PATH, "r") as f:
            lines = f.readlines()
            for line in lines[1:]:
                values = line.strip().split(",")
                if len(values) >= 6:
                    existing.add((values[0], values[5]))

        now = datetime.now()
        date_today = now.strftime("%d/%m/%Y")
        time_now = now.strftime("%H:%M:%S")

        if (str(student_id), date_today) in existing or str(student_id) in self.marked_today:
            print(f"Attendance already marked today for: {name} (ID: {student_id})")
            self.root.after(0, lambda: self.info_label.configure(
                text=f"{name} - Attendance already marked today"
            ))
            return

        with open(self.ATTENDANCE_PATH, "a") as f:
            f.write(f"{student_id},{name},{roll},{department},{time_now},{date_today},Present\n")
            self.marked_today.add(str(student_id))
            # FIX 1: reset confirmation after marking so we don't immediately re-trigger
            self._confirm_counts.pop(student_id, None)

        print(f"Attendance marked: {student_id} - {name} at {time_now}")

        self.root.after(0, lambda: self.info_label.configure(
            text=f"Attendance Marked!\nName: {name}\nRoll: {roll}\nTime: {time_now}"
        ))

def main():
    """Main entry point for the application"""
    root = Tk()
    app = FaceRecognitionSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
