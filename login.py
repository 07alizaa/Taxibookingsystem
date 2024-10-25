from tkinter import *
from PIL import Image, ImageTk
from CustomerDashboard import CustomerDashboard
from register import TaxiBookingSystem
from tkinter import messagebox
from Admindashboard import AdminDashboard
from driverdashboard import DriverDashboard
import sqlite3
import Globalvariable

class Login:
    def __init__(self, window):
        self.window = window
        self.window.geometry('900x718')
        self.window.resizable(0, False)
        self.window.state('zoomed')
        self.window.title('Login Page')
        self.createLabel()



    def createLabel(self):
        # ==========LoginFrame=============
        self.login_frame = Frame(self.window, bg='#1D1A39', width=950, height=600)
        self.login_frame.place(x=200, y=70)

        # ====================Center Image===============
        center_image = Image.open('C:\\Users\\simkh\\OneDrive\\Desktop\\nainital-cab-2.png')
        center_photo = ImageTk.PhotoImage(center_image)
        center_label = Label(self.login_frame, image=center_photo, bg='#1D1A39')
        center_label.image = center_photo
        center_label.place(relx=0.5, rely=0.2, anchor='center') 
        # ====================Username================
        username_label = Label(self.login_frame, text="User Name", fg="white", bg="#1D1A39", font=("yu gothic ui", 12, "bold"))
        username_label.place(x=100, y=300)
        self.username_entry = Entry(self.login_frame, bg="#D2DAFF", fg="black", font=("yu gothic ui", 13, "bold"))
        self.username_entry.place(x=200, y=300, width=270)

        # =========================Password Entry================
        password_label = Label(self.login_frame, text="Password", fg="white",bg="#1D1A39", font=("yu gothic ui", 12, "bold"))
        password_label.place(x=100, y=400)
        self.password_entry = Entry(self.login_frame, bg="#D2DAFF", fg="black", font=("yu gothic ui", 13, "bold"), show="*")
        self.password_entry.place(x=200, y=396, width=270)

        # =========================Login Button=======================
        login_button = Button(self.login_frame, text="Login", bg="#4CAF50", fg="white", font=("yu gothic ui", 12), command=self.login)
        login_button.place(x=200, y=480, width=120)  

        # =========================Register Button=======================
        register_button = Button(self.login_frame, text="Register", bg="#008CBA", fg="white", font=("yu gothic ui", 12),command=self.cus_register)
        register_button.place(x=340, y=480, width=120)  
        
        label = Label(self.login_frame, text="Are you a driver? ", fg="white", bg="#1D1A39", font=("yu gothic ui", 12, "bold"))
        label.place(x=180, y=540)

        driver = Button(self.login_frame, text="Driver", bg="#1D1A39", fg="red", font=("yu gothic ui", 12),bd=0,command=self.new_driver)
        driver.place(x=310, y=540, width=120)  

        
       

    def register_function(self):
        self.window.destroy()  
        window = Tk()
        TaxiBookingSystem(window)

    def login(self):
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()

        if self.username_entry.get()=="" or  self.password_entry.get() =="":
            messagebox.showerror("Login Failed", "Please enter  your username and password")

        elif self.username_entry.get()!="" or  self.password_entry.get()!="":
            result = self.check_credentials(entered_username, entered_password)
            
            if result is not None:
                Globalvariable.customer = result
                messagebox.showinfo("Login Successful", f"Welcome, {Globalvariable.customer[1]}")
            
                self.window.destroy()
                root = Tk()
                CustomerDashboard(root)
                root.mainloop()
                



            elif entered_username=="admin"and  entered_password =="admin":
                
                messagebox.showinfo("Login Successful", "Welcome, {}".format(entered_username))

                root1 = Tk()
                AdminDashboard(root1)
                self.window.destroy()

            else:
                messagebox.showinfo("Login Failed","Invalid username/password")

        else:
                messagebox.showerror("login","login failed")



    def check_credentials(self, username, password):
        # Connect to the database
        connection = sqlite3.connect("taxi_booking.db")
        cursor = connection.cursor()

        # Execute a query to check if the username and password match
        cursor.execute('''
            SELECT * FROM register_cus1
            WHERE User_name = ? AND Password = ?
        ''', (username, password))

        result = cursor.fetchone()
        connection.close()
        return result 
    
    def cus_register(self):
        self.window1 = Toplevel(self.window)
        self.app = TaxiBookingSystem(self.window1)


    
    def check(self, entered_username, entered_password):
        # Connect to the database
        connection = sqlite3.connect("taxi_booking.db")
        cursor = connection.cursor()

        # Execute a query to check if the username and password match
        cursor.execute('''
            SELECT * FROM register_driver
            WHERE User_name = ? AND Password = ?
        ''', (entered_username, entered_password))

        result1 = cursor.fetchone()
        if result1 is None:
            messagebox.showinfo("Error", "Username or Password incorrect.")
        connection.close()
        return result1
        
        

    def new_driver(self):
            entered_username = self.username_entry.get()
            entered_password = self.password_entry.get()

            if self.username_entry.get()=="" or  self.password_entry.get() =="":
                messagebox.showerror("Login Failed", "Invalid username or password")

            elif self.username_entry.get()!="" or  self.password_entry.get()!="":
                result1 = self.check(entered_username, entered_password)
                    
                if result1:
                    Globalvariable.Driver = result1
                    messagebox.showinfo("Login Successful", f"Welcome, {Globalvariable.Driver[1]}")


                    root = Tk()
                    DriverDashboard(root)
                    self.window.destroy()

            else:
                messagebox.showerror('login','login error')
    
if __name__ == "__main__":
    root = Tk()
    app = Login(root)
    root.mainloop()
