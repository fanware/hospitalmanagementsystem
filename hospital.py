import sqlite3
from tkinter import *
from tkinter import messagebox, ttk

# Database setup
conn = sqlite3.connect("hospital_management.db")
cursor = conn.cursor()

# Creating tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        address TEXT,
        phone TEXT,
        admission_date TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialty TEXT NOT NULL,
        phone TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS pharmacy (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        drug_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS wards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ward_number TEXT NOT NULL,
        capacity INTEGER NOT NULL,
        occupied INTEGER DEFAULT 0
    )
''')

conn.commit()

# Tkinter setup
root = Tk()
root.title("Hospital Management System")
root.geometry("800x600")

# Notebook for sections
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Frames for each section
frame_patient = Frame(notebook, width=800, height=500)
frame_doctor = Frame(notebook, width=800, height=500)
frame_pharmacy = Frame(notebook, width=800, height=500)
frame_ward = Frame(notebook, width=800, height=500)

frame_patient.pack(fill="both", expand=1)
frame_doctor.pack(fill="both", expand=1)
frame_pharmacy.pack(fill="both", expand=1)
frame_ward.pack(fill="both", expand=1)

notebook.add(frame_patient, text="Patient Management")
notebook.add(frame_doctor, text="Doctor Management")
notebook.add(frame_pharmacy, text="Pharmacy Management")
notebook.add(frame_ward, text="Ward Management")

# Patient Management Functions
def add_patient():
    name = entry_patient_name.get()
    age = entry_patient_age.get()
    gender = entry_patient_gender.get()
    address = entry_patient_address.get()
    phone = entry_patient_phone.get()
    admission_date = entry_patient_admission.get()

    cursor.execute("INSERT INTO patients (name, age, gender, address, phone, admission_date) VALUES (?, ?, ?, ?, ?, ?)",
                   (name, age, gender, address, phone, admission_date))
    conn.commit()
    messagebox.showinfo("Success", "Patient added successfully!")
    clear_patient_entries()

def clear_patient_entries():
    entry_patient_name.delete(0, END)
    entry_patient_age.delete(0, END)
    entry_patient_gender.delete(0, END)
    entry_patient_address.delete(0, END)
    entry_patient_phone.delete(0, END)
    entry_patient_admission.delete(0, END)

def search_patient():
    name = entry_patient_search.get()
    cursor.execute("SELECT * FROM patients WHERE name=?", (name,))
    records = cursor.fetchall()
    display_patient_records(records)

def display_patient_records(records):
    listbox_patient.delete(0, END)
    if records:
        for record in records:
            listbox_patient.insert(END, f"ID: {record[0]}, Name: {record[1]}, Age: {record[2]}, Gender: {record[3]}, Address: {record[4]}, Phone: {record[5]}, Admission Date: {record[6]}")
    else:
        listbox_patient.insert(END, "No patient records found.")

# Doctor Management Functions
def add_doctor():
    name = entry_doctor_name.get()
    specialty = entry_doctor_specialty.get()
    phone = entry_doctor_phone.get()

    cursor.execute("INSERT INTO doctors (name, specialty, phone) VALUES (?, ?, ?)", (name, specialty, phone))
    conn.commit()
    messagebox.showinfo("Success", "Doctor added successfully!")
    clear_doctor_entries()

def clear_doctor_entries():
    entry_doctor_name.delete(0, END)
    entry_doctor_specialty.delete(0, END)
    entry_doctor_phone.delete(0, END)

# Pharmacy Management Functions
def add_drug():
    drug_name = entry_drug_name.get()
    quantity = entry_drug_quantity.get()
    price = entry_drug_price.get()

    cursor.execute("INSERT INTO pharmacy (drug_name, quantity, price) VALUES (?, ?, ?)", (drug_name, quantity, price))
    conn.commit()
    messagebox.showinfo("Success", "Drug added successfully!")
    clear_pharmacy_entries()

def clear_pharmacy_entries():
    entry_drug_name.delete(0, END)
    entry_drug_quantity.delete(0, END)
    entry_drug_price.delete(0, END)

# Ward Management Functions
def add_ward():
    ward_number = entry_ward_number.get()
    capacity = entry_ward_capacity.get()

    cursor.execute("INSERT INTO wards (ward_number, capacity) VALUES (?, ?)", (ward_number, capacity))
    conn.commit()
    messagebox.showinfo("Success", "Ward added successfully!")
    clear_ward_entries()

def clear_ward_entries():
    entry_ward_number.delete(0, END)
    entry_ward_capacity.delete(0, END)

# Patient Management UI
Label(frame_patient, text="Patient Name:").grid(row=0, column=0, sticky=W)
entry_patient_name = Entry(frame_patient, width=30)
entry_patient_name.grid(row=0, column=1)

Label(frame_patient, text="Age:").grid(row=1, column=0, sticky=W)
entry_patient_age = Entry(frame_patient, width=30)
entry_patient_age.grid(row=1, column=1)

Label(frame_patient, text="Gender:").grid(row=2, column=0, sticky=W)
entry_patient_gender = Entry(frame_patient, width=30)
entry_patient_gender.grid(row=2, column=1)

Label(frame_patient, text="Address:").grid(row=3, column=0, sticky=W)
entry_patient_address = Entry(frame_patient, width=30)
entry_patient_address.grid(row=3, column=1)

Label(frame_patient, text="Phone:").grid(row=4, column=0, sticky=W)
entry_patient_phone = Entry(frame_patient, width=30)
entry_patient_phone.grid(row=4, column=1)

Label(frame_patient, text="Admission Date:").grid(row=5, column=0, sticky=W)
entry_patient_admission = Entry(frame_patient, width=30)
entry_patient_admission.grid(row=5, column=1)

Button(frame_patient, text="Add Patient", command=add_patient).grid(row=6, columnspan=2, pady=10)

Label(frame_patient, text="Search Patient by Name:").grid(row=7, column=0, sticky=W)
entry_patient_search = Entry(frame_patient, width=30)
entry_patient_search.grid(row=7, column=1)

Button(frame_patient, text="Search Patient", command=search_patient).grid(row=8, columnspan=2, pady=10)

listbox_patient = Listbox(frame_patient, width=80, height=10)
listbox_patient.grid(row=9, columnspan=2, pady=10)

# Similar UI setups for Doctor, Pharmacy, and Ward sections here...
# These would include Entry widgets, Labels, and Buttons for each section's respective functionalities.

# Run the application
root.mainloop()
