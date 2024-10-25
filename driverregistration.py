import sqlite3
from tkinter import *
from tkinter import messagebox
# from login import YourClassName

class DriverRegistrationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Driver Registration Page")
        self.root.geometry("900x650+200+10")
        self.root.resizable(False, False)
        self.root.configure(bg="#83A2FF")
        self.database_connection()
        self.create_labels()

    def create_labels(self):
        registration_title = Label(self.root, text="Driver Registration Form", width=30, font=("Arial", 20, "bold"),
                                   bg="#83A2FF")
        registration_title.pack(pady=10)

        name_label = Label(self.root, text="Full Name:", bg="#83A2FF", font=("Arial", 13, "bold"), width="15")
        name_label.place(x=200, y=100)
        self.name_entry = Entry(self.root, font=("Arial", 13, "bold"), width="25")
        self.name_entry.place(x=430, y=100)

        email_label = Label(self.root, text="Email:", bg="#83A2FF", font=("Arial", 13, "bold"), width="15")
        email_label.place(x=200, y=150)
        self.email_entry = Entry(self.root, font=("Arial", 13, "bold"), width="25")
        self.email_entry.place(x=430, y=150)

        contact_label = Label(self.root, text="Contact:", bg="#83A2FF", font=("Arial", 13, "bold"), width="15")
        contact_label.place(x=200, y=200)
        self.contact_entry = Entry(self.root, font=("Arial", 13, "bold"), width="25")
        self.contact_entry.place(x=430, y=200)

        license_label = Label(self.root, text="License Number:", bg="#83A2FF", font=("Arial", 13, "bold"), width="15")
        license_label.place(x=200, y=250)
        self.license_entry = Entry(self.root, font=("Arial", 13, "bold"), width="25")
        self.license_entry.place(x=430, y=250)

        username_label = Label(self.root, text="Username", bg="#83A2FF", font=("Arial", 13, "bold"), width="15")
        username_label.place(x=200, y=300)
        self.username_entry = Entry(self.root, font=("Arial", 13, "bold"), width="25")
        self.username_entry.place(x=430, y=300)

        password_label = Label(self.root, text="Password:", bg="#83A2FF", font=("Arial", 13, "bold"), width="15")
        password_label.place(x=200, y=350)
        self.password_entry = Entry(self.root, font=("Arial", 13, "bold"), width="25", show="*")
        self.password_entry.place(x=430, y=350)
    
        signup_button = Button(self.root, text="Register", font=("Arial", 12, "bold"), command=self.insert_info,
                               width="11", bg="blue", fg="white")
        signup_button.place(x=400, y=550)

    def insert_info(self):
        full_name = self.name_entry.get()
        email = self.email_entry.get()
        contact = self.contact_entry.get()
        license_number = self.license_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
       

        if not all([full_name, email, contact, license_number, username, password]):
            messagebox.showerror("Error", "All fields are required")
        else:
            confirmation_message = f"Driver registered successfully!\n\nUsername: {username}\nPassword: {password}\nLicense Number: {license_number}"
            messagebox.showinfo("Registered Successfully", confirmation_message)
    

            self.insert_data(full_name, email, contact, license_number, username, password)


    def insert_data(self, full_name, email, contact, license_number, username, password):
        with sqlite3.connect("taxi_booking.db") as connection:
            cursor = connection.cursor()

            cursor.execute('''
               INSERT INTO register_driver ( Full_name, Email, contact, License_number, User_name, Password)
               VALUES ( ?, ?, ?, ?, ?, ?)
           ''', ( full_name, email, contact, license_number, username, password))
            

    def database_connection(self):
        with sqlite3.connect("taxi_booking.db") as connection:
            cursor = connection.cursor()

            cursor.execute('''
                   CREATE TABLE IF NOT EXISTS register_driver (
                       driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       Full_name TEXT,
                       Email TEXT,
                       contact TEXT,
                       License_number TEXT,
                       User_name TEXT,
                       Password TEXT
                   )
               ''')

if __name__ == "__main__":
    root = Tk()
    app = DriverRegistrationSystem(root)
    root.mainloop()
