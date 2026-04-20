import os
import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import csv
from time import strftime, localtime
from datetime import datetime
from collections import Counter

mydata = []

# ─────────────────────────────────────────────────────────────────────────────
#  DB HELPER  — returns (semester, year, course, department) for a student_id
#  Returns ("", "", "", "") silently if DB is unreachable or student not found.
# Takes student_id Fetches semester yearn course department If DB fails → returns empty values (no crash)
# ─────────────────────────────────────────────────────────────────────────────
def fetch_student_info_from_db(student_id):
    try:
        conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="face_recognizer"
        )
        cur = conn.cursor()
        cur.execute(
            "SELECT semester, year, course, department FROM student WHERE student_id = %s",
            (student_id,)
        )
        row = cur.fetchone()
        conn.close()
        if row:
            return (str(row[0]), str(row[1]), str(row[2]), str(row[3]))
    except Exception:
        pass
    return ("", "", "", "")


class AttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("1530x850+0+0")
        self.root.state('zoomed')

        # ── VARIABLES ────────────────────────────────────────────────
        self.var_std_id            = StringVar()
        self.var_std_name          = StringVar()
        self.var_roll              = StringVar()
        self.var_department        = StringVar()
        self.var_course            = StringVar()
        self.var_semester          = StringVar()
        self.var_year              = StringVar()
        self.var_date              = StringVar()
        self.var_time              = StringVar()
        self.var_status            = StringVar()
        self.var_search_department = StringVar()
        self.var_search_course     = StringVar()
        self.var_search_semester   = StringVar()
        self.var_search_year       = StringVar()
        self.var_search_date       = StringVar()
        self._filtered_data        = []

        # ── DEPARTMENT → COURSE MAPPING (mirrors student.py) ─────────
        self.department_courses = {
            "Arts":     ("BA", "BFA", "BHM"),
            "IT":       ("BCA", "BIM"),
            "Science":  ("BSC", "BSC-CSIT"),
            "Commerce": ("BBA", "BBS"),
        }

        # ── COLORS ───────────────────────────────────────────────────
        self.colors = {
            'bg_dark': '#0a0e27', 'bg_card': '#1a1f3a',
            'primary': '#4a90e2', 'secondary': '#50e3c2',
            'success': '#27ae60', 'danger':   '#e74c3c',
            'warning': '#f39c12', 'info':     '#3498db'
        }
        self.root.configure(bg=self.colors['bg_dark'])

        Label(self.root, text="STUDENT ATTENDANCE MANAGEMENT SYSTEM",
              font=("Helvetica", 28, "bold"),
              bg=self.colors['bg_dark'], fg="white").pack(pady=(8, 2))

        main_frame = Frame(self.root, bg=self.colors['bg_dark'])
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        # ── STATISTICS BAR ───────────────────────────────────────────
        #  Shows total records, present count, absent count, and attendance rate.
        stats_frame = LabelFrame(
            main_frame, bd=2, bg=self.colors['bg_card'], relief=RIDGE,
            text="Attendance Statistics ",
            font=("Helvetica", 12, "bold"), fg="white")
        stats_frame.pack(fill=X, pady=(0, 6))

        self.stats_container = Frame(stats_frame, bg=self.colors['bg_card'])
        self.stats_container.pack(fill=X, padx=10, pady=8)
        self._create_stat_card("Total Records",   "0",  self.colors['info'],    0)
        self._create_stat_card("Present",         "0",  self.colors['success'], 1)
        self._create_stat_card("Absent",          "0",  self.colors['danger'],  2)
        self._create_stat_card("Attendance Rate", "0%", self.colors['warning'], 3)

        # ── BODY ─────────────────────────────────────────────────────
        body = Frame(main_frame, bg=self.colors['bg_dark'])
        body.pack(fill=BOTH, expand=True)

        # ════ LEFT SIDE ══════════════════════════════════════════════
        # ════ LEFT SIDEBAR (FIXED VERSION) ═══════════════════════════════
        Left_frame = LabelFrame(
            body, bd=2, bg=self.colors['bg_card'], relief=RIDGE,
            text="Search & Filter Controls",
            font=("Helvetica", 12, "bold"), fg="white", width=390
        )
        Left_frame.pack(side=LEFT, fill=Y, padx=(0, 6), pady=2)

        # Use grid layout inside Left_frame
        Left_frame.grid_rowconfigure(0, weight=0)  # Filter
        Left_frame.grid_rowconfigure(1, weight=1)  # Details (expand)
        Left_frame.grid_rowconfigure(2, weight=0)  # Buttons
        Left_frame.grid_columnconfigure(0, weight=1)

        # ── FILTER SECTION ───────────────────────────────────────────────
        filter_lf = LabelFrame(
            Left_frame, bd=2, bg=self.colors['bg_card'], relief=RIDGE,
            text="Filter Options",
            font=("Helvetica", 11, "bold"), fg=self.colors['secondary']
        )
        filter_lf.grid(row=0, column=0, sticky="ew", padx=8, pady=8)

        # Department
        Label(filter_lf, text="Department:", bg=self.colors['bg_card'],
            fg="white", font=("Helvetica", 11, "bold")
            ).grid(row=0, column=0, padx=8, pady=6, sticky=W)

        self.dept_combo = ttk.Combobox(
            filter_lf, textvariable=self.var_search_department,
            font=("Helvetica", 11), state="readonly", width=20
        )
        self.dept_combo["values"] = ("All Departments", "Arts", "IT", "Science", "Commerce")
        self.dept_combo.current(0)
        self.dept_combo.grid(row=0, column=1, padx=8, pady=6)
        self.dept_combo.bind("<<ComboboxSelected>>", self._on_dept_change)

        # Course
        Label(filter_lf, text="Course:", bg=self.colors['bg_card'],
            fg="white", font=("Helvetica", 11, "bold")
            ).grid(row=1, column=0, padx=8, pady=6, sticky=W)

        self.course_combo = ttk.Combobox(
            filter_lf, textvariable=self.var_search_course,
            font=("Helvetica", 11), state="readonly", width=20
        )
        self.course_combo["values"] = ("All Courses",)
        self.course_combo.current(0)
        self.course_combo.grid(row=1, column=1, padx=8, pady=6)

        # Semester
        Label(filter_lf, text="Semester:", bg=self.colors['bg_card'],
            fg="white", font=("Helvetica", 11, "bold")
            ).grid(row=2, column=0, padx=8, pady=6, sticky=W)

        self.semester_combo = ttk.Combobox(
            filter_lf, textvariable=self.var_search_semester,
            font=("Helvetica", 11), state="readonly", width=20
        )
        self.semester_combo["values"] = (
            "All Semesters", "Semester 1", "Semester 2", "Semester 3",
            "Semester 4", "Semester 5", "Semester 6",
            "Semester 7", "Semester 8"
        )
        self.semester_combo.current(0)
        self.semester_combo.grid(row=2, column=1, padx=8, pady=6)

        # Year
        Label(filter_lf, text="Year:", bg=self.colors['bg_card'],
            fg="white", font=("Helvetica", 11, "bold")
            ).grid(row=3, column=0, padx=8, pady=6, sticky=W)

        self.year_combo = ttk.Combobox(
            filter_lf, textvariable=self.var_search_year,
            font=("Helvetica", 11), state="readonly", width=20
        )
        self.year_combo["values"] = (
            "All Years", "2020-21", "2021-22", "2022-23",
            "2023-24", "2024-25"
        )
        self.year_combo.current(0)
        self.year_combo.grid(row=3, column=1, padx=8, pady=6)

        # Date
        Label(filter_lf, text="Date:", bg=self.colors['bg_card'],
            fg="white", font=("Helvetica", 11, "bold")
            ).grid(row=4, column=0, padx=8, pady=6, sticky=W)

        date_frame = Frame(filter_lf, bg=self.colors['bg_card'])
        date_frame.grid(row=4, column=1, padx=8, pady=6, sticky=W)

        ttk.Entry(date_frame, width=12, textvariable=self.var_search_date,
                font=("Helvetica", 11)).pack(side=LEFT)

        Button(date_frame, text="Today", width=6,
            bg=self.colors['bg_dark'], fg="white",
            command=lambda: self.var_search_date.set(
                strftime("%d/%m/%Y", localtime()))
            ).pack(side=LEFT, padx=2)

        Button(date_frame, text="Clear", width=6,
            bg=self.colors['bg_dark'], fg="white",
            command=lambda: self.var_search_date.set("")
            ).pack(side=LEFT, padx=2)

        self.var_search_date.set(strftime("%d/%m/%Y", localtime()))

        # Buttons
        btn_row = Frame(filter_lf, bg=self.colors['bg_card'])
        btn_row.grid(row=5, column=0, columnspan=2, pady=10)

        Button(btn_row, text="Apply Filters", width=14,
            bg=self.colors['info'], fg="white",
            command=self.apply_filters).pack(side=LEFT, padx=4)

        Button(btn_row, text="Show All", width=10,
            bg=self.colors['bg_dark'], fg="white",
            command=self.show_all).pack(side=LEFT, padx=4)


        # ── SELECTED RECORD DETAILS (FIXED) ──────────────────────────────
        det_lf = LabelFrame(
            Left_frame, bd=2, bg=self.colors['bg_card'], relief=RIDGE,
            text="Selected Record Details",
            font=("Helvetica", 11, "bold"), fg=self.colors['secondary']
        )
        det_lf.grid(row=1, column=0, sticky="nsew", padx=8, pady=4)

        det_lf.grid_columnconfigure(1, weight=1)

        for r, (lbl, var) in enumerate([
            ("Student ID:", self.var_std_id),
            ("Name:", self.var_std_name),
            ("Roll No:", self.var_roll),
            ("Department:", self.var_department),
            ("Course:", self.var_course),
            ("Semester:", self.var_semester),
            ("Year:", self.var_year),
            ("Date:", self.var_date),
            ("Time:", self.var_time),
        ]):
            Label(det_lf, text=lbl, bg=self.colors['bg_card'],
                fg="white", font=("Helvetica", 10, "bold")
                ).grid(row=r, column=0, padx=8, pady=3, sticky=W)

            ttk.Entry(det_lf, textvariable=var).grid(
                row=r, column=1, padx=8, pady=3, sticky="ew"
            )

        Label(det_lf, text="Status:", bg=self.colors['bg_card'],
            fg="white", font=("Helvetica", 10, "bold")
            ).grid(row=9, column=0, padx=8, pady=3, sticky=W)

        ttk.Combobox(det_lf, textvariable=self.var_status,
                    values=("Select", "Present", "Absent"),
                    state="readonly"
                    ).grid(row=9, column=1, padx=8, pady=3, sticky="ew")


        # ── ACTION BUTTONS ───────────────────────────────────────────────
        act = Frame(Left_frame, bd=2, relief=RIDGE, bg=self.colors['bg_card'])
        act.grid(row=2, column=0, sticky="ew", padx=8, pady=6)

        act.grid_columnconfigure(0, weight=1)
        act.grid_columnconfigure(1, weight=1)

        Button(act, text="Import CSV", bg=self.colors['success'], fg="white",
            command=self.import_csv).grid(row=0, column=0, padx=4, pady=4, sticky="ew")

        Button(act, text="Export CSV", bg=self.colors['primary'], fg="white",
            command=self.export_csv).grid(row=0, column=1, padx=4, pady=4, sticky="ew")

        Button(act, text="Reset", bg=self.colors['warning'], fg="white",
            command=self.reset_data).grid(row=1, column=0, padx=4, pady=4, sticky="ew")

        Button(act, text="Refresh", bg=self.colors['info'], fg="white",
            command=self.refresh_all).grid(row=1, column=1, padx=4, pady=4, sticky="ew")
        # ════ RIGHT SIDE ═════════════════════════════════════════════
        right_side = Frame(body, bg=self.colors['bg_dark'])
        right_side.pack(side=LEFT, fill=BOTH, expand=True)

        # ── Table ────────────────────────────────────────────────────
        tbl_lf = LabelFrame(
            right_side, bd=2, bg=self.colors['bg_card'], relief=RIDGE,
            text="Attendance Records",
            font=("Helvetica", 12, "bold"), fg="white")
        tbl_lf.pack(fill=BOTH, expand=True, pady=(0, 4))

        qsf = Frame(tbl_lf, bg=self.colors['bg_card'])
        qsf.pack(fill=X, padx=8, pady=4)
        Label(qsf, text="Quick Search:", bg=self.colors['bg_card'],
              fg="white", font=("Helvetica", 11, "bold")).pack(side=LEFT, padx=4)
        #quick search filters within the currently filtered dataset (mydata or _filtered_data)
        self.search_var = StringVar()
        self.search_var.trace('w', lambda *a: self.quick_search())
        ttk.Entry(qsf, textvariable=self.search_var,
                  font=("Helvetica", 11), width=28).pack(side=LEFT, padx=4)
        Label(qsf, text="Searches within active filter",
              bg=self.colors['bg_card'], fg="#aaaaaa",
              font=("Helvetica", 9)).pack(side=LEFT, padx=4)

        tf = Frame(tbl_lf, bd=2, relief=RIDGE, bg=self.colors['bg_card'])
        tf.pack(fill=BOTH, expand=True, padx=8, pady=4)
        sx = ttk.Scrollbar(tf, orient=HORIZONTAL)
        sy = ttk.Scrollbar(tf, orient=VERTICAL)

        # Internal row layout (10 columns):
        # [0]id [1]name [2]roll [3]dept [4]course [5]sem [6]year [7]date [8]time [9]status
        self.attendance_table = ttk.Treeview(
            tf,
            columns=("id", "name", "roll", "dept", "course",
                     "sem", "year", "date", "time", "status"),
            xscrollcommand=sx.set, yscrollcommand=sy.set)
        sx.pack(side=BOTTOM, fill=X)
        sy.pack(side=RIGHT,  fill=Y)
        sx.config(command=self.attendance_table.xview)
        sy.config(command=self.attendance_table.yview)

        for col, heading, w, anc in [
            ("id",     "Student ID", 90,  CENTER),
            ("name",   "Name",       155, W),
            ("roll",   "Roll No",    70,  CENTER),
            ("dept",   "Department", 105, CENTER),
            ("course", "Course",     80,  CENTER),
            ("sem",    "Semester",   95,  CENTER),
            ("year",   "Year",       80,  CENTER),
            ("date",   "Date",       95,  CENTER),
            ("time",   "Time",       80,  CENTER),
            ("status", "Status",     80,  CENTER),
        ]:
            self.attendance_table.heading(
                col, text=heading,
                command=lambda c=col: self._sort_col(c))
            self.attendance_table.column(col, width=w, anchor=anc)

        self.attendance_table["show"] = "headings"
        self.attendance_table.pack(fill=BOTH, expand=True)
        self.attendance_table.bind("<ButtonRelease>", self.get_cursor)
        self.attendance_table.tag_configure('present', background='#d4edda')
        self.attendance_table.tag_configure('absent',  background='#f8d7da')

        # ── Analysis panel ───────────────────────────────────────────
        # Displays today's summary, per-semester present count, date range summary, and recent entries.
        ana_lf = LabelFrame(
            right_side, bd=2, bg=self.colors['bg_card'], relief=RIDGE,
            text="📊  Attendance Analysis",
            font=("Helvetica", 12, "bold"), fg=self.colors['secondary'])
        ana_lf.pack(fill=X, pady=(0, 2))

        ac = Frame(ana_lf, bg=self.colors['bg_card'])
        ac.pack(fill=X, padx=8, pady=6)
        for i in range(4):
            ac.grid_columnconfigure(i, weight=1)

        def _card(col, title):
            f = Frame(ac, bg=self.colors['bg_dark'], relief=RIDGE, bd=1)
            f.grid(row=0, column=col, padx=4, pady=2, sticky="nsew")
            Label(f, text=title, font=("Helvetica", 10, "bold"),
                  bg=self.colors['bg_dark'], fg=self.colors['secondary']
                  ).pack(pady=(6, 2))
            return f

        c0 = _card(0, "📆 Today's Summary")
        self.lbl_t_present = Label(c0, text="Present : 0",
            font=("Helvetica", 10, "bold"), bg=self.colors['bg_dark'], fg="#4ae24a")
        self.lbl_t_present.pack(anchor=W, padx=8)
        self.lbl_t_absent = Label(c0, text="Absent  : 0",
            font=("Helvetica", 10, "bold"), bg=self.colors['bg_dark'], fg="#e74c3c")
        self.lbl_t_absent.pack(anchor=W, padx=8)
        self.lbl_t_rate = Label(c0, text="Rate    : 0%",
            font=("Helvetica", 10, "bold"), bg=self.colors['bg_dark'], fg=self.colors['warning'])
        self.lbl_t_rate.pack(anchor=W, padx=8, pady=(0, 6))

        # ★ NEW: per-semester present count replaces old "By Department"
        c1 = _card(1, "📚 By Semester")
        self.lbl_sem = Label(c1, text="—",
            font=("Helvetica", 9), bg=self.colors['bg_dark'], fg="white", justify=LEFT)
        self.lbl_sem.pack(anchor=W, padx=8, pady=(0, 6))

        c2 = _card(2, "📅 Date Range")
        self.lbl_date_range = Label(c2, text="—",
            font=("Helvetica", 9), bg=self.colors['bg_dark'], fg="white")
        self.lbl_date_range.pack(anchor=W, padx=8)
        self.lbl_total_days = Label(c2, text="",
            font=("Helvetica", 9), bg=self.colors['bg_dark'], fg="#cccccc")
        self.lbl_total_days.pack(anchor=W, padx=8, pady=(0, 6))

        c3 = _card(3, "🕐 Last 3 Entries")
        self.lbl_recent = Label(c3, text="—",
            font=("Helvetica", 9), bg=self.colors['bg_dark'], fg="white", justify=LEFT)
        self.lbl_recent.pack(anchor=W, padx=8, pady=(0, 6))

        # ── Load on startup ───────────────────────────────────────────
        self.load_from_csv()
        self.update_statistics()
        self.update_analysis(mydata)

    # ═════════════════════════════════════════════════════════════════
    def _create_stat_card(self, title, value, color, col):
        card = Frame(self.stats_container, bg=color, relief=RIDGE, bd=2)
        card.grid(row=0, column=col, padx=8, pady=4, sticky="ew")
        self.stats_container.grid_columnconfigure(col, weight=1)
        Label(card, text=title, font=("Helvetica", 12, "bold"),
              bg=color, fg="white").pack(pady=(8, 4))
        lbl = Label(card, text=value, font=("Helvetica", 22, "bold"),
                    bg=color, fg="white")
        lbl.pack(pady=(4, 8))
        if   col == 0: self.total_label   = lbl
        elif col == 1: self.present_label = lbl
        elif col == 2: self.absent_label  = lbl
        elif col == 3: self.rate_label    = lbl

    def _sort_col(self, col):
        data = [(self.attendance_table.set(k, col), k)
                for k in self.attendance_table.get_children("")]
        data.sort()
        for i, (_, k) in enumerate(data):
            self.attendance_table.move(k, "", i)

    def _on_dept_change(self, event=None):
        dept = self.var_search_department.get().strip()
        if dept in self.department_courses:
            courses = list(self.department_courses[dept])
        else:
            courses = []
            for c in self.department_courses.values():
                courses.extend(c)
        self.course_combo["values"] = ["All Courses"] + courses
        self.course_combo.current(0)

    # ═════════════════════════════════════════════════════════════════
    #  DB ENRICHMENT
    #  Builds a 10-element internal row:
    #  [0]id [1]name [2]roll [3]dept [4]course [5]sem [6]year [7]date [8]time [9]status
    #  DB values (semester, year, course, dept) take priority over CSV values.
    # ═════════════════════════════════════════════════════════════════
    def _enrich(self, student_id, name, roll, dept_csv, course_csv,
                date, time_, status):
        sem, year, course_db, dept_db = fetch_student_info_from_db(student_id)
        dept   = dept_db   if dept_db   else dept_csv
        course = course_db if course_db else course_csv
        return [student_id, name, roll, dept, course, sem, year, date, time_, status]

    # ═════════════════════════════════════════════════════════════════
    def get_cursor(self, event=""):
        d = self.attendance_table.item(self.attendance_table.focus())["values"]
        if len(d) < 10:
            return
        self.var_std_id.set(d[0]);    self.var_std_name.set(d[1])
        self.var_roll.set(d[2]);      self.var_department.set(d[3])
        self.var_course.set(d[4]);    self.var_semester.set(d[5])
        self.var_year.set(d[6]);      self.var_date.set(d[7])
        self.var_time.set(d[8]);      self.var_status.set(d[9])

    def fetch_data(self, rows):
        self.attendance_table.delete(*self.attendance_table.get_children())
        for row in rows:
            if len(row) >= 10:
                tag = 'present' if str(row[9]).strip().lower() == 'present' else 'absent'
                self.attendance_table.insert("", END, values=row, tags=(tag,))

    # ═════════════════════════════════════════════════════════════════
    #  CSV LOAD
    #  Handles both old 8-col and newer 9-col CSV formats.
    #  After reading, every row is enriched with DB semester + year.
    # ═════════════════════════════════════════════════════════════════
    def load_from_csv(self):
        global mydata
        mydata.clear()
        csv_paths = [
            "attendance.csv",
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "attendance.csv"),
        ]
        csv_file = next((p for p in csv_paths if os.path.exists(p)), None)
        if not csv_file:
            print("attendance.csv not found")
            return
        try:
            with open(csv_file, "r") as f:
                reader = csv.reader(f)
                next(reader, None)              # skip header
                for row in reader:
                    if not row or len(row) < 8:
                        continue
                    sid        = row[0].strip()
                    name       = row[1]
                    roll       = row[2]
                    dept_csv   = row[3]
                    course_csv = row[4]
                    # 8-col: date=row[5], time=row[6], status=row[7]
                    # 9-col: (old sem)=row[5], date=row[6], time=row[7], status=row[8]
                    if len(row) >= 9:
                        date, time_, status = row[6], row[7], row[8]
                    else:
                        date, time_, status = row[5], row[6], row[7]
                    mydata.append(
                        self._enrich(sid, name, roll, dept_csv, course_csv,
                                     date, time_, status)
                    )
            self._filtered_data = mydata.copy()
            self.fetch_data(mydata)
            self._on_dept_change()
            print(f"Loaded {len(mydata)} records from {csv_file}")
        except Exception as e:
            print(f"CSV error: {e}")

    def import_csv(self):
        global mydata
        mydata.clear()
        fln = filedialog.askopenfilename(
            initialdir=os.getcwd(), title="Open CSV",
            filetypes=(("CSV", "*.csv"), ("All", "*.*")), parent=self.root)
        if not fln:
            return
        try:
            with open(fln) as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if not row or len(row) < 8:
                        continue
                    sid        = row[0].strip()
                    name       = row[1]
                    roll       = row[2]
                    dept_csv   = row[3]
                    course_csv = row[4]
                    if len(row) >= 9:
                        date, time_, status = row[6], row[7], row[8]
                    else:
                        date, time_, status = row[5], row[6], row[7]
                    mydata.append(
                        self._enrich(sid, name, roll, dept_csv, course_csv,
                                     date, time_, status)
                    )
            self._filtered_data = mydata.copy()
            self.fetch_data(mydata)
            self._on_dept_change()
            self.update_statistics()
            self.update_analysis(mydata)
            messagebox.showinfo("Success", f"Imported {len(mydata)} records.")
        except Exception as e:
            messagebox.showerror("Error", f"Import failed: {e}")

    def export_csv(self):
        if not mydata:
            messagebox.showerror("Error", "No data to export!", parent=self.root)
            return
        fln = filedialog.asksaveasfilename(
            initialdir=os.getcwd(), title="Save CSV",
            defaultextension=".csv",
            filetypes=(("CSV", "*.csv"), ("All", "*.*")), parent=self.root)
        if fln:
            try:
                with open(fln, "w", newline="") as f:
                    w = csv.writer(f)
                    w.writerow([
                        "StudentID", "Name", "Roll", "Department", "Course",
                        "Semester", "Year", "Date", "Time", "Status"
                    ])
                    for row in mydata:
                        w.writerow(row)
                messagebox.showinfo("Success", f"Exported to {fln}")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {e}")

    # ═════════════════════════════════════════════════════════════════
    #  FILTERS
    #  [3]dept  [4]course  [5]sem  [6]year  [7]date  [9]status
    # ═════════════════════════════════════════════════════════════════
    def apply_filters(self):
        dept     = self.var_search_department.get().strip()
        course   = self.var_search_course.get().strip()
        sem      = self.var_search_semester.get().strip()
        year     = self.var_search_year.get().strip()
        date_str = self.var_search_date.get().strip()

        filtered = mydata.copy()

        if dept and dept != "All Departments":
            filtered = [r for r in filtered
                        if len(r) > 3 and r[3].strip().lower() == dept.lower()]

        if course and course != "All Courses":
            filtered = [r for r in filtered
                        if len(r) > 4 and r[4].strip().lower() == course.lower()]

        if sem and sem != "All Semesters":
            filtered = [r for r in filtered
                        if len(r) > 5 and r[5].strip().lower() == sem.lower()]

        if year and year != "All Years":
            filtered = [r for r in filtered
                        if len(r) > 6 and r[6].strip() == year]

        if date_str:
            filtered = [r for r in filtered
                        if len(r) > 7 and r[7].strip() == date_str]

        self._filtered_data = filtered
        self.search_var.set("")
        self.fetch_data(filtered)
        self.update_statistics(filtered)
        self.update_analysis(filtered)

        if not filtered:
            parts = []
            if dept   and dept   != "All Departments": parts.append(f"Department = '{dept}'")
            if course and course != "All Courses":      parts.append(f"Course = '{course}'")
            if sem    and sem    != "All Semesters":    parts.append(f"Semester = '{sem}'")
            if year   and year   != "All Years":        parts.append(f"Year = '{year}'")
            if date_str:                                parts.append(f"Date = '{date_str}'")
            messagebox.showinfo(
                "No Results",
                "No records found for:\n" + "\n".join(parts) +
                "\n\nTip: Use 'Clear Date' if you want all dates, "
                "or 'Show All' to remove all filters.",
                parent=self.root)

    def show_all(self):
        self._filtered_data = mydata.copy()
        self.search_var.set("")
        self.var_search_department.set("All Departments")
        self.var_search_course.set("All Courses")
        self.var_search_semester.set("All Semesters")
        self.var_search_year.set("All Years")
        self.fetch_data(mydata)
        self.update_statistics()
        self.update_analysis(mydata)

    def quick_search(self):
        term   = self.search_var.get().strip().lower()
        source = self._filtered_data if self._filtered_data is not None else mydata
        if not term:
            self.fetch_data(source)
            self.update_statistics(source)
            return
        result = [r for r in source if any(term in str(c).lower() for c in r)]
        self.fetch_data(result)
        self.update_statistics(result)

    # ═════════════════════════════════════════════════════════════════
    #  STATISTICS    status at index [9]
    # ═════════════════════════════════════════════════════════════════
    def update_statistics(self, data=None):
        if data is None:
            data = mydata
        total   = len(data)
        present = sum(1 for r in data
                      if len(r) > 9 and str(r[9]).strip().lower() == 'present')
        absent  = total - present
        rate    = (present / total * 100) if total else 0
        self.total_label.config(text=str(total))
        self.present_label.config(text=str(present))
        self.absent_label.config(text=str(absent))
        self.rate_label.config(text=f"{rate:.1f}%")

    # ═════════════════════════════════════════════════════════════════
    #  ANALYSIS
    #  date=[7]  time=[8]  status=[9]  sem=[5]
    # ═════════════════════════════════════════════════════════════════
    def update_analysis(self, data=None):
        if data is None:
            data = mydata
        today_str = strftime("%d/%m/%Y", localtime())

        # Today's summary (always from full mydata)
        today_rows = [r for r in mydata if len(r) > 7 and r[7].strip() == today_str]
        tp = sum(1 for r in today_rows if len(r) > 9 and str(r[9]).strip().lower() == 'present')
        ta = len(today_rows) - tp
        tr = (tp / len(today_rows) * 100) if today_rows else 0
        self.lbl_t_present.config(text=f"Present : {tp}")
        self.lbl_t_absent.config( text=f"Absent  : {ta}")
        self.lbl_t_rate.config(   text=f"Rate    : {tr:.1f}%")

        # Per-semester breakdown
        sem_ctr = Counter(r[5].strip() for r in data if len(r) > 5 and r[5].strip())
        if sem_ctr:
            lines = []
            for sem, cnt in sorted(sem_ctr.items()):
                p = sum(1 for r in data
                        if len(r) > 9 and r[5].strip() == sem
                        and str(r[9]).strip().lower() == 'present')
                lines.append(f"{sem:<12} {p}/{cnt} present")
            self.lbl_sem.config(text="\n".join(lines))
        else:
            self.lbl_sem.config(text="No semester data\n(DB not connected?)")

        # Date range
        dates = [r[7].strip() for r in data if len(r) > 7 and r[7].strip()]
        if dates:
            def _p(d):
                try:    return datetime.strptime(d, "%d/%m/%Y")
                except: return None
            parsed = [x for x in (_p(d) for d in dates) if x]
            if parsed:
                mn = min(parsed).strftime("%d/%m/%Y")
                mx = max(parsed).strftime("%d/%m/%Y")
                self.lbl_date_range.config(text=f"{mn}  →  {mx}")
                self.lbl_total_days.config(text=f"{len(set(dates))} unique date(s)")
            else:
                self.lbl_date_range.config(text="—")
                self.lbl_total_days.config(text="")
        else:
            self.lbl_date_range.config(text="No data")
            self.lbl_total_days.config(text="")

        # Last 3 entries
        if data:
            lines = []
            for r in data[-3:][::-1]:
                name = str(r[1])[:14] if len(r) > 1 else "?"
                tm   = r[8] if len(r) > 8 else ""
                st   = r[9] if len(r) > 9 else ""
                lines.append(f"{name} | {tm} | {st}")
            self.lbl_recent.config(text="\n".join(lines))
        else:
            self.lbl_recent.config(text="No data")

    # ═════════════════════════════════════════════════════════════════
    def refresh_all(self):
        self.load_from_csv()
        self.update_statistics()
        self.update_analysis(mydata)

    def reset_data(self):
        self.var_std_id.set("");    self.var_std_name.set("")
        self.var_roll.set("");      self.var_department.set("")
        self.var_course.set("");    self.var_semester.set("")
        self.var_year.set("")
        self.var_date.set(strftime("%d/%m/%Y", localtime()))
        self.var_time.set(strftime("%H:%M:%S", localtime()))
        self.var_status.set("Select")
        self.var_search_department.set("All Departments")
        self.var_search_course.set("All Courses")
        self.var_search_semester.set("All Semesters")
        self.var_search_year.set("All Years")
        self.var_search_date.set(strftime("%d/%m/%Y", localtime()))
        self.search_var.set("")
        self._filtered_data = mydata.copy()
        self.fetch_data(mydata)
        self.update_statistics()
        self.update_analysis(mydata)


if __name__ == "__main__":
    root = Tk()
    app = AttendanceSystem(root)
    root.mainloop()