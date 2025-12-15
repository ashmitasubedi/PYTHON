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
