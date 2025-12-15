from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector
from PIL import Image, ImageTk
import os
from main import Face_Recognition_System


class ModernLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition - Login System")
        self.root.geometry("1400x800+50+50")
        self.root.configure(bg="#0f0f1e")
        self.root.resizable(False, False)
        
        self.create_gradient_background()
        self.create_login_ui()
    
    def create_gradient_background(self):
        """Create modern gradient background"""
        canvas = Canvas(self.root, width=1400, height=800, bg="#0f0f1e", highlightthickness=0)
        canvas.place(x=0, y=0)
        
        # Gradient effect with overlapping circles
        canvas.create_oval(-100, -100, 600, 600, fill="#1a1a3e", outline="")
        canvas.create_oval(800, 200, 1600, 1000, fill="#16213e", outline="")
        canvas.create_oval(300, 400, 1100, 1200, fill="#0f3460", outline="")
        
        # Accent circles
        canvas.create_oval(100, 50, 250, 200, fill="#e94560", outline="")
        canvas.create_oval(1200, 600, 1350, 750, fill="#533483", outline="")
        
        self.canvas = canvas
    
    def create_login_ui(self):
        """Create main login interface"""
        # Left Panel - Branding
        left_frame = Frame(self.root, bg="#1a1a3e", bd=0)
        left_frame.place(x=100, y=150, width=500, height=500)
        
        # Title
        title = Label(left_frame, text="Welcome Back!", 
                     font=("Segoe UI", 42, "bold"), 
                     fg="#e94560", bg="#1a1a3e")
        title.place(x=50, y=80)
        
        subtitle = Label(left_frame, text="Face Recognition System", 
                        font=("Segoe UI", 18), 
                        fg="#ffffff", bg="#1a1a3e")
        subtitle.place(x=50, y=150)
        
        desc = Label(left_frame, text="Secure access to your workspace\nwith advanced biometric authentication", 
                    font=("Segoe UI", 11), 
                    fg="#a8a8a8", bg="#1a1a3e", justify=LEFT)
        desc.place(x=50, y=200)
        
        # Feature highlights
        features = [
            "🔒 Secure Authentication",
            "⚡ Fast Recognition",
            "🎯 99% Accuracy"
        ]
        
        y_pos = 280
        for feature in features:
            Label(left_frame, text=feature, 
                 font=("Segoe UI", 12), 
                 fg="#ffffff", bg="#1a1a3e",
                 anchor=W).place(x=50, y=y_pos)
            y_pos += 35
        
        # Right Panel - Login Form
        self.create_login_form()
    
    def create_login_form(self):
        """Create modern login form"""
        form_frame = Frame(self.root, bg="#ffffff", bd=0)
        form_frame.place(x=700, y=150, width=550, height=500)
        
        # Add shadow effect
        shadow = Frame(self.root, bg="#000000")
        shadow.place(x=705, y=155, width=550, height=500)
        form_frame.lift()
        
        # Form Title
        Label(form_frame, text="Sign In", 
              font=("Segoe UI", 32, "bold"), 
              fg="#1a1a3e", bg="#ffffff").place(x=200, y=40)
        
        # Username Field
        Label(form_frame, text="USERNAME", 
              font=("Segoe UI", 9, "bold"), 
              fg="#666666", bg="#ffffff").place(x=75, y=130)
        
        username_frame = Frame(form_frame, bg="#f0f0f0", bd=0)
        username_frame.place(x=75, y=155, width=400, height=50)
        
        Label(username_frame, text="👤", font=("Segoe UI", 18), 
              bg="#f0f0f0", fg="#666666").place(x=15, y=10)
        
        self.txtuser = Entry(username_frame, font=("Segoe UI", 12), 
                            bg="#f0f0f0", fg="#1a1a3e", 
                            bd=0, insertbackground="#1a1a3e")
        self.txtuser.place(x=60, y=13, width=320)
        self.txtuser.insert(0, "Enter your email")
        self.txtuser.bind("<FocusIn>", lambda e: self.on_entry_focus(self.txtuser, "Enter your email"))
        self.txtuser.bind("<FocusOut>", lambda e: self.on_entry_leave(self.txtuser, "Enter your email"))
        
        # Password Field
        Label(form_frame, text="PASSWORD", 
              font=("Segoe UI", 9, "bold"), 
              fg="#666666", bg="#ffffff").place(x=75, y=230)
        
        password_frame = Frame(form_frame, bg="#f0f0f0", bd=0)
        password_frame.place(x=75, y=255, width=400, height=50)
        
        Label(password_frame, text="🔒", font=("Segoe UI", 18), 
              bg="#f0f0f0", fg="#666666").place(x=15, y=10)
        
        self.txtpass = Entry(password_frame, font=("Segoe UI", 12), 
                            bg="#f0f0f0", fg="#1a1a3e", 
                            bd=0, show="", insertbackground="#1a1a3e")
        self.txtpass.place(x=60, y=13, width=320)
        self.txtpass.insert(0, "Enter your password")
        self.txtpass.bind("<FocusIn>", lambda e: self.on_password_focus())
        self.txtpass.bind("<FocusOut>", lambda e: self.on_password_leave())
        
        # Login Button
        login_btn = Button(form_frame, text="LOGIN", 
                          font=("Segoe UI", 13, "bold"), 
                          bg="#e94560", fg="#ffffff", 
                          bd=0, cursor="hand2",
                          activebackground="#d63447",
                          activeforeground="#ffffff",
                          command=self.login)
        login_btn.place(x=75, y=340, width=400, height=50)
        
        # Hover effect
        login_btn.bind("<Enter>", lambda e: login_btn.config(bg="#d63447"))
        login_btn.bind("<Leave>", lambda e: login_btn.config(bg="#e94560"))
        
        # Additional Options
        forgot_btn = Button(form_frame, text="Forgot Password?", 
                           font=("Segoe UI", 9, "underline"), 
                           fg="#e94560", bg="#ffffff", 
                           bd=0, cursor="hand2",
                           activeforeground="#d63447",
                           activebackground="#ffffff",
                           command=self.open_reset_window)
        forgot_btn.place(x=75, y=410)
        
        Label(form_frame, text="Don't have an account?", 
              font=("Segoe UI", 9), 
              fg="#666666", bg="#ffffff").place(x=240, y=410)
        
        register_btn = Button(form_frame, text="Sign Up", 
                             font=("Segoe UI", 9, "bold underline"), 
                             fg="#e94560", bg="#ffffff", 
                             bd=0, cursor="hand2",
                             activeforeground="#d63447",
                             activebackground="#ffffff",
                             command=self.open_register)
        register_btn.place(x=390, y=410)
    
    def on_entry_focus(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, END)
            entry.config(fg="#1a1a3e")
    
    def on_entry_leave(self, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="#999999")
    
    def on_password_focus(self):
        if self.txtpass.get() == "Enter your password":
            self.txtpass.delete(0, END)
            self.txtpass.config(show="●", fg="#1a1a3e")
    
    def on_password_leave(self):
        if self.txtpass.get() == "":
            self.txtpass.config(show="")
            self.txtpass.insert(0, "Enter your password")
            self.txtpass.config(fg="#999999")
    
    def login(self):
        username = self.txtuser.get()
        password = self.txtpass.get()
        
        if username in ["", "Enter your email"] or password in ["", "Enter your password"]:
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
            return
        
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="face_recognizer"
            )
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM register WHERE email=%s AND password=%s",
                (username, password)
            )
            row = cursor.fetchone()
            
            if row is None:
                messagebox.showerror("Error", "Invalid Username or Password!", parent=self.root)
            else:
                messagebox.showinfo("Success", f"Welcome back, {row[1]}!", parent=self.root)
                self.open_main()
            
            conn.close()
            
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}", parent=self.root)
    
    def open_reset_window(self):
        ResetPassword(Toplevel(self.root), self.txtuser.get())
    
    def open_register(self):
        Register(Toplevel(self.root))
    def open_main(self):
        self.__new__window=Toplevel(self.root)
        self.app=Face_Recognition_System(self.__new__window)
        print("Train Data clicked")




class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Create Account")
        self.root.geometry("650x700+350+50")
        self.root.configure(bg="#ffffff")
        self.root.resizable(False, False)
        
        # Header
        header = Frame(self.root, bg="#e94560", height=80)
        header.place(x=0, y=0, width=650, height=80)
        
        Label(header, text="Create Account", 
              font=("Segoe UI", 28, "bold"), 
              fg="#ffffff", bg="#e94560").place(x=180, y=20)
        
        # Main container with scrollbar
        main_container = Frame(self.root, bg="#ffffff")
        main_container.place(x=0, y=80, width=650, height=620)
        
        # Canvas for scrolling
        canvas = Canvas(main_container, bg="#ffffff", highlightthickness=0)
        scrollbar = Scrollbar(main_container, orient="vertical", command=canvas.yview)
        
        # Scrollable frame
        scrollable_frame = Frame(canvas, bg="#ffffff")
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Form inside scrollable frame
        form = Frame(scrollable_frame, bg="#ffffff")
        form.pack(padx=75, pady=30)
        
        # First Name
        Label(form, text="FIRST NAME", font=("Segoe UI", 9, "bold"), 
              fg="#666666", bg="#ffffff").grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.fname = Entry(form, font=("Segoe UI", 12), bg="#f0f0f0", 
                          fg="#1a1a3e", bd=0, insertbackground="#1a1a3e")
        self.fname.grid(row=1, column=0, ipady=12, sticky="ew", pady=(0, 20))
        
        # Last Name
        Label(form, text="LAST NAME", font=("Segoe UI", 9, "bold"), 
              fg="#666666", bg="#ffffff").grid(row=2, column=0, sticky="w", pady=(0, 5))
        self.lname = Entry(form, font=("Segoe UI", 12), bg="#f0f0f0", 
                          fg="#1a1a3e", bd=0, insertbackground="#1a1a3e")
        self.lname.grid(row=3, column=0, ipady=12, sticky="ew", pady=(0, 20))
        
        # Email
        Label(form, text="EMAIL", font=("Segoe UI", 9, "bold"), 
              fg="#666666", bg="#ffffff").grid(row=4, column=0, sticky="w", pady=(0, 5))
        self.email = Entry(form, font=("Segoe UI", 12), bg="#f0f0f0", 
                          fg="#1a1a3e", bd=0, insertbackground="#1a1a3e")
        self.email.grid(row=5, column=0, ipady=12, sticky="ew", pady=(0, 20))
        
        # Contact
        Label(form, text="CONTACT NUMBER", font=("Segoe UI", 9, "bold"), 
              fg="#666666", bg="#ffffff").grid(row=6, column=0, sticky="w", pady=(0, 5))
        self.contact = Entry(form, font=("Segoe UI", 12), bg="#f0f0f0", 
                            fg="#1a1a3e", bd=0, insertbackground="#1a1a3e")
        self.contact.grid(row=7, column=0, ipady=12, sticky="ew", pady=(0, 20))
        
        # Password
        Label(form, text="PASSWORD", font=("Segoe UI", 9, "bold"), 
              fg="#666666", bg="#ffffff").grid(row=8, column=0, sticky="w", pady=(0, 5))
        self.password = Entry(form, font=("Segoe UI", 12), bg="#f0f0f0", 
                             fg="#1a1a3e", bd=0, show="●", insertbackground="#1a1a3e")
        self.password.grid(row=9, column=0, ipady=12, sticky="ew", pady=(0, 20))
        
        # Confirm Password
        Label(form, text="CONFIRM PASSWORD", font=("Segoe UI", 9, "bold"), 
              fg="#666666", bg="#ffffff").grid(row=10, column=0, sticky="w", pady=(0, 5))
        self.confirm_pass = Entry(form, font=("Segoe UI", 12), bg="#f0f0f0", 
                                 fg="#1a1a3e", bd=0, show="●", insertbackground="#1a1a3e")
        self.confirm_pass.grid(row=11, column=0, ipady=12, sticky="ew", pady=(0, 20))
        
        # Security Question
        Label(form, text="SECURITY QUESTION", font=("Segoe UI", 9, "bold"), 
              fg="#666666", bg="#ffffff").grid(row=12, column=0, sticky="w", pady=(0, 5))
        
        style = ttk.Style()
        style.configure("Custom.TCombobox", fieldbackground="#f0f0f0", 
                       background="#f0f0f0", foreground="#1a1a3e")
        
        self.security_q = ttk.Combobox(form, font=("Segoe UI", 11), 
                                       state="readonly", style="Custom.TCombobox")
        self.security_q['values'] = ("Select", "Your Birth Place", 
                                      "Your Best Friend Name", "Your Pet Name")
        self.security_q.current(0)
        self.security_q.grid(row=13, column=0, ipady=12, sticky="ew", pady=(0, 20))
        
        # Security Answer
        Label(form, text="SECURITY ANSWER", font=("Segoe UI", 9, "bold"), 
              fg="#666666", bg="#ffffff").grid(row=14, column=0, sticky="w", pady=(0, 5))
        self.security_a = Entry(form, font=("Segoe UI", 12), bg="#f0f0f0", 
                               fg="#1a1a3e", bd=0, insertbackground="#1a1a3e")
        self.security_a.grid(row=15, column=0, ipady=12, sticky="ew", pady=(0, 30))
        
        # Configure column width
        form.columnconfigure(0, minsize=500)
        
        # Register Button
        register_btn = Button(form, text="CREATE ACCOUNT", 
                             font=("Segoe UI", 13, "bold"), 
                             bg="#e94560", fg="#ffffff", bd=0, cursor="hand2",
                             activebackground="#d63447", activeforeground="#ffffff",
                             command=self.register_user)
        register_btn.grid(row=16, column=0, ipady=15, sticky="ew", pady=(0, 30))
        
        register_btn.bind("<Enter>", lambda e: register_btn.config(bg="#d63447"))
        register_btn.bind("<Leave>", lambda e: register_btn.config(bg="#e94560"))
    
    def register_user(self):
        if (self.fname.get() == "" or self.lname.get() == "" or 
            self.email.get() == "" or self.contact.get() == "" or
            self.password.get() == "" or self.confirm_pass.get() == "" or
            self.security_q.get() == "Select" or self.security_a.get() == ""):
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
            return
        
        if self.password.get() != self.confirm_pass.get():
            messagebox.showerror("Error", "Passwords do not match!", parent=self.root)
            return
        
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="face_recognizer"
            )
            cursor = conn.cursor()
            
            # Check if user exists
            cursor.execute("SELECT * FROM register WHERE email=%s", (self.email.get(),))
            if cursor.fetchone():
                messagebox.showerror("Error", "Email already registered!", parent=self.root)
                return
            
            # Insert new user
            cursor.execute(
                "INSERT INTO register (fname, lname, email, password, contact, securityQ, securityA) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (self.fname.get(), self.lname.get(), self.email.get(), 
                 self.password.get(), self.contact.get(), 
                 self.security_q.get(), self.security_a.get())
            )
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Registration Successful!", parent=self.root)
            self.root.destroy()
            
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}", parent=self.root)


class ResetPassword:
    def __init__(self, root, email):
        self.root = root
        self.email = email
        self.root.title("Reset Password")
        self.root.geometry("500x550+450+150")
        self.root.configure(bg="#ffffff")
        self.root.resizable(False, False)
        
        # Header
        header = Frame(self.root, bg="#533483", height=80)
        header.place(x=0, y=0, width=500, height=80)
        
        Label(header, text="Reset Password", 
              font=("Segoe UI", 24, "bold"), 
              fg="#ffffff", bg="#533483").place(x=130, y=20)
        
        # Form
        form = Frame(self.root, bg="#ffffff")
        form.place(x=50, y=110, width=400, height=420)
        
        # Email (read-only)
        Label(form, text="EMAIL", font=("Segoe UI", 9, "bold"), 
              fg="#666666", bg="#ffffff").place(x=0, y=0)
        email_entry = Entry(form, font=("Segoe UI", 12), bg="#f0f0f0", 
                           fg="#999999", bd=0, state="readonly")
        email_entry.place(x=0, y=25, width=400, height=40)
        email_entry.config(state="normal")
        email_entry.insert(0, self.email if self.email else "Enter email in login page")
        email_entry.config(state="readonly")
        
        # Security Question
        Label(form, text="SECURITY QUESTION", font=("Segoe UI", 9, "bold"), 
              fg="#666666", bg="#ffffff").place(x=0, y=85)
        
        self.security_q = ttk.Combobox(form, font=("Segoe UI", 11), state="readonly")
        self.security_q['values'] = ("Select", "Your Birth Place", 
                                      "Your Best Friend Name", "Your Pet Name")
        self.security_q.current(0)
        self.security_q.place(x=0, y=110, width=400, height=40)
        
        # Security Answer
        Label(form, text="SECURITY ANSWER", font=("Segoe UI", 9, "bold"), 
              fg="#666666", bg="#ffffff").place(x=0, y=170)
        self.security_a = Entry(form, font=("Segoe UI", 12), bg="#f0f0f0", 
                               fg="#1a1a3e", bd=0, insertbackground="#1a1a3e")
        self.security_a.place(x=0, y=195, width=400, height=40)
        
        # New Password
        Label(form, text="NEW PASSWORD", font=("Segoe UI", 9, "bold"), 
              fg="#666666", bg="#ffffff").place(x=0, y=255)
        self.new_pass = Entry(form, font=("Segoe UI", 12), bg="#f0f0f0", 
                             fg="#1a1a3e", bd=0, show="●", insertbackground="#1a1a3e")
        self.new_pass.place(x=0, y=280, width=400, height=40)
        
        # Reset Button
        reset_btn = Button(form, text="RESET PASSWORD", 
                          font=("Segoe UI", 13, "bold"), 
                          bg="#533483", fg="#ffffff", bd=0, cursor="hand2",
                          activebackground="#3d2661", activeforeground="#ffffff",
                          command=self.reset_password)
        reset_btn.place(x=50, y=350, width=300, height=50)
        
        reset_btn.bind("<Enter>", lambda e: reset_btn.config(bg="#3d2661"))
        reset_btn.bind("<Leave>", lambda e: reset_btn.config(bg="#533483"))
    
    def reset_password(self):
        if (self.security_q.get() == "Select" or 
            self.security_a.get() == "" or self.new_pass.get() == ""):
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
            return
        
        if not self.email or self.email == "Enter your email":
            messagebox.showerror("Error", "Please enter email in login page first!", parent=self.root)
            return
        
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="face_recognizer"
            )
            cursor = conn.cursor()
            
            # Verify security question and answer
            cursor.execute(
                "SELECT * FROM register WHERE email=%s AND securityQ=%s AND securityA=%s",
                (self.email, self.security_q.get(), self.security_a.get())
            )
            
            if cursor.fetchone() is None:
                messagebox.showerror("Error", "Invalid security answer!", parent=self.root)
                return
            
            # Update password
            cursor.execute(
                "UPDATE register SET password=%s WHERE email=%s",
                (self.new_pass.get(), self.email)
            )
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Password reset successfully!", parent=self.root)
            self.root.destroy()
            
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    ModernLogin(root)
    root.mainloop()