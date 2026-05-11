from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import os
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import cv2


class Student1:
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
        self.var_search_by = StringVar()
        self.var_search_txt = StringVar()

        
        
        # Color scheme          
        self.colors = {# Custom color palette
            'bg_dark': '#0a0e27',
            'bg_card': '#1a1f3a',
            'primary': '#4a90e2',
            'secondary': '#50e3c2',
            'success': '#27ae60',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'search_bg': '#2c3e50',
            'search_hover': '#34495e'
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
        #courses 
        self.department_courses = {
        "Arts": ("BA", "BFA", "BHM"),
        "IT": ("BCA", "BIM"),
        "Science": ("BSC", "BSC-CSIT"),
        "Commerce": ("BBA", "BBS")
}

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

        # Bind selection event
        dep_combo.bind("<<ComboboxSelected>>", self.update_courses)


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

        self.course_combo = ttk.Combobox(
        current_course,
        textvariable=self.var_course,
        font=("Helvetica", 12, "bold"),
        state="readonly",
         width=20
            )
        self.course_combo["values"] = ("Select Course",)
        self.course_combo.current(0)
        self.course_combo.grid(row=1, column=3, padx=10, pady=5, sticky=W)

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

        take_photo_btn = Button(row2, text="Take Photo Sample",width=20, command=self.generate_dataset,
                                font=("Helvetica", 12, "bold"), bg=self.colors['bg_dark'], fg="white")
        take_photo_btn.pack(side=LEFT, padx=20)

        update_photo_btn = Button(row2, text="Update Photo Sample", width=20,
                                font=("Helvetica", 12, "bold"), bg=self.colors['bg_card'], fg="white")
        update_photo_btn.pack(side=LEFT, padx=20)

        # Right Label Frame
        #--------------------------------------------#
        #-----------------------------------------=---#
        Right_frame = LabelFrame(main_frame, bd=2, bg=self.colors['primary'], relief=RIDGE,
                                text="Student Details", font=("Helvetica", 12, "bold"), fg="white")
        Right_frame.place(x=780, y=10, width=740, height=580)

        # ==================== ENHANCED SEARCH SYSTEM ====================
        # Main search container with modern design
        search_container = LabelFrame(
            Right_frame, 
            bd=3, 
            bg=self.colors['search_bg'], 
            relief=GROOVE,
            text="🔍 Advanced Search System", 
            font=("Helvetica", 13, "bold"), 
            fg="#50e3c2"
        )
        search_container.place(x=10, y=5, width=710, height=85)

        # Search criteria frame
        search_criteria_frame = Frame(search_container, bg=self.colors['search_bg'])
        search_criteria_frame.pack(pady=8, padx=10, fill=X)

        # Search by label
        search_by_label = Label(
            search_criteria_frame,
            text="Search By:",
            font=("Helvetica", 11, "bold"),
            bg=self.colors['search_bg'],
            fg="white"
        )
        search_by_label.pack(side=LEFT, padx=5)

        # Enhanced search combobox with more options
        self.search_combo = ttk.Combobox(
            search_criteria_frame,
            textvariable=self.var_search_by,
            font=("Helvetica", 11, "bold"),
            state="readonly",
            width=14
        )
        self.search_combo["values"] = (
            "Select Option",
            "Student ID", 
            "Name",
            "Roll No", 
            "Phone No",
            "Email",
            "Department",
            "Course"
        )
        self.search_combo.current(0)
        self.search_combo.pack(side=LEFT, padx=5)

        # Search entry with placeholder effect
        self.search_entry = ttk.Entry(
            search_criteria_frame,
            textvariable=self.var_search_txt,
            width=22,
            font=("Helvetica", 11)
        )
        self.search_entry.pack(side=LEFT, padx=5)
        
        # Bind Enter key to search
        self.search_entry.bind('<Return>', lambda e: self.advanced_search())
        
        # Real-time search toggle
        self.realtime_var = IntVar()
        realtime_check = ttk.Checkbutton(
            search_criteria_frame,
            text="Live",
            variable=self.realtime_var,
            command=self.toggle_realtime_search
        )
        realtime_check.pack(side=LEFT, padx=5)

        # Button frame
        search_btn_frame = Frame(search_criteria_frame, bg=self.colors['search_bg'])
        search_btn_frame.pack(side=LEFT, padx=5)

        # Modern search button
        search_btn = Button(
            search_btn_frame, 
            text="🔎 Search", 
            width=10, 
            command=self.advanced_search,
            font=("Helvetica", 10, "bold"),
            bg="#27ae60", 
            fg="white", 
            bd=0,
            relief=FLAT,
            cursor="hand2"
        )
        search_btn.pack(side=LEFT, padx=3)

        # Show All button
        showAll_btn = Button(
            search_btn_frame, 
            text="📋 Show All", 
            width=10, 
            command=self.fetch_data,
            font=("Helvetica", 10, "bold"),
            bg="#3498db", 
            fg="white", 
            bd=0,
            relief=FLAT,
            cursor="hand2"
        )
        showAll_btn.pack(side=LEFT, padx=3)

        # Clear search button
        clear_btn = Button(
            search_btn_frame, 
            text="✖ Clear", 
            width=8, 
            command=self.clear_search,
            font=("Helvetica", 10, "bold"),
            bg="#e74c3c", 
            fg="white", 
            bd=0,
            relief=FLAT,
            cursor="hand2"
        )
        clear_btn.pack(side=LEFT, padx=3)

        # Result count label
        self.result_label = Label(
            Right_frame,
            text="Total Records: 0",
            font=("Helvetica", 10, "italic"),
            bg=self.colors['primary'],
            fg="white"
        )
        self.result_label.place(x=10, y=92)

        # Table Frame
        table_frame = Frame(Right_frame, bd=2, bg=self.colors['bg_card'], relief=RIDGE)
        table_frame.place(x=10, y=115, width=710, height=450)
        
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
            #update result count
            self.result_label.config(text=f"Total Records: {len(data)}")
        else:
            self.result_label.config(text="Total Records: 0")
        
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
                    self.var_std_id.get()==id+1
                ))
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()
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
                cap = cv2.VideoCapture(0)
                img_id = 0 #image capture vayepaxi yesma save hunxa
                while True:
                    ret, my_frame = cap.read()
                    if face_cropped(my_frame) is not None:
                        img_id += 1
                        face = cv2.resize(face_cropped(my_frame), (450, 450))#image ligeko lai crop garya
                        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)#convert to gray scale
                        file_name_path = "data/user." + str(id) + "." + str(img_id) + ".jpg"#for eg user/.1.13.jpg
                        cv2.imwrite(file_name_path, face)
                        cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)#face mathi rectangle banauxa
                        cv2.imshow("Cropped Face", face)

                    if cv2.waitKey(1) == 13 or int(img_id) == 100: #13 is the enter key enter thichepaxi close hunxa
                        break
                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("Result", "Generating data set completed!!!")
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def update_courses(self, event):
        department = self.var_dep.get()

        if department in self.department_courses:
            courses = self.department_courses[department]
            self.course_combo["values"] = ("Select Course",) + courses
            self.course_combo.current(0)
        else:
            self.course_combo["values"] = ("Select Course",)
            self.course_combo.current(0)
            
    # ==================== ADVANCED SEARCH FUNCTIONS ====================
    
    def advanced_search(self):
        """Enhanced search function with multiple criteria support"""
        if self.var_search_by.get() == "Select Option" or self.var_search_txt.get() == "":
            messagebox.showerror("Error", "Please select search criteria and enter search value", parent=self.root)
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                username="root",
                password="",
                database="face_recognizer"
            )
            my_cursor = conn.cursor()

            # Map combobox selection to database column
            column_map = {
                "Student ID": "student_id",
                "Name": "name",
                "Roll No": "roll_no",
                "Phone No": "phone",
                "Email": "email",
                "Department": "department",
                "Course": "course"
            }

            column = column_map[self.var_search_by.get()]
            
            # Use LOWER() for case-insensitive search
            query = f"SELECT * FROM student WHERE LOWER({column}) LIKE LOWER(%s)"
            search_value = "%" + self.var_search_txt.get() + "%"

            my_cursor.execute(query, (search_value,))
            data = my_cursor.fetchall()

            # Clear existing table data
            self.student_table.delete(*self.student_table.get_children())

            if len(data) != 0:
                for row in data:
                    self.student_table.insert("", END, values=row)
                self.result_label.config(text=f"Found {len(data)} record(s)")
                messagebox.showinfo("Search Result", f"Found {len(data)} matching record(s)", parent=self.root)
            else:
                self.result_label.config(text="No records found")
                messagebox.showinfo("Search Result", "No matching records found", parent=self.root)

            conn.close()

        except Exception as es:
            messagebox.showerror("Error", f"Search failed: {str(es)}", parent=self.root)
    
    def toggle_realtime_search(self):
        """Toggle real-time search functionality"""
        if self.realtime_var.get() == 1:
            # Enable real-time search
            self.search_entry.bind('<KeyRelease>', self.realtime_search)
            messagebox.showinfo("Real-time Search", "Live search enabled! Results will update as you type.", parent=self.root)
        else:
            # Disable real-time search
            self.search_entry.unbind('<KeyRelease>')
            messagebox.showinfo("Real-time Search", "Live search disabled.", parent=self.root)
    
    def realtime_search(self, event=None):
        """Perform search as user types"""
        if self.var_search_by.get() == "Select Option":
            return
        
        if self.var_search_txt.get() == "":
            self.fetch_data()
            return
        
        try:
            conn = mysql.connector.connect(
                host="localhost",
                username="root",
                password="",
                database="face_recognizer"
            )
            my_cursor = conn.cursor()

            column_map = {
                "Student ID": "student_id",
                "Name": "name",
                "Roll No": "roll_no",
                "Phone No": "phone",
                "Email": "email",
                "Department": "department",
                "Course": "course"
            }

            column = column_map[self.var_search_by.get()]
            query = f"SELECT * FROM student WHERE LOWER({column}) LIKE LOWER(%s)"
            search_value = "%" + self.var_search_txt.get() + "%"

            my_cursor.execute(query, (search_value,))
            data = my_cursor.fetchall()

            self.student_table.delete(*self.student_table.get_children())

            if len(data) != 0:
                for row in data:
                    self.student_table.insert("", END, values=row)
                self.result_label.config(text=f"Found {len(data)} record(s)")
            else:
                self.result_label.config(text="No records found")

            conn.close()

        except Exception as es:
            pass  # Silent fail for real-time search to avoid popup spam
    
    def clear_search(self):
        """Clear search fields and show all records"""
        self.var_search_by.set("Select Option")
        self.var_search_txt.set("")
        self.search_combo.current(0)
        self.realtime_var.set(0)
        self.search_entry.unbind('<KeyRelease>')
        self.fetch_data()
        messagebox.showinfo("Search Cleared", "Search filters cleared. Showing all records.", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = Student1(root)
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
        self.CONFIDENCE_THRESHOLD = 50
        
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
        button_frame.place(x=450, y=580, width=650, height=50)
        
        # Start button
        self.btn_start = Button(
            button_frame,
            text="▶ Start Recognition",
            command=self.start_face_recognition,
            cursor="hand2",
            font=("Times New Roman", 15, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#1e8449",
            activeforeground="white"
        )
        self.btn_start.pack(side="left", padx=10, ipadx=20, ipady=5)
        
        # Stop button
        self.btn_stop = Button(
            button_frame,
            text="⬛ Stop Recognition",
            command=self.stop_face_recognition,
            cursor="hand2",
            font=("Times New Roman", 15, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            state="disabled"
        )
        self.btn_stop.pack(side="left", padx=10, ipadx=20, ipady=5)
        
        # Check Files button
        self.btn_check = Button(
            button_frame,
            text="🔍 Check Files",
            command=self.check_files,
            cursor="hand2",
            font=("Times New Roman", 15, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white"
        )
        self.btn_check.pack(side="left", padx=10, ipadx=20, ipady=5)
    
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
        # Create file if missing
        if not os.path.exists(self.ATTENDANCE_PATH):
            with open(self.ATTENDANCE_PATH, "w") as f:
                f.write("StudentID,Name,Roll,Department,Time,Date,Status")

        # Read existing attendance
        with open(self.ATTENDANCE_PATH, "r") as f:
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
        with open(self.ATTENDANCE_PATH, "a") as f:
            f.write(f"\n{student_id},{name},{roll},{department},{time_now},{date_today},Present")

        print(f"✓ Attendance marked: {student_id} - {name} at {time_now}")


def main():
    """Main entry point for the application"""
    root = Tk()
    app = FaceRecognitionSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()