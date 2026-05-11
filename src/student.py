from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import os
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import cv2
import re
import numpy as np
from face_duplicate_checker import FaceDuplicateChecker   


class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition Attendance System")
        self.root.configure(bg="#0a0e27")

        # Variables
        self.var_dep = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_roll = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()
        self.var_teacher = StringVar()
        self.var_photo_sample = StringVar()
        self.var_search_by = StringVar()
        self.var_search_txt = StringVar()

        # Color scheme
        self.colors = {
            'bg_dark': '#0a0e27',
            'bg_card': '#1a1f3a',
            'primary': '#4a90e2',
            'secondary': '#50e3c2',
            'success': '#27ae60',
            'danger': '#e74c3c',
            'warning': '#f39c12'
        }

        title_lbl = Label(self.root, text="STUDENT MANAGEMENT SYSTEM",
                          font=("Helvetica", 30, "bold"), bg=self.colors['bg_dark'], fg="white")
        title_lbl.pack(pady=20)

        main_frame = Frame(self.root, bg=self.colors['bg_dark'])
        main_frame.place(x=0, y=100, width=1530, height=600)

        # ───────────────────────────────────────────
        # LEFT FRAME
        # ───────────────────────────────────────────
        Left_frame = LabelFrame(main_frame, bd=2, bg=self.colors['primary'], relief=RIDGE,
                                text="Student Details", font=("Helvetica", 12, "bold"), fg="white")
        Left_frame.place(x=10, y=10, width=760, height=580)

        # Department → Course mapping
        self.department_courses = {
            "Arts":     ("BA", "BFA", "BHM"),
            "IT":       ("BCA", "BIM"),
            "Science":  ("BSC", "BSC-CSIT"),
            "Commerce": ("BBA", "BBS")
        }

        # ── Current Courses sub-frame ──
        current_course = LabelFrame(Left_frame, bd=2, bg=self.colors['primary'], relief=RIDGE,
                                    text="Current Courses", font=("Helvetica", 12, "bold"), fg="white")
        current_course.place(x=5, y=5, width=740, height=130)

        # Department
        Label(current_course, text="Department", font=("Helvetica", 12, "bold"),
              bg=self.colors['primary'], fg="white").grid(row=0, column=0, padx=10, pady=5, sticky=W)

        dep_combo = ttk.Combobox(current_course, textvariable=self.var_dep,
                                 font=("Helvetica", 12, "bold"), state="readonly", width=20)
        dep_combo["values"] = ("Select Department", "Arts", "IT", "Science", "Commerce")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=10, pady=5, sticky=W)
        dep_combo.bind("<<ComboboxSelected>>", self.update_courses)

        # Semester
        Label(current_course, text="Semester", font=("Helvetica", 12, "bold"),
              bg=self.colors['primary'], fg="white").grid(row=0, column=2, padx=10, pady=5, sticky=W)

        semester_combo = ttk.Combobox(current_course, textvariable=self.var_semester,
                                      font=("Helvetica", 12, "bold"), state="readonly", width=20)
        semester_combo["values"] = ("Select Semester",
                                    "Semester 1", "Semester 2", "Semester 3", "Semester 4",
                                    "Semester 5", "Semester 6", "Semester 7", "Semester 8")
        semester_combo.current(0)
        semester_combo.grid(row=0, column=3, padx=10, pady=5, sticky=W)

        # Year
        Label(current_course, text="Year", font=("Helvetica", 12, "bold"),
              bg=self.colors['primary'], fg="white").grid(row=1, column=0, padx=10, pady=5, sticky=W)

        year_combo = ttk.Combobox(current_course, textvariable=self.var_year,
                                  font=("Helvetica", 12, "bold"), state="readonly", width=20)
        year_combo["values"] = ("Select Year", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25")
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=10, pady=5, sticky=W)

        # Course
        Label(current_course, text="Course", font=("Helvetica", 12, "bold"),
              bg=self.colors['primary'], fg="white").grid(row=1, column=2, padx=10, pady=5, sticky=W)

        self.course_combo = ttk.Combobox(current_course, textvariable=self.var_course,
                                         font=("Helvetica", 12, "bold"), state="readonly", width=20)
        self.course_combo["values"] = ("Select Course",)
        self.course_combo.current(0)
        self.course_combo.grid(row=1, column=3, padx=10, pady=5, sticky=W)

        # ── Student Information sub-frame ──
        student_info = LabelFrame(Left_frame, bd=2, bg=self.colors['primary'], relief=RIDGE,
                                  text="Student Information", font=("Helvetica", 12, "bold"), fg="white")
        student_info.place(x=5, y=140, width=740, height=430)

        # Student ID
        Label(student_info, text="Student ID", font=("Helvetica", 12, "bold"),
              bg=self.colors['primary'], fg="white").grid(row=0, column=0, padx=10, pady=5, sticky=W)
        ttk.Entry(student_info, width=20, textvariable=self.var_std_id,
                  font=("Helvetica", 12, "bold")).grid(row=0, column=1, padx=10, pady=5, sticky=W)

        # Student Name
        Label(student_info, text="Student Name", font=("Helvetica", 12, "bold"),
              bg=self.colors['primary'], fg="white").grid(row=0, column=2, padx=10, pady=5, sticky=W)
        ttk.Entry(student_info, width=20, textvariable=self.var_std_name,
                  font=("Helvetica", 12, "bold")).grid(row=0, column=3, padx=10, pady=5, sticky=W)

        # Class Roll No
        Label(student_info, text="Class Roll No", font=("Helvetica", 12, "bold"),
              bg=self.colors['primary'], fg="white").grid(row=1, column=0, padx=10, pady=5, sticky=W)
        ttk.Entry(student_info, width=20, textvariable=self.var_roll,
                  font=("Helvetica", 12, "bold")).grid(row=1, column=1, padx=10, pady=5, sticky=W)

        # Gender
        Label(student_info, text="Gender", font=("Helvetica", 12, "bold"),
              bg=self.colors['primary'], fg="white").grid(row=1, column=2, padx=10, pady=5, sticky=W)

        gender_frame = Frame(student_info, bg=self.colors['primary'])
        gender_frame.grid(row=1, column=3, padx=10, pady=5, sticky=W)

        self.gender_var = StringVar()
        self.gender_var.set("Male")

        ttk.Radiobutton(gender_frame, text="Male",   variable=self.gender_var, value="Male").pack(side=LEFT, padx=5)
        ttk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, value="Female").pack(side=LEFT, padx=5)
        ttk.Radiobutton(gender_frame, text="Other",  variable=self.gender_var, value="Other").pack(side=LEFT, padx=5)

        # Date of Birth
        Label(student_info, text="Date of Birth", font=("Helvetica", 12, "bold"),
              bg=self.colors['primary'], fg="white").grid(row=2, column=0, padx=10, pady=5, sticky=W)
        DateEntry(student_info, width=18, textvariable=self.var_dob,
                  font=("Helvetica", 12, "bold"), date_pattern="yyyy-mm-dd").grid(row=2, column=1, padx=10, pady=5, sticky=W)

        # Email
        Label(student_info, text="Email", font=("Helvetica", 12, "bold"),
              bg=self.colors['primary'], fg="white").grid(row=2, column=2, padx=10, pady=5, sticky=W)
        ttk.Entry(student_info, width=20, textvariable=self.var_email,
                  font=("Helvetica", 12, "bold")).grid(row=2, column=3, padx=10, pady=5, sticky=W)

        # Phone No
        Label(student_info, text="Phone No", font=("Helvetica", 12, "bold"),
              bg=self.colors['primary'], fg="white").grid(row=3, column=0, padx=10, pady=5, sticky=W)
        ttk.Entry(student_info, width=20, textvariable=self.var_phone,
                  font=("Helvetica", 12, "bold")).grid(row=3, column=1, padx=10, pady=5, sticky=W)

        # Address
        Label(student_info, text="Address", font=("Helvetica", 12, "bold"),
              bg=self.colors['primary'], fg="white").grid(row=3, column=2, padx=10, pady=5, sticky=W)
        ttk.Entry(student_info, width=20, textvariable=self.var_address,
                  font=("Helvetica", 12, "bold")).grid(row=3, column=3, padx=10, pady=5, sticky=W)

        # Teacher Name
        Label(student_info, text="Teacher Name", font=("Helvetica", 12, "bold"),
              bg=self.colors['primary'], fg="white").grid(row=4, column=0, padx=10, pady=5, sticky=W)
        ttk.Entry(student_info, width=20, textvariable=self.var_teacher,
                  font=("Helvetica", 12, "bold")).grid(row=4, column=1, padx=10, pady=5, sticky=W)

        # Photo Sample Radio Buttons
        self.var_photo_sample = StringVar()
        self.var_photo_sample.set("No")

        ttk.Radiobutton(student_info, text="Take Photo Sample",
                        variable=self.var_photo_sample, value="Yes").grid(row=5, column=0, padx=10, pady=10, sticky=W)
        ttk.Radiobutton(student_info, text="No Photo Sample",
                        variable=self.var_photo_sample, value="No").grid(row=5, column=1, padx=10, pady=10, sticky=W)

        # ── Buttons ──
        btn_frame = Frame(student_info, bd=2, relief=RIDGE, bg=self.colors['primary'])
        btn_frame.place(x=5, y=250, width=720, height=90)

        row1 = Frame(btn_frame, bg=self.colors['primary'])
        row1.pack(pady=5)

        Button(row1, text="Save",   command=self.add_data,    width=15, font=("Helvetica", 12, "bold"),
               bg=self.colors['success'], fg="white").pack(side=LEFT, padx=10)
        Button(row1, text="Update", command=self.update_data, width=15, font=("Helvetica", 12, "bold"),
               bg=self.colors['primary'], fg="white").pack(side=LEFT, padx=10)
        Button(row1, text="Delete", command=self.delete_data, width=15, font=("Helvetica", 12, "bold"),
               bg=self.colors['danger'], fg="white").pack(side=LEFT, padx=10)
        Button(row1, text="Reset",  command=self.reset_data,  width=15, font=("Helvetica", 12, "bold"),
               bg=self.colors['warning'], fg="white").pack(side=LEFT, padx=10)

        row2 = Frame(btn_frame, bg=self.colors['primary'])
        row2.pack(pady=5)

        Button(row2, text="Take Photo Sample",   command=self.generate_dataset,     width=20,
               font=("Helvetica", 12, "bold"), bg=self.colors['bg_dark'], fg="white").pack(side=LEFT, padx=20)
        Button(row2, text="Update Photo Sample", command=self.update_photo_sample,  width=20,
               font=("Helvetica", 12, "bold"), bg=self.colors['bg_card'], fg="white").pack(side=LEFT, padx=20)

        # ───────────────────────────────────────────
        # RIGHT FRAME
        # ───────────────────────────────────────────
        Right_frame = LabelFrame(main_frame, bd=2, bg=self.colors['primary'], relief=RIDGE,
                                 text="Student Details", font=("Helvetica", 12, "bold"), fg="white")
        Right_frame.place(x=780, y=10, width=740, height=580)

        Label(Right_frame, text="Search System", font=("Helvetica", 12, "bold"),
              bg=self.colors['primary'], fg="white").grid(row=0, column=0, padx=10, pady=5, sticky=W)

        search_frame = Frame(Right_frame, bg=self.colors['primary'])
        search_frame.grid(row=1, column=0, columnspan=5, padx=10, pady=5, sticky=W)

        search_combo = ttk.Combobox(search_frame, textvariable=self.var_search_by,
                                    font=("Helvetica", 12, "bold"), state="readonly", width=12)
        search_combo["values"] = ("Select", "Roll No", "Phone No", "Student ID")
        search_combo.current(0)
        search_combo.pack(side=LEFT, padx=5)

        ttk.Entry(search_frame, textvariable=self.var_search_txt,
                  width=18, font=("Helvetica", 12, "bold")).pack(side=LEFT, padx=5)

        Button(search_frame, text="Search",   command=self.search_data, width=10,
               font=("Helvetica", 12, "bold"), bg=self.colors['bg_dark'], fg="white", bd=0).pack(side=LEFT, padx=5)
        Button(search_frame, text="Show All", command=self.fetch_data,  width=10,
               font=("Helvetica", 12, "bold"), bg=self.colors['bg_dark'], fg="white", bd=0).pack(side=LEFT, padx=5)

        # Table
        table_frame = Frame(Right_frame, bd=2, bg=self.colors['bg_card'], relief=RIDGE)
        table_frame.place(x=10, y=100, width=560, height=450)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.student_table = ttk.Treeview(
            table_frame,
            columns=("dep", "course", "year", "sem", "id", "name", "roll",
                     "gender", "dob", "email", "phone", "address", "teacher", "photo"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT,  fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        headings = {
            "dep": "Department", "course": "Course", "year": "Year", "sem": "Semester",
            "id": "Student ID", "name": "Name", "roll": "Roll No", "gender": "Gender",
            "dob": "D.O.B", "email": "Email", "phone": "Phone No",
            "address": "Address", "teacher": "Teacher Name", "photo": "Photo Sample Status"
        }
        widths = {
            "dep": 100, "course": 100, "year": 100, "sem": 100, "id": 100,
            "name": 100, "roll": 100, "gender": 100, "dob": 100,
            "email": 150, "phone": 100, "address": 150, "teacher": 100, "photo": 150
        }
        for col, text in headings.items():
            self.student_table.heading(col, text=text)
            self.student_table.column(col, width=widths[col])

        self.student_table['show'] = 'headings'
        self.student_table.pack(fill=BOTH, expand=1)

        self.fetch_data()
        self.student_table.bind("<ButtonRelease>", self.get_cursor)

    # ─────────────────────────────────────────────────────
    # VALIDATE FIELDS
    # ─────────────────────────────────────────────────────
    def validate_fields(self):
        if self.var_dep.get() == "Select Department":
            messagebox.showerror("Error", "Please select Department", parent=self.root)
            return False
        if self.var_course.get() == "Select Course":
            messagebox.showerror("Error", "Please select Course", parent=self.root)
            return False
        if self.var_year.get() == "Select Year":
            messagebox.showerror("Error", "Please select Year", parent=self.root)
            return False
        if self.var_semester.get() == "Select Semester":
            messagebox.showerror("Error", "Please select Semester", parent=self.root)
            return False
        if not self.var_std_id.get().strip():
            messagebox.showerror("Error", "Student ID is required", parent=self.root)
            return False
        if not self.var_std_id.get().isdigit():
            messagebox.showerror("Error", "Student ID must be numeric", parent=self.root)
            return False
        if not self.var_std_name.get().strip():
            messagebox.showerror("Error", "Student Name is required", parent=self.root)
            return False
        if not self.var_std_name.get().replace(" ", "").isalpha():
            messagebox.showerror("Error", "Name must contain letters only", parent=self.root)
            return False
        if not self.var_roll.get().strip():
            messagebox.showerror("Error", "Roll number is required", parent=self.root)
            return False
        if not self.var_roll.get().isdigit():
            messagebox.showerror("Error", "Roll number must be numeric", parent=self.root)
            return False
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, self.var_email.get()):
            messagebox.showerror("Error", "Invalid email format (e.g. user@example.com)", parent=self.root)
            return False
        if not self.var_phone.get().strip():
            messagebox.showerror("Error", "Phone number is required", parent=self.root)
            return False
        if not (self.var_phone.get().isdigit() and len(self.var_phone.get()) == 10):
            messagebox.showerror("Error", "Phone number must be exactly 10 digits", parent=self.root)
            return False
        if not self.var_address.get().strip():
            messagebox.showerror("Error", "Address is required", parent=self.root)
            return False
        if not self.var_dob.get().strip():
            messagebox.showerror("Error", "Please select Date of Birth", parent=self.root)
            return False
        if not self.var_teacher.get().strip():
            messagebox.showerror("Error", "Teacher Name is required", parent=self.root)
            return False
        if not self.var_teacher.get().replace(" ", "").isalpha():
            messagebox.showerror("Error", "Teacher name must contain letters only", parent=self.root)
            return False
        return True

    # ─────────────────────────────────────────────────────
    # ADD DATA
    # ─────────────────────────────────────────────────────
    def add_data(self):
        if not self.validate_fields():
            return
        try:
            conn = mysql.connector.connect(
                host="localhost", username="root", password="", database="face_recognizer"
            )
            my_cursor = conn.cursor()
            my_cursor.execute(
                "INSERT INTO student VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                    self.var_dep.get(), self.var_course.get(), self.var_year.get(),
                    self.var_semester.get(), self.var_std_id.get(), self.var_std_name.get(),
                    self.var_roll.get(), self.gender_var.get(), self.var_dob.get(),
                    self.var_email.get(), self.var_phone.get(), self.var_address.get(),
                    self.var_teacher.get(), self.var_photo_sample.get()
                )
            )
            conn.commit()
            conn.close()
            self.fetch_data()
            messagebox.showinfo("Success", "Student details added successfully", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    # ─────────────────────────────────────────────────────
    # FETCH DATA
    # ─────────────────────────────────────────────────────
    def fetch_data(self):
        try:
            conn = mysql.connector.connect(
                host="localhost", username="root", password="", database="face_recognizer"
            )
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT * FROM student")
            data = my_cursor.fetchall()
            conn.close()

            self.student_table.delete(*self.student_table.get_children())
            for row in data:
                self.student_table.insert("", END, values=row)

        except Error as e:
            messagebox.showerror("Error", f"Due To: {str(e)}", parent=self.root)

    # ─────────────────────────────────────────────────────
    # GET CURSOR (row click → fill form)
    # ─────────────────────────────────────────────────────
    def get_cursor(self, event=""):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data = content["values"]
        if not data:
            return

        self.var_dep.set(data[0])
        self.var_course.set(data[1])
        self.var_year.set(data[2])
        self.var_semester.set(data[3])
        self.var_std_id.set(data[4])
        self.var_std_name.set(data[5])
        self.var_roll.set(data[6])
        self.gender_var.set(data[7])
        self.var_dob.set(data[8])
        self.var_email.set(data[9])
        self.var_phone.set(data[10])
        self.var_address.set(data[11])
        self.var_teacher.set(data[12])
        self.var_photo_sample.set(data[13])

    # ─────────────────────────────────────────────────────
    # UPDATE DATA
    # ─────────────────────────────────────────────────────
    def update_data(self):
        if not self.validate_fields():
            return
        try:
            confirm = messagebox.askyesno("Update", "Do you want to update this student's details?", parent=self.root)
            if not confirm:
                return

            conn = mysql.connector.connect(
                host="localhost", username="root", password="", database="face_recognizer"
            )
            my_cursor = conn.cursor()
            my_cursor.execute(
                """UPDATE student
                   SET department=%s, course=%s, year=%s, semester=%s,
                       name=%s, roll_no=%s, gender=%s, dob=%s,
                       email=%s, phone=%s, address=%s, teacher=%s, photoSample=%s
                   WHERE student_id=%s""",
                (
                    self.var_dep.get(), self.var_course.get(), self.var_year.get(),
                    self.var_semester.get(), self.var_std_name.get(), self.var_roll.get(),
                    self.gender_var.get(), self.var_dob.get(), self.var_email.get(),
                    self.var_phone.get(), self.var_address.get(), self.var_teacher.get(),
                    self.var_photo_sample.get(),
                    self.var_std_id.get()
                )
            )
            conn.commit()
            conn.close()
            self.fetch_data()
            messagebox.showinfo("Success", "Student details updated successfully", parent=self.root)

        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    # ─────────────────────────────────────────────────────
    # DELETE PHOTO SAMPLES FROM data/ FOLDER
    # ─────────────────────────────────────────────────────
    def _delete_photos(self, student_id):
        """
        Delete all images of a student from the correct data folder
        """

        # ✅ YOUR ACTUAL FOLDER (FIXED PATH)
        data_dir = r"C:\Users\Dell\Desktop\PYTHON\data"

        if not os.path.exists(data_dir):
            print("[ERROR] Data folder not found:", data_dir)
            return 0

        deleted = 0

        for filename in os.listdir(data_dir):
            file_path = os.path.join(data_dir, filename)

            # ✅ Flexible matching (important fix)
            if str(student_id) in filename and filename.endswith(".jpg"):
                try:
                    os.remove(file_path)
                    print("[DELETED]:", filename)
                    deleted += 1
                except Exception as e:
                    print("[ERROR] Could not delete:", filename, e)

        print("[INFO] Total deleted:", deleted)
        return deleted

    # ─────────────────────────────────────────────────────
    # DELETE DATA
    # ─────────────────────────────────────────────────────
    def delete_data(self):
        if not self.var_std_id.get().strip():
            messagebox.showerror("Error", "Student ID is required", parent=self.root)
            return
        try:
            confirm = messagebox.askyesno(
                "Delete",
                "Do you want to delete this student?\n\n"
                "This will also permanently delete all photo samples for this student.",
                parent=self.root
            )
            if not confirm:
                return

            student_id = self.var_std_id.get()

            # ── Delete from database ──
            conn = mysql.connector.connect(
                host="localhost", username="root", password="", database="face_recognizer"
            )
            my_cursor = conn.cursor()
            my_cursor.execute("DELETE FROM student WHERE student_id=%s", (student_id,))
            conn.commit()
            conn.close()

            # ── Delete photo samples from disk ──
            photos_deleted = self._delete_photos(student_id)

            self.fetch_data()
            self.reset_data()

            if photos_deleted > 0:
                messagebox.showinfo(
                    "Delete",
                    f"Student deleted successfully.\n"
                    f"{photos_deleted} photo sample(s) also removed from disk.",
                    parent=self.root
                )
            else:
                messagebox.showinfo(
                    "Delete",
                    "Student deleted successfully.\n(No photo samples were found on disk.)",
                    parent=self.root
                )

        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    # ─────────────────────────────────────────────────────
    # RESET DATA
    # ─────────────────────────────────────────────────────
    def reset_data(self):
        self.var_dep.set("Select Department")
        self.var_course.set("Select Course")
        self.var_year.set("Select Year")
        self.var_semester.set("Select Semester")
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_roll.set("")
        self.gender_var.set("Male")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_teacher.set("")
        self.var_photo_sample.set("No")

    # ─────────────────────────────────────────────────────
    # CHECK IF FACE PHOTOS ALREADY EXIST FOR THIS STUDENT
    # ─────────────────────────────────────────────────────
    def _photos_already_exist(self, student_id):
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        if not os.path.exists(data_dir):
            return False, 0

        prefix = f"user.{student_id}."
        matching = [f for f in os.listdir(data_dir) if f.startswith(prefix) and f.endswith(".jpg")]
        return len(matching) > 0, len(matching)

    # ─────────────────────────────────────────────────────
    # CHECK IF FACE IS ALREADY RECOGNISED BY TRAINED MODEL
    # ─────────────────────────────────────────────────────
    def _face_already_in_model(self, student_id, cascade_path, classifier_path, cap):
        if not os.path.exists(classifier_path):
            return False, None

        try:
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.read(classifier_path)
        except Exception:
            return False, None

        face_cascade = cv2.CascadeClassifier(cascade_path)
        if face_cascade.empty():
            return False, None

        best_distance = None
        frames_checked = 0
        max_frames = 20

        while frames_checked < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
            frames_checked += 1

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(80, 80))

            for (x, y, w, h) in faces:
                face_roi = gray[y:y + h, x:x + w]
                face_resized = cv2.resize(face_roi, (450, 450))
                predicted_id, distance = clf.predict(face_resized)

                if best_distance is None or distance < best_distance:
                    best_distance = distance

                if predicted_id == int(student_id) and distance < 60:
                    return True, distance

        return False, best_distance

    # ─────────────────────────────────────────────────────
    # GENERATE DATASET (take photo samples)  ← UPDATED
    # ─────────────────────────────────────────────────────
    def generate_dataset(self):
        if not self.validate_fields():
            return

        student_id = self.var_std_id.get()

        # ── Step 1: fast filename check (same ID, no camera needed) ──────
        photos_exist, photo_count = self._photos_already_exist(student_id)
        if photos_exist:
            messagebox.showerror(
                "Already Exists",
                f"Photo samples for Student ID {student_id} already exist!\n"
                f"({photo_count} photos found in the data/ folder)\n\n"
                f"Use 'Update Photo Sample' to re-capture.",
                parent=self.root
            )
            return

        # ── Step 2: verify required files ────────────────────────────────
        if not os.path.exists("data"):
            os.makedirs("data")

        cascade_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "haarcascade_frontalface_default.xml"
        )
        if not os.path.exists(cascade_path):
            messagebox.showerror(
                "Error", f"Cascade file not found at:\n{cascade_path}", parent=self.root
            )
            return

        face_classifier = cv2.CascadeClassifier(cascade_path)
        if face_classifier.empty():
            messagebox.showerror("Error", "Failed to load cascade classifier", parent=self.root)
            return

        # ── Step 3: open camera ONCE (reused for all checks + capture) ───
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Could not open camera", parent=self.root)
            return

        # ── Step 4: CROSS-ID duplicate face check (NEW) ──────────────────
        #   Catches someone registering the SAME face under a DIFFERENT ID.
        messagebox.showinfo(
            "Face Duplicate Check",
            "Please look at the camera.\n\n"
            "The system will compare your face against ALL existing students\n"
            "to make sure this face is not already registered under another ID.\n\n"
            "Click OK to begin.",
            parent=self.root
        )

        checker = FaceDuplicateChecker(data_dir="data")
        is_dup, matched_id, dist = checker.is_duplicate_face(
            cap=cap,
            cascade_path=cascade_path,
            exclude_student_id=None   # compare against everyone
        )

        if is_dup:
            cap.release()
            cv2.destroyAllWindows()
            messagebox.showerror(
                "Duplicate Face Detected",
                f"This face is already registered as Student ID: {matched_id}\n"
                f"(LBPH similarity distance: {dist:.1f}  —  threshold: 60)\n\n"
                "A new registration cannot be created for an existing face.\n"
                "If this is an error, contact the administrator.",
                parent=self.root
            )
            return

        # ── Step 5: trained-model check (existing logic kept) ────────────
        classifier_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "classifier.xml"
        )
        already_recognised, best_dist = self._face_already_in_model(
            student_id, cascade_path, classifier_path, cap
        )
        if already_recognised:
            cap.release()
            cv2.destroyAllWindows()
            messagebox.showerror(
                "Face Already Registered",
                f"The face is already recognised as Student ID {student_id} in the model.\n"
                f"(Recognition distance: {best_dist:.1f})\n\n"
                "Use 'Update Photo Sample' to re-capture if needed.",
                parent=self.root
            )
            return

        # ── Step 6: save student details to DB before capturing ──────────
        try:
            conn = mysql.connector.connect(
                host="localhost", username="root", password="", database="face_recognizer"
            )
            my_cursor = conn.cursor()
            my_cursor.execute(
                """UPDATE student
                   SET department=%s, course=%s, year=%s, semester=%s,
                       name=%s, roll_no=%s, gender=%s, dob=%s,
                       email=%s, phone=%s, address=%s, teacher=%s
                   WHERE student_id=%s""",
                (
                    self.var_dep.get(), self.var_course.get(), self.var_year.get(),
                    self.var_semester.get(), self.var_std_name.get(), self.var_roll.get(),
                    self.gender_var.get(), self.var_dob.get(), self.var_email.get(),
                    self.var_phone.get(), self.var_address.get(), self.var_teacher.get(),
                    student_id
                )
            )
            conn.commit()
            conn.close()
        except Exception as db_err:
            cap.release()
            messagebox.showerror(
                "Database Error", f"Could not save student info:\n{db_err}", parent=self.root
            )
            return

        # ── Step 7: capture 100 face photos ──────────────────────────────
        def face_cropped(img):
            gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                return img[y:y + h, x:x + w]
            return None

        img_id = 0
        messagebox.showinfo(
            "Ready to Capture",
            "All checks passed — no duplicate found.\n\n"
            "Camera will now capture 100 photo samples.\n"
            "Press ENTER or wait for completion.",
            parent=self.root
        )

        while True:
            ret, my_frame = cap.read()
            if not ret:
                messagebox.showerror("Error", "Failed to capture frame", parent=self.root)
                break

            cropped_face = face_cropped(my_frame)
            if cropped_face is not None:
                img_id += 1
                face = cv2.resize(cropped_face, (450, 450))
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                cv2.imwrite(f"data/user.{student_id}.{img_id}.jpg", face)
                cv2.putText(face, f"{img_id}/100", (50, 50),
                            cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
                cv2.imshow("Cropped Face", face)

            display_frame = my_frame.copy()
            cv2.putText(display_frame, f"Capturing: {img_id}/100", (20, 40),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Camera Feed", display_frame)

            if cv2.waitKey(1) == 13 or img_id == 100:
                break

        cap.release()
        cv2.destroyAllWindows()

        # ── Step 8: mark photoSample = Yes in DB ─────────────────────────
        if img_id > 0:
            try:
                conn = mysql.connector.connect(
                    host="localhost", username="root", password="", database="face_recognizer"
                )
                my_cursor = conn.cursor()
                my_cursor.execute(
                    "UPDATE student SET photoSample=%s WHERE student_id=%s",
                    ("Yes", student_id)
                )
                conn.commit()
                conn.close()
            except Exception as db_err:
                messagebox.showwarning(
                    "Warning",
                    f"Photos saved but could not update DB status:\n{db_err}",
                    parent=self.root
                )

            self.fetch_data()
            messagebox.showinfo(
                "Success",
                f"Dataset generation completed!\n{img_id} photos saved for Student ID {student_id}.",
                parent=self.root
            )
        else:
            messagebox.showwarning(
                "Warning",
                "No face detected during capture. Please try again.",
                parent=self.root
            )

    # ─────────────────────────────────────────────────────
    # UPDATE COURSES (department → course dropdown)
    # ─────────────────────────────────────────────────────
    def update_courses(self, event):
        department = self.var_dep.get()
        if department in self.department_courses:
            self.course_combo["values"] = ("Select Course",) + self.department_courses[department]
        else:
            self.course_combo["values"] = ("Select Course",)
        self.course_combo.current(0)

    # ─────────────────────────────────────────────────────
    # SEARCH DATA
    # ─────────────────────────────────────────────────────
    def search_data(self):
        if self.var_search_by.get() == "Select" or not self.var_search_txt.get().strip():
            messagebox.showerror("Error", "Please select search criteria and enter a value", parent=self.root)
            return
        try:
            conn = mysql.connector.connect(
                host="localhost", username="root", password="", database="face_recognizer"
            )
            my_cursor = conn.cursor()

            column_map = {"Roll No": "roll_no", "Phone No": "phone", "Student ID": "student_id"}
            column = column_map[self.var_search_by.get()]
            my_cursor.execute(f"SELECT * FROM student WHERE {column} LIKE %s",
                              ("%" + self.var_search_txt.get() + "%",))
            data = my_cursor.fetchall()
            conn.close()

            self.student_table.delete(*self.student_table.get_children())
            if data:
                for row in data:
                    self.student_table.insert("", END, values=row)
            else:
                messagebox.showinfo("Result", "No record found", parent=self.root)

        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    # ─────────────────────────────────────────────────────
    # UPDATE PHOTO SAMPLE
    # ─────────────────────────────────────────────────────
    def update_photo_sample(self):
        if not self.var_std_id.get().strip():
            messagebox.showerror("Error", "Student ID is required", parent=self.root)
            return
        try:
            conn = mysql.connector.connect(
                host="localhost", username="root", password="", database="face_recognizer"
            )
            my_cursor = conn.cursor()
            my_cursor.execute("UPDATE student SET photoSample=%s WHERE student_id=%s",
                              ("Yes", self.var_std_id.get()))
            conn.commit()
            conn.close()
            self.fetch_data()
            messagebox.showinfo("Success", "Photo sample updated successfully", parent=self.root)

        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)


# ─────────────────────────────────────────────────────
if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()