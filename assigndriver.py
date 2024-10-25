import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import Globalvariable
class AssignDriver:
    def __init__(self, root):
        self.root = root
        self.root.title("Assign driver to the customer")
        self.root.geometry("800x718+200+10")
        self.root.resizable(False, False)
        self.root.configure(bg="#B1B2FF")

        self.create_widgets()
        self.create_widgets1()
        

    def create_widgets(self):
        tk.Label(self.root, text="Driver ID:", bg="#B1B2FF", font=("Arial", 15, "bold")).place(x=50, y=100)
        self.drive_assign0 = tk.Entry(self.root, font=("Arial", 15, "bold"), width=30)
        self.drive_assign0.place(x=230, y=100)

        tk.Label(self.root, text="Pickup Address:", bg="#B1B2FF", font=("Arial", 15, "bold")).place(x=50, y=150)
        self.drive_assign1 = tk.Entry(self.root, font=("Arial", 15, "bold"), width=30)
        self.drive_assign1.place(x=230, y=150)

        self.booking_id = tk.Entry(self.root)
        self.booking_id.place(x=600,y=2000,height=30,width=100)

        tk.Label(self.root, text="Drop Address:", bg="#B1B2FF", font=("Arial", 15, "bold")).place(x=50, y=200)
        self.drive_assign2 = tk.Entry(self.root, font=("Arial", 15, "bold"), width=30)
        self.drive_assign2.place(x=230, y=200)

        tk.Label(self.root, text="Pickup Date:", bg="#B1B2FF", font=("Arial", 15, "bold")).place(x=50, y=250)
        self.drive_assign3 = tk.Entry(self.root, font=("Arial", 15, "bold"), width=30)
        self.drive_assign3.place(x=230, y=250)

        tk.Label(self.root, text="Pick Time:", bg="#B1B2FF", font=("Arial", 15, "bold")).place(x=50, y=300)
        self.drive_assign4 = tk.Entry(self.root, font=("Arial", 15, "bold"), width=30)
        self.drive_assign4.place(x=230, y=300)

        assign_button = tk.Button(self.root, text="Assign Driver", font=("Arial", 15, "bold"),command=self.assign_driver, bg="#4CAF50", fg="white")
        assign_button.place(x=250, y=350)

        close_button = tk.Button(self.root, text="Close", command=self.root.destroy, font=("Arial", 15, "bold"), bg="#FF6347", fg="white")
        close_button.place(x=500, y=350)
        

     # Treeview for assigned drivers
    def create_widgets1(self):
        columns_assigned_driver = (
            "Booking ID", "Customer ID", "Pickup Address", "Drop Address", "Pickup Date", "Pickup Time",
        )

        self.assigned_driver_tree = ttk.Treeview(self.root, columns=columns_assigned_driver, show="headings", height=10)
        style_assigned_driver = ttk.Style()
        style_assigned_driver.theme_use("clam")
        style_assigned_driver.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#4B6DFF", foreground="white")
        style_assigned_driver.configure("Treeview", font=("Arial", 10))

        for col in columns_assigned_driver:
            self.assigned_driver_tree.heading(col, text=col)
            self.assigned_driver_tree.column(col,width=120, anchor="center")

        self.assigned_driver_tree.place(x=50, y=450)
        self.view_drivers()
        self.assigned_driver_tree.bind("<ButtonRelease-1>", self.getting_data)

    def view_drivers(self):
        query = '''SELECT  booking_id, customer_id, pickup_address, drop_address,pick_up_date,pick_up_time FROM triped '''
        result = self.execute_query(query)

        if not result:
            messagebox.showinfo("No Drivers", "No driver records found.")
            return

        self.assigned_driver_tree.delete(*self.assigned_driver_tree.get_children())  # Clear previous data

        for record in result:
            self.assigned_driver_tree.insert("", "end", values=record)

        

    def assign_driver(self):

        
        driver_id = self.drive_assign0.get()
        pickup_address = self.drive_assign1.get()
        drop_address = self.drive_assign2.get()
        pickup_date = self.drive_assign3.get()
        pickup_time = self.drive_assign4.get()

        if driver_id and pickup_address and drop_address and pickup_date and pickup_time:
            booking_id =self.booking_id.get()
            driver_id = self.drive_assign0.get()
            try:
                connection = sqlite3.connect("taxi_booking.db")
                cursor = connection.cursor()
                query = '''UPDATE triped set driver_id=? where Booking_id=?'''
                params = (driver_id, booking_id)
                cursor.execute(query, params)
                messagebox.showinfo("Success", "Driver assigned successfully!")
                
                connection.commit()
                cursor.close()
                connection.close()
            except sqlite3.Error as error:
                print(f"{error}")
        else:
            messagebox.showwarning("Incomplete Information", "Please fill in all the details.")

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
    
    def getting_data(self, event=''):
        selected_item = self.assigned_driver_tree.selection()

        if selected_item:
            values = self.assigned_driver_tree.item(selected_item, 'values') 
            self.drive_assign1.delete(0, "end")
            self.drive_assign1.insert(0, values[2])
            self.booking_id.delete(0, "end")
            self.booking_id.insert(0, values[0])
            self.drive_assign2.delete(0, "end")
            self.drive_assign2.insert(0, values[3])
            self.drive_assign3.delete(0, "end")
            self.drive_assign3.insert(0, values[4])
            self.drive_assign4.delete(0, "end")
            self.drive_assign4.insert(0, values[5])
    
if __name__ == "__main__":
    root = tk.Tk()
    app = AssignDriver(root)
    root.mainloop()
