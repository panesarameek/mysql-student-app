# Student Management System

A desktop app I built with Python and Tkinter to replace paper registration forms. Student details are entered in a form, saved to a MySQL database, and can be viewed in a table or exported to CSV for Excel.

## What it does

- **Registration form** with fields for name, email, mobile, age, course, address and status (Active / Inactive)
- **Input checks** when you click Save:
  - name is required
  - email must look like a real email address
  - mobile must be exactly 10 digits
  - age must be a number
  - a clear error message shows under the form if something is wrong
- **Duplicate check:** the database stops the same email or mobile number being saved twice, and the app shows a message
- **Manage Students window** with a scrollable table of all saved records, a record count, and a Refresh button
- **Export to CSV** button that saves all records with pandas, so the file opens directly in Excel

## Built with

Python, Tkinter, MySQL (`mysql-connector-python`), pandas

## How to run it

1. Install the packages:
   ```
   pip install mysql-connector-python pandas
   ```
2. Open `schema.sql` in MySQL Workbench and run it. This creates the `Student` database and the `students` table.
3. Set your MySQL password as an environment variable so it is not stored in the code. On Windows, run this in Command Prompt, then reopen it:
   ```
   setx DB_PASSWORD "your_mysql_password"
   ```
4. Start the app:
   ```
   python student_management.py
   ```

## What it does not do yet

- Records can be added and viewed, but not edited or deleted from the app.
- Validation runs when you press Save, not while typing.

Ameek Singh Panesar
