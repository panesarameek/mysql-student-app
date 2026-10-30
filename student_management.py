import os
import pandas as pd
import re
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "os.environ.get("DB_PASSWORD", "")",
    "database": "Student"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def validate_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def validate_mobile(mobile):
    return re.match(r'^\d{10}$', mobile)

class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1050x680")
        self.root.configure(bg="#0D1B2A")
        self.root.resizable(True, True)
        self.BG = "#0D1B2A"
        self.PANEL = "#132338"
        self.ACCENT = "#00C9A7"
        self.ACCENT2 = "#0077B6"
        self.TEXT = "#E8F1F2"
        self.MUTED = "#8899A6"
        self.ENTRY_BG = "#1A2E44"
        self.ERR = "#FF6B6B"
        self.build_ui()

    def build_ui(self):
        left = Frame(self.root, bg=self.PANEL, width=400)
        left.pack(side=LEFT, fill=Y, padx=(18, 0), pady=18)
        left.pack_propagate(False)

        Label(left, text="STUDENT FORM",
              font=("Courier New", 17, "bold"),
              bg=self.PANEL, fg=self.ACCENT).pack(pady=(28, 4))
        Label(left, text="Fill in details and save to database",
              font=("Helvetica", 9), bg=self.PANEL, fg=self.MUTED).pack(pady=(0, 22))

        self.entries = {}
        fields = [
            ("Student Name", "student_name"),
            ("Email", "email"),
            ("Mobile (10 digits)", "mobile"),
            ("Age", "age"),
            ("Course", "course"),
            ("Address", "address"),
        ]
        for label, key in fields:
            self._field(left, label, key)

        Label(left, text="Status", font=("Helvetica", 10, "bold"),
              bg=self.PANEL, fg=self.TEXT).pack(anchor=W, padx=30, pady=(10, 2))
        self.status_var = StringVar(value="Active")
        status_dd = ttk.Combobox(left, textvariable=self.status_var,
                                  values=["Active", "Inactive"],
                                  state="readonly", width=34,
                                  font=("Helvetica", 10))
        status_dd.pack(padx=30, pady=(0, 16))

        self.err_label = Label(left, text="", font=("Helvetica", 9),
                               bg=self.PANEL, fg=self.ERR, wraplength=330)
        self.err_label.pack(pady=(0, 6))

        Button(left, text="SAVE RECORD", command=self.save_record,
               font=("Helvetica", 10, "bold"),
               bg=self.ACCENT, fg="#0D1B2A",
               relief=FLAT, bd=0, cursor="hand2",
               pady=9).pack(padx=30, fill=X, pady=(4, 6))

        Button(left, text="MANAGE STUDENTS", command=self.open_manage,
               font=("Helvetica", 10, "bold"),
               bg=self.ACCENT2, fg=self.TEXT,
               relief=FLAT, bd=0, cursor="hand2",
               pady=9).pack(padx=30, fill=X, pady=(0, 24))

        right = Frame(self.root, bg=self.BG)
        right.pack(side=LEFT, fill=BOTH, expand=True, padx=18, pady=18)

        Label(right, text="Student Management System",
              font=("Courier New", 22, "bold"),
              bg=self.BG, fg=self.ACCENT, justify=CENTER).pack(pady=(80, 8))
        Label(right, text="Python  |  MySQL  |  Excel CSV",
              font=("Helvetica", 10), bg=self.BG, fg=self.MUTED).pack()

        self.status_bar = Label(right, text="Ready",
                                font=("Helvetica", 9), bg=self.BG, fg=self.MUTED)
        self.status_bar.pack(side=BOTTOM, pady=8)

    def _field(self, parent, label, key):
        Label(parent, text=label, font=("Helvetica", 10, "bold"),
              bg=self.PANEL, fg=self.TEXT).pack(anchor=W, padx=30, pady=(8, 2))
        e = Entry(parent, font=("Helvetica", 10), width=36,
                  bg=self.ENTRY_BG, fg=self.TEXT,
                  insertbackground=self.ACCENT,
                  relief=FLAT, bd=0, highlightthickness=1,
                  highlightbackground=self.MUTED,
                  highlightcolor=self.ACCENT)
        e.pack(padx=30, ipady=5, pady=(0, 2))
        self.entries[key] = e

    def set_status(self, msg, colour=None):
        self.status_bar.config(text=msg, fg=colour or self.MUTED)

    def save_record(self):
        self.err_label.config(text="")
        data = {k: e.get().strip() for k, e in self.entries.items()}
        data["status"] = self.status_var.get()

        if not data["student_name"]:
            self.err_label.config(text="Student name is required.")
            return
        if not validate_email(data["email"]):
            self.err_label.config(text="Enter a valid email address.")
            return
        if not validate_mobile(data["mobile"]):
            self.err_label.config(text="Mobile must be exactly 10 digits.")
            return
        if not data["age"].isdigit():
            self.err_label.config(text="Age must be a number.")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            sql = """INSERT INTO students
                     (student_name, email, mobile, age, course, address, status)
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (
                data["student_name"], data["email"],
                data["mobile"], int(data["age"]),
                data["course"], data["address"],
                data["status"]
            ))
            conn.commit()
            conn.close()
            self.set_status("Record saved successfully!", self.ACCENT)
            messagebox.showinfo("Saved", "Student saved successfully!")
            for e in self.entries.values():
                e.delete(0, END)
            self.status_var.set("Active")
        except mysql.connector.IntegrityError as ie:
            msg = str(ie)
            if "email" in msg:
                self.err_label.config(text="This email is already registered.")
            elif "mobile" in msg:
                self.err_label.config(text="This mobile number is already registered.")
            else:
                self.err_label.config(text=str(ie))
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def open_manage(self):
        win = Toplevel(self.root)
        win.title("Manage Students")
        win.geometry("1020x560")
        win.configure(bg=self.BG)

        hdr = Frame(win, bg=self.PANEL)
        hdr.pack(fill=X)
        Label(hdr, text="All Students", font=("Courier New", 14, "bold"),
              bg=self.PANEL, fg=self.ACCENT).pack(side=LEFT, padx=20, pady=12)
        Button(hdr, text="Export to CSV",
               command=self.export_csv,
               font=("Helvetica", 10, "bold"),
               bg=self.ACCENT, fg="#0D1B2A",
               relief=FLAT, padx=14, pady=6,
               cursor="hand2").pack(side=RIGHT, padx=16, pady=10)
        Button(hdr, text="Refresh",
               command=lambda: self.load_table(tree),
               font=("Helvetica", 10),
               bg=self.ENTRY_BG, fg=self.TEXT,
               relief=FLAT, padx=10, pady=6,
               cursor="hand2").pack(side=RIGHT, padx=4, pady=10)

        cols = ("ID", "Name", "Email", "Mobile", "Age", "Course", "Address", "Status", "Created At")

        frame = Frame(win, bg=self.BG)
        frame.pack(fill=BOTH, expand=True, padx=16, pady=12)

        xscroll = Scrollbar(frame, orient=HORIZONTAL)
        yscroll = Scrollbar(frame, orient=VERTICAL)
        tree = ttk.Treeview(frame, columns=cols, show="headings",
                             xscrollcommand=xscroll.set,
                             yscrollcommand=yscroll.set)
        xscroll.config(command=tree.xview)
        yscroll.config(command=tree.yview)
        xscroll.pack(side=BOTTOM, fill=X)
        yscroll.pack(side=RIGHT, fill=Y)
        tree.pack(fill=BOTH, expand=True)

        widths = [50, 140, 180, 100, 50, 120, 180, 80, 140]
        for col, w in zip(cols, widths):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor=CENTER)

        self.tree = tree
        self.load_table(tree)

        self.count_label = Label(win, text="",
                                  font=("Helvetica", 9),
                                  bg=self.BG, fg=self.MUTED)
        self.count_label.pack(pady=(0, 6))

    def load_table(self, tree):
        for row in tree.get_children():
            tree.delete(row)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT student_id, student_name, email, mobile, age, course, address, status, created_at FROM students")
            rows = cursor.fetchall()
            conn.close()
            for row in rows:
                tree.insert("", END, values=row)
            if hasattr(self, "count_label"):
                self.count_label.config(text="Total records: " + str(len(rows)))
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def export_csv(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save Student Data as CSV"
        )
        if not path:
            return
        try:
            conn = get_connection()
            df = pd.read_sql("SELECT student_id, student_name, email, mobile, age, course, address, status, created_at FROM students", conn)
            conn.close()
            df.to_csv(path, index=False)
            messagebox.showinfo("Exported", "File saved! Open it in Excel.")
            self.set_status("Exported successfully!", self.ACCENT)
        except Exception as ex:
            messagebox.showerror("Export Error", str(ex))


if __name__ == "__main__":
    root = Tk()
    app = StudentApp(root)
    root.mainloop()
