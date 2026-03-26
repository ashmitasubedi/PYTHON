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
