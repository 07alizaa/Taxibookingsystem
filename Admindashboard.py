import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from assigndriver import AssignDriver
import subprocess
import Globalvariable

class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)
        self.root.configure(bg="#F2F2F2")

        self.create_left_frame()
        self.create_center_frame()

        
    
    def create_left_frame(self):
        left_frame = tk.Frame(self.root, bg="#4B6DFF", width=600, height=800)
        left_frame.place(x=0, y=0)
 
        view_trips_button = tk.Button(left_frame, text="View Trips", bg="#D2DAFF", width=16, fg="black", font=("Arial", 12, "bold"), command=self.view_trips)
        view_trips_button.place(x=10, y=10)

        assign_driver_button = tk.Button(left_frame, text="Assign Driver", bg="#D2DAFF", width=16, fg="black", font=("Arial", 12, "bold"), command=self.show_assign_driver)
        assign_driver_button.place(x=10, y=60)

        register_driver_button = tk.Button(left_frame, text="Register Driver", bg="#D2DAFF", width=16, fg="black", font=("Arial", 12, "bold"), command=self.register1)
        register_driver_button.place(x=10, y=110)

        driver_booking_button = tk.Button(left_frame, text="View Driver", bg="#D2DAFF", width=16, fg="black", font=("Arial", 12, "bold"), command=self.view_drivers)
        driver_booking_button.place(x=10, y=210)

        logout_button = tk.Button(left_frame, text="Logout", bg="#D2DAFF", width=16, fg="black", font=("Arial", 12, "bold"), command=self.root.destroy)
        logout_button.place(x=10, y=260)

    def create_center_frame(self):
        self.center_frame = tk.Frame(self.root, bg="white", width=800, height=800)
        self.center_frame.place(x=200, y=0)

        #===== Treeview======#
        columns_trip = (
            "Booking ID", "Customer ID", "Pickup Address", "Drop Address", "Pickup Date", "Pickup Time",
        )
        self.trip_tree = ttk.Treeview(self.center_frame, columns=columns_trip, show="headings", height=20)
        style_trip = ttk.Style()
        style_trip.theme_use("clam")
        style_trip.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#4B6DFF", foreground="white")
        style_trip.configure("Treeview", font=("Arial", 10))

        for col in columns_trip:
            self.trip_tree.heading(col, text=col)
            self.trip_tree.column(col, width=110, anchor="center")

        self.trip_tree.place(x=10, y=50)

        # Treeview for displaying drivers
        columns_driver = (
            "Driver ID", "Full Name", "Email", "Contact", "License Number",
        )
        self.driver_tree = ttk.Treeview(self.center_frame, columns=columns_driver, show="headings", height=15)
        style_driver = ttk.Style()
        style_driver.theme_use("clam")
        style_driver.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#4B6DFF", foreground="white")
        style_driver.configure("Treeview", font=("Arial", 10))

        for col in columns_driver:
            self.driver_tree.heading(col, text=col)
            self.driver_tree.column(col, width=110, anchor="center")

        self.driver_tree.place(x=10, y=300)

    def view_drivers(self):
        query = '''SELECT * FROM register_driver'''
        result = self.execute_query(query)

        if not result:
            messagebox.showinfo("No Drivers", "No driver records found.")
            return

        self.driver_tree.delete(*self.driver_tree.get_children())  

        for record in result:
            self.driver_tree.insert("", "end", values=record)

       

    def view_trips(self):
        query = '''SELECT * FROM triped'''
        result = self.execute_query(query)

        if not result:
            messagebox.showinfo("No Trips", "No trip records found.")
            return

        self.trip_tree.delete(*self.trip_tree.get_children())  

        for record in result:
            status_mapping = {'1': 'Driver Available', '2': 'Driver Not Available', '3': 'Trip Completed'}
            record_with_status = list(record)
            status_value = str(record[6])  
            record_with_status[6] = status_mapping.get(status_value, 'Unknown Status')

            self.trip_tree.insert("", "end", values=record_with_status)


    def show_assign_driver(self):
        new_root = tk.Tk()
        AssignDriver(new_root)
        new_root.mainloop()

    def execute_query(self, query, parameters=None):
        connection = sqlite3.connect("taxi_booking.db")
        cursor = connection.cursor()
        if parameters:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        return result
    
    def register1(self):
        subprocess.run(['python', 'driverregistration.py'])

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminDashboard(root)
    root.mainloop()
