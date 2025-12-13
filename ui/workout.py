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
        self.name_textbox.grid(row=1, column=1, pady=(10, 10), padx=(10, 20), columnspan=2)

        # Weight Section
        self.weight_label = tb.Label(
            self.workoutframe,
            text="Weight (Kg):",
            font=("roboto", 14)
        )
        self.weight_label.grid(row=2, column=0, pady=(10, 10), sticky="e",
                               padx=(20, 10))

        self.weight_textbox = tb.Entry(self.workoutframe, width=20)
        self.weight_textbox.grid(row=2, column=1, pady=(10, 10), padx=(10, 20), columnspan=2)

        # Sets Section
        self.sets_label = tb.Label(
            self.workoutframe,
            text="Sets:",
            font=("roboto", 14)
        )
        self.sets_label.grid(row=3, column=0, pady=(10, 10), sticky="e",
                             padx=(20, 10))

        self.sets_textbox = tb.Entry(self.workoutframe, width=20)
        self.sets_textbox.grid(row=3, column=1, pady=(10, 10), padx=(10, 20), columnspan=2)

        # Reps Section
        self.reps_label = tb.Label(
            self.workoutframe,
            text="Reps:",
            font=("roboto", 14)
        )
        self.reps_label.grid(row=4, column=0, pady=(10, 10), sticky="e",
                             padx=(20, 10))

        self.reps_textbox = tb.Entry(self.workoutframe, width=20)
        self.reps_textbox.grid(row=4, column=1, pady=(10, 10), padx=(10, 10), columnspan=2)

        # Main Action Buttons
        self.button_frame = tb.Frame(self.workoutframe)
        self.button_frame.grid(row=5, column=0, columnspan=3, pady=(30, 10))

        self.exercise_add_button = tb.Button(
            self.button_frame,
            text="Log Workout",
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
        self.dash_button.grid(row=6, column=0, columnspan=3, pady=(230, 20),
                              padx=20)

    def database_inc(self):
        """
        Validates and saves exercise data to the database
        """
        # Get values from entries
        exercise_name = self.name_textbox.get().strip()
        exercise_weight = self.weight_textbox.get().strip()
        exercise_sets = self.sets_textbox.get().strip()
        exercise_reps = self.reps_textbox.get().strip()

        # Validate exercise name
        if not exercise_name:
            messagebox.showerror("Error", "Exercise name cannot be empty.")
            self.name_textbox.focus()
            return

        if not all(part.isalpha() or part.isspace() for part in exercise_name):
            messagebox.showerror(
                "Error",
                "Exercise name can only contain letters."
            )
            self.name_textbox.focus()
            return

        # Validate weight
        if not exercise_weight:
            messagebox.showerror("Error", "Weight cannot be empty.")
            self.weight_textbox.focus()
            return

        if not exercise_weight.replace('.', '', 1).isdigit():
            messagebox.showerror("Error", "Enter a numerical weight value.")
            self.weight_textbox.focus()
            return

        try:
            weight_val = float(exercise_weight)
            if weight_val <= 0:
                messagebox.showerror("Error", "Weight must be a positive number.")
                self.weight_textbox.focus()
                return
        except ValueError:
            messagebox.showerror("Error", "Enter a valid weight value.")
            self.weight_textbox.focus()
            return

        # Validate sets
        if not exercise_sets:
            messagebox.showerror("Error", "Sets cannot be empty.")
            self.sets_textbox.focus()
            return

        if not exercise_sets.isdigit():
            messagebox.showerror("Error", "Enter a numerical value for sets.")
            self.sets_textbox.focus()
            return

        sets_val = int(exercise_sets)
        if sets_val <= 0:
            messagebox.showerror("Error", "Sets must be a positive number.")
            self.sets_textbox.focus()
            return

        # Validate reps
        if not exercise_reps:
            messagebox.showerror("Error", "Reps cannot be empty.")
            self.reps_textbox.focus()
            return

        if not exercise_reps.isdigit():
            messagebox.showerror("Error", "Enter a numerical value for reps.")
            self.reps_textbox.focus()
            return

        reps_val = int(exercise_reps)
        if reps_val <= 0:
            messagebox.showerror("Error", "Reps must be a positive number.")
            self.reps_textbox.focus()
            return

        # All fields are valid, save to database
        try:
            save_workout(
                self.user.user_id,
                exercise_name,
                exercise_weight,
                exercise_sets,
                exercise_reps
            )
            messagebox.showinfo(
                "Success",
                f"{exercise_name}: {exercise_weight}kg x {exercise_sets} sets x {exercise_reps} reps logged successfully!"
            )

            # Clear all fields after successful save
            self.name_textbox.delete(0, 'end')
            self.weight_textbox.delete(0, 'end')
            self.sets_textbox.delete(0, 'end')
            self.reps_textbox.delete(0, 'end')
            self.name_textbox.focus()

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