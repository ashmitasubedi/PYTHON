from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import os
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error







class Student:
    def __init__(self, root):#CONSTUUCTOR CALLED root represents the main Tkinter window
        self.root = root
        self.root.geometry("1530x790+0+0")#SETTING THE GEOMETRY OF THE WINDOW
        self.root.title("Face Recognition Attendance System")
        self.root.configure(bg="#0a0e27")
        #variables
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
        
        
        # Color scheme          
        self.colors = {# Custom color palette
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
        # Left Label Frame
        Left_frame = LabelFrame(main_frame, bd=2, bg=self.colors['primary'], relief=RIDGE,#LabelFrame banako
                                text="Student Details", font=("Helvetica", 12, "bold"), fg="white")
        Left_frame.place(x=10, y=10, width=760, height=580)
       # current courses
        current_course = LabelFrame(
            Left_frame, 
            bd=2, 
            bg=self.colors['primary'], 
            relief=RIDGE,
            text="Current Courses", 
            font=("Helvetica", 12, "bold"), 
            fg="white"
        )
        current_course.place(x=5, y=5, width=740, height=130)

        # ------------------ Department ------------------
        dep_label = Label(
            current_course,
            text="Department",
            font=("Helvetica", 12, "bold"),
            bg=self.colors['primary'],
            fg="white"
        )
        dep_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        dep_combo = ttk.Combobox(
            current_course,
            textvariable=self.var_dep,
            font=("Helvetica", 12, "bold"),
            state="readonly",
            width=20
        )
        dep_combo["values"] = ("Select Department", "Arts", "IT", "Science", "Commerce")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        # ------------------ Semester ------------------
        semester_label = Label(
            current_course,
            text="Semester",
            font=("Helvetica", 12, "bold"),
            bg=self.colors['primary'],
            fg="white"
        )
        semester_label.grid(row=0, column=2, padx=10, pady=5, sticky=W)

        semester_combo = ttk.Combobox(
            current_course,
            textvariable=self.var_semester,
            font=("Helvetica", 12, "bold"),
            state="readonly",
            width=20
        )
        semester_combo["values"] = (
            "Select Semester",
            "Semester 1", "Semester 2", "Semester 3", "Semester 4",
            "Semester 5", "Semester 6", "Semester 7", "Semester 8"
        )
        semester_combo.current(0)
        semester_combo.grid(row=0, column=3, padx=10, pady=5, sticky=W)

        # ------------------ Year ------------------
        year_label = Label(
            current_course,
            text="Year",
            font=("Helvetica", 12, "bold"),
            bg=self.colors['primary'],
            fg="white"
        )
        year_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)

        year_combo = ttk.Combobox(
            current_course,
            textvariable=self.var_year,
            font=("Helvetica", 12, "bold"),
            state="readonly",
            width=20
        )
        year_combo["values"] = ("Select Year", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25")
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=10, pady=5, sticky=W)

        # ------------------ Course ------------------
        course_label = Label(
            current_course,
            text="Course",
            font=("Helvetica", 12, "bold"),
            bg=self.colors['primary'],
            fg="white"
        )
        course_label.grid(row=1, column=2, padx=10, pady=5, sticky=W)

        course_combo = ttk.Combobox(
            current_course,
            textvariable=self.var_course,
            font=("Helvetica", 12, "bold"),
            state="readonly",
            width=20
        )
        course_combo["values"] = ("Select Course", "BCA", "BBA", "BSC-CSIT", "BIM", "BBS")
        course_combo.current(0)
        course_combo.grid(row=1, column=3, padx=10, pady=5, sticky=W)

        #class student information
        student_info = LabelFrame( Left_frame, bd=2, bg=self.colors['primary'],  relief=RIDGE, text="Student Information", font=("Helvetica", 12, "bold"),  fg="white")
        student_info.place(x=5, y=140, width=740, height=430)
        # ------------------ Student ID ------------------
        studentId_label = Label(student_info,text="Student ID", font=("Helvetica", 12, "bold"),bg=self.colors['primary'], fg="white")
        studentId_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)
        studentId_entry = ttk.Entry( student_info,width=20,textvariable=self.var_std_id,font=("Helvetica", 12, "bold"))
        studentId_entry.grid(row=0, column=1, padx=10, pady=5, sticky=W)
        # Student Name
        studentName_label = Label(student_info,text="Student Name", font=("Helvetica", 12, "bold"),bg=self.colors['primary'], fg="white")
        studentName_label.grid(row=0, column=2, padx=10, pady=5, sticky=W)
        studentName_entry = ttk.Entry( student_info,width=20,textvariable=self.var_std_name,font=("Helvetica", 12, "bold"))
        studentName_entry.grid(row=0, column=3, padx=10, pady=5, sticky=W)
        #class roll no  
        classRoll_label = Label(student_info,text="Class Roll No", font=("Helvetica", 12, "bold"),bg=self.colors['primary'], fg="white")
        classRoll_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)
        classRoll_entry = ttk.Entry( student_info,width=20,textvariable=self.var_roll,font=("Helvetica", 12, "bold"))
        classRoll_entry.grid(row=1, column=1, padx=10, pady=5, sticky=W)
        # Gender
            # Gender
        gender_label = Label(student_info, text="Gender", font=("Helvetica", 12, "bold"),
                            bg=self.colors['primary'], fg="white")
        gender_label.grid(row=1, column=2, padx=10, pady=5, sticky=W)

        # Frame to hold radio buttons horizontally
        gender_frame = Frame(student_info, bg=self.colors['primary'])
        gender_frame.grid(row=1, column=3, padx=10, pady=5, sticky=W)

        self.gender_var = StringVar()
        self.gender_var.set("Male")  # default selected

        male_radio = ttk.Radiobutton(gender_frame, text="Male",
                                    variable=self.gender_var, value="Male")
        male_radio.pack(side=LEFT, padx=5)

        female_radio = ttk.Radiobutton(gender_frame, text="Female",
                                    variable=self.gender_var, value="Female")
        female_radio.pack(side=LEFT, padx=5)

        other_radio = ttk.Radiobutton(gender_frame, text="Other",
                                    variable=self.gender_var, value="Other")
        other_radio.pack(side=LEFT, padx=5)

        # Date of Birth
      

        # Date of Birth
        dob_label = Label(student_info, text="Date of Birth", font=("Helvetica", 12, "bold"),
                        bg=self.colors['primary'], fg="white")
        dob_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)

        dob_entry = DateEntry(student_info, width=18,textvariable=self.var_dob, font=("Helvetica", 12, "bold"),
                            date_pattern="yyyy-mm-dd")   # or "dd-mm-yyyy"
        dob_entry.grid(row=2, column=1, padx=10, pady=5, sticky=W)

        #email
        email_label = Label(student_info,text="Email", font=("Helvetica", 12, "bold"),bg=self.colors['primary'], fg="white")
        email_label.grid(row=2, column=2, padx=10, pady=5, sticky=W)
        email_entry = ttk.Entry( student_info,width=20,textvariable=self.var_email,font=("Helvetica", 12, "bold"))
        email_entry.grid(row=2, column=3, padx=10, pady=5, sticky=W)
        #phone no
        phone_label = Label(student_info,text="Phone No", font=("Helvetica", 12, "bold"),bg=self.colors['primary'], fg="white")
        phone_label.grid(row=3, column=0, padx=10, pady=5, sticky=W)
        phone_entry = ttk.Entry( student_info,width=20,textvariable=self.var_phone,font=("Helvetica", 12, "bold"))
        phone_entry.grid(row=3, column=1, padx=10, pady=5, sticky=W)
        #address
        address_label = Label(student_info,text="Address", font=("Helvetica", 12, "bold"),bg=self.colors['primary'], fg="white")
        address_label.grid(row=3, column=2, padx=10, pady=5, sticky=W)
        address_entry = ttk.Entry( student_info,width=20,textvariable=self.var_address,font=("Helvetica", 12, "bold"))
        address_entry.grid(row=3, column=3, padx=10, pady=5, sticky=W)

        #teacher name
        teacherName_label = Label(student_info,text="Teacher Name", font=("Helvetica", 12, "bold"),bg=self.colors['primary'], fg="white")
        teacherName_label.grid(row=4, column=0, padx=10, pady=  5, sticky=W)
        teacherName_entry = ttk.Entry( student_info,width=20,textvariable=self.var_teacher,font=("Helvetica", 12, "bold"))
        teacherName_entry.grid(row=4, column=1, padx=10, pady=5, sticky=W)
        # Radio Buttons
        self.var_photo_sample = StringVar()
        self.var_photo_sample.set("No")  # Default value

        radiobtn1 = ttk.Radiobutton(student_info, text="Take Photo Sample",
                                    variable=self.var_photo_sample, value="Yes")
        radiobtn1.grid(row=5, column=0, padx=10, pady=10, sticky=W)

        radiobtn2 = ttk.Radiobutton(student_info, text="No Photo Sample",
                                    variable=self.var_photo_sample, value="No")
        radiobtn2.grid(row=5, column=1, padx=10, pady=10, sticky=W)

     # Buttons Frame (Main)
        btn_frame = Frame(student_info, bd=2, relief=RIDGE, bg=self.colors['primary'])
        btn_frame.place(x=5, y=250, width=720, height=90)

        # Row 1 button frame
        row1 = Frame(btn_frame, bg=self.colors['primary'])
        row1.pack(pady=5)

        save_btn = Button(row1, text="Save",command=self.add_data, width=15, font=("Helvetica", 12, "bold"),
                        bg=self.colors['success'], fg="white")
        save_btn.pack(side=LEFT, padx=10)

        update_btn = Button(row1, text="Update", width=15, font=("Helvetica", 12, "bold"),
                    bg=self.colors['primary'], fg="white", command=self.update_data)

        update_btn.pack(side=LEFT, padx=10)

        delete_btn = Button(row1, text="Delete", width=15,command=self.delete_data, font=("Helvetica", 12, "bold"),
                            bg=self.colors['danger'], fg="white")
        delete_btn.pack(side=LEFT, padx=10)

        reset_btn = Button(row1, text="Reset", width=15,command=self.reset_data, font=("Helvetica", 12, "bold"),
                        bg=self.colors['warning'], fg="white")
        reset_btn.pack(side=LEFT, padx=10)

        # Row 2 button frame
        row2 = Frame(btn_frame, bg=self.colors['primary'])
        row2.pack(pady=5)

        take_photo_btn = Button(row2, text="Take Photo Sample", width=20, 
                                font=("Helvetica", 12, "bold"), bg=self.colors['bg_dark'], fg="white")
        take_photo_btn.pack(side=LEFT, padx=20)

        update_photo_btn = Button(row2, text="Update Photo Sample", width=20,
                                font=("Helvetica", 12, "bold"), bg=self.colors['bg_card'], fg="white")
        update_photo_btn.pack(side=LEFT, padx=20)

                # Right Label Frame
        Right_frame = LabelFrame(main_frame, bd=2, bg=self.colors['primary'], relief=RIDGE,
                                text="Student Details", font=("Helvetica", 12, "bold"), fg="white")
        Right_frame.place(x=780, y=10, width=740, height=580)

        # Search System Label
        search_lbl = Label(Right_frame, text="Search System", font=("Helvetica", 12, "bold"),
                        bg=self.colors['primary'], fg="white")
        search_lbl.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        # Sub-frame for search controls
        search_frame = Frame(Right_frame, bg=self.colors['primary'])
        search_frame.grid(row=1, column=0, columnspan=5, padx=10, pady=5, sticky=W)

        # Search By Combobox
        search_combo = ttk.Combobox(search_frame, font=("Helvetica", 12, "bold"),
                                    state="readonly", width=12)
        search_combo["values"] = ("Select", "Roll No", "Phone No", "Student ID")
        search_combo.current(0)
        search_combo.pack(side=LEFT, padx=5)

        # Search Entry
        search_entry = ttk.Entry(search_frame, width=18, font=("Helvetica", 12, "bold"))
        search_entry.pack(side=LEFT, padx=5)

        # Search Button
        search_btn = Button(search_frame, text="Search", width=10, font=("Helvetica", 12, "bold"),
                            bg=self.colors['bg_dark'], fg="white", bd=0)
        search_btn.pack(side=LEFT, padx=5)

        # Show All Button
        showAll_btn = Button(search_frame, text="Show All", width=10, font=("Helvetica", 12, "bold"),
                            bg=self.colors['bg_dark'], fg="white", bd=0)
        showAll_btn.pack(side=LEFT, padx=5)
        # Table Frame
        table_frame = Frame(Right_frame, bd=2, bg=self.colors['bg_card'], relief=RIDGE)
        table_frame.place(x=10, y=100, width=560, height=450)
        # Scrollbars
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)
        self.student_table = ttk.Treeview(table_frame, columns=("dep", "course", "year", "sem", "id", "name", "roll","gender", "dob", "email", "phone", "address", "teacher", "photo"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        #configuring scrollbars
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("dep", text="Department")
        self.student_table.heading("course", text="Course")
        self.student_table.heading("year", text="Year")
        self.student_table.heading("sem", text="Semester")
        self.student_table.heading("id", text="Student ID")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("roll", text="Roll No")
        self.student_table.heading("gender", text="Gender")
        self.student_table.heading("dob", text="D.O.B")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("phone", text="Phone No")
        self.student_table.heading("address", text="Address")
        self.student_table.heading("teacher", text="Teacher Name")
        self.student_table.heading("photo", text="Photo Sample Status")
        self.student_table['show'] = 'headings'
        self.student_table.column("dep", width=100)
        self.student_table.column("course", width=100)

        self.student_table.column("year", width=100)
        self.student_table.column("sem", width=100)
        self.student_table.column("id", width=100)
        self.student_table.column("name", width=100)
        self.student_table.column("roll", width=100)
        self.student_table.column("gender", width=100)
        self.student_table.column("dob", width=100)
        self.student_table.column("email", width=150)
        self.student_table.column("phone", width=100)
        self.student_table.column("address", width=150)
        self.student_table.column("teacher", width=100)
        self.student_table.column("photo", width=150)
        self.student_table.pack(fill=BOTH, expand=1)
        self.fetch_data()
        self.student_table.bind("<ButtonRelease>", self.get_cursor)
    #function declearation
    def add_data(self):
        if self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "" or self.var_roll.get() == "" or self.var_email.get() == "" or self.var_phone.get() == "" or self.var_address.get() == "" or self.var_teacher.get() == "" or self.var_dob.get() == "" or self.var_course.get() == "Select Course" or self.var_year.get() == "Select Year" or self.var_semester.get() == "Select Semester":  
            messagebox.showerror("Error", "All Fields are required", parent=self.root)

        else:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    username="root",
                    password="",
                    database="face_recognizer"
                )
                my_cursor = conn.cursor()
                my_cursor.execute("INSERT INTO student VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                    
                    self.var_dep.get(),
                    self.var_course.get(),
                    self.var_year.get(),
                    self.var_semester.get(),
                    self.var_std_id.get(),
                    self.var_std_name.get(),
                    self.var_roll.get(),
                    self.gender_var.get(),
                    self.var_dob.get(),
                    self.var_email.get(),
                    self.var_phone.get(),
                    self.var_address.get(),
                    self.var_teacher.get(),
                    self.var_photo_sample.get() # Assuming photo sample status is "No" by default
                ))
                conn.commit() 
                conn.close()
                self.fetch_data()
                messagebox.showinfo("Success", "Student details has been added successfully", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)  
    #fetch data from database
    def fetch_data(self):
      try:
        conn = mysql.connector.connect(
            host="localhost",
            username="root",
            password="",
            database="face_recognizer"
        )
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM student")
        data = my_cursor.fetchall()

        if len(data) != 0:
            self.student_table.delete(*self.student_table.get_children())
            for row in data:
                self.student_table.insert("", END, values=row)
        
        conn.close()
      except Error as e:
        messagebox.showerror("Error", f"Due To: {str(e)}", parent=self.root)

#get cursor
    def get_cursor(self, event=""):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)#item is used to get the data of the selected row
        data = content["values"]#list ma value save vayo

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
    #update function

    def update_data(self):
         if self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "" or self.var_roll.get() == "" or self.var_email.get() == "" or self.var_phone.get() == "" or self.var_address.get() == "" or self.var_teacher.get() == "" or self.var_dob.get() == "" or self.var_course.get() == "Select Course" or self.var_year.get() == "Select Year" or self.var_semester.get() == "Select Semester":  
            messagebox.showerror("Error", "All Fields are required", parent=self.root)

         else:
            try:
                Update = messagebox.askyesno("Update", "Do you want to update this student details?", parent=self.root)
                if Update > 0:
                    conn = mysql.connector.connect(
                        host="localhost",
                        username="root",
                        password="",
                        database="face_recognizer"
                    )
                    my_cursor = conn.cursor()
                    
                    my_cursor = conn.cursor()
                    my_cursor.execute("UPDATE student SET department=%s, course=%s, year=%s, semester=%s, name=%s, roll_no=%s, gender=%s, dob=%s, email=%s, phone=%s, address=%s, teacher=%s ,photoSample=%s WHERE student_id=%s", (
                        self.var_dep.get(),
                        self.var_course.get(),
                        self.var_year.get(),
                        self.var_semester.get(),
                        self.var_std_name.get(),
                        self.var_roll.get(),
                        self.gender_var.get(),
                        self.var_dob.get(),
                        self.var_email.get(),
                        self.var_phone.get(),
                        self.var_address.get(),
                        self.var_teacher.get(),
                        self.var_photo_sample.get(),
                        self.var_std_id.get()
                    ))
                    conn.commit()
                    self.fetch_data()
                    conn.close()
                    messagebox.showinfo("Success", "Student details successfully updated", parent=self.root)
                else:
                    return

            except Exception as es:
                 messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)
    #delete function
    def delete_data(self):
        if self.var_std_id.get() == "":
            messagebox.showerror("Error", "Student ID must be required", parent=self.root)
        else:
            try:
                delete = messagebox.askyesno("Delete", "Do you want to delete this student?", parent=self.root)
                if delete > 0:
                    conn = mysql.connector.connect(
                        host="localhost",
                        username="root",
                        password="",
                        database="face_recognizer"
                    )
                    my_cursor = conn.cursor()
                    sql = "DELETE FROM student WHERE student_id=%s"
                    val = (self.var_std_id.get(),)
                    my_cursor.execute(sql, val)
                else:
                    if not delete:
                        return
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Delete", "Successfully deleted student details", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)
    #reset function
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
#generate data set or take photo sample
    def generate_dataset(self):
        if self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "" or self.var_roll.get() == "" or self.var_email.get() == "" or self.var_phone.get() == "" or self.var_address.get() == "" or self.var_teacher.get() == "" or self.var_dob.get() == "" or self.var_course.get() == "Select Course" or self.var_year.get() == "Select Year" or self.var_semester.get() == "Select Semester":  
            messagebox.showerror("Error", "All Fields are required", parent=self.root)  
        else:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    username="root",
                    password="",
                    database="face_recognizer"
                )
                my_cursor = conn.cursor()
                my_cursor.execute("select * from student")
                myresult = my_cursor.fetchall()
                id = 0
                for x in myresult:
                    id += 1
                my_cursor.execute("update student set department=%s, course=%s, year=%s, semester=%s, name=%s, roll_no=%s, gender=%s, dob=%s, email=%s, phone=%s, address=%s, teacher=%s ,photoSample=%s WHERE student_id=%s", (
                    
                    self.var_dep.get(),
                    self.var_course.get(),
                    self.var_year.get(),
                    self.var_semester.get(),
                    self.var_std_name.get(),
                    self.var_roll.get(),
                    self.gender_var.get(),
                    self.var_dob.get(),
                    self.var_email.get(),
                    self.var_phone.get(),
                    self.var_address.get(),
                    self.var_teacher.get(),
                    self.var_photo_sample.get(),
                    self.var_std_id.get()
                ))
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)
  #load predefined data on face frontals from opencv
                #  haarcascade classifier
                face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
                def face_cropped(img):
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
                    # scaling factor = 1.3
                    # minimum neighbor = 5
                    for (x, y, w, h) in faces:
                        face_cropped = img[y:y+h, x:x+w]
                        return face_cropped             


    
if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()


