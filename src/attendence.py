import os
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import csv
from time import strftime, localtime
from datetime import datetime
from collections import Counter

mydata = []

class AttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("1530x850+0+0")
        self.root.state('zoomed')  # Maximize window

        # =================== VARIABLES ===================
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_roll = StringVar()
        self.var_department = StringVar()
        self.var_date = StringVar()
        self.var_time = StringVar()
        self.var_status = StringVar()
        
        # Search/Filter variables
        self.var_search_department = StringVar()
        self.var_search_semester = StringVar()
        self.var_search_date = StringVar()

        # =================== COLOR SCHEME ===================
        self.colors = {
            'bg_dark': '#0a0e27',
            'bg_card': '#1a1f3a',
            'primary': '#4a90e2',
            'secondary': '#50e3c2',
            'success': '#27ae60',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'info': '#3498db'
        }

        self.root.configure(bg=self.colors['bg_dark'])

        # =================== TITLE ===================
        title_lbl = Label(
            self.root,
            text="STUDENT ATTENDANCE MANAGEMENT SYSTEM",
            font=("Helvetica", 32, "bold"),
            bg=self.colors['bg_dark'],
            fg="white"
        )
     
        # =================== MAIN FRAME ===================
        main_frame = Frame(self.root, bg=self.colors['bg_dark'])
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # =================== TOP SECTION - STATISTICS ===================
        stats_frame = LabelFrame(
            main_frame,
            bd=2,
            bg=self.colors['bg_card'],
            relief=RIDGE,
            text="Today's Attendance Statistics",
            font=("Helvetica", 14, "bold"),
            fg="white"
        )
        stats_frame.pack(fill=X, pady=(0, 10))

        # Statistics cards
        self.stats_container = Frame(stats_frame, bg=self.colors['bg_card'])
        self.stats_container.pack(fill=X, padx=10, pady=10)

        self.create_stat_card(self.stats_container, "Total Records", "0", self.colors['info'], 0)
        self.create_stat_card(self.stats_container, "Present", "0", self.colors['success'], 1)
        self.create_stat_card(self.stats_container, "Absent", "0", self.colors['danger'], 2)
        self.create_stat_card(self.stats_container, "Attendance Rate", "0%", self.colors['warning'], 3)

        # =================== LEFT FRAME - FILTERS & CONTROLS ===================
        Left_frame = LabelFrame(
            main_frame,
            bd=2,
            bg=self.colors['bg_card'],
            relief=RIDGE,
            text="Search & Filter Controls",
            font=("Helvetica", 13, "bold"),
            fg="white"
        )
        Left_frame.place(relx=0, rely=0.22, relwidth=0.35, relheight=0.78)

        # Search Section
        search_section = LabelFrame(
            Left_frame,
            bd=2,
            bg=self.colors['bg_card'],
            relief=RIDGE,
            text="Filter Options",
            font=("Helvetica", 11, "bold"),
            fg=self.colors['secondary']
        )
        search_section.pack(fill=X, padx=10, pady=10)

        # Department Filter
        Label(search_section, text="Department:", bg=self.colors['bg_card'], 
              fg="white", font=("Helvetica", 11, "bold")).grid(row=0, column=0, 
              padx=10, pady=10, sticky=W)
        dept_combo = ttk.Combobox(
            search_section,
            textvariable=self.var_search_department,
            font=("Helvetica", 11),
            state="readonly",
            width=20
        )
        dept_combo["values"] = ("All", "BCA", "BBA", "B.Tech", "MCA", "MBA")
        dept_combo.current(0)
        dept_combo.grid(row=0, column=1, padx=10, pady=10)

        # Semester Filter
        Label(search_section, text="Semester:", bg=self.colors['bg_card'], 
              fg="white", font=("Helvetica", 11, "bold")).grid(row=1, column=0, 
              padx=10, pady=10, sticky=W)
        sem_combo = ttk.Combobox(
            search_section,
            textvariable=self.var_search_semester,
            font=("Helvetica", 11),
            state="readonly",
            width=20
        )
        sem_combo["values"] = ("All", "1", "2", "3", "4", "5", "6", "7", "8")
        sem_combo.current(0)
        sem_combo.grid(row=1, column=1, padx=10, pady=10)

        # Date Filter
        Label(search_section, text="Date:", bg=self.colors['bg_card'], 
              fg="white", font=("Helvetica", 11, "bold")).grid(row=2, column=0, 
              padx=10, pady=10, sticky=W)
        date_entry = ttk.Entry(search_section, width=22, 
                              textvariable=self.var_search_date,
                              font=("Helvetica", 11))
        date_entry.grid(row=2, column=1, padx=10, pady=10)
        self.var_search_date.set(strftime("%d/%m/%Y", localtime()))

        # Search Button
        Button(search_section, text="🔍 Apply Filters", width=20, 
               command=self.apply_filters,
               font=("Helvetica", 11, "bold"), 
               bg=self.colors['info'], fg="white",
               cursor="hand2").grid(row=3, column=0, columnspan=2, 
                                   padx=10, pady=15)

        # Student Details Section
        details_section = LabelFrame(
            Left_frame,
            bd=2,
            bg=self.colors['bg_card'],
            relief=RIDGE,
            text="Student Details",
            font=("Helvetica", 11, "bold"),
            fg=self.colors['secondary']
        )
        details_section.pack(fill=X, padx=10, pady=(10, 5))

        # Student ID
        Label(details_section, text="Student ID:", bg=self.colors['bg_card'], 
              fg="white", font=("Helvetica", 11, "bold")).grid(row=0, column=0, 
              padx=10, pady=8, sticky=W)
        ttk.Entry(details_section, width=22, textvariable=self.var_std_id,
                 font=("Helvetica", 11)).grid(row=0, column=1, padx=10, pady=8)

        # Name
        Label(details_section, text="Name:", bg=self.colors['bg_card'], 
              fg="white", font=("Helvetica", 11, "bold")).grid(row=1, column=0, 
              padx=10, pady=8, sticky=W)
        ttk.Entry(details_section, width=22, textvariable=self.var_std_name,
                 font=("Helvetica", 11)).grid(row=1, column=1, padx=10, pady=8)

        # Roll Number
        Label(details_section, text="Roll No:", bg=self.colors['bg_card'], 
              fg="white", font=("Helvetica", 11, "bold")).grid(row=2, column=0, 
              padx=10, pady=8, sticky=W)
        ttk.Entry(details_section, width=22, textvariable=self.var_roll,
                 font=("Helvetica", 11)).grid(row=2, column=1, padx=10, pady=8)

        # Department
        Label(details_section, text="Department:", bg=self.colors['bg_card'], 
              fg="white", font=("Helvetica", 11, "bold")).grid(row=3, column=0, 
              padx=10, pady=8, sticky=W)
        ttk.Entry(details_section, width=22, textvariable=self.var_department,
                 font=("Helvetica", 11)).grid(row=3, column=1, padx=10, pady=8)

        # Date
        Label(details_section, text="Date:", bg=self.colors['bg_card'], 
              fg="white", font=("Helvetica", 11, "bold")).grid(row=4, column=0, 
              padx=10, pady=8, sticky=W)
        ttk.Entry(details_section, width=22, textvariable=self.var_date,
                 font=("Helvetica", 11)).grid(row=4, column=1, padx=10, pady=8)

        # Time
        Label(details_section, text="Time:", bg=self.colors['bg_card'], 
              fg="white", font=("Helvetica", 11, "bold")).grid(row=5, column=0, 
              padx=10, pady=8, sticky=W)
        ttk.Entry(details_section, width=22, textvariable=self.var_time,
                 font=("Helvetica", 11)).grid(row=5, column=1, padx=10, pady=8)

        # Status
        Label(details_section, text="Status:", bg=self.colors['bg_card'], 
              fg="white", font=("Helvetica", 11, "bold")).grid(row=6, column=0, 
              padx=10, pady=8, sticky=W)
        status_combo = ttk.Combobox(
            details_section,
            textvariable=self.var_status,
            font=("Helvetica", 11),
            state="readonly",
            width=20
        )
        status_combo["values"] = ("Select", "Present", "Absent")
        status_combo.current(0)
        status_combo.grid(row=6, column=1, padx=10, pady=8)

        # =================== BUTTON FRAME ===================
        btn_frame = Frame(Left_frame, bd=2, relief=RIDGE, 
                         bg=self.colors['bg_card'])
        btn_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Configure grid weights for proper button display
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

        Button(btn_frame, text="📥 Import CSV", 
               command=self.import_csv,
               font=("Helvetica", 11, "bold"), 
               bg=self.colors['success'], fg="white",
               cursor="hand2", height=2).grid(row=0, column=0, 
               padx=5, pady=8, sticky="ew")

        Button(btn_frame, text="📤 Export CSV", 
               command=self.export_csv,
               font=("Helvetica", 11, "bold"), 
               bg=self.colors['primary'], fg="white",
               cursor="hand2", height=2).grid(row=0, column=1, 
               padx=5, pady=8, sticky="ew")

        Button(btn_frame, text="🔄 Reset", 
               command=self.reset_data,
               font=("Helvetica", 11, "bold"), 
               bg=self.colors['warning'], fg="white",
               cursor="hand2", height=2).grid(row=1, column=0, 
               padx=5, pady=8, sticky="ew")

        Button(btn_frame, text="📊 Refresh Stats", 
               command=self.update_statistics,
               font=("Helvetica", 11, "bold"), 
               bg=self.colors['info'], fg="white",
               cursor="hand2", height=2).grid(row=1, column=1, 
               padx=5, pady=8, sticky="ew")

        # =================== RIGHT FRAME - TABLE ===================
        Right_frame = LabelFrame(
            main_frame,
            bd=2,
            bg=self.colors['bg_card'],
            relief=RIDGE,
            text="Attendance Records",
            font=("Helvetica", 13, "bold"),
            fg="white"
        )
        Right_frame.place(relx=0.36, rely=0.22, relwidth=0.64, relheight=0.78)

        # Search bar in table section
        search_bar_frame = Frame(Right_frame, bg=self.colors['bg_card'])
        search_bar_frame.pack(fill=X, padx=10, pady=5)

        Label(search_bar_frame, text="Quick Search:", 
              bg=self.colors['bg_card'], fg="white",
              font=("Helvetica", 11, "bold")).pack(side=LEFT, padx=5)
        
        self.search_var = StringVar()
        self.search_var.trace('w', lambda *args: self.quick_search())
        search_entry = ttk.Entry(search_bar_frame, textvariable=self.search_var,
                                font=("Helvetica", 11), width=30)
        search_entry.pack(side=LEFT, padx=5)

        Label(search_bar_frame, text="(Search by ID, Name, Roll, or Department)",
              bg=self.colors['bg_card'], fg="#cccccc",
              font=("Helvetica", 9)).pack(side=LEFT, padx=5)

        # Table Frame with scrollbars
        table_frame = Frame(Right_frame, bd=2, relief=RIDGE, 
                           bg=self.colors['bg_card'])
        table_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        # Scrollbars
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        # Treeview widget
        self.attendance_table = ttk.Treeview(
            table_frame,
            columns=("id", "name", "roll", "dept", "date", "time", "status"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        # Pack scrollbars
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        # Configure scrollbars
        scroll_x.config(command=self.attendance_table.xview)
        scroll_y.config(command=self.attendance_table.yview)

        # Configure table headings
        self.attendance_table.heading("id", text="Student ID")
        self.attendance_table.heading("name", text="Name")
        self.attendance_table.heading("roll", text="Roll No")
        self.attendance_table.heading("dept", text="Department")
        self.attendance_table.heading("date", text="Date")
        self.attendance_table.heading("time", text="Time")
        self.attendance_table.heading("status", text="Status")

        self.attendance_table["show"] = "headings"

        # Column widths
        self.attendance_table.column("id", width=100, anchor=CENTER)
        self.attendance_table.column("name", width=200, anchor=W)
        self.attendance_table.column("roll", width=100, anchor=CENTER)
        self.attendance_table.column("dept", width=120, anchor=CENTER)
        self.attendance_table.column("date", width=120, anchor=CENTER)
        self.attendance_table.column("time", width=100, anchor=CENTER)
        self.attendance_table.column("status", width=100, anchor=CENTER)

        self.attendance_table.pack(fill=BOTH, expand=True)
        self.attendance_table.bind("<ButtonRelease>", self.get_cursor)

        # Configure tag colors for status
        self.attendance_table.tag_configure('present', background='#d4edda')
        self.attendance_table.tag_configure('absent', background='#f8d7da')

        # Load initial data
        self.load_from_csv()
        self.update_statistics()

    def create_stat_card(self, parent, title, value, color, col):
        """Create a statistics card"""
        card = Frame(parent, bg=color, relief=RIDGE, bd=2)
        card.grid(row=0, column=col, padx=10, pady=5, sticky="ew")
        parent.grid_columnconfigure(col, weight=1)

        Label(card, text=title, font=("Helvetica", 12, "bold"),
              bg=color, fg="white").pack(pady=(10, 5))
        
        lbl = Label(card, text=value, font=("Helvetica", 20, "bold"),
                    bg=color, fg="white")
        lbl.pack(pady=(5, 10))
        
        # Store reference for updating
        if col == 0:
            self.total_label = lbl
        elif col == 1:
            self.present_label = lbl
        elif col == 2:
            self.absent_label = lbl
        elif col == 3:
            self.rate_label = lbl

    def get_cursor(self, event=""):
        """Get selected row data"""
        cursor = self.attendance_table.focus()
        content = self.attendance_table.item(cursor)
        data = content["values"]

        if len(data) < 7:
            return

        self.var_std_id.set(data[0])
        self.var_std_name.set(data[1])
        self.var_roll.set(data[2])
        self.var_department.set(data[3])
        self.var_date.set(data[5])
        self.var_time.set(data[4])
        self.var_status.set(data[6])

    def fetch_data(self, rows):
        """Display data in table"""
        self.attendance_table.delete(*self.attendance_table.get_children())
        for row in rows:
            if len(row) >= 7:
                tag = 'present' if row[6].lower() == 'present' else 'absent'
                self.attendance_table.insert("", END, values=row, tags=(tag,))

    def load_from_csv(self):
        """Load data from attendance.csv if exists"""
        global mydata
        mydata.clear()
        
        # Try multiple possible locations
        csv_paths = [
            "attendance.csv",
            os.path.join(os.path.dirname(__file__), "attendance.csv"),
            r"C:\Users\Dell\Desktop\PYTHON\src\attendance.csv"
        ]
        
        csv_file = None
        for path in csv_paths:
            if os.path.exists(path):
                csv_file = path
                break
        
        if csv_file:
            try:
                with open(csv_file, "r") as f:
                    csvread = csv.reader(f)
                    header = next(csvread, None)  # Read header
                    
                    for row in csvread:
                        if row and len(row) >= 7:  # Skip empty rows
                            # Reorder columns: CSV has Time,Date but code expects Date,Time
                            # CSV format: StudentID,Name,Roll,Department,Time,Date,Status
                            # Code expects: StudentID,Name,Roll,Department,Date,Time,Status
                            reordered_row = [
                                row[0],  # StudentID
                                row[1],  # Name
                                row[2],  # Roll
                                row[3],  # Department
                                row[5],  # Date (was at index 5)
                                row[4],  # Time (was at index 4)
                                row[6]   # Status
                            ]
                            mydata.append(reordered_row)
                self.fetch_data(mydata)
                print(f"Loaded {len(mydata)} records from {csv_file}")
            except Exception as e:
                print(f"Error loading CSV: {e}")
        else:
            print("attendance.csv not found in any expected location")

    def import_csv(self):
        """Import CSV file"""
        global mydata
        mydata.clear()
        fln = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Open CSV",
            filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")),
            parent=self.root
        )

        if fln:
            try:
                with open(fln) as myfile:
                    csvread = csv.reader(myfile)
                    next(csvread, None)  # Skip header
                    for row in csvread:
                        if row:  # Skip empty rows
                            mydata.append(row)
                self.fetch_data(mydata)
                self.update_statistics()
                messagebox.showinfo("Success", "Data imported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import: {str(e)}")

    def export_csv(self):
        """Export data to CSV"""
        if len(mydata) < 1:
            messagebox.showerror("Error", "No data available to export!", 
                               parent=self.root)
            return

        fln = filedialog.asksaveasfilename(
            initialdir=os.getcwd(),
            title="Save CSV",
            defaultextension=".csv",
            filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")),
            parent=self.root
        )

        if fln:
            try:
                with open(fln, mode="w", newline="") as myfile:
                    csvwriter = csv.writer(myfile)
                    csvwriter.writerow(["StudentID", "Name", "Roll", 
                                      "Department", "Date", "Time", "Status"])
                    for row in mydata:
                        csvwriter.writerow(row)
                messagebox.showinfo("Success", 
                                  f"Data exported successfully to {fln}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def apply_filters(self):
        """Apply department, semester, and date filters"""
        global mydata
        
        dept = self.var_search_department.get()
        semester = self.var_search_semester.get()
        date = self.var_search_date.get()

        filtered_data = mydata.copy()

        # Filter by department
        if dept != "All":
            filtered_data = [row for row in filtered_data 
                           if len(row) > 3 and dept.lower() in row[3].lower()]

        # Filter by semester (extract from roll number or department)
        if semester != "All":
            filtered_data = [row for row in filtered_data 
                           if len(row) > 2 and semester in row[2]]

        # Filter by date
        if date:
            filtered_data = [row for row in filtered_data 
                           if len(row) > 4 and date in row[4]]

        self.fetch_data(filtered_data)
        self.update_statistics(filtered_data)

    def quick_search(self):
        """Quick search through table"""
        search_term = self.search_var.get().lower()
        
        if not search_term:
            self.fetch_data(mydata)
            return

        filtered = [row for row in mydata if any(search_term in str(cell).lower() 
                   for cell in row)]
        self.fetch_data(filtered)

    def update_statistics(self, data=None):
        """Update statistics cards"""
        if data is None:
            data = mydata

        total = len(data)
        present = sum(1 for row in data if len(row) > 6 and 
                     row[6].lower() == 'present')
        absent = sum(1 for row in data if len(row) > 6 and 
                    row[6].lower() == 'absent')
        
        rate = (present / total * 100) if total > 0 else 0

        self.total_label.config(text=str(total))
        self.present_label.config(text=str(present))
        self.absent_label.config(text=str(absent))
        self.rate_label.config(text=f"{rate:.1f}%")

    def reset_data(self):
        """Reset form fields"""
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_roll.set("")
        self.var_department.set("")
        self.var_date.set(strftime("%d/%m/%Y", localtime()))
        self.var_time.set(strftime("%H:%M:%S", localtime()))
        self.var_status.set("Select")
        self.var_search_department.set("All")
        self.var_search_semester.set("All")
        self.var_search_date.set(strftime("%d/%m/%Y", localtime()))
        self.search_var.set("")
        self.fetch_data(mydata)
        self.update_statistics()


# =================== MAIN ===================
if __name__ == "__main__":
    root = Tk()
    app = AttendanceSystem(root)
    root.mainloop()