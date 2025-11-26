import os
from datetime import datetime
from tkinter import messagebox
import ttkbootstrap as tb
from db.db_handler import save_metrics, get_all_days_metrics
from logic.calculations import bmi_calc, bmi_status
from logic.user import User
from ui.ui_handler import return_to_dashboard


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
        self.measure_label.grid(row=0, column=0, pady=(20, 30), columnspan=3,
                                padx=20)

        self.height_value_label = tb.Label(
            self.measureframe,
            text=f"Height: {self.height_val}",
            font=("roboto", 14)
        )
        self.height_value_label.grid(row=1, column=0, columnspan=3,
                                     pady=(10, 10), padx=20)

        self.weight_value_label = tb.Label(
            self.measureframe,
            text=f"Weight: {self.weight_val}",
            font=("roboto", 14)
        )
        self.weight_value_label.grid(row=2, column=0, columnspan=3,
                                     pady=(10, 10), padx=20)

        self.bmi_label = tb.Label(
            self.measureframe,
            text="BMI: 0",
            font=("roboto", 14)
        )
        self.bmi_label.grid(row=3, column=0, pady=(10, 30), columnspan=3,
                            padx=20)

        self.height_label = tb.Label(
            self.measureframe,
            text="Record Your Height(M):",
            font=("roboto", 14)
        )
        self.height_label.grid(row=4, column=0, pady=(10, 10),
                               padx=(20, 10), sticky="e")

        self.height_entry = tb.Entry(self.measureframe, width=15)
        self.height_entry.grid(row=4, column=1, padx=(10, 10), pady=(10, 10), columnspan=2)

        # Weight Input Section
        self.weight_label = tb.Label(
            self.measureframe,
            text="Record Your Weight(Kg):",
            font=("roboto", 14)
        )
        self.weight_label.grid(row=5, column=0, pady=(10, 10),
                               padx=(20, 10), sticky="e")

        self.weight_entry = tb.Entry(self.measureframe, width=15)
        self.weight_entry.grid(row=5, column=1, padx=(10, 10), pady=(10, 10), columnspan=2)

        self.bmi_calc_button = tb.Button(
            self.measureframe,
            text="Calculate BMI",
            command=self.bmi_inc
        )
        self.bmi_calc_button.grid(row=6, column=0, columnspan=1,
                                  pady=(30, 10), padx=10)

        self.download_button = tb.Button(
            self.measureframe,
            text="Download Measurement History",
            command=self.download_records
        )
        self.download_button.grid(row=6, column=1, columnspan=2,
                                  pady=(30, 10), padx=10)

        # Back to Dashboard Button
        self.dash_button = tb.Button(
            self.measureframe,
            text="Back to Dashboard",
            command=self.return_to_dash
        )
        self.dash_button.grid(row=7, column=0, columnspan=3, pady=(170, 20),
                              padx=20)

    def bmi_inc(self):
        """
        Calculates BMI using given values.
        """
        # Get values from entries
        height_input = self.height_entry.get().strip()
        weight_input = self.weight_entry.get().strip()

        # Validate height
        if not height_input:
            messagebox.showerror(
                "Failed input",
                "Please enter your height as a number in cm."
            )
            return

        try:
            height_val = float(height_input)
            if height_val <= 0:
                messagebox.showerror(
                    "Failed input",
                    "Height must be a positive number."
                )
                return
            self.height_val = str(height_val)
        except ValueError:
            messagebox.showerror(
                "Failed input",
                "Please enter your height as a number in cm."
            )
            return

        # Validate weight
        if not weight_input:
            messagebox.showerror(
                "Failed input",
                "Please enter your weight as a number in kg."
            )
            return

        try:
            weight_val = float(weight_input)
            if weight_val <= 0:
                messagebox.showerror(
                    "Failed input",
                    "Weight must be a positive number."
                )
                return
            self.weight_val = str(weight_val)
        except ValueError:
            messagebox.showerror(
                "Failed input",
                "Please enter your weight as a number in kg."
            )
            return

        try:
            value = bmi_calc(self.weight_val, self.height_val)
            self.bmi_val = value

            # Update display labels
            self.height_value_label.config(
                text=f"Height: {self.height_val} cm"
            )
            self.weight_value_label.config(
                text=f"Weight: {self.weight_val} kg"
            )
            self.bmi_label.config(
                text=f"BMI: {self.bmi_val} ({bmi_status(self.bmi_val)})"
            )

            # Saves metrics to the database
            save_metrics(self.user.user_id, float(self.height_val),
                         float(self.weight_val))
            messagebox.showinfo("Saved",
                                "Measurement data saved successfully.")

            # Clear entries
            self.height_entry.delete(0, 'end')
            self.weight_entry.delete(0, 'end')
        except (ValueError, ZeroDivisionError):
            messagebox.showerror(
                "Failed input",
                "Error in calculating BMI or saving data."
            )

    def download_records(self):
        """
        Downloads all past measurement records for the user to a text file.
        """
        try:
            # Fetch all metrics using db_handler function
            records = get_all_days_metrics(self.user.user_id)

            if not records:
                messagebox.showinfo(
                    "No Records",
                    "No measurement records found for this user."
                )
                return

            met_log_directory = os.path.join(
                os.path.dirname(__file__),
                "..",
                "metric_logs"
            )
            met_log_directory = os.path.abspath(met_log_directory)
            os.makedirs(met_log_directory, exist_ok=True)

            # Creates filename with current date
            current_date = datetime.now().strftime("%d-%m-%Y")
            filename = os.path.join(
                met_log_directory,
                f"metric_log_{current_date}.txt"
            )

            # Writes records to file
            with open(filename, 'w') as file:
                file.write(f"Measurement Records for {self.user.username}\n")
                file.write(
                    f"Downloaded on: {datetime.now().strftime('%d-%m-%Y %H:%M')}\n"
                )
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

            messagebox.showinfo(
                "Success",
                f"Records downloaded successfully to {filename}"
            )

        except Exception as e:
            messagebox.showerror("Error",
                                 f"Failed to download records: {str(e)}")

    def return_to_dash(self):
        """
        Returns to the dashboard screen.
        """
        return_to_dashboard(self.measureframe, self.root, self.user)


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007",
                     "29/08/2025")
    app = Measurement(root, test_user)
    root.mainloop()