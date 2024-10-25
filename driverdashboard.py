import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sqlite3
import Globalvariable

class DriverDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Driver Dashboard")
        self.root.geometry("1200x900")  
        self.root.resizable(False, False)

        self.create_left_frame()
        self.create_top_frame()
        self.create_center_frame()
        driver_id = Globalvariable.Driver[0]
        self.trip_confirmation_frame.place_forget()
        

    def create_left_frame(self):
        left_frame = tk.Frame(self.root, bg="#7988FF", width=200, height=900)
        left_frame.place(x=0, y=0)

        view_trips_button = tk.Button(left_frame, text="View Trips", bg="#D2DAFF", width=16, fg="black", font=("Arial", 12, "bold"), command=self.show_trip_view)
        view_trips_button.place(x=10, y=70)

        confirm_trip_button = tk.Button(left_frame, text="Complete Trip", bg="#D2DAFF", width=16, fg="black", font=("Arial", 12, "bold"), command=self.confirm_trip)
        confirm_trip_button.place(x=10, y=130)

        logout_button = tk.Button(left_frame, text="Logout", bg="#D2DAFF", width=16, fg="black", font=("Arial", 12, "bold"), command=self.logout)
        logout_button.place(x=10, y=190)

    def create_top_frame(self):
        top_frame = tk.Frame(self.root, bg="#4B6DFF", width=1000, height=80)
        top_frame.place(x=200, y=0)

        title_label = tk.Label(top_frame, text="Welcome to Driver Dashboard", bg="#4B6DFF", font=("Arial", 24, "bold"), fg="white")
        title_label.place(x=190, y=20)

    def create_center_frame(self):
        self.center_frame = tk.Frame(self.root, bg="white", width=1000, height=770)
        self.center_frame.place(x=200, y=80)

        # Create Treeview for displaying trips
        columns = (
            "Booking Id", "Customer Id","Pickup Address", "Pickup Date", "Pickup Time", "Drop Address","status"
        )
        self.trip_tree = ttk.Treeview(self.center_frame, columns=columns, show="headings", height=20)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#4B6DFF", foreground="white")
        style.configure("Treeview", font=("Arial", 11))

        for col in columns:
            self.trip_tree.heading(col, text=col)
            self.trip_tree.column(col, width=120, anchor="center")

        self.trip_tree.place(x=10, y=30)

        # Frame for trip confirmation
        self.trip_confirmation_frame = tk.Frame(self.center_frame, bg="white", width=600, height=150)
        self.trip_confirmation_frame.place(x=200, y=250)

        confirm_label = tk.Label(self.trip_confirmation_frame, text="Confirm Trip:", bg="white", font=("Arial", 16, "bold"))
        confirm_label.place(x=10, y=10)

        confirm_trip_label = tk.Label(self.trip_confirmation_frame, text="", bg="white", font=("Arial", 14))
        confirm_trip_label.place(x=10, y=50)

        confirm_button = tk.Button(self.trip_confirmation_frame, text="Confirm", bg="#4B6DFF", fg="white", font=("Arial", 12, "bold"), command=self.confirm_trip)
        confirm_button.place(x=10, y=90)

        cancel_button = tk.Button(self.trip_confirmation_frame, text="Cancel", bg="#4B6DFF", fg="white", font=("Arial", 12, "bold"), command=self.cancel_confirmation)
        cancel_button.place(x=120, y=90)

    def show_profile(self):
     profile_frame = tk.Toplevel(self.root)
     profile_frame.title("My Profile")
     profile_frame.geometry("400x300")
     profile_frame.resizable(False, False)

     profile_label = tk.Label(profile_frame, text="My Profile", font=("Arial", 20, "bold"))
     profile_label.pack(pady=10)

     driver_name_label = tk.Label(profile_frame, text=f"Driver Name: {self.driver_name}", font=("Arial", 14))
     driver_name_label.pack(pady=5)

     license_plate_label = tk.Label(profile_frame, text=f"License Plate: {self.license_plate}", font=("Arial", 14))
     license_plate_label.pack(pady=5)

     add_license_plate_button = tk.Button(profile_frame, text="Add License Plate", bg="#4B6DFF", fg="white", font=("Arial", 12, "bold"), command=self.add_license_plate)
     add_license_plate_button.pack(pady=10)

     close_button = tk.Button(profile_frame, text="Close", bg="#4B6DFF", fg="white", font=("Arial", 12, "bold"), command=profile_frame.destroy)
     close_button.pack(pady=10)
   

    def show_trip_view(self):

        driver_id = Globalvariable.Driver[0]
        connection = sqlite3.connect("taxi_booking.db")
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM triped WHERE `driver_id` = {driver_id}")
        rows = cursor.fetchall()
        for row in rows:
            self.trip_tree.insert("", "end", values=(row[0], row[1], row[2], row[4], row[5], row[3],row[7]))
        

    def confirm_trip(self):
        selected_item = self.trip_tree.selection()
        if selected_item:
            trip_id = self.trip_tree.item(selected_item, "values")[0]
            try:
                connection = sqlite3.connect("taxi_booking.db")
                cursor = connection.cursor()
                cursor.execute(f"UPDATE triped SET `status`='Completed' WHERE `Booking_id` = '{trip_id}'")
                connection.commit()
                cursor.close()
                connection.close()
                messagebox.showinfo("Success","Ride has been completed")
                self.root.destroy()
                new_root = tk.Tk()
                DriverDashboard(new_root)
                new_root.mainloop()
            
            except Exception as error:
                print(f"{error}")

    def cancel_confirmation(self):
        self.trip_confirmation_frame.place_forget()  

    def logout(self):
        self.root.destroy()
            
    def execute_query(self, query, parameters=None):
        connection = sqlite3.connect("taxi_booking.db")
        cursor = connection.cursor()
        if parameters:
            cursor.execute(query, parameters)
        else:
            driver = Globalvariable.Driver[0]
            cursor.execute(query,driver)
        driver = cursor.fetchall()
        connection.commit()
        connection.close()
        return driver

if __name__ == "__main__":
    root = tk.Tk()
    app = DriverDashboard(root)
    root.mainloop()


