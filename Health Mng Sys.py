import tkinter as tk
from tkinter import messagebox
import datetime
import mysql.connector as c

class HealthManagementSystemGUI:
    def __init__(self, master):
        self.master = master
        master.title("Health Management System")

        self.create_widgets()

        # MySQL connection setup
        self.con = c.connect(host="localhost", user="root", passwd="4321", database="health")
        self.cursor = self.con.cursor()

    def create_widgets(self):
        # Patient Name Entry
        self.name_label = tk.Label(self.master, text="Select Patient:")
        self.name_label.pack()

        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(self.master, textvariable=self.name_var)
        self.name_entry.pack()

        # Options Radio Buttons
        self.value_label = tk.Label(self.master, text="Select Option:")
        self.value_label.pack()

        self.value_var = tk.IntVar()
        self.value_entry1 = tk.Radiobutton(self.master, text="Enter Eaten Food", variable=self.value_var, value=1)
        self.value_entry1.pack()

        self.value_entry2 = tk.Radiobutton(self.master, text="See Eaten Food Details", variable=self.value_var, value=2)
        self.value_entry2.pack()

        # Diet Entry
        self.diet_label = tk.Label(self.master, text="Enter Eaten Food:")
        self.diet_label.pack()

        self.diet_entry = tk.Entry(self.master)
        self.diet_entry.pack()

        # Submit Button
        self.submit_button = tk.Button(self.master, text="Submit", command=self.submit_button_clicked)
        self.submit_button.pack()

        # MySQL Button
        self.mysql_button = tk.Button(self.master, text="MySQL Data Entry/Retrieval", command=self.mysql_button_clicked)
        self.mysql_button.pack()

    def get_date(self):
        return datetime.datetime.now()

    def save_data(self, patient_name, diet_entry):
        file_name = f"{patient_name.lower()}.txt"
        with open(file_name, "a") as file:
            file.write(f"{self.get_date()}: {diet_entry}\n")
        messagebox.showinfo("Success", "Your details have been saved successfully!")

    def show_data(self, patient_name):
        file_name = f"{patient_name.lower()}.txt"
        try:
            with open(file_name, "r") as file:
                data = file.read()
                messagebox.showinfo(f"{patient_name}'s Eaten Food Details", data)
        except FileNotFoundError:
            messagebox.showinfo("Error", f"No data found for {patient_name}.")

    def submit_button_clicked(self):
        patient_name = self.name_var.get()
        value = self.value_var.get()

        if patient_name and value:
            if value == 1:
                self.save_data(patient_name, self.diet_entry.get())
            elif value == 2:
                self.show_data(patient_name)
        else:
            messagebox.showinfo("Error", "Please enter valid name and selection.")

    def mysql_button_clicked(self):
        new = int(input("Enter 1 to enter data and 2 to see data : "))

        if new == 1:
            while True:
                Id = int(input("Enter the id of Patient : "))
                patientName = input("Enter PatientName :")
                Gender = input("Enter Gender :")
                Disease = input("Enter Disease :")
                Date = input("Enter last visited date :")
                Time = input("Enter Time :")
                Prescription = input("Enter prescription given by doctor : ")
                query = "INSERT INTO patient VALUES({},'{}','{}','{}','{}','{}','{}')".format(
                    Id, patientName, Gender, Disease, Date, Time, Prescription)
                self.cursor.execute(query)
                self.con.commit()
                print("Data inserted successfully.")
                x = int(input("1->Enter more\n2->Exit\nEnter choice:"))
                if x == 2:
                    break

        elif new == 2:
            self.cursor.execute("SELECT * FROM patient")
            result = self.cursor.fetchall()
            for row in result:
                print(row)
            if not result:
                print("No data found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = HealthManagementSystemGUI(root)
    root.mainloop()