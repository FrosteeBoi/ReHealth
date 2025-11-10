import ttkbootstrap as tb
from tkinter import messagebox
from logic.user import User
from db.db_handler import save_workout, get_all_workouts
from datetime import datetime
import os
from ui_handler import return_to_dashboard


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
        self.workout_label.grid(row=0, column=0, pady=(20, 30), columnspan=2)

        self.name_label = tb.Label(
            self.workoutframe,
            text="Exercise Name:",
            font=("roboto", 14)
        )
        self.name_label.grid(row=1, column=0, pady=(10, 10), sticky="e", padx=(0, 10))

        self.weight_label = tb.Label(
            self.workoutframe,
            text="Weight (kg):",
            font=("roboto", 14)
        )
        self.weight_label.grid(row=2, column=0, pady=(10, 10), sticky="e", padx=(0, 10))

        self.sets_label = tb.Label(
            self.workoutframe,
            text="Sets:",
            font=("roboto", 14)
        )
        self.sets_label.grid(row=3, column=0, pady=(10, 10), sticky="e", padx=(0, 10))

        self.reps_label = tb.Label(
            self.workoutframe,
            text="Reps:",
            font=("roboto", 14)
        )
        self.reps_label.grid(row=4, column=0, pady=(10, 10), sticky="e", padx=(0, 10))

        # Textboxes
        self.name_textbox = tb.Entry(self.workoutframe)
        self.name_textbox.grid(row=1, column=1, pady=(10, 10), padx=(10, 0))

        self.weight_textbox = tb.Entry(self.workoutframe)
        self.weight_textbox.grid(row=2, column=1, pady=(10, 10), padx=(10, 0))

        self.sets_textbox = tb.Entry(self.workoutframe)
        self.sets_textbox.grid(row=3, column=1, pady=(10, 10), padx=(10, 0))

        self.reps_textbox = tb.Entry(self.workoutframe)
        self.reps_textbox.grid(row=4, column=1, pady=(10, 10), padx=(10, 0))

        # Buttons
        self.exercise_add_button = tb.Button(
            self.workoutframe,
            text="Add Exercise",
            command=self.database_inc
        )
        self.exercise_add_button.grid(row=5, column=0, pady=(30, 10), columnspan=2)

        # Download Workout History Button
        self.download_button = tb.Button(
            self.workoutframe,
            text="Download Workout History",
            command=self.download_records
        )
        self.download_button.grid(row=6, column=0, pady=(10, 20), columnspan=2)

    def database_inc(self):
        self.exercise_name = self.name_textbox.get()
        if not self.exercise_name.strip() or not all(part.isalpha() for part in self.exercise_name.split()):
            messagebox.showerror(
                "Error",
                "Exercise name can only consist of letters and cannot be blank."
            )
            return

        self.exercise_weight = self.weight_textbox.get()
        if not self.exercise_weight.strip() or not self.exercise_weight.isdigit():
            messagebox.showerror("Error", "Enter a numerical weight value")
            return

        self.exercise_sets = self.sets_textbox.get()
        if not self.exercise_sets.strip() or not self.exercise_sets.isdigit():
            messagebox.showerror("Error", "Input a numerical weight value")
            return

        self.exercise_reps = self.reps_textbox.get()
        if not self.exercise_reps.strip() or not self.exercise_reps.isdigit():
            messagebox.showerror("Error", "Enter a numerical value for reps")
            return

        save_workout(
            self.user.user_id,
            self.exercise_name,
            self.exercise_weight,
            self.exercise_sets,
            self.exercise_reps
        )
        messagebox.showinfo("Success", f"{self.exercise_name} logged successfully!")

    def download_records(self):
        """
        Downloads all past workout records for the user to a text file
        """
        try:
            # Fetch all workouts using db_handler function
            records = get_all_workouts(self.user.user_id)

            if not records:
                messagebox.showinfo("No Records", "No workout records found for this user.")
                return

            # Create directory path for workout logs (relative to project root)
            met_log_directory = os.path.join(os.path.dirname(__file__), "..", "metric_logs")
            met_log_directory = os.path.abspath(met_log_directory)

            # Create directory if it doesn't exist
            os.makedirs(met_log_directory, exist_ok=True)

            # Create filename with current date
            current_date = datetime.now().strftime("%d-%m-%y")
            filename = os.path.join(met_log_directory, f"workout_log_{current_date}.txt")

            # Write records to file
            with open(filename, 'w') as file:
                file.write(f"Workout Records for {self.user.username}\n")
                file.write(f"Downloaded on: {datetime.now().strftime('%d-%m-%Y %H:%M')}\n")
                file.write("=" * 60 + "\n\n")

                for record in records:
                    date, exercise_name, weight, sets, reps = record

                    file.write(f"Date: {date}\n")
                    file.write(f"Exercise: {exercise_name}\n")
                    file.write(f"Weight: {weight} kg\n")
                    file.write(f"Sets: {sets}\n")
                    file.write(f"Reps: {reps}\n")
                    file.write("-" * 60 + "\n")

            messagebox.showinfo("Success", f"Workout records downloaded successfully to {filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to download records: {str(e)}")


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Workouts(root, test_user)
    root.mainloop()