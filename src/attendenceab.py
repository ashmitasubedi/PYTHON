import os
import csv
import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from time import strftime, localtime
from collections import Counter

# ─────────────────────────────────────────────────────────────────────────────
#  AbsentStudentSystem
#
#  Data sources:
#   1. MySQL (face_recognizer DB) — student master list
#      Table: students(student_id, name, roll, department, course, semester, year)
#
#   2. attendance.csv — every row = one PRESENT record
#      Columns: student_id, name, roll, department, course, semester, year, date, time
#
#  Absent logic:
#   • For a chosen date → anyone in MySQL students table who has NO row
#     in attendance.csv for that date = ABSENT.
#   • Time is NOT shown (not relevant for absent students).
# ─────────────────────────────────────────────────────────────────────────────

CSV_PATH = "attendance.csv"

# ── MySQL connection config — edit to match your setup ───────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "",          # your MySQL root password
    "database": "face_recognizer",
}


# ══════════════════════════════════════════════════════════════════════════════
#  Helper: fetch all students from MySQL
# ══════════════════════════════════════════════════════════════════════════════
def fetch_students_from_mysql():
    """
    Returns dict {student_id: {name, roll, dept, course, sem, year}}
    Auto-discovers table and column names so it works with any
    face_recognizer project variant.
    """
    students = {}
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cur  = conn.cursor(dictionary=True)

        # ── discover table ───────────────────────────────────────────
        cur.execute("SHOW TABLES")
        tables = [list(r.values())[0].lower() for r in cur.fetchall()]
        print(f"[MySQL] Tables: {tables}")

        tbl = None
        for candidate in ("students", "student", "users", "student_details", "studentdetails"):
            if candidate in tables:
                tbl = candidate
                break
        if not tbl and tables:
            tbl = tables[0]
        if not tbl:
            print("[MySQL] No tables found in face_recognizer database.")
            conn.close()
            return students

        # ── discover columns ─────────────────────────────────────────
        cur.execute(f"DESCRIBE `{tbl}`")
        cols = [r["Field"].lower() for r in cur.fetchall()]
        print(f"[MySQL] Columns in '{tbl}': {cols}")

        def pick(*candidates):
            for c in candidates:
                if c in cols:
                    return c
            return None

        c_id   = pick("student_id", "studentid", "id", "sid", "std_id")
        c_name = pick("name", "student_name", "fullname", "full_name", "std_name")
        c_roll = pick("roll", "roll_no", "rollno", "roll_number", "std_roll")
        c_dept = pick("department", "dept", "dep", "std_dept")
        c_crs  = pick("course", "program", "branch", "std_course")
        c_sem  = pick("semester", "sem", "std_sem")
        c_yr   = pick("year", "yr", "batch", "std_year")

        if not c_id:
            print("[MySQL] Could not find a student_id column.")
            conn.close()
            return students

        cur.execute(f"SELECT * FROM `{tbl}`")
        for row in cur.fetchall():
            sid = str(row.get(c_id, "") or "").strip()
            if not sid:
                continue
            students[sid] = {
                "name":   str(row.get(c_name, "") or "").strip(),
                "roll":   str(row.get(c_roll, "") or "").strip(),
                "dept":   str(row.get(c_dept, "") or "").strip(),
                "course": str(row.get(c_crs,  "") or "").strip(),
                "sem":    str(row.get(c_sem,  "") or "").strip(),
                "year":   str(row.get(c_yr,   "") or "").strip(),
            }

        conn.close()
        print(f"[MySQL] Loaded {len(students)} students from '{tbl}'.")

    except mysql.connector.Error as e:
        print(f"[MySQL] Connection error: {e}")
        messagebox.showerror(
            "MySQL Error",
            f"Could not connect to MySQL:\n{e}\n\n"
            "Please update DB_CONFIG at the top of absent_student_system.py.",
        )
    return students


# ══════════════════════════════════════════════════════════════════════════════
#  Main Application
# ══════════════════════════════════════════════════════════════════════════════
class AbsentStudentSystem:

    def __init__(self, root):
        self.root = root
        self.root.title("Absent Student Management System")
        self.root.geometry("1530x850+0+0")
        self.root.state("zoomed")

        # ── internal data ────────────────────────────────────────────
        self._all_students  = {}   # sid -> {name, roll, dept, course, sem, year}
        self._csv_records   = []   # list of dicts — every Present row in CSV
        self._absent_data   = []   # current absent rows (list of lists)
        self._filtered_data = []   # after filter/search

        # ── StringVars ───────────────────────────────────────────────
        self.var_std_id     = StringVar()
        self.var_std_name   = StringVar()
        self.var_roll       = StringVar()
        self.var_department = StringVar()
        self.var_course     = StringVar()
        self.var_semester   = StringVar()
        self.var_year       = StringVar()
        self.var_date       = StringVar()
        self.var_status     = StringVar()

        self.var_search_department = StringVar()
        self.var_search_course     = StringVar()
        self.var_search_semester   = StringVar()
        self.var_search_year       = StringVar()
        self.var_search_date       = StringVar()

        self.department_courses = {
            "Arts":     ("BA", "BFA", "BHM"),
            "IT":       ("BCA", "BIM"),
            "Science":  ("BSC", "BSC-CSIT"),
            "Commerce": ("BBA", "BBS"),
        }

        self.colors = {
            "bg_dark":  "#0a0e27",
            "bg_card":  "#1a1f3a",
            "primary":  "#4a90e2",
            "secondary":"#50e3c2",
            "success":  "#27ae60",
            "danger":   "#e74c3c",
            "warning":  "#f39c12",
            "info":     "#3498db",
        }
        self.root.configure(bg=self.colors["bg_dark"])

        # ── Title ────────────────────────────────────────────────────
        Label(
            self.root,
            text="ABSENT STUDENT MANAGEMENT SYSTEM",
            font=("Helvetica", 28, "bold"),
            bg=self.colors["bg_dark"],
            fg=self.colors["danger"],
        ).pack(pady=(8, 2))

        main_frame = Frame(self.root, bg=self.colors["bg_dark"])
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        # ════════════════════════════════════════════════════════════
        #  LEFT SIDEBAR
        # ════════════════════════════════════════════════════════════
        Left_frame = LabelFrame(
            main_frame, bd=2, bg=self.colors["bg_card"], relief=RIDGE,
            text="Search & Filter Controls",
            font=("Helvetica", 12, "bold"), fg="white", width=390,
        )
        Left_frame.pack(side=LEFT, fill=Y, padx=(0, 6), pady=2)
        Left_frame.grid_rowconfigure(1, weight=1)
        Left_frame.grid_columnconfigure(0, weight=1)

        # ── Filter Options ────────────────────────────────────────────
        filter_lf = LabelFrame(
            Left_frame, bd=2, bg=self.colors["bg_card"], relief=RIDGE,
            text="Filter Options",
            font=("Helvetica", 11, "bold"), fg=self.colors["secondary"],
        )
        filter_lf.grid(row=0, column=0, sticky="ew", padx=8, pady=8)

        # Date row
        Label(filter_lf, text="Date:", bg=self.colors["bg_card"],
              fg="white", font=("Helvetica", 11, "bold")
              ).grid(row=0, column=0, padx=8, pady=6, sticky=W)
        date_frame = Frame(filter_lf, bg=self.colors["bg_card"])
        date_frame.grid(row=0, column=1, padx=8, pady=6, sticky=W)
        ttk.Entry(date_frame, width=12, textvariable=self.var_search_date,
                  font=("Helvetica", 11)).pack(side=LEFT)
        Button(date_frame, text="Today", width=6,
               bg=self.colors["bg_dark"], fg="white",
               command=lambda: self.var_search_date.set(
                   strftime("%d/%m/%Y", localtime()))
               ).pack(side=LEFT, padx=2)
        Button(date_frame, text="Clear", width=6,
               bg=self.colors["bg_dark"], fg="white",
               command=lambda: self.var_search_date.set("")
               ).pack(side=LEFT, padx=2)
        self.var_search_date.set(strftime("%d/%m/%Y", localtime()))

        # Department
        Label(filter_lf, text="Department:", bg=self.colors["bg_card"],
              fg="white", font=("Helvetica", 11, "bold")
              ).grid(row=1, column=0, padx=8, pady=6, sticky=W)
        self.dept_combo = ttk.Combobox(
            filter_lf, textvariable=self.var_search_department,
            font=("Helvetica", 11), state="readonly", width=20)
        self.dept_combo["values"] = ("All Departments","Arts","IT","Science","Commerce")
        self.dept_combo.current(0)
        self.dept_combo.grid(row=1, column=1, padx=8, pady=6)
        self.dept_combo.bind("<<ComboboxSelected>>", self._on_dept_change)

        # Course
        Label(filter_lf, text="Course:", bg=self.colors["bg_card"],
              fg="white", font=("Helvetica", 11, "bold")
              ).grid(row=2, column=0, padx=8, pady=6, sticky=W)
        self.course_combo = ttk.Combobox(
            filter_lf, textvariable=self.var_search_course,
            font=("Helvetica", 11), state="readonly", width=20)
        self.course_combo["values"] = ("All Courses",)
        self.course_combo.current(0)
        self.course_combo.grid(row=2, column=1, padx=8, pady=6)

        # Semester
        Label(filter_lf, text="Semester:", bg=self.colors["bg_card"],
              fg="white", font=("Helvetica", 11, "bold")
              ).grid(row=3, column=0, padx=8, pady=6, sticky=W)
        self.semester_combo = ttk.Combobox(
            filter_lf, textvariable=self.var_search_semester,
            font=("Helvetica", 11), state="readonly", width=20)
        self.semester_combo["values"] = (
            "All Semesters","Semester 1","Semester 2","Semester 3",
            "Semester 4","Semester 5","Semester 6","Semester 7","Semester 8")
        self.semester_combo.current(0)
        self.semester_combo.grid(row=3, column=1, padx=8, pady=6)

        # Year
        Label(filter_lf, text="Year:", bg=self.colors["bg_card"],
              fg="white", font=("Helvetica", 11, "bold")
              ).grid(row=4, column=0, padx=8, pady=6, sticky=W)
        self.year_combo = ttk.Combobox(
            filter_lf, textvariable=self.var_search_year,
            font=("Helvetica", 11), state="readonly", width=20)
        self.year_combo["values"] = (
            "All Years","2020-21","2021-22","2022-23","2023-24","2024-25")
        self.year_combo.current(0)
        self.year_combo.grid(row=4, column=1, padx=8, pady=6)

        btn_row = Frame(filter_lf, bg=self.colors["bg_card"])
        btn_row.grid(row=5, column=0, columnspan=2, pady=10)
        Button(btn_row, text="Apply Filters", width=14,
               bg=self.colors["info"], fg="white",
               command=self.apply_filters).pack(side=LEFT, padx=4)
        Button(btn_row, text="Show All", width=10,
               bg=self.colors["bg_dark"], fg="white",
               command=self.show_all).pack(side=LEFT, padx=4)

        # ── Selected Record Details (no Time) ────────────────────────
        det_lf = LabelFrame(
            Left_frame, bd=2, bg=self.colors["bg_card"], relief=RIDGE,
            text="Selected Record Details",
            font=("Helvetica", 11, "bold"), fg=self.colors["secondary"],
        )
        det_lf.grid(row=1, column=0, sticky="nsew", padx=8, pady=4)
        det_lf.grid_columnconfigure(1, weight=1)

        for r, (lbl, var, readonly) in enumerate([
            ("Student ID:", self.var_std_id,     False),
            ("Name:",       self.var_std_name,   False),
            ("Roll No:",    self.var_roll,        False),
            ("Department:", self.var_department,  False),
            ("Course:",     self.var_course,      False),
            ("Semester:",   self.var_semester,    False),
            ("Year:",       self.var_year,        False),
            ("Date:",       self.var_date,        False),
            ("Status:",     self.var_status,      True),
        ]):
            Label(det_lf, text=lbl, bg=self.colors["bg_card"],
                  fg="white", font=("Helvetica", 10, "bold")
                  ).grid(row=r, column=0, padx=8, pady=3, sticky=W)
            e = ttk.Entry(det_lf, textvariable=var,
                          state="readonly" if readonly else "normal")
            e.grid(row=r, column=1, padx=8, pady=3, sticky="ew")

        # ── Action Buttons ────────────────────────────────────────────
        act = Frame(Left_frame, bd=2, relief=RIDGE, bg=self.colors["bg_card"])
        act.grid(row=2, column=0, sticky="ew", padx=8, pady=6)
        act.grid_columnconfigure(0, weight=1)
        act.grid_columnconfigure(1, weight=1)

        Button(act, text="Reload DB", bg=self.colors["success"], fg="white",
               command=self.reload_db
               ).grid(row=0, column=0, padx=4, pady=4, sticky="ew")
        Button(act, text="Export CSV", bg=self.colors["primary"], fg="white",
               command=self.export_csv
               ).grid(row=0, column=1, padx=4, pady=4, sticky="ew")
        Button(act, text="Reset", bg=self.colors["warning"], fg="white",
               command=self.reset_fields
               ).grid(row=1, column=0, padx=4, pady=4, sticky="ew")
        Button(act, text="Refresh", bg=self.colors["info"], fg="white",
               command=self.refresh_all
               ).grid(row=1, column=1, padx=4, pady=4, sticky="ew")

        # ════════════════════════════════════════════════════════════
        #  RIGHT SIDE
        # ════════════════════════════════════════════════════════════
        right_side = Frame(main_frame, bg=self.colors["bg_dark"])
        right_side.pack(side=LEFT, fill=BOTH, expand=True)

        # ── Stats bar (4 cards) ──────────────────────────────────────
        stats_frame = Frame(right_side, bg=self.colors["bg_dark"])
        stats_frame.pack(fill=X, pady=(0, 4))
        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)

        def stat_card(col, title, color):
            f = Frame(stats_frame, bg=color, relief=RIDGE, bd=2)
            f.grid(row=0, column=col, padx=6, pady=2, sticky="ew")
            Label(f, text=title, font=("Helvetica", 11, "bold"),
                  bg=color, fg="white").pack(pady=(6, 2))
            lbl = Label(f, text="0", font=("Helvetica", 22, "bold"),
                        bg=color, fg="white")
            lbl.pack(pady=(2, 6))
            return lbl

        self.total_label   = stat_card(0, "Total Students",  "#2c3e50")
        self.absent_label  = stat_card(1, "Absent",          self.colors["danger"])
        self.present_label = stat_card(2, "Present",         self.colors["success"])
        self.rate_label    = stat_card(3, "Absence Rate",    self.colors["warning"])

        # ── Table ────────────────────────────────────────────────────
        tbl_lf = LabelFrame(
            right_side, bd=2, bg=self.colors["bg_card"], relief=RIDGE,
            text="Absent Student Records",
            font=("Helvetica", 12, "bold"), fg="white",
        )
        tbl_lf.pack(fill=BOTH, expand=True, pady=(0, 4))

        # Quick search bar
        qsf = Frame(tbl_lf, bg=self.colors["bg_card"])
        qsf.pack(fill=X, padx=8, pady=4)
        Label(qsf, text="Quick Search:", bg=self.colors["bg_card"],
              fg="white", font=("Helvetica", 11, "bold")).pack(side=LEFT, padx=4)
        self.search_var = StringVar()
        self.search_var.trace("w", lambda *a: self.quick_search())
        ttk.Entry(qsf, textvariable=self.search_var,
                  font=("Helvetica", 11), width=28).pack(side=LEFT, padx=4)
        Label(qsf, text="Searches within active filter",
              bg=self.colors["bg_card"], fg="#aaaaaa",
              font=("Helvetica", 9)).pack(side=LEFT, padx=4)

        # Treeview — no Time column
        tf = Frame(tbl_lf, bd=2, relief=RIDGE, bg=self.colors["bg_card"])
        tf.pack(fill=BOTH, expand=True, padx=8, pady=4)
        sx = ttk.Scrollbar(tf, orient=HORIZONTAL)
        sy = ttk.Scrollbar(tf, orient=VERTICAL)

        self.attendance_table = ttk.Treeview(
            tf,
            columns=("id","name","roll","dept","course","sem","year","date","status"),
            xscrollcommand=sx.set,
            yscrollcommand=sy.set,
        )
        sx.pack(side=BOTTOM, fill=X)
        sy.pack(side=RIGHT,  fill=Y)
        sx.config(command=self.attendance_table.xview)
        sy.config(command=self.attendance_table.yview)

        for col, heading, w, anc in [
            ("id",     "Student ID", 90,  CENTER),
            ("name",   "Name",       170, W),
            ("roll",   "Roll No",    75,  CENTER),
            ("dept",   "Department", 110, CENTER),
            ("course", "Course",     90,  CENTER),
            ("sem",    "Semester",   95,  CENTER),
            ("year",   "Year",       80,  CENTER),
            ("date",   "Date",       100, CENTER),
            ("status", "Status",     80,  CENTER),
        ]:
            self.attendance_table.heading(
                col, text=heading, command=lambda c=col: self._sort_col(c))
            self.attendance_table.column(col, width=w, anchor=anc)

        self.attendance_table["show"] = "headings"
        self.attendance_table.pack(fill=BOTH, expand=True)
        self.attendance_table.bind("<ButtonRelease>", self.get_cursor)
        self.attendance_table.tag_configure(
            "absent", background="#f8d7da", foreground="#333333")

        # ── Analysis panel ────────────────────────────────────────────
        ana_lf = LabelFrame(
            right_side, bd=2, bg=self.colors["bg_card"], relief=RIDGE,
            text="📊  Absence Analysis",
            font=("Helvetica", 12, "bold"), fg=self.colors["secondary"],
        )
        ana_lf.pack(fill=X, pady=(0, 2))

        ac = Frame(ana_lf, bg=self.colors["bg_card"])
        ac.pack(fill=X, padx=8, pady=6)
        for i in range(3):
            ac.grid_columnconfigure(i, weight=1)

        def _card(col, title):
            f = Frame(ac, bg=self.colors["bg_dark"], relief=RIDGE, bd=1)
            f.grid(row=0, column=col, padx=4, pady=2, sticky="nsew")
            Label(f, text=title, font=("Helvetica", 10, "bold"),
                  bg=self.colors["bg_dark"], fg=self.colors["secondary"]
                  ).pack(pady=(6, 2))
            lbl = Label(f, text="—", font=("Helvetica", 9),
                        bg=self.colors["bg_dark"], fg="white", justify=LEFT)
            lbl.pack(anchor=W, padx=8, pady=(0, 6))
            return lbl

        self.lbl_sem      = _card(0, "📚 Absent by Semester")
        self.lbl_dept_ana = _card(1, "🏫 Absent by Department")
        self.lbl_recent   = _card(2, "📋 First 5 Absent Students")

        # ── Boot ─────────────────────────────────────────────────────
        self.load_data()

    # ═════════════════════════════════════════════════════════════════
    #  DATA LOADING
    # ═════════════════════════════════════════════════════════════════
    def load_data(self):
        """Pull students from MySQL and present records from CSV, then refresh."""
        self._all_students = fetch_students_from_mysql()
        self._csv_records  = self._load_csv_records()

        if not self._all_students:
            messagebox.showwarning(
                "No Students",
                "No student records found in MySQL.\n"
                "Check DB_CONFIG at the top of the file.",
                parent=self.root,
            )

        self._absent_data   = self._build_absent_rows()
        self._filtered_data = self._absent_data.copy()
        self.fetch_data(self._absent_data)
        self._on_dept_change()
        self.update_statistics(self._absent_data)
        self.update_analysis(self._absent_data)
        print(f"[App] Students: {len(self._all_students)} | "
              f"CSV rows: {len(self._csv_records)} | "
              f"Absent today: {len(self._absent_data)}")

    def _load_csv_records(self, csv_file=None):
        """
        Read attendance.csv → list of {student_id, date}.
        Every row in this file represents a PRESENT record.
        Only student_id and date are needed for absent logic.
        """
        if csv_file is None:
            candidates = [
                CSV_PATH,
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "attendance.csv"),
            ]
            csv_file = next((p for p in candidates if os.path.exists(p)), None)

        if not csv_file or not os.path.exists(csv_file):
            print("[CSV] attendance.csv not found — all students will show as absent.")
            return []

        records = []
        try:
            with open(csv_file, newline="") as f:
                reader = csv.reader(f)
                header = next(reader, [])
                print(f"[CSV] Header: {header}")
                for row in reader:
                    if not row or len(row) < 2:
                        continue
                    sid = row[0].strip()
                    # date column: index 7 in 9-col, index 5 in 8-col
                    if len(row) >= 9:
                        date = row[7].strip()
                    elif len(row) >= 8:
                        date = row[6].strip()
                    else:
                        date = row[len(row)-1].strip()
                    if sid:
                        records.append({"student_id": sid, "date": date})
        except Exception as e:
            print(f"[CSV] Read error: {e}")
        print(f"[CSV] Loaded {len(records)} present records.")
        return records

    # ═════════════════════════════════════════════════════════════════
    #  ABSENT LOGIC
    # ═════════════════════════════════════════════════════════════════
    def _build_absent_rows(self, date_str=None):
        """
        Returns sorted list of rows for students ABSENT on date_str.
        Row = [student_id, name, roll, dept, course, sem, year, date, 'Absent']
        Time is intentionally excluded — absent students have no recorded time.
        """
        if date_str is None:
            date_str = self.var_search_date.get().strip()

        if date_str:
            present_ids = {
                rec["student_id"]
                for rec in self._csv_records
                if rec["date"] == date_str
            }
        else:
            present_ids = set()   # no date → treat all as potentially absent

        rows = []
        for sid, info in self._all_students.items():
            if sid in present_ids:
                continue                  # student IS present — skip
            rows.append([
                sid,
                info["name"],
                info["roll"],
                info["dept"],
                info["course"],
                info["sem"],
                info["year"],
                date_str if date_str else "—",
                "Absent",
            ])

        rows.sort(key=lambda r: r[1].lower())   # sort alphabetically by name
        return rows

    # ═════════════════════════════════════════════════════════════════
    #  TABLE HELPERS
    # ═════════════════════════════════════════════════════════════════
    def fetch_data(self, rows):
        self.attendance_table.delete(*self.attendance_table.get_children())
        for row in rows:
            self.attendance_table.insert("", END, values=row, tags=("absent",))

    def get_cursor(self, event=""):
        selected = self.attendance_table.focus()
        if not selected:
            return
        d = self.attendance_table.item(selected)["values"]
        if len(d) < 9:
            return
        self.var_std_id.set(d[0])
        self.var_std_name.set(d[1])
        self.var_roll.set(d[2])
        self.var_department.set(d[3])
        self.var_course.set(d[4])
        self.var_semester.set(d[5])
        self.var_year.set(d[6])
        self.var_date.set(d[7])
        self.var_status.set(d[8])

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
            courses = [c for v in self.department_courses.values() for c in v]
        self.course_combo["values"] = ["All Courses"] + courses
        self.course_combo.current(0)

    # ═════════════════════════════════════════════════════════════════
    #  FILTERS
    # ═════════════════════════════════════════════════════════════════
    def apply_filters(self):
        dept     = self.var_search_department.get().strip()
        course   = self.var_search_course.get().strip()
        sem      = self.var_search_semester.get().strip()
        year     = self.var_search_year.get().strip()
        date_str = self.var_search_date.get().strip()

        self._absent_data = self._build_absent_rows(date_str or None)
        filtered = self._absent_data.copy()

        if dept   and dept   != "All Departments":
            filtered = [r for r in filtered if r[3].strip().lower() == dept.lower()]
        if course and course != "All Courses":
            filtered = [r for r in filtered if r[4].strip().lower() == course.lower()]
        if sem    and sem    != "All Semesters":
            filtered = [r for r in filtered if r[5].strip().lower() == sem.lower()]
        if year   and year   != "All Years":
            filtered = [r for r in filtered if r[6].strip() == year]

        self._filtered_data = filtered
        self.search_var.set("")
        self.fetch_data(filtered)
        self.update_statistics(filtered)
        self.update_analysis(filtered)

        if not filtered:
            parts = []
            if date_str:                                parts.append(f"Date = '{date_str}'")
            if dept   and dept   != "All Departments": parts.append(f"Department = '{dept}'")
            if course and course != "All Courses":     parts.append(f"Course = '{course}'")
            if sem    and sem    != "All Semesters":   parts.append(f"Semester = '{sem}'")
            if year   and year   != "All Years":       parts.append(f"Year = '{year}'")
            messagebox.showinfo(
                "No Results",
                "No absent students found for:\n" + "\n".join(parts),
                parent=self.root,
            )

    def show_all(self):
        self.var_search_department.set("All Departments")
        self.var_search_course.set("All Courses")
        self.var_search_semester.set("All Semesters")
        self.var_search_year.set("All Years")
        self.var_search_date.set("")
        self.search_var.set("")
        self._absent_data   = self._build_absent_rows(None)
        self._filtered_data = self._absent_data.copy()
        self.fetch_data(self._absent_data)
        self.update_statistics(self._absent_data)
        self.update_analysis(self._absent_data)

    def quick_search(self):
        term   = self.search_var.get().strip().lower()
        source = self._filtered_data if self._filtered_data else self._absent_data
        if not term:
            self.fetch_data(source)
            self.update_statistics(source)
            return
        result = [r for r in source if any(term in str(c).lower() for c in r)]
        self.fetch_data(result)
        self.update_statistics(result)

    # ═════════════════════════════════════════════════════════════════
    #  STATISTICS
    # ═════════════════════════════════════════════════════════════════
    def update_statistics(self, data=None):
        if data is None:
            data = self._absent_data
        total   = len(self._all_students)
        absent  = len(data)
        present = max(total - absent, 0)
        rate    = (absent / total * 100) if total else 0
        self.total_label.config(text=str(total))
        self.absent_label.config(text=str(absent))
        self.present_label.config(text=str(present))
        self.rate_label.config(text=f"{rate:.1f}%")

    # ═════════════════════════════════════════════════════════════════
    #  ANALYSIS PANEL
    # ═════════════════════════════════════════════════════════════════
    def update_analysis(self, data=None):
        if data is None:
            data = self._absent_data

        sem_counts = Counter(r[5] for r in data if r[5] and r[5] not in ("", "—"))
        self.lbl_sem.config(
            text="\n".join(f"{k}: {v} absent"
                           for k, v in sem_counts.most_common(6)) or "No data")

        dept_counts = Counter(r[3] for r in data if r[3] and r[3] not in ("", "—"))
        self.lbl_dept_ana.config(
            text="\n".join(f"{k}: {v} absent"
                           for k, v in dept_counts.most_common(6)) or "No data")

        sample = data[:5]
        self.lbl_recent.config(
            text="\n".join(f"{r[1]} | {r[4]} | {r[7]}"
                           for r in sample) or "No absent students")

    # ═════════════════════════════════════════════════════════════════
    #  EXPORT / RELOAD / REFRESH / RESET
    # ═════════════════════════════════════════════════════════════════
    def export_csv(self):
        rows = self._filtered_data if self._filtered_data else self._absent_data
        if not rows:
            messagebox.showerror("Error", "No absent records to export!", parent=self.root)
            return
        fln = filedialog.asksaveasfilename(
            initialdir=os.getcwd(), title="Save Absent Students",
            defaultextension=".csv",
            filetypes=(("CSV", "*.csv"), ("All", "*.*")),
            parent=self.root,
        )
        if not fln:
            return
        try:
            with open(fln, "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["StudentID","Name","Roll","Department",
                             "Course","Semester","Year","Date","Status"])
                for row in rows:
                    w.writerow(row)
            messagebox.showinfo("Exported",
                                f"Exported {len(rows)} absent record(s) to:\n{fln}",
                                parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Export failed:\n{e}", parent=self.root)

    def reload_db(self):
        """Re-fetch student master from MySQL without touching the CSV."""
        self._all_students = fetch_students_from_mysql()
        self._absent_data   = self._build_absent_rows()
        self._filtered_data = self._absent_data.copy()
        self.fetch_data(self._absent_data)
        self.update_statistics(self._absent_data)
        self.update_analysis(self._absent_data)
        messagebox.showinfo(
            "Reloaded",
            f"Reloaded {len(self._all_students)} students from MySQL.",
            parent=self.root,
        )

    def refresh_all(self):
        """Full reload — MySQL students + CSV present records."""
        self.load_data()

    def reset_fields(self):
        for v in (self.var_std_id, self.var_std_name, self.var_roll,
                  self.var_department, self.var_course, self.var_semester,
                  self.var_year, self.var_date, self.var_status):
            v.set("")
        self.var_search_department.set("All Departments")
        self.var_search_course.set("All Courses")
        self.var_search_semester.set("All Semesters")
        self.var_search_year.set("All Years")
        self.var_search_date.set(strftime("%d/%m/%Y", localtime()))
        self.search_var.set("")
        self._absent_data   = self._build_absent_rows()
        self._filtered_data = self._absent_data.copy()
        self.fetch_data(self._absent_data)
        self.update_statistics(self._absent_data)
        self.update_analysis(self._absent_data)


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = Tk()
    app  = AbsentStudentSystem(root)
    root.mainloop()