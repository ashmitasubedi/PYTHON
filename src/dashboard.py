"""
AttendIQ — Student Attendance Dashboard
Built with tkinter + matplotlib + pandas
CSV columns: StudentID, Name, Roll, Department, Time, Date, Status
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as mpatches
from datetime import datetime, date
import os, csv, io

# ─────────────────────────────────────────────
#  THEME
# ─────────────────────────────────────────────
T = {
    "bg":       "#0b0d12",
    "surface":  "#12151d",
    "surface2": "#181c27",
    "surface3": "#1e2332",
    "border":   "#1e2332",
    "text":     "#dfe2ec",
    "text2":    "#7e82a0",
    "text3":    "#464a62",
    "accent":   "#5b7fff",
    "green":    "#2ecc8a",
    "red":      "#f06060",
    "amber":    "#f5a623",
    "teal":     "#1ed8c0",
    "pink":     "#e864b0",
    "coral":    "#f07040",
}

DEPT_COLORS = ["#5b7fff", "#2ecc8a", "#f5a623", "#e864b0", "#1ed8c0", "#f07040"]
STATUS_COLORS = {"Present": "#2ecc8a", "Absent": "#f06060", "Late": "#f5a623"}

matplotlib.rcParams.update({
    "figure.facecolor":  T["surface"],
    "axes.facecolor":    T["surface2"],
    "axes.edgecolor":    T["border"],
    "axes.labelcolor":   T["text2"],
    "xtick.color":       T["text3"],
    "ytick.color":       T["text3"],
    "text.color":        T["text"],
    "grid.color":        T["surface3"],
    "grid.linewidth":    0.6,
    "font.family":       "monospace",
    "axes.titlesize":    11,
    "axes.labelsize":    9,
    "xtick.labelsize":   8,
    "ytick.labelsize":   8,
    "legend.fontsize":   8,
    "legend.facecolor":  T["surface2"],
    "legend.edgecolor":  T["border"],
    "legend.labelcolor": T["text2"],
})

# ─────────────────────────────────────────────
#  DATA LAYER
# ─────────────────────────────────────────────
SEED = [
    {"StudentID": "12", "Name": "ashmita subedi", "Roll": "18", "Department": "IT",
     "Time": "10:07:40", "Date": "12/12/2025", "Status": "Present"},
    {"StudentID": "12", "Name": "ashmita subedi", "Roll": "18", "Department": "IT",
     "Time": "21:26:02", "Date": "20/12/2025", "Status": "Present"},
    {"StudentID": "7",  "Name": "sajan",          "Roll": "7",  "Department": "Commerce",
     "Time": "21:26:07", "Date": "20/12/2025", "Status": "Present"},
    {"StudentID": "12", "Name": "ashmita subedi", "Roll": "18", "Department": "IT",
     "Time": "15:05:45", "Date": "19/01/2026", "Status": "Present"},
]
COLS = ["StudentID", "Name", "Roll", "Department", "Time", "Date", "Status"]


def parse_date(s):
    """Convert DD/MM/YYYY or YYYY-MM-DD to a date object."""
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(str(s).strip(), fmt).date()
        except ValueError:
            pass
    return None


def load_csv(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            r = {c: row.get(c, "").strip() for c in COLS}
            rows.append(r)
    return rows


def save_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLS)
        writer.writeheader()
        writer.writerows(rows)


class DataStore:
    def __init__(self):
        self.records = [dict(r) for r in SEED]
        self._nid = 100

    def new_id(self):
        self._nid += 1
        return str(self._nid)

    def add(self, rec):
        self.records.append(rec)

    def delete_by_indices(self, indices):
        indices_set = set(indices)
        self.records = [r for i, r in enumerate(self.records) if i not in indices_set]

    def to_df(self):
        df = pd.DataFrame(self.records, columns=COLS)
        df["_date"] = df["Date"].apply(parse_date)
        return df

    def filter(self, search="", department="", status="", date_from=None, date_to=None):
        df = self.to_df()
        if search:
            s = search.lower()
            mask = (df["Name"].str.lower().str.contains(s, na=False) |
                    df["StudentID"].str.lower().str.contains(s, na=False) |
                    df["Department"].str.lower().str.contains(s, na=False) |
                    df["Roll"].str.lower().str.contains(s, na=False))
            df = df[mask]
        if department:
            df = df[df["Department"] == department]
        if status:
            df = df[df["Status"] == status]
        if date_from:
            df = df[df["_date"].apply(lambda d: d >= date_from if d else False)]
        if date_to:
            df = df[df["_date"].apply(lambda d: d <= date_to if d else False)]
        return df

    def student_stats(self):
        df = self.to_df()
        g = df.groupby("StudentID").agg(
            Name=("Name", "first"),
            Roll=("Roll", "first"),
            Department=("Department", "first"),
            Total=("Status", "count"),
            Present=("Status", lambda x: (x.isin(["Present", "Late"])).sum()),
            Absent=("Status", lambda x: (x == "Absent").sum()),
        ).reset_index()
        g["Rate"] = (g["Present"] / g["Total"] * 100).round(1)
        return g

    def departments(self):
        return sorted(set(r["Department"] for r in self.records))

    def import_from_path(self, path):
        rows = load_csv(path)
        self.records.extend(rows)

    def export_to_path(self, path):
        save_csv(path, self.records)


# ─────────────────────────────────────────────
#  WIDGET HELPERS
# ─────────────────────────────────────────────

def styled_button(parent, text, cmd, color=None, **kw):
    bg = color or T["surface2"]
    fg = T["text"]
    btn = tk.Button(
        parent, text=text, command=cmd,
        bg=bg, fg=fg,
        relief="flat", bd=0,
        padx=14, pady=6,
        font=("Courier", 10, "bold"),
        activebackground=T["surface3"],
        activeforeground=T["text"],
        cursor="hand2",
        **kw
    )
    return btn


def label(parent, text, size=10, color=None, bold=False, **kw):
    font = ("Courier", size, "bold" if bold else "normal")
    return tk.Label(parent, text=text, bg=T["surface"], fg=color or T["text"],
                    font=font, **kw)


def frame(parent, bg=None, **kw):
    return tk.Frame(parent, bg=bg or T["surface"], **kw)


def separator(parent):
    return tk.Frame(parent, bg=T["border"], height=1)


def entry(parent, **kw):
    e = tk.Entry(parent,
                 bg=T["surface2"], fg=T["text"],
                 insertbackground=T["text"],
                 relief="flat", bd=0,
                 font=("Courier", 10),
                 highlightthickness=1,
                 highlightcolor=T["accent"],
                 highlightbackground=T["border"],
                 **kw)
    return e


def combobox(parent, values, **kw):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Dark.TCombobox",
                    fieldbackground=T["surface2"],
                    background=T["surface2"],
                    foreground=T["text"],
                    selectbackground=T["accent"],
                    selectforeground="white",
                    bordercolor=T["border"],
                    arrowcolor=T["text2"],
                    relief="flat")
    cb = ttk.Combobox(parent, values=values, style="Dark.TCombobox",
                      font=("Courier", 10), state="readonly", **kw)
    return cb


def card(parent, title, value, sub, accent):
    f = tk.Frame(parent, bg=T["surface2"], padx=16, pady=14)
    # top accent line
    tk.Frame(f, bg=accent, height=2).pack(fill="x")
    tk.Label(f, text=title.upper(), bg=T["surface2"], fg=T["text3"],
             font=("Courier", 8, "bold")).pack(anchor="w", pady=(8, 0))
    tk.Label(f, text=str(value), bg=T["surface2"], fg=accent,
             font=("Courier", 22, "bold")).pack(anchor="w")
    tk.Label(f, text=sub, bg=T["surface2"], fg=T["text3"],
             font=("Courier", 8)).pack(anchor="w")
    return f


# ─────────────────────────────────────────────
#  TREEVIEW (table)
# ─────────────────────────────────────────────

def build_treeview(parent, columns, col_widths=None):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Dark.Treeview",
                    background=T["surface"],
                    foreground=T["text"],
                    fieldbackground=T["surface"],
                    borderwidth=0,
                    rowheight=28,
                    font=("Courier", 9))
    style.configure("Dark.Treeview.Heading",
                    background=T["surface2"],
                    foreground=T["text2"],
                    borderwidth=0,
                    font=("Courier", 9, "bold"),
                    relief="flat")
    style.map("Dark.Treeview",
              background=[("selected", T["accent"])],
              foreground=[("selected", "white")])
    style.map("Dark.Treeview.Heading",
              background=[("active", T["surface3"])])

    frame_ = tk.Frame(parent, bg=T["border"], pady=1)
    sv = tk.Scrollbar(frame_, orient="vertical", bg=T["surface2"])
    sh = tk.Scrollbar(frame_, orient="horizontal", bg=T["surface2"])

    tree = ttk.Treeview(frame_, columns=columns, show="headings",
                        style="Dark.Treeview",
                        yscrollcommand=sv.set,
                        xscrollcommand=sh.set,
                        selectmode="extended")

    sv.config(command=tree.yview)
    sh.config(command=tree.xview)

    for i, col in enumerate(columns):
        w = (col_widths[i] if col_widths and i < len(col_widths) else 100)
        tree.heading(col, text=col)
        tree.column(col, width=w, minwidth=60, anchor="w")

    tree.grid(row=0, column=0, sticky="nsew")
    sv.grid(row=0, column=1, sticky="ns")
    sh.grid(row=1, column=0, sticky="ew")
    frame_.rowconfigure(0, weight=1)
    frame_.columnconfigure(0, weight=1)

    # alternate row colors
    tree.tag_configure("odd",  background=T["surface"])
    tree.tag_configure("even", background=T["surface2"])
    tree.tag_configure("present", foreground=T["green"])
    tree.tag_configure("absent",  foreground=T["red"])
    tree.tag_configure("late",    foreground=T["amber"])

    return tree, frame_


# ─────────────────────────────────────────────
#  CHARTS
# ─────────────────────────────────────────────

def make_figure(w=6, h=3.2):
    fig = Figure(figsize=(w, h), dpi=96, facecolor=T["surface"])
    return fig


def embed_figure(fig, parent):
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    return canvas


# ─────────────────────────────────────────────
#  MAIN APPLICATION
# ─────────────────────────────────────────────

class AttendIQ(tk.Tk):
    def __init__(self):
        super().__init__()
        self.ds = DataStore()
        self.title("AttendIQ — Attendance Dashboard")
        self.geometry("1280x800")
        self.minsize(960, 640)
        self.configure(bg=T["bg"])
        self._build_ui()
        self._switch_view("overview")

    # ── UI SHELL ──────────────────────────────
    def _build_ui(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self._build_sidebar()
        self._build_content_area()

    def _build_sidebar(self):
        sb = tk.Frame(self, bg=T["surface"], width=200)
        sb.grid(row=0, column=0, sticky="ns")
        sb.pack_propagate(False)

        # logo
        logo_f = tk.Frame(sb, bg=T["surface"], pady=20, padx=16)
        logo_f.pack(fill="x")
        tk.Label(logo_f, text="◈ AttendIQ", bg=T["surface"], fg=T["accent"],
                 font=("Courier", 14, "bold")).pack(anchor="w")
        tk.Label(logo_f, text="Smart Tracker v1.0", bg=T["surface"], fg=T["text3"],
                 font=("Courier", 8)).pack(anchor="w")
        separator(sb).pack(fill="x")

        # nav buttons
        nav = tk.Frame(sb, bg=T["surface"], pady=12)
        nav.pack(fill="x")

        self._nav_btns = {}
        nav_items = [
            ("overview",  "▦  Overview"),
            ("department","▤  By Department"),
            ("students",  "▣  Students"),
            ("records",   "▢  All Records"),
        ]
        for key, label_text in nav_items:
            btn = tk.Button(nav, text=label_text,
                            bg=T["surface"], fg=T["text2"],
                            relief="flat", bd=0,
                            padx=16, pady=9,
                            font=("Courier", 10),
                            anchor="w",
                            activebackground=T["surface2"],
                            activeforeground=T["accent"],
                            cursor="hand2",
                            command=lambda k=key: self._switch_view(k))
            btn.pack(fill="x")
            self._nav_btns[key] = btn

        separator(sb).pack(fill="x")

        # data actions
        acts = tk.Frame(sb, bg=T["surface"], pady=12)
        acts.pack(fill="x")
        tk.Label(acts, text="DATA", bg=T["surface"], fg=T["text3"],
                 font=("Courier", 8, "bold"), padx=16).pack(anchor="w")
        styled_button(acts, "+ Add Record",   self._open_add_modal,  T["accent"]).pack(fill="x", padx=10, pady=3)
        styled_button(acts, "↑ Import CSV",   self._import_csv,  T["surface2"]).pack(fill="x", padx=10, pady=3)
        styled_button(acts, "↓ Export CSV",   self._export_csv,  T["surface2"]).pack(fill="x", padx=10, pady=3)

        # live counter
        separator(sb).pack(fill="x")
        live_f = tk.Frame(sb, bg=T["surface"], pady=12, padx=16)
        live_f.pack(fill="x")
        self._live_var = tk.StringVar(value="0")
        tk.Label(live_f, text="● TODAY PRESENT", bg=T["surface"], fg=T["text3"],
                 font=("Courier", 8, "bold")).pack(anchor="w")
        tk.Label(live_f, textvariable=self._live_var, bg=T["surface"], fg=T["green"],
                 font=("Courier", 20, "bold")).pack(anchor="w")

    def _build_content_area(self):
        self._content = tk.Frame(self, bg=T["bg"])
        self._content.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self._content.columnconfigure(0, weight=1)
        self._content.rowconfigure(0, weight=1)

        self._views = {}
        for name, cls in [
            ("overview",   OverviewView),
            ("department", DepartmentView),
            ("students",   StudentsView),
            ("records",    RecordsView),
        ]:
            v = cls(self._content, self.ds, self)
            v.grid(row=0, column=0, sticky="nsew")
            self._views[name] = v

    def _switch_view(self, name):
        for key, btn in self._nav_btns.items():
            if key == name:
                btn.config(bg=T["surface2"], fg=T["accent"], font=("Courier", 10, "bold"))
            else:
                btn.config(bg=T["surface"], fg=T["text2"], font=("Courier", 10))
        for key, view in self._views.items():
            if key == name:
                view.tkraise()
                view.refresh()
            else:
                view.lower()
        self._update_live()

    def _update_live(self):
        today = date.today().strftime("%d/%m/%Y")
        count = sum(1 for r in self.ds.records
                    if r["Date"] == today and r["Status"] == "Present")
        self._live_var.set(str(count))

    # ── ADD RECORD MODAL ──────────────────────
    def _open_add_modal(self):
        modal = tk.Toplevel(self)
        modal.title("Add Attendance Record")
        modal.geometry("440x420")
        modal.configure(bg=T["surface"])
        modal.resizable(False, False)
        modal.grab_set()

        tk.Label(modal, text="Add Attendance Record", bg=T["surface"], fg=T["text"],
                 font=("Courier", 13, "bold"), pady=16).pack()
        separator(modal).pack(fill="x")

        form = tk.Frame(modal, bg=T["surface"], padx=24, pady=16)
        form.pack(fill="both", expand=True)

        fields = {}

        def row(lbl, widget_fn, **kw):
            r = tk.Frame(form, bg=T["surface"])
            r.pack(fill="x", pady=5)
            tk.Label(r, text=lbl.upper(), bg=T["surface"], fg=T["text3"],
                     font=("Courier", 8, "bold")).pack(anchor="w")
            w = widget_fn(r, **kw)
            w.pack(fill="x", pady=2)
            return w

        fields["Name"]       = row("Student Name", entry)
        fields["StudentID"]  = row("Student ID",   entry)
        fields["Roll"]       = row("Roll No.",      entry)

        dept_vals = self.ds.departments() or ["IT", "Commerce", "Science", "Arts"]
        fields["Department"] = row("Department",   combobox, values=dept_vals)
        fields["Department"].set(dept_vals[0] if dept_vals else "IT")

        fields["Date"] = row("Date (DD/MM/YYYY)", entry)
        fields["Date"].insert(0, date.today().strftime("%d/%m/%Y"))

        fields["Time"] = row("Time (HH:MM:SS)", entry)
        fields["Time"].insert(0, datetime.now().strftime("%H:%M:%S"))

        fields["Status"] = row("Status", combobox, values=["Present", "Absent", "Late"])
        fields["Status"].set("Present")

        def save():
            name = fields["Name"].get().strip()
            sid  = fields["StudentID"].get().strip()
            if not name:
                messagebox.showwarning("Required", "Student Name is required.", parent=modal)
                return
            rec = {
                "StudentID":  sid or self.ds.new_id(),
                "Name":       name,
                "Roll":       fields["Roll"].get().strip(),
                "Department": fields["Department"].get(),
                "Time":       fields["Time"].get().strip(),
                "Date":       fields["Date"].get().strip(),
                "Status":     fields["Status"].get(),
            }
            self.ds.add(rec)
            modal.destroy()
            self._refresh_current()
            self._update_live()

        separator(modal).pack(fill="x")
        btn_f = tk.Frame(modal, bg=T["surface"], pady=12, padx=24)
        btn_f.pack(fill="x")
        styled_button(btn_f, "Cancel", modal.destroy).pack(side="right", padx=6)
        styled_button(btn_f, "Save Record", save, T["accent"]).pack(side="right")

    def _refresh_current(self):
        for view in self._views.values():
            try:
                view.refresh()
            except Exception:
                pass

    # ── IMPORT / EXPORT ───────────────────────
    def _import_csv(self):
        path = filedialog.askopenfilename(
            title="Import CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not path:
            return
        try:
            self.ds.import_from_path(path)
            messagebox.showinfo("Imported", f"Records loaded from:\n{path}")
            self._refresh_current()
            self._update_live()
        except Exception as e:
            messagebox.showerror("Import Error", str(e))

    def _export_csv(self):
        path = filedialog.asksaveasfilename(
            title="Export CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        try:
            self.ds.export_to_path(path)
            messagebox.showinfo("Exported", f"Saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))


# ─────────────────────────────────────────────
#  BASE VIEW
# ─────────────────────────────────────────────

class BaseView(tk.Frame):
    def __init__(self, parent, ds, app):
        super().__init__(parent, bg=T["bg"])
        self.ds = ds
        self.app = app
        self._canvas_refs = []
        self.build()

    def build(self): pass
    def refresh(self): pass

    def _scrollable(self, parent):
        """Return (outer_frame, inner_frame) with vertical scrolling."""
        outer = tk.Frame(parent, bg=T["bg"])
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(0, weight=1)

        canvas = tk.Canvas(outer, bg=T["bg"], highlightthickness=0)
        sb = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)

        inner = tk.Frame(canvas, bg=T["bg"])
        win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        def on_resize(e):
            canvas.itemconfig(win_id, width=canvas.winfo_width())
        canvas.bind("<Configure>", on_resize)

        def on_frame_resize(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        inner.bind("<Configure>", on_frame_resize)

        def on_mousewheel(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        canvas.grid(row=0, column=0, sticky="nsew")
        sb.grid(row=0, column=1, sticky="ns")
        return outer, inner

    def _kpi_row(self, parent, cards_data):
        f = tk.Frame(parent, bg=T["bg"])
        f.pack(fill="x", padx=20, pady=(16, 0))
        for i, (title, val, sub, accent) in enumerate(cards_data):
            c = card(f, title, val, sub, accent)
            c.grid(row=0, column=i, sticky="ew", padx=(0, 10) if i < len(cards_data)-1 else 0)
            f.columnconfigure(i, weight=1)

    def _section(self, parent, title):
        f = tk.Frame(parent, bg=T["bg"], pady=8, padx=20)
        f.pack(fill="x")
        tk.Label(f, text=title, bg=T["bg"], fg=T["text"],
                 font=("Courier", 11, "bold")).pack(anchor="w")
        return f

    def _filter_row(self, parent, widgets_fn):
        f = tk.Frame(parent, bg=T["surface"], padx=16, pady=12)
        f.pack(fill="x", padx=20, pady=(0, 8))
        widgets_fn(f)
        return f

    def _embed_chart(self, fig, parent, fill="both", expand=True, padx=20, pady=8):
        wrapper = tk.Frame(parent, bg=T["bg"], padx=padx, pady=pady)
        wrapper.pack(fill=fill, expand=expand)
        canvas = FigureCanvasTkAgg(fig, master=wrapper)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill=fill, expand=expand)
        self._canvas_refs.append(canvas)
        return canvas


# ─────────────────────────────────────────────
#  OVERVIEW VIEW
# ─────────────────────────────────────────────

class OverviewView(BaseView):
    def build(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self._outer, self._inner = self._scrollable(self)
        self._outer.grid(row=0, column=0, sticky="nsew")
        self._outer.columnconfigure(0, weight=1)

        # ── header
        hdr = tk.Frame(self._inner, bg=T["bg"], pady=20, padx=20)
        hdr.pack(fill="x")
        tk.Label(hdr, text="Attendance Overview", bg=T["bg"], fg=T["text"],
                 font=("Courier", 16, "bold")).pack(side="left")
        styled_button(hdr, "+ Add Record", self.app._open_add_modal, T["accent"]).pack(side="right")
        styled_button(hdr, "↓ Export",     self.app._export_csv).pack(side="right", padx=8)

        # ── filters
        flt = tk.Frame(self._inner, bg=T["surface"], padx=16, pady=12)
        flt.pack(fill="x", padx=20, pady=(0, 8))
        self._build_filters(flt)

        # ── KPI cards placeholder
        self._kpi_frame = tk.Frame(self._inner, bg=T["bg"])
        self._kpi_frame.pack(fill="x", padx=20, pady=(8, 0))

        # ── chart row
        chart_row = tk.Frame(self._inner, bg=T["bg"])
        chart_row.pack(fill="x", padx=20, pady=10)
        chart_row.columnconfigure(0, weight=3)
        chart_row.columnconfigure(1, weight=2)
        self._daily_frame = tk.Frame(chart_row, bg=T["surface2"])
        self._daily_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self._donut_frame = tk.Frame(chart_row, bg=T["surface2"])
        self._donut_frame.grid(row=0, column=1, sticky="nsew")

        # ── dept chart
        dept_wrap = tk.Frame(self._inner, bg=T["bg"])
        dept_wrap.pack(fill="x", padx=20, pady=(0, 10))
        dept_wrap.columnconfigure(0, weight=1)
        dept_wrap.columnconfigure(1, weight=1)
        self._dept_frame = tk.Frame(dept_wrap, bg=T["surface2"])
        self._dept_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self._heatmap_frame = tk.Frame(dept_wrap, bg=T["surface2"])
        self._heatmap_frame.grid(row=0, column=1, sticky="nsew")

        # ── table
        tbl_sec = tk.Frame(self._inner, bg=T["bg"], padx=20, pady=0)
        tbl_sec.pack(fill="x")
        self._build_table(tbl_sec)

    def _build_filters(self, parent):
        # row 1
        r1 = tk.Frame(parent, bg=T["surface"])
        r1.pack(fill="x", pady=(0, 6))

        tk.Label(r1, text="SEARCH", bg=T["surface"], fg=T["text3"],
                 font=("Courier", 8, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 6))
        self._ov_search = entry(r1, width=22)
        self._ov_search.grid(row=1, column=0, padx=(0, 12))
        self._ov_search.bind("<KeyRelease>", lambda e: self.refresh())

        tk.Label(r1, text="DEPARTMENT", bg=T["surface"], fg=T["text3"],
                 font=("Courier", 8, "bold")).grid(row=0, column=1, sticky="w", padx=(0, 6))
        self._ov_dept = combobox(r1, values=["", "IT", "Commerce"], width=14)
        self._ov_dept.grid(row=1, column=1, padx=(0, 12))
        self._ov_dept.bind("<<ComboboxSelected>>", lambda e: self.refresh())

        tk.Label(r1, text="STATUS", bg=T["surface"], fg=T["text3"],
                 font=("Courier", 8, "bold")).grid(row=0, column=2, sticky="w", padx=(0, 6))
        self._ov_stat = combobox(r1, values=["", "Present", "Absent", "Late"], width=12)
        self._ov_stat.grid(row=1, column=2, padx=(0, 12))
        self._ov_stat.bind("<<ComboboxSelected>>", lambda e: self.refresh())

        tk.Label(r1, text="FROM (DD/MM/YYYY)", bg=T["surface"], fg=T["text3"],
                 font=("Courier", 8, "bold")).grid(row=0, column=3, sticky="w", padx=(0, 6))
        self._ov_from = entry(r1, width=13)
        self._ov_from.grid(row=1, column=3, padx=(0, 12))
        self._ov_from.bind("<FocusOut>", lambda e: self.refresh())

        tk.Label(r1, text="TO (DD/MM/YYYY)", bg=T["surface"], fg=T["text3"],
                 font=("Courier", 8, "bold")).grid(row=0, column=4, sticky="w", padx=(0, 6))
        self._ov_to = entry(r1, width=13)
        self._ov_to.grid(row=1, column=4, padx=(0, 12))
        self._ov_to.bind("<FocusOut>", lambda e: self.refresh())

        styled_button(r1, "Reset", self._reset_filters).grid(row=1, column=5, padx=(4, 0))

    def _reset_filters(self):
        self._ov_search.delete(0, "end")
        self._ov_dept.set("")
        self._ov_stat.set("")
        self._ov_from.delete(0, "end")
        self._ov_to.delete(0, "end")
        self.refresh()

    def _build_table(self, parent):
        hdr = tk.Frame(parent, bg=T["bg"])
        hdr.pack(fill="x", pady=(8, 4))
        self._rec_label = tk.Label(hdr, text="Records", bg=T["bg"], fg=T["text"],
                                   font=("Courier", 11, "bold"))
        self._rec_label.pack(side="left")

        self._quick_search = entry(hdr, width=20)
        self._quick_search.pack(side="right")
        self._quick_search.bind("<KeyRelease>", lambda e: self._apply_table())
        tk.Label(hdr, text="Quick search:", bg=T["bg"], fg=T["text3"],
                 font=("Courier", 9)).pack(side="right", padx=6)

        styled_button(hdr, "✕ Delete Selected",
                       self._delete_selected, T["red"]).pack(side="right", padx=8)

        cols = ["#", "StudentID", "Name", "Roll", "Department", "Date", "Time", "Status", "Rate%"]
        widths = [30, 80, 160, 50, 100, 90, 80, 75, 60]
        self._tree, tree_frame = build_treeview(parent, cols, widths)
        tree_frame.pack(fill="x", expand=False)

    def _get_filtered_df(self):
        q    = self._ov_search.get().strip()
        dept = self._ov_dept.get().strip()
        stat = self._ov_stat.get().strip()
        f    = self._ov_from.get().strip()
        t    = self._ov_to.get().strip()
        df_from = parse_date(f) if f else None
        df_to   = parse_date(t) if t else None
        return self.ds.filter(search=q, department=dept, status=stat,
                              date_from=df_from, date_to=df_to)

    def refresh(self):
        # update dept dropdown
        depts = [""] + self.ds.departments()
        self._ov_dept["values"] = depts

        df = self._get_filtered_df()
        self._update_kpi(df)
        self._update_charts(df)
        self._apply_table(df)
        self.app._update_live()

    def _update_kpi(self, df):
        for w in self._kpi_frame.winfo_children():
            w.destroy()
        total   = len(df)
        uniq    = df["StudentID"].nunique() if not df.empty else 0
        present = (df["Status"] == "Present").sum() if not df.empty else 0
        absent  = (df["Status"] == "Absent").sum()  if not df.empty else 0
        late    = (df["Status"] == "Late").sum()     if not df.empty else 0
        rate    = round((present + late) / total * 100, 1) if total else 0
        cards_data = [
            ("Students",      uniq,    f"{total} records", T["accent"]),
            ("Present",       present, f"{round(present/total*100,1) if total else 0}%", T["green"]),
            ("Absent",        absent,  f"{round(absent/total*100,1) if total else 0}%",  T["red"]),
            ("Late",          late,    f"{round(late/total*100,1) if total else 0}%",    T["amber"]),
            ("Att. Rate",     f"{rate}%", "Present+Late÷total",                          T["teal"]),
            ("Total Records", total,   f"{uniq} students",                               T["pink"]),
        ]
        for i, (title, val, sub, accent) in enumerate(cards_data):
            c = card(self._kpi_frame, title, val, sub, accent)
            c.grid(row=0, column=i, sticky="ew",
                   padx=(0, 8) if i < len(cards_data)-1 else 0)
            self._kpi_frame.columnconfigure(i, weight=1)

    def _update_charts(self, df):
        # clear
        for f in [self._daily_frame, self._donut_frame,
                  self._dept_frame, self._heatmap_frame]:
            for w in f.winfo_children():
                w.destroy()

        # ── daily bar chart
        if not df.empty:
            by_day = df.groupby(["_date", "Status"]).size().unstack(fill_value=0)
            for s in ["Present", "Absent", "Late"]:
                if s not in by_day.columns:
                    by_day[s] = 0
            by_day = by_day.sort_index()

            fig1 = make_figure(w=5.5, h=3)
            ax = fig1.add_subplot(111)
            x = range(len(by_day))
            labels = [d.strftime("%d/%m") for d in by_day.index]
            w = 0.28
            ax.bar([i - w for i in x], by_day["Present"], width=w,
                   color=T["green"], label="Present", alpha=0.85)
            ax.bar(x,                  by_day["Absent"],  width=w,
                   color=T["red"],   label="Absent",  alpha=0.85)
            ax.bar([i + w for i in x], by_day["Late"],    width=w,
                   color=T["amber"], label="Late",    alpha=0.85)
            ax.set_xticks(list(x)); ax.set_xticklabels(labels, rotation=30, ha="right")
            ax.yaxis.get_major_locator().set_params(integer=True)
            ax.set_title("Daily Attendance"); ax.legend(); ax.grid(axis="y")
            fig1.tight_layout(pad=1.2)
            FigureCanvasTkAgg(fig1, self._daily_frame).get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)

        # ── donut chart
        if not df.empty:
            counts = df["Status"].value_counts()
            fig2 = make_figure(w=3.2, h=3)
            ax2 = fig2.add_subplot(111)
            wedge_colors = [STATUS_COLORS.get(s, T["text3"]) for s in counts.index]
            wedges, texts, autotexts = ax2.pie(
                counts.values, labels=counts.index,
                colors=wedge_colors,
                autopct="%1.0f%%", startangle=90,
                wedgeprops=dict(width=0.55, edgecolor=T["surface"]),
                textprops=dict(color=T["text2"], fontsize=8))
            for at in autotexts:
                at.set_color(T["text"]); at.set_fontsize(8)
            ax2.set_title("Status Breakdown")
            fig2.tight_layout(pad=1.2)
            FigureCanvasTkAgg(fig2, self._donut_frame).get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)

        # ── dept bar
        if not df.empty:
            depts = df["Department"].unique()
            dept_rates = []
            for dep in depts:
                sub = df[df["Department"] == dep]
                p = sub[sub["Status"].isin(["Present", "Late"])].shape[0]
                dept_rates.append(round(p / len(sub) * 100, 1))
            fig3 = make_figure(w=4.5, h=3)
            ax3 = fig3.add_subplot(111)
            cols_used = [DEPT_COLORS[i % len(DEPT_COLORS)] for i in range(len(depts))]
            bars = ax3.barh(list(depts), dept_rates, color=cols_used, alpha=0.85, height=0.5)
            ax3.set_xlim(0, 110)
            ax3.set_title("Dept Attendance %")
            for bar, val in zip(bars, dept_rates):
                ax3.text(val + 1, bar.get_y() + bar.get_height()/2,
                         f"{val}%", va="center", fontsize=8, color=T["text2"])
            ax3.grid(axis="x"); fig3.tight_layout(pad=1.2)
            FigureCanvasTkAgg(fig3, self._dept_frame).get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)

        # ── records per day heatmap (grid)
        if not df.empty:
            day_counts = df.groupby("_date").size().to_dict()
            fig4 = make_figure(w=4.5, h=3)
            ax4 = fig4.add_subplot(111)
            sorted_dates = sorted(day_counts.keys())
            vals = [day_counts[d] for d in sorted_dates]
            xlabels = [d.strftime("%d/%m") for d in sorted_dates]
            cmap_colors = [T["accent"]] * len(vals)
            max_v = max(vals) if vals else 1
            alphas = [0.2 + 0.8 * (v / max_v) for v in vals]
            bars2 = ax4.bar(xlabels, vals, color=[T["accent"]], alpha=0.7)
            for bar, alpha in zip(bars2, alphas):
                bar.set_alpha(alpha)
            ax4.set_title("Records Per Day")
            ax4.yaxis.get_major_locator().set_params(integer=True)
            ax4.grid(axis="y"); fig4.tight_layout(pad=1.2)
            FigureCanvasTkAgg(fig4, self._heatmap_frame).get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)

    def _apply_table(self, df=None):
        if df is None:
            df = self._get_filtered_df()
        q = self._quick_search.get().strip().lower()
        if q:
            mask = (df["Name"].str.lower().str.contains(q, na=False) |
                    df["Department"].str.lower().str.contains(q, na=False))
            df = df[mask]

        stats = self.ds.student_stats()
        rate_map = dict(zip(stats["StudentID"], stats["Rate"]))

        self._tree.delete(*self._tree.get_children())
        for i, (_, row) in enumerate(df.iterrows()):
            rate = rate_map.get(row["StudentID"], 0)
            tag = "even" if i % 2 == 0 else "odd"
            st_tag = row["Status"].lower() if row["Status"] in ["Present", "Absent", "Late"] else ""
            self._tree.insert("", "end",
                              values=(i+1, row["StudentID"], row["Name"], row["Roll"],
                                      row["Department"], row["Date"], row["Time"],
                                      row["Status"], f"{rate}%"),
                              tags=(tag, st_tag))
        self._rec_label.config(text=f"Records  [{len(df)}]")

    def _delete_selected(self):
        selected = self._tree.selection()
        if not selected:
            messagebox.showwarning("Nothing selected", "Select rows to delete.")
            return
        if not messagebox.askyesno("Confirm", f"Delete {len(selected)} record(s)?"):
            return
        indices_to_delete = []
        df = self._get_filtered_df()
        for item in selected:
            idx = int(self._tree.item(item)["values"][0]) - 1
            if idx < len(df):
                name  = df.iloc[idx]["Name"]
                date_ = df.iloc[idx]["Date"]
                for j, r in enumerate(self.ds.records):
                    if r["Name"] == name and r["Date"] == date_:
                        indices_to_delete.append(j)
                        break
        self.ds.delete_by_indices(set(indices_to_delete))
        self.refresh()


# ─────────────────────────────────────────────
#  DEPARTMENT VIEW
# ─────────────────────────────────────────────

class DepartmentView(BaseView):
    def build(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self._outer, self._inner = self._scrollable(self)
        self._outer.grid(row=0, column=0, sticky="nsew")
        self._outer.columnconfigure(0, weight=1)

        hdr = tk.Frame(self._inner, bg=T["bg"], pady=20, padx=20)
        hdr.pack(fill="x")
        tk.Label(hdr, text="Department Breakdown", bg=T["bg"], fg=T["text"],
                 font=("Courier", 16, "bold")).pack(side="left")

        self._cards_frame = tk.Frame(self._inner, bg=T["bg"])
        self._cards_frame.pack(fill="x", padx=20, pady=(0, 10))

        self._grouped_frame = tk.Frame(self._inner, bg=T["surface2"])
        self._grouped_frame.pack(fill="x", padx=20, pady=(0, 10))

        performers_lbl = tk.Frame(self._inner, bg=T["bg"], padx=20, pady=4)
        performers_lbl.pack(fill="x")
        tk.Label(performers_lbl, text="Top Performing Students", bg=T["bg"], fg=T["text"],
                 font=("Courier", 11, "bold")).pack(anchor="w")

        self._perf_frame = tk.Frame(self._inner, bg=T["surface"])
        self._perf_frame.pack(fill="x", padx=20, pady=(0, 20))

    def refresh(self):
        self._render_dept_cards()
        self._render_grouped_chart()
        self._render_top_performers()

    def _render_dept_cards(self):
        for w in self._cards_frame.winfo_children():
            w.destroy()
        depts = self.ds.departments()
        for i, dep in enumerate(depts):
            recs = [r for r in self.ds.records if r["Department"] == dep]
            students = len(set(r["StudentID"] for r in recs))
            present  = sum(1 for r in recs if r["Status"] in ["Present", "Late"])
            absent   = sum(1 for r in recs if r["Status"] == "Absent")
            dates    = set(r["Date"] for r in recs)
            avg_day  = round(sum(1 for r in recs if r["Status"] == "Present") / max(len(dates), 1), 1)
            rate     = round(present / max(len(recs), 1) * 100, 1)
            col      = DEPT_COLORS[i % len(DEPT_COLORS)]

            f = tk.Frame(self._cards_frame, bg=T["surface2"], padx=14, pady=12)
            f.grid(row=0, column=i, sticky="ew",
                   padx=(0, 10) if i < len(depts)-1 else 0)
            self._cards_frame.columnconfigure(i, weight=1)

            tk.Frame(f, bg=col, height=3).pack(fill="x")
            hdr_f = tk.Frame(f, bg=T["surface2"])
            hdr_f.pack(fill="x", pady=(8, 0))
            tk.Label(hdr_f, text=dep, bg=T["surface2"], fg=T["text"],
                     font=("Courier", 13, "bold")).pack(side="left")
            tk.Label(hdr_f, text=f"{rate}%", bg=T["surface2"], fg=col,
                     font=("Courier", 18, "bold")).pack(side="right")

            stats_f = tk.Frame(f, bg=T["surface2"])
            stats_f.pack(fill="x", pady=8)
            for j, (lbl, val, fc) in enumerate([
                ("STUDENTS", students, T["text"]),
                ("PRESENT",  present,  T["green"]),
                ("ABSENT",   absent,   T["red"]),
                ("AVG/DAY",  avg_day,  col),
            ]):
                c = tk.Frame(stats_f, bg=T["surface2"])
                c.grid(row=0, column=j, sticky="ew")
                stats_f.columnconfigure(j, weight=1)
                tk.Label(c, text=lbl, bg=T["surface2"], fg=T["text3"],
                         font=("Courier", 7, "bold")).pack()
                tk.Label(c, text=str(val), bg=T["surface2"], fg=fc,
                         font=("Courier", 14, "bold")).pack()

            # rate bar
            bar_bg = tk.Frame(f, bg=T["surface3"], height=5)
            bar_bg.pack(fill="x")
            bar_bg.update_idletasks()
            w_total = bar_bg.winfo_width() or 200
            fill_w = max(1, int(w_total * rate / 100))
            tk.Frame(bar_bg, bg=col, height=5, width=fill_w).place(x=0, y=0)

    def _render_grouped_chart(self):
        for w in self._grouped_frame.winfo_children():
            w.destroy()
        df = self.ds.to_df()
        if df.empty:
            return
        depts  = self.ds.departments()
        dates  = sorted(df["_date"].dropna().unique())
        date_labels = [d.strftime("%d/%m/%y") for d in dates]

        fig = make_figure(w=9, h=3.4)
        ax = fig.add_subplot(111)
        n = len(depts)
        width = 0.7 / max(n, 1)

        for i, dep in enumerate(depts):
            vals = []
            for d in dates:
                cnt = df[(df["Department"] == dep) & (df["_date"] == d) &
                         (df["Status"] == "Present")].shape[0]
                vals.append(cnt)
            offset = (i - n / 2 + 0.5) * width
            x = [j + offset for j in range(len(dates))]
            ax.bar(x, vals, width=width * 0.9,
                   color=DEPT_COLORS[i % len(DEPT_COLORS)],
                   label=dep, alpha=0.85)

        ax.set_xticks(range(len(dates)))
        ax.set_xticklabels(date_labels, rotation=30, ha="right")
        ax.yaxis.get_major_locator().set_params(integer=True)
        ax.set_title("Students Present per Department per Day")
        ax.legend(); ax.grid(axis="y")
        fig.tight_layout(pad=1.2)
        FigureCanvasTkAgg(fig, self._grouped_frame).get_tk_widget().pack(
            fill="both", expand=True, padx=8, pady=8)

    def _render_top_performers(self):
        for w in self._perf_frame.winfo_children():
            w.destroy()
        stats = self.ds.student_stats().sort_values("Rate", ascending=False)
        for i, (_, row) in enumerate(stats.iterrows()):
            col = DEPT_COLORS[i % len(DEPT_COLORS)]
            f = tk.Frame(self._perf_frame, bg=T["surface"], pady=8, padx=16)
            f.pack(fill="x")
            if i > 0:
                tk.Frame(self._perf_frame, bg=T["border"], height=1).pack(fill="x")

            # rank
            tk.Label(f, text=f"#{i+1}", bg=T["surface"], fg=T["text3"],
                     font=("Courier", 10, "bold"), width=3).pack(side="left")
            # avatar circle (canvas)
            av = tk.Canvas(f, width=32, height=32, bg=T["surface"],
                           highlightthickness=0)
            av.pack(side="left", padx=8)
            av.create_oval(2, 2, 30, 30, fill=col + "33", outline=col, width=1)
            initials = "".join(w[0].upper() for w in str(row["Name"]).split()[:2])
            av.create_text(16, 16, text=initials, fill=col, font=("Courier", 9, "bold"))

            info = tk.Frame(f, bg=T["surface"])
            info.pack(side="left", fill="x", expand=True)
            tk.Label(info, text=row["Name"].title(), bg=T["surface"], fg=T["text"],
                     font=("Courier", 10, "bold"), anchor="w").pack(anchor="w")
            tk.Label(info, text=f"{row['Department']}  ·  Roll {row['Roll']}  ·  {row['Total']} records",
                     bg=T["surface"], fg=T["text3"], font=("Courier", 8), anchor="w").pack(anchor="w")

            rate_col = T["green"] if row["Rate"] >= 80 else T["amber"] if row["Rate"] >= 60 else T["red"]
            tk.Label(f, text=f"{row['Rate']}%", bg=T["surface"], fg=rate_col,
                     font=("Courier", 14, "bold")).pack(side="right")


# ─────────────────────────────────────────────
#  STUDENTS VIEW
# ─────────────────────────────────────────────

class StudentsView(BaseView):
    def build(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self._outer, self._inner = self._scrollable(self)
        self._outer.grid(row=0, column=0, sticky="nsew")
        self._outer.columnconfigure(0, weight=1)

        hdr = tk.Frame(self._inner, bg=T["bg"], pady=20, padx=20)
        hdr.pack(fill="x")
        tk.Label(hdr, text="Student Profiles", bg=T["bg"], fg=T["text"],
                 font=("Courier", 16, "bold")).pack(side="left")

        flt = tk.Frame(self._inner, bg=T["surface"], padx=16, pady=12)
        flt.pack(fill="x", padx=20, pady=(0, 8))
        self._build_filters(flt)

        self._cards_frame = tk.Frame(self._inner, bg=T["bg"])
        self._cards_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def _build_filters(self, parent):
        r = tk.Frame(parent, bg=T["surface"])
        r.pack(fill="x")

        tk.Label(r, text="SEARCH", bg=T["surface"], fg=T["text3"],
                 font=("Courier", 8, "bold")).grid(row=0, column=0, sticky="w")
        self._st_search = entry(r, width=22)
        self._st_search.grid(row=1, column=0, padx=(0, 12))
        self._st_search.bind("<KeyRelease>", lambda e: self.refresh())

        tk.Label(r, text="DEPARTMENT", bg=T["surface"], fg=T["text3"],
                 font=("Courier", 8, "bold")).grid(row=0, column=1, sticky="w")
        self._st_dept = combobox(r, values=[""], width=14)
        self._st_dept.grid(row=1, column=1, padx=(0, 12))
        self._st_dept.bind("<<ComboboxSelected>>", lambda e: self.refresh())

        tk.Label(r, text="SORT BY", bg=T["surface"], fg=T["text3"],
                 font=("Courier", 8, "bold")).grid(row=0, column=2, sticky="w")
        self._st_sort = combobox(r, values=["Rate ↓", "Rate ↑", "Name A-Z", "Most Records"], width=16)
        self._st_sort.set("Rate ↓")
        self._st_sort.grid(row=1, column=2, padx=(0, 12))
        self._st_sort.bind("<<ComboboxSelected>>", lambda e: self.refresh())

        styled_button(r, "Reset", self._reset).grid(row=1, column=3)

    def _reset(self):
        self._st_search.delete(0, "end")
        self._st_dept.set("")
        self._st_sort.set("Rate ↓")
        self.refresh()

    def refresh(self):
        self._st_dept["values"] = [""] + self.ds.departments()
        for w in self._cards_frame.winfo_children():
            w.destroy()

        stats = self.ds.student_stats()
        q    = self._st_search.get().strip().lower()
        dept = self._st_dept.get().strip()
        sort = self._st_sort.get()

        if q:
            stats = stats[stats["Name"].str.lower().str.contains(q, na=False) |
                          stats["Department"].str.lower().str.contains(q, na=False)]
        if dept:
            stats = stats[stats["Department"] == dept]

        if sort == "Rate ↑":
            stats = stats.sort_values("Rate")
        elif sort == "Name A-Z":
            stats = stats.sort_values("Name")
        elif sort == "Most Records":
            stats = stats.sort_values("Total", ascending=False)
        else:
            stats = stats.sort_values("Rate", ascending=False)

        if stats.empty:
            tk.Label(self._cards_frame, text="No students found.",
                     bg=T["bg"], fg=T["text3"], font=("Courier", 11)).pack(pady=40)
            return

        # grid layout — 3 columns
        for i, (_, row) in enumerate(stats.iterrows()):
            col_idx = i % 3
            row_idx = i // 3
            self._cards_frame.columnconfigure(col_idx, weight=1)

            col    = DEPT_COLORS[i % len(DEPT_COLORS)]
            rate   = row["Rate"]
            rc_col = T["green"] if rate >= 80 else T["amber"] if rate >= 60 else T["red"]

            f = tk.Frame(self._cards_frame, bg=T["surface2"], padx=14, pady=12)
            f.grid(row=row_idx, column=col_idx, sticky="ew",
                   padx=(0, 10) if col_idx < 2 else 0,
                   pady=(0, 10))

            # avatar + name
            top = tk.Frame(f, bg=T["surface2"])
            top.pack(fill="x", pady=(0, 8))
            av = tk.Canvas(top, width=40, height=40, bg=T["surface2"],
                           highlightthickness=0)
            av.pack(side="left", padx=(0, 10))
            av.create_oval(2, 2, 38, 38, fill=col + "22", outline=col, width=1)
            initials = "".join(w[0].upper() for w in str(row["Name"]).split()[:2])
            av.create_text(20, 20, text=initials, fill=col, font=("Courier", 11, "bold"))

            info = tk.Frame(top, bg=T["surface2"])
            info.pack(side="left", fill="x", expand=True)
            tk.Label(info, text=row["Name"].title(), bg=T["surface2"], fg=T["text"],
                     font=("Courier", 10, "bold"), anchor="w").pack(anchor="w")
            tk.Label(info, text=f"{row['Department']}  ·  Roll {row['Roll']}",
                     bg=T["surface2"], fg=T["text3"], font=("Courier", 8), anchor="w").pack(anchor="w")

            tk.Label(top, text=f"{rate}%", bg=T["surface2"], fg=rc_col,
                     font=("Courier", 16, "bold")).pack(side="right")

            # stats
            stats_f = tk.Frame(f, bg=T["surface2"])
            stats_f.pack(fill="x", pady=(0, 8))
            for j, (lbl, val, fc) in enumerate([
                ("TOTAL",   row["Total"],   T["text"]),
                ("PRESENT", row["Present"], T["green"]),
                ("ABSENT",  row["Absent"],  T["red"]),
            ]):
                c = tk.Frame(stats_f, bg=T["surface2"])
                c.grid(row=0, column=j, sticky="ew")
                stats_f.columnconfigure(j, weight=1)
                tk.Label(c, text=lbl, bg=T["surface2"], fg=T["text3"],
                         font=("Courier", 7, "bold")).pack()
                tk.Label(c, text=str(val), bg=T["surface2"], fg=fc,
                         font=("Courier", 13, "bold")).pack()

            # rate bar
            bar_bg = tk.Frame(f, bg=T["surface3"], height=4)
            bar_bg.pack(fill="x")
            bar_bg.update_idletasks()
            tw = bar_bg.winfo_width() or 180
            tk.Frame(bar_bg, bg=rc_col, height=4,
                     width=max(1, int(tw * rate / 100))).place(x=0, y=0)


# ─────────────────────────────────────────────
#  ALL RECORDS VIEW
# ─────────────────────────────────────────────

class RecordsView(BaseView):
    def build(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        hdr = tk.Frame(self, bg=T["bg"], pady=18, padx=20)
        hdr.grid(row=0, column=0, sticky="ew")
        tk.Label(hdr, text="All Records", bg=T["bg"], fg=T["text"],
                 font=("Courier", 16, "bold")).pack(side="left")
        styled_button(hdr, "✕ Delete Selected", self._delete_selected, T["red"]).pack(side="right")
        styled_button(hdr, "↓ Export", self.app._export_csv).pack(side="right", padx=8)
        styled_button(hdr, "+ Add Record", self.app._open_add_modal, T["accent"]).pack(side="right", padx=8)

        # filters
        flt = tk.Frame(self, bg=T["surface"], padx=16, pady=12)
        flt.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 8))
        self._build_filters(flt)
        self.rowconfigure(1, weight=0)

        # table
        tbl_wrap = tk.Frame(self, bg=T["bg"])
        tbl_wrap.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        tbl_wrap.columnconfigure(0, weight=1)
        tbl_wrap.rowconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self._count_lbl = tk.Label(tbl_wrap, text="Records [0]",
                                   bg=T["bg"], fg=T["text"],
                                   font=("Courier", 11, "bold"), anchor="w")
        self._count_lbl.grid(row=0, column=0, sticky="w", pady=(0, 6))

        cols   = ["#", "StudentID", "Name", "Roll", "Department", "Date", "Time", "Status"]
        widths = [30, 80, 180, 50, 110, 90, 80, 80]
        self._tree, tree_frame = build_treeview(tbl_wrap, cols, widths)
        tree_frame.grid(row=1, column=0, sticky="nsew")
        tbl_wrap.rowconfigure(1, weight=1)

    def _build_filters(self, parent):
        r = tk.Frame(parent, bg=T["surface"])
        r.pack(fill="x")

        tk.Label(r, text="SEARCH", bg=T["surface"], fg=T["text3"],
                 font=("Courier", 8, "bold")).grid(row=0, column=0, sticky="w")
        self._rc_q = entry(r, width=22)
        self._rc_q.grid(row=1, column=0, padx=(0, 12))
        self._rc_q.bind("<KeyRelease>", lambda e: self.refresh())

        tk.Label(r, text="DEPARTMENT", bg=T["surface"], fg=T["text3"],
                 font=("Courier", 8, "bold")).grid(row=0, column=1, sticky="w")
        self._rc_dept = combobox(r, values=[""], width=14)
        self._rc_dept.grid(row=1, column=1, padx=(0, 12))
        self._rc_dept.bind("<<ComboboxSelected>>", lambda e: self.refresh())

        tk.Label(r, text="STATUS", bg=T["surface"], fg=T["text3"],
                 font=("Courier", 8, "bold")).grid(row=0, column=2, sticky="w")
        self._rc_stat = combobox(r, values=["", "Present", "Absent", "Late"], width=12)
        self._rc_stat.grid(row=1, column=2, padx=(0, 12))
        self._rc_stat.bind("<<ComboboxSelected>>", lambda e: self.refresh())

        tk.Label(r, text="FROM", bg=T["surface"], fg=T["text3"],
                 font=("Courier", 8, "bold")).grid(row=0, column=3, sticky="w")
        self._rc_from = entry(r, width=12)
        self._rc_from.grid(row=1, column=3, padx=(0, 12))
        self._rc_from.bind("<FocusOut>", lambda e: self.refresh())

        tk.Label(r, text="TO", bg=T["surface"], fg=T["text3"],
                 font=("Courier", 8, "bold")).grid(row=0, column=4, sticky="w")
        self._rc_to = entry(r, width=12)
        self._rc_to.grid(row=1, column=4, padx=(0, 12))
        self._rc_to.bind("<FocusOut>", lambda e: self.refresh())

        styled_button(r, "Reset", self._reset).grid(row=1, column=5)

    def _reset(self):
        self._rc_q.delete(0, "end")
        self._rc_dept.set("")
        self._rc_stat.set("")
        self._rc_from.delete(0, "end")
        self._rc_to.delete(0, "end")
        self.refresh()

    def refresh(self):
        self._rc_dept["values"] = [""] + self.ds.departments()
        q    = self._rc_q.get().strip()
        dept = self._rc_dept.get().strip()
        stat = self._rc_stat.get().strip()
        f    = self._rc_from.get().strip()
        t    = self._rc_to.get().strip()
        df   = self.ds.filter(search=q, department=dept, status=stat,
                              date_from=parse_date(f) if f else None,
                              date_to=parse_date(t) if t else None)

        self._tree.delete(*self._tree.get_children())
        for i, (_, row) in enumerate(df.iterrows()):
            tag    = "even" if i % 2 == 0 else "odd"
            st_tag = row["Status"].lower() if row["Status"] in ["Present", "Absent", "Late"] else ""
            self._tree.insert("", "end",
                              values=(i+1, row["StudentID"], row["Name"], row["Roll"],
                                      row["Department"], row["Date"], row["Time"], row["Status"]),
                              tags=(tag, st_tag))
        self._count_lbl.config(text=f"Records  [{len(df)}]")

    def _delete_selected(self):
        selected = self._tree.selection()
        if not selected:
            messagebox.showwarning("Nothing selected", "Select rows first.")
            return
        if not messagebox.askyesno("Confirm", f"Delete {len(selected)} record(s)?"):
            return
        names_dates = []
        for item in selected:
            vals = self._tree.item(item)["values"]
            names_dates.append((str(vals[2]), str(vals[5])))
        to_del = []
        for i, r in enumerate(self.ds.records):
            if (r["Name"], r["Date"]) in names_dates:
                to_del.append(i)
        self.ds.delete_by_indices(set(to_del))
        self.refresh()


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    app = AttendIQ()
    app.mainloop()