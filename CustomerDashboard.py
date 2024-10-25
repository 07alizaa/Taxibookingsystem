import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from tkinter import StringVar
from  tkcalendar import DateEntry
import Globalvariable

class CustomerDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Dashboard")
        self.root.geometry("900x718+200+10")
        self.root.resizable(False, False)
        self.root.configure(bg="#B1B2FF")

        customer_id = Globalvariable.customer[0]

        self.conn = sqlite3.connect("taxi_booking.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

        self.create_widgets()
        self.view_table()
        
        self.read_records()
        
    
    def create_tables(self):
        queries = [
            '''
            CREATE TABLE IF NOT EXISTS triped (
                Booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                pickup_address TEXT,
                drop_address TEXT,
                pick_up_date TEXT,
                pick_up_time TEXT,
                driver_id TEXT,
                status TEXT DEFAULT 'Pending',  -- Add the status column
                FOREIGN KEY (driver_id) REFERENCES register_driver(driver_id),
                FOREIGN KEY (customer_id) REFERENCES register_cus(customer_id)
        )
        '''
    ]

        

        for query in queries:
            self.conn.execute(query)

        self.conn.commit()
        


    def create_widgets(self):
        # Upper Frame
        upper_frame = tk.Frame(self.root, bg="#4056A1")
        upper_frame.place(relx=0, rely=0, relwidth=1, relheight=0.15)

        welcome_label = tk.Label(upper_frame, text="Welcome to Customer Dashboard", font=("Arial", 16, "bold"), bg="#4056A1", fg="white")
        welcome_label.pack(pady=5)

        self.booking_id = tk.Entry(self.root)
        self.booking_id.place(x=1000,y=3000,width=100,height=35)

        self.customer_info_label = tk.Label(upper_frame, text="", font=("Arial", 12), bg="#4056A1", fg="white")
        self.customer_info_label.pack(pady=5)

        tk.Label(self.root, text="Pickup Address:", bg="#B1B2FF", font=("Arial", 12, "bold")).place(x=50, y=200)
        self.pickup_entry1 = tk.Entry(self.root, font=("Arial", 12, "bold"), width=25)
        self.pickup_entry1.place(x=180, y=200)

        tk.Label(self.root, text="Drop Address:", bg="#B1B2FF", font=("Arial", 12, "bold")).place(x=50, y=230)
        self.pickup_entry2 = tk.Entry(self.root, font=("Arial", 12, "bold"), width=25)
        self.pickup_entry2.place(x=180, y=230)

        tk.Label(self.root, text="Pickup Date:", bg="#B1B2FF", font=("Arial", 12, "bold")).place(x=50, y=260)
        self.pickup_entry3 = DateEntry(self.root, font=("Arial", 12, "bold"), width=25,selectmode='day')
        self.pickup_entry3.place(x=180, y=260)

        tk.Label(self.root, text="Pick Time:", bg="#B1B2FF", font=("Arial", 12, "bold")).place(x=50, y=290)
        self.pickup_entry4 = tk.Entry(self.root, font=("Arial", 12, "bold"), width=25)
        self.pickup_entry4.place(x=180, y=290)

        book_button = tk.Button(self.root, text="Book Trip", font=("Arial", 12, "bold"), command=self.book_trip)
        book_button.place(x=50, y=330)

        cancel_button = tk.Button(self.root, text="Cancel Trip", font=("Arial", 12, "bold"), command=self.delete_record)
        cancel_button.place(x=250, y=330)

        update_button = tk.Button(self.root, text="Update Trip", font=("Arial", 12, "bold"), command=self.update_trip)
        update_button.place(x=450, y=330)



    def read_records(self):
        customer_id = Globalvariable.customer[0]
        self.tree.delete(*self.tree.get_children())
        
        # Fix: Add a comma after the 'customer_id' to make it a tuple
        self.cursor.execute('''SELECT * FROM triped WHERE customer_id=?''', (customer_id,))
        records = self.cursor.fetchall()

        if records:
            for record in records:
                self.tree.insert("", "end", values=record)


    def delete_record(self):
        booking_id_value = self.booking_id.get()
        selected_item = self.tree.selection()
        

        customer_id = self.tree.item(selected_item, "values")[0]
        self.cursor.execute(f'DELETE FROM triped WHERE `Booking_id`={booking_id_value}')
        self.conn.commit()
        messagebox.showinfo("Success", "Record deleted successfully!")
        self.read_records()  # Update the Treeview after deletion
        self.entries_clear()
        

    def book_trip(self):
        if Globalvariable.customer is None:
            messagebox.showerror("Error", "Customer information not available. Please log in.")
            return
        else:

            

            pickup_address = self.pickup_entry1.get()
            drop_address = self.pickup_entry2.get()
            pick_up_date = self.pickup_entry3.get()
            pick_up_time = self.pickup_entry4.get()

            try:
                if pickup_address and drop_address and pick_up_date and pick_up_time:
                    customer_id = Globalvariable.customer[0]
                    self.cursor.execute('''
                        INSERT INTO triped ("customer_ID", "Pickup_Address", "Drop_Address", "Pick_up_Time", "Pick_up_Date")
                        VALUES (?, ?, ?, ?, ?)
                    ''', (customer_id, pickup_address, drop_address, pick_up_time, pick_up_date))

                    self.conn.commit()
                    messagebox.showinfo("Success", "Booking  successfully done!")
                    self.entries_clear()
                    self.read_records()
                else:
                    messagebox.showerror("Error", "Please fill in all fields.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def entries_clear(self):
        self.pickup_entry1.delete(0, tk.END)
        
        self.pickup_entry2.delete(0, tk.END)
        self.pickup_entry3.delete(0, tk.END)
        self.pickup_entry4.delete(0, tk.END)

    def view_trips(self):
        customer_id = Globalvariable.customer[0]
        if not customer_id:
            messagebox.showerror("Error", "Please enter Customer ID.")
            return

        try:
            customer_id = int(customer_id)
        except ValueError:
            messagebox.showerror("Error", "Customer ID must be a number.")
            return

        self.show_booking_history(customer_id)

    def update_trip(self):
        try:
            conn = sqlite3.connect("taxi_booking.db")
            cursor = conn.cursor()
      
            booking_id_value = self.booking_id.get()

            new_pickup_address = self.pickup_entry1.get()
            new_drop_address = self.pickup_entry2.get()
            new_pick_up_date = self.pickup_entry3.get()
            new_pick_up_time = self.pickup_entry4.get()

           

            update_query = f"UPDATE triped SET `pickup_address`=?,`drop_address`=?,`pick_up_date`=?,`pick_up_time`=? WHERE `Booking_id`=?"
            update_values = (new_pickup_address,new_drop_address,new_pick_up_date,new_pick_up_time,booking_id_value)


            cursor.execute(update_query,update_values)
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Record updated successfully!")
            self.root.destroy()
            new_root = tk.Tk()
            CustomerDashboard(new_root)
            new_root.mainloop()
        
        except Exception as error:
            print(f"{error}")

    def view_table(self):
        columns = (
            "Booking ID", "Customer ID", "Pickup Address","Drop Address", "Pickup Date", "Pickup Time","Driver ID", "status"
        )

        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=90, anchor="center")
        self.tree.place(x=50, y=400)
        self.tree.bind("<ButtonRelease-1>", self.getting_data)

        close_button = tk.Button(self.root, text="Logout", padx=10, pady=6, font=("Arial", 14, "bold"), command=self.logout,
                                 bg="#9FBB73")
        close_button.place(x=750, y=650)

    def logout(self):
        self.root.destroy()

    def getting_data(self, event=''):
        selected_item = self.tree.selection()

        if selected_item:
            values = self.tree.item(selected_item, 'values') 
            self.pickup_entry1.delete(0, "end")
            self.pickup_entry1.insert(0, values[2])
            self.booking_id.delete(0, "end")
            self.booking_id.insert(0, values[0])
            self.pickup_entry2.delete(0, "end")
            self.pickup_entry2.insert(0, values[3])
            self.pickup_entry3.delete(0, "end")
            self.pickup_entry3.insert(0, values[4])
            self.pickup_entry4.delete(0, "end")
            self.pickup_entry4.insert(0, values[5])

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerDashboard(root)
    root.mainloop()
