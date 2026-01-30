"""Workout Module - ReHealth"""

import os
from datetime import datetime
from tkinter import messagebox

import ttkbootstrap as tb

from db.db_handler import save_workout, get_all_workouts
from logic.user import User
from ui.ui_handler import return_to_dashboard, BasePage


def validate_exercise_name(exercise_name: str) -> tuple[bool, str]:
    """
    Validates the exercise name input.

    Args:
        exercise_name: Raw text input from the exercise name entry field.

    Returns:
        A tuple of (is_valid, error_message).
        If valid, error_message is empty.
    """
    if not exercise_name:
        return False, "Exercise name cannot be empty."

    if not all(part.isalpha() or part.isspace() for part in exercise_name):
        return False, "Exercise name can only contain letters."

    return True, ""


def validate_weight(weight_input: str) -> tuple[bool, float, str]:
    """
    Validates the weight input.

    Args:
        weight_input: Raw text input from the weight entry field.

    Returns:
        A tuple of (is_valid, weight_value, error_message).
        If valid, error_message is empty.
    """
    if not weight_input:
        return False, 0.0, "Weight cannot be empty."

    try:
        weight_val = float(weight_input)
    except ValueError:
        return False, 0.0, "Enter a numerical weight value."

    if weight_val < 1 or weight_val > 3000:
        return False, 0.0, "Weight must be a positive value between 1 and 3000 inclusive."

    return True, weight_val, ""


def validate_sets(sets_input: str) -> tuple[bool, int, str]:
    """
    Validates the sets input.

    Args:
        sets_input: Raw text input from the sets entry field.

    Returns:
        A tuple of (is_valid, sets_value, error_message).
        If valid, error_message is empty.
    """
    if not sets_input:
        return False, 0, "Sets cannot be empty."

    if not sets_input.isdigit():
        return False, 0, "Enter an integer, numerical and positive value for sets."

    sets_val = int(sets_input)
    if sets_val < 1 or sets_val > 50:
        return False, 0, "The amount of sets entered must be a positive number between 1 and 50 inclusive."

    return True, sets_val, ""


def validate_reps(reps_input: str) -> tuple[bool, int, str]:
    """
    Validates the reps input.

    Args:
        reps_input: Raw text input from the reps entry field.

    Returns:
        A tuple of (is_valid, reps_value, error_message).
        If valid, error_message is empty.
    """
    if not reps_input:
        return False, 0, "Reps cannot be empty."

    if not reps_input.isdigit():
        return False, 0, "Enter an integer, numerical and positive value for reps."

    reps_val = int(reps_input)
    if reps_val <1 or reps_val > 50:
        return False, 0, "The amount of reps entered must be a positive number between 1 and 50 inclusive."

    return True, reps_val, ""


class Workouts(BasePage):
    """Workout tracking screen: validates exercise input, saves to database, and exports workout history."""

    def __init__(self, root: tb.Window, user: User) -> None:
        """
        Args:
            root: Main application window.
            user: Logged-in user (used for user_id and username).
        """
        # Initialise state
        self.exercise_name = None
        self.exercise_weight = None
        self.exercise_reps = None
        self.exercise_sets = None

        # Call parent constructor
        super().__init__(root, user, "Workouts")

    def _build_ui(self) -> None:
        """Build all UI components."""
        self._create_title()
        self._create_input_section()
        self._create_action_buttons()
        self._create_dashboard_button()

    def _create_title(self) -> None:
        """Create the main title label."""
        self.workout_label = tb.Label(
            self.frame,
            text=f"{self.user.username}'s Workouts",
            font=("roboto", 18, "bold")
        )
        self.workout_label.grid(row=0, column=0, pady=(20, 30), columnspan=3, padx=20)

    def _create_input_section(self) -> None:
        """Create all input fields for exercise data."""
        # Exercise Name Section
        self.name_label = tb.Label(
            self.frame,
            text="Exercise Name:",
            font=("roboto", 14)
        )
        self.name_label.grid(row=1, column=0, pady=(10, 10), sticky="e", padx=(20, 10))

        self.name_textbox = tb.Entry(self.frame, width=20)
        self.name_textbox.grid(row=1, column=1, pady=(10, 10), padx=(10, 20), columnspan=2)

        # Weight Section
        self.weight_label = tb.Label(
            self.frame,
            text="Weight (Kg):",
            font=("roboto", 14)
        )
        self.weight_label.grid(row=2, column=0, pady=(10, 10), sticky="e", padx=(20, 10))

        self.weight_textbox = tb.Entry(self.frame, width=20)
        self.weight_textbox.grid(row=2, column=1, pady=(10, 10), padx=(10, 20), columnspan=2)

        # Sets Section
        self.sets_label = tb.Label(
            self.frame,
            text="Sets:",
            font=("roboto", 14)
        )
        self.sets_label.grid(row=3, column=0, pady=(10, 10), sticky="e", padx=(20, 10))

        self.sets_textbox = tb.Entry(self.frame, width=20)
        self.sets_textbox.grid(row=3, column=1, pady=(10, 10), padx=(10, 20), columnspan=2)

        # Reps Section
        self.reps_label = tb.Label(
            self.frame,
            text="Reps:",
            font=("roboto", 14)
        )
        self.reps_label.grid(row=4, column=0, pady=(10, 10), sticky="e", padx=(20, 10))

        self.reps_textbox = tb.Entry(self.frame, width=20)
        self.reps_textbox.grid(row=4, column=1, pady=(10, 10), padx=(10, 10), columnspan=2)

    def _create_action_buttons(self) -> None:
        """Create the log workout and download buttons."""
        self.button_frame = tb.Frame(self.frame)
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

    def _create_dashboard_button(self) -> None:
        """Create the back to dashboard button."""
        self.dash_button = tb.Button(
            self.frame,
            text="Back to Dashboard",
            command=self.return_to_dash
        )
        self.dash_button.grid(row=6, column=0, columnspan=3, pady=(230, 20), padx=20)

    def database_inc(self) -> None:
        """
        Validates and saves exercise data to the database.
        """
        # Get values from entries
        exercise_name = self.name_textbox.get().strip()
        exercise_weight = self.weight_textbox.get().strip()
        exercise_sets = self.sets_textbox.get().strip()
        exercise_reps = self.reps_textbox.get().strip()

        # Validate exercise name
        name_valid, name_error = validate_exercise_name(exercise_name)
        if not name_valid:
            messagebox.showerror("Error", name_error)
            self.name_textbox.focus()
            return

        # Validate weight
        weight_valid, weight_val, weight_error = validate_weight(exercise_weight)
        if not weight_valid:
            messagebox.showerror("Error", weight_error)
            self.weight_textbox.focus()
            return

        # Validate sets
        sets_valid, sets_val, sets_error = validate_sets(exercise_sets)
        if not sets_valid:
            messagebox.showerror("Error", sets_error)
            self.sets_textbox.focus()
            return

        # Validate reps
        reps_valid, reps_val, reps_error = validate_reps(exercise_reps)
        if not reps_valid:
            messagebox.showerror("Error", reps_error)
            self.reps_textbox.focus()
            return

        try:
            self._save_and_clear(exercise_name, exercise_weight, exercise_sets, exercise_reps)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save workout: {str(e)}")

    def _save_and_clear(self, exercise_name: str, weight: str, sets: str, reps: str) -> None:
        """
        Saves workout to database and clears input fields.

        Args:
            exercise_name: Name of the exercise.
            weight: Weight lifted in kg.
            sets: Number of sets performed.
            reps: Number of reps per set.
        """
        # Save to database
        save_workout(
            self.user.user_id,
            exercise_name,
            weight,
            sets,
            reps
        )

        # Show success message
        messagebox.showinfo(
            "Success",
            f"{exercise_name}: {weight}kg x {sets} sets x {reps} reps logged successfully!"
        )

        # Clear all fields for next entry
        self.name_textbox.delete(0, 'end')
        self.weight_textbox.delete(0, 'end')
        self.sets_textbox.delete(0, 'end')
        self.reps_textbox.delete(0, 'end')
        self.name_textbox.focus()

    def download_records(self) -> None:
        """
        Downloads all past workout records for the user to a text file.
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

            # Create directory path for workout logs
            met_log_directory = os.path.join(
                os.path.dirname(__file__),
                "..",
                "metric_logs"
            )
            met_log_directory = os.path.abspath(met_log_directory)
            os.makedirs(met_log_directory, exist_ok=True)

            # Create filename with current date
            current_date = datetime.now().strftime("%d-%m-%y")
            filename = os.path.join(
                met_log_directory,
                f"{self.user.username}_workout_log_{current_date}.txt"
            )

            # Write records to file
            self._write_workout_file(filename, records)

            messagebox.showinfo(
                "Success",
                f"Workout records downloaded successfully to {filename}"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to download records: {str(e)}")

    def _write_workout_file(self, filename: str, records: list) -> None:
        """
        Writes workout records to a text file.

        Args:
            filename: Path to the output file.
            records: List of workout records from database.
        """
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

    def return_to_dash(self) -> None:
        """
        Returns to the dashboard screen.
        """
        return_to_dashboard(self.frame, self.root, self.user)


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Workouts(root, test_user)
    root.mainloop()