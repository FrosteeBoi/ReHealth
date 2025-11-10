import os
from datetime import datetime
from tkinter import messagebox

import ttkbootstrap as tb

from logic.user import User
from logic.calculations import bmi_calc, bmi_status
from db.db_handler import save_metrics, get_all_days_metrics
from ui_handler import return_to_dashboard


class Measurement:
    """
    Class created to record measurements like user height, weight,
    and calculate BMI.
    """

    def __init__(self, root, user: User):
        """
        Main window for measurement initialised.
        """
        self.root = root
        self.user = user
        self.measureframe = tb.Frame(self.root)
        self.measureframe.place(relx=0.5, rely=0, anchor="n")
        self.root.geometry("490x630")
        self.root.title("ReHealth")

        # Initialises measurement values as empty strings
        self.height_val = 0
        self.weight_val = 0
        self.bmi_val = 0

        # Labels initialised and placed
        self.measure_label = tb.Label(
            self.measureframe,
            text=f"{self.user.username}'s Measurements",
            font=("roboto", 18, "bold")
        )
        self.measure_label.grid(row=0, column=0, pady=(20, 30), columnspan=3, padx=20)

        self.height_value_label = tb.Label(
            self.measureframe,
            text=f"Height: {self.height_val}",
            font=("roboto", 14)
        )
        self.height_value_label.grid(row=1, column=0, columnspan=3, pady=(10, 10), padx=20)

        self.weight_value_label = tb.Label(
            self.measureframe,
            text=f"Weight: {self.weight_val}",
            font=("roboto", 14)
        )
        self.weight_value_label.grid(row=2, column=0, columnspan=3, pady=(10, 10), padx=20)

        self.bmi_label = tb.Label(
            self.measureframe,
            text="BMI: 0",
            font=("roboto", 14)
        )
        self.bmi_label.grid(row=3, column=0, pady=(10, 30), columnspan=3, padx=20)

        self.height_label = tb.Label(
            self.measureframe,
            text="Record Your Height:",
            font=("roboto", 14)
        )
        self.height_label.grid(row=4, column=0, pady=(10, 10), padx=(20, 10), sticky="e")

        self.height_entry = tb.Entry(self.measureframe, width=15)
        self.height_entry.grid(row=4, column=1, padx=(10, 10), pady=(10, 10))

        self.height_button = tb.Button(
            self.measureframe,
            text="Add",
            command=self.height_inc,
            width=8
        )
        self.height_button.grid(row=4, column=2, padx=(10, 20), pady=(10, 10))

        # Weight Input Section
        self.weight_label = tb.Label(
            self.measureframe,
            text="Record Your Weight:",
            font=("roboto", 14)
        )
        self.weight_label.grid(row=5, column=0, pady=(10, 10), padx=(20, 10), sticky="e")

        self.weight_entry = tb.Entry(self.measureframe, width=15)
        self.weight_entry.grid(row=5, column=1, padx=(10, 10), pady=(10, 10))

        self.weight_button = tb.Button(
            self.measureframe,
            text="Add",
            command=self.weight_inc,
            width=8
        )
        self.weight_button.grid(row=5, column=2, padx=(10, 20), pady=(10, 10))

        # BMI Calculate Button
        self.bmi_calc_button = tb.Button(
            self.measureframe,
            text="Calculate BMI",
            command=self.bmi_inc
        )
        self.bmi_calc_button.grid(row=6, column=0, columnspan=3, pady=(30, 10), padx=20)

        # Download Records Button
        self.download_button = tb.Button(
            self.measureframe,
            text="Download Measurement History",
            command=self.download_records
        )
        self.download_button.grid(row=7, column=0, columnspan=3, pady=(10, 20), padx=20)

        # Back to Dashboard Button
        self.dash_button = tb.Button(
            self.measureframe,
            text="Back to Dashboard",
            command=self.return_to_dash
        )
        self.dash_button.grid(row=8, column=0, columnspan=3, pady=(10, 20), padx=20)

    def height_inc(self):
        """
        Updates height value from the entry field and displays it.
        """
        try:
            value = float(self.height_entry.get())
            self.height_val = str(value)
            self.height_entry.delete(0, 'end')
            self.height_value_label.config(text=f"Height: {self.height_val} cm")
        except ValueError:
            messagebox.showerror("Failed input", "Please enter your height as a number in cm.")

    def weight_inc(self):
        """
        Updates weight value from the entry field and displays it.
        """
        try:
            value = float(self.weight_entry.get())
            self.weight_val = str(value)
            self.weight_entry.delete(0, 'end')
            self.weight_value_label.config(text=f"Weight: {self.weight_val} kg")
        except ValueError:
            messagebox.showerror("Failed input", "Please enter your weight as a number in kg.")

    def bmi_inc(self):
        """
        Calculates BMI using given values.
        """
        try:
            value = bmi_calc(self.weight_val, self.height_val)
            self.bmi_val = value
            self.bmi_label.config(text=f"BMI: {self.bmi_val} ({bmi_status(self.bmi_val)})")

            # Saves metrics to the database
            save_metrics(self.user.user_id, float(self.height_val), float(self.weight_val))
            messagebox.showinfo("Saved", "Measurement data saved successfully.")
        except (ValueError, ZeroDivisionError):
            messagebox.showerror("Failed input", "Error in calculating BMI or saving data.")

    def download_records(self):
        """
        Downloads all past measurement records for the user to a text file.
        """
        try:
            # Fetch all metrics using db_handler function
            records = get_all_days_metrics(self.user.user_id)

            if not records:
                messagebox.showinfo("No Records", "No measurement records found for this user.")
                return

            met_log_directory = os.path.join(os.path.dirname(__file__), "..", "metric_logs")
            met_log_directory = os.path.abspath(met_log_directory)
            os.makedirs(met_log_directory, exist_ok=True)

            # Creates filename with current date
            current_date = datetime.now().strftime("%d-%m-%Y")
            filename = os.path.join(met_log_directory, f"metric_log_{current_date}.txt")

            # Writes records to file
            with open(filename, 'w') as file:
                file.write(f"Measurement Records for {self.user.username}\n")
                file.write(f"Downloaded on: {datetime.now().strftime('%d-%m-%Y %H:%M')}\n")
                file.write("=" * 60 + "\n\n")

                for record in records:
                    date, height, weight = record
                    # Calculates BMI for each record
                    bmi = bmi_calc(str(weight), str(height))
                    status = bmi_status(bmi)

                    file.write(f"Date: {date}\n")
                    file.write(f"Height: {height} cm\n")
                    file.write(f"Weight: {weight} kg\n")
                    file.write(f"BMI: {bmi} ({status})\n")
                    file.write("-" * 60 + "\n")

            messagebox.showinfo("Success", f"Records downloaded successfully to {filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to download records: {str(e)}")

    def return_to_dash(self):
        """
        Returns to the dashboard screen.
        """
        return_to_dashboard(self.measureframe, self.root, self.user)


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Measurement(root, test_user)
    root.mainloop()
