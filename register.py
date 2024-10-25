import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

class TaxiBookingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration Page")
        self.root.geometry("900x718+200+10")
        self.root.resizable(False, False)
        self.root.configure(bg="#83A2FF")
        self.database_connection()
        self.customer_id = 1
        self.createLabel()

    def createLabel(self):
        registration_title = Label(self.root, text="Registration Form", width=20, font=("Arial", 20, "bold"),
                                   bg="#83A2FF")
        registration_title.pack(pady=10)


        name_label = Label(self.root, text="FullName:",bg="#83A2FF" ,font=("Arial", 13, "bold"), width="15")
        name_label.place(x=200, y=100)
        self.name_entry = Entry(self.root, font=("Arial", 13, "bold"), width="25")
        self.name_entry.place(x=430, y=100)

        email_label = Label(self.root, text="Email:",bg="#83A2FF", font=("Arial", 13, "bold"), width="15")
        email_label.place(x=200, y=150)
        self.email_entry = Entry(self.root, font=("Arial", 13, "bold"), width="25")
        self.email_entry.place(x=430, y=150)

        contact_label = Label(self.root, text="Contact:",bg="#83A2FF", font=("Arial", 13, "bold"), width="15")
        contact_label.place(x=200, y=200)
        self.contact_entry = Entry(self.root, font=("Arial", 13, "bold"), width="25")
        self.contact_entry.place(x=430, y=200)

        gender_label = Label(self.root, text="Gender:",bg="#83A2FF", font=("Arial", 11, "bold"), width="15")
        gender_label.place(x=200, y=250)
        self.vars = IntVar()
        Radiobutton(self.root, text="Male", padx=10, variable=self.vars, font=("Arial", 11, "bold"), value=1).place(
            x=430, y=250)
        Radiobutton(self.root, text="Female", padx=10, variable=self.vars, font=("Arial", 11, "bold"),
                    value=2).place(x=540, y=250)


        country_label = Label(self.root, text="Country:" ,font=("Arial", 11, "bold"), bg="#83A2FF", width='15')
        country_label.place(x=200, y=300)
        self.cv = StringVar()
        self.country_list = ["India", "Nepal", "UK", "USA"]
        cnt_list = OptionMenu(self.root, self.cv, *self.country_list)
        cnt_list.config(width=25, font=("Arial", 11, "bold"))
        self.cv.set("Select Your Country")
        cnt_list.place(x=430, y=300)

        username_label = Label(self.root, text="UserName",bg="#83A2FF",font=("Arial", 13, "bold"), width="15")
        username_label.place(x=200, y=350)
        self.username_entry = Entry(self.root, font=("Arial", 13, "bold"), width="25")
        self.username_entry.place(x=430, y=350)

        #=============== Password Label =========================================#
        password = Label(self.root, text="Password:",bg="#83A2FF", font=("Arial", 13, "bold"), width="15")
        password.place(x=200, y=400)
        self.password_e = Entry(self.root, font=("Arial", 13, "bold"), width="25")
        self.password_e.place(x=430, y=400)

        #====================Payment method =============================================#
        payment_label = Label(self.root, text="Payment Method:", bg="#83A2FF", font=("Arial", 11, "bold"), width="15")
        payment_label.place(x=200, y=450)
        self.payment_method_var = StringVar()
        payment_methods = ["Phone Pay", "Esewa", "Khalti", "Connect IPS", "Other"]
        payment_menu = ttk.Combobox(self.root, textvariable=self.payment_method_var, values=payment_methods, font=("Arial", 11, "bold"))
        payment_menu.set("Select Payment Method")
        payment_menu.config(width=25)
        payment_menu.place(x=430, y=450)

        #============================Signup Button ===================================#
        signup_button = Button(self.root, text="SignUp", font=("Arial", 12, "bold"),command=self.insert_info, width="11", bg="blue", fg="white")
        signup_button.place(x=400, y=505)

        login_button = Button(self.root, text="Login", font=("Arial", 12, "bold",),
                              width="11", bg="blue", fg="white", command=self.login_logic)
        login_button.place(x=510, y=505)

    def login_logic(self):
        if self.username_entry == "" or self.password_e=="":
            messagebox.showerror("Error","All field are required")

        else:
            self.root.destroy()  
            root = Tk()  
            from login import YourClassName
            YourClassName(root)

    def database_connection(self):
        with sqlite3.connect("taxi_booking.db") as connection:
            cursor = connection.cursor()

            cursor.execute('''
                   CREATE TABLE IF NOT EXISTS register_cus1 (
                       customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       Full_name TEXT,
                       Email TEXT,
                       contact TEXT,
                       gender TEXT,
                       country TEXT,
                       User_name TEXT,
                       Password TEXT,
                       payment_method TEXT
                   )
               ''')

    def insert_info(self):

        Full_name = self.name_entry.get()
        Email = self.email_entry.get()
        contact = self.contact_entry.get()
        gender = self.vars.get()
        country = self.cv.get()
        User_name = self.username_entry.get()
        Password = self.password_e.get()
        payment_method = self.payment_method_var.get()
        if not all([Full_name, Email, contact, gender, country, User_name, Password,payment_method]):
            messagebox.showerror("Error", "All fields are required")
        else:
            confirmation_message = f"Username and password successful!\n\nUsername: {User_name}\nPassword: {Password}\nCountry: {country}"
            messagebox.showinfo("Registered Successfully", confirmation_message)

            self.insert_data(Full_name, Email, contact, gender, country, User_name, Password,payment_method)
            self.customer_id += 1


    def insert_data(self, Full_name, Email, contact, gender, country, User_name, Password,payment_method):
        with sqlite3.connect("taxi_booking.db") as connection:
            cursor = connection.cursor()

            cursor.execute('''
                   INSERT INTO register_cus1 (Full_name, Email, contact, gender, country, User_name, Password,Payment_method)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)
               ''', (Full_name, Email, contact, gender, country, User_name, Password,payment_method))


if __name__ == "__main__":
    root = Tk()
    app = TaxiBookingSystem(root)
    root.mainloop()
