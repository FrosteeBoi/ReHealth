import os
from datetime import datetime
from tkinter import messagebox

import ttkbootstrap as tb

from db.db_handler import save_workout, get_all_workouts
from logic.user import User
from ui.ui_handler import return_to_dashboard


class Workouts:
    """
    Class created to manage and add user exercises
    """

    def __init__(self, root, user: User):
        """
        Main window for managing exercises initialised
        """
        self.root = root
        self.user = user

        # Main frame
        self.workoutframe = tb.Frame(self.root)
        self.workoutframe.place(relx=0.5, rely=0, anchor="n")

        # Window settings
        self.root.geometry("490x630")
        self.root.title("ReHealth")

        self.exercise_name = None
        self.exercise_weight = None
        self.exercise_reps = None
        self.exercise_sets = None

        # Labels
        self.workout_label = tb.Label(
            self.workoutframe,
            text=f"{self.user.username}'s Workouts",
            font=("roboto", 18, "bold")
        )
        self.workout_label.grid(row=0, column=0, pady=(20, 30), columnspan=3, padx=20)

        # Exercise Name Section
        self.name_label = tb.Label(
            self.workoutframe,
            text="Exercise Name:",
            font=("roboto", 14)
        )
        self.name_label.grid(row=1, column=0, pady=(10, 10), sticky="e",
                             padx=(20, 10))

        self.name_textbox = tb.Entry(self.workoutframe, width=20)
        self.name_textbox.grid(row=1, column=1, pady=(10, 10), padx=(10, 10))

        self.name_add_button = tb.Button(
            self.workoutframe,
            text="Add",
            command=self.name_inc,
            width=8
        )
        self.name_add_button.grid(row=1, column=2, pady=(10, 10), padx=(10, 20))

        # Weight Section
        self.weight_label = tb.Label(
            self.workoutframe,
            text="Weight (kg):",
            font=("roboto", 14)
        )
        self.weight_label.grid(row=2, column=0, pady=(10, 10), sticky="e",
                               padx=(20, 10))

        self.weight_textbox = tb.Entry(self.workoutframe, width=20)
        self.weight_textbox.grid(row=2, column=1, pady=(10, 10), padx=(10, 10))

        self.weight_add_button = tb.Button(
            self.workoutframe,
            text="Add",
            command=self.weight_inc,
            width=8
        )
        self.weight_add_button.grid(row=2, column=2, pady=(10, 10), padx=(10, 20))

        # Sets Section
        self.sets_label = tb.Label(
            self.workoutframe,
            text="Sets:",
            font=("roboto", 14)
        )
        self.sets_label.grid(row=3, column=0, pady=(10, 10), sticky="e",
                             padx=(20, 10))

        self.sets_textbox = tb.Entry(self.workoutframe, width=20)
        self.sets_textbox.grid(row=3, column=1, pady=(10, 10), padx=(10, 10))

        self.sets_add_button = tb.Button(
            self.workoutframe,
            text="Add",
            command=self.sets_inc,
            width=8
        )
        self.sets_add_button.grid(row=3, column=2, pady=(10, 10), padx=(10, 20))

        # Reps Section
        self.reps_label = tb.Label(
            self.workoutframe,
            text="Reps:",
            font=("roboto", 14)
        )
        self.reps_label.grid(row=4, column=0, pady=(10, 10), sticky="e",
                             padx=(20, 10))

        self.reps_textbox = tb.Entry(self.workoutframe, width=20)
        self.reps_textbox.grid(row=4, column=1, pady=(10, 10), padx=(10, 10))

        self.reps_add_button = tb.Button(
            self.workoutframe,
            text="Add",
            command=self.reps_inc,
            width=8
        )
        self.reps_add_button.grid(row=4, column=2, pady=(10, 10), padx=(10, 20))

        # Main Action Buttons
        self.button_frame = tb.Frame(self.workoutframe)
        self.button_frame.grid(row=5, column=0, columnspan=3, pady=(30, 10))

        self.exercise_add_button = tb.Button(
            self.button_frame,
            text="Add to Database",
            command=self.database_inc
        )
        self.exercise_add_button.grid(row=0, column=0, padx=(0, 5))

        self.download_button = tb.Button(
            self.button_frame,
            text="Download Workout History",
            command=self.download_records
        )
        self.download_button.grid(row=0, column=1, padx=(5, 0))

        # Back to Dashboard Button
        self.dash_button = tb.Button(
            self.workoutframe,
            text="Back to Dashboard",
            command=self.return_to_dash
        )
        self.dash_button.grid(row=6, column=0, columnspan=3, pady=(160, 20),
                              padx=20)

    def name_inc(self):
        """
        Records exercise name
        """
        self.exercise_name = self.name_textbox.get()
        if not self.exercise_name.strip():
            messagebox.showerror("Error", "Exercise name cannot be empty.")
            return
        if not all(part.isalpha() or part.isspace() for part in self.exercise_name):
            messagebox.showerror(
                "Error",
                "Exercise name can only contain letters."
            )
            return
        self.name_textbox.delete(0, 'end')
        messagebox.showinfo("Success", f"Exercise: {self.exercise_name} recorded!")

    def weight_inc(self):
        """
        Records weight value
        """
        self.exercise_weight = self.weight_textbox.get()
        if not self.exercise_weight.strip():
            messagebox.showerror("Error", "Weight cannot be empty.")
            return
        if not self.exercise_weight.replace('.', '', 1).isdigit():
            messagebox.showerror("Error", "Enter a numerical weight value.")
            return
        self.weight_textbox.delete(0, 'end')
        messagebox.showinfo("Success", f"Weight: {self.exercise_weight} kg recorded!")

    def sets_inc(self):
        """
        Records number of sets
        """
        self.exercise_sets = self.sets_textbox.get()
        if not self.exercise_sets.strip():
            messagebox.showerror("Error", "Sets cannot be empty.")
            return
        if not self.exercise_sets.isdigit():
            messagebox.showerror("Error", "Enter a numerical value for sets.")
            return
        self.sets_textbox.delete(0, 'end')
        messagebox.showinfo("Success", f"Sets: {self.exercise_sets} recorded!")

    def reps_inc(self):
        """
        Records number of reps
        """
        self.exercise_reps = self.reps_textbox.get()
        if not self.exercise_reps.strip():
            messagebox.showerror("Error", "Reps cannot be empty.")
            return
        if not self.exercise_reps.isdigit():
            messagebox.showerror("Error", "Enter a numerical value for reps.")
            return
        self.reps_textbox.delete(0, 'end')
        messagebox.showinfo("Success", f"Reps: {self.exercise_reps} recorded!")

    def database_inc(self):
        """
        Validates and saves exercise data to the database
        """
        # Check if all fields are filled
        if self.exercise_name is None or not self.exercise_name.strip():
            messagebox.showerror(
                "Missing Information",
                "Please enter an exercise name first!"
            )
            return

        if self.exercise_weight is None or not str(self.exercise_weight).strip():
            messagebox.showerror(
                "Missing Information",
                "Please enter the weight first!"
            )
            return

        if self.exercise_sets is None or not str(self.exercise_sets).strip():
            messagebox.showerror(
                "Missing Information",
                "Please enter the number of sets first!"
            )
            return

        if self.exercise_reps is None or not str(self.exercise_reps).strip():
            messagebox.showerror(
                "Missing Information",
                "Please enter the number of reps first!"
            )
            return

        # All fields are valid, save to database
        try:
            save_workout(
                self.user.user_id,
                self.exercise_name,
                self.exercise_weight,
                self.exercise_sets,
                self.exercise_reps
            )
            messagebox.showinfo(
                "Success",
                f"{self.exercise_name}: {self.exercise_weight}kg x {self.exercise_sets} sets x {self.exercise_reps} reps logged successfully!"
            )

            # Reset fields after successful save
            self.exercise_name = None
            self.exercise_weight = None
            self.exercise_sets = None
            self.exercise_reps = None

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"Failed to save workout: {str(e)}"
            )

    def download_records(self):
        """
        Downloads all past workout records for the user to a text file
        """
        try:
            # Fetch all workouts using db_handler function
            records = get_all_workouts(self.user.user_id)

            if not records:
                messagebox.showinfo(
                    "No Records",
                    "No workout records found for this user."
                )
                return

            # Create directory path for workout logs (relative to project root)
            met_log_directory = os.path.join(
                os.path.dirname(__file__),
                "..",
                "metric_logs"
            )
            met_log_directory = os.path.abspath(met_log_directory)

            # Create directory if it doesn't exist
            os.makedirs(met_log_directory, exist_ok=True)

            # Create filename with current date
            current_date = datetime.now().strftime("%d-%m-%y")
            filename = os.path.join(
                met_log_directory,
                f"workout_log_{current_date}.txt"
            )

            # Write records to file
            with open(filename, 'w') as file:
                file.write(f"Workout Records for {self.user.username}\n")
                file.write(
                    f"Downloaded on: {datetime.now().strftime('%d-%m-%Y %H:%M')}\n"
                )
                file.write("=" * 60 + "\n\n")

                for record in records:
                    date, exercise_name, weight, sets, reps = record

                    file.write(f"Date: {date}\n")
                    file.write(f"Exercise: {exercise_name}\n")
                    file.write(f"Weight: {weight} kg\n")
                    file.write(f"Sets: {sets}\n")
                    file.write(f"Reps: {reps}\n")
                    file.write("-" * 60 + "\n")

            messagebox.showinfo(
                "Success",
                f"Workout records downloaded successfully to {filename}"
            )

        except Exception as e:
            messagebox.showerror("Error",
                                 f"Failed to download records: {str(e)}")

    def return_to_dash(self):
        """
        Returns to the dashboard screen
        """
        return_to_dashboard(self.workoutframe, self.root, self.user)


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007",
                     "29/08/2025")
    app = Workouts(root, test_user)
    root.mainloop()