import tkinter
import ttkbootstrap as tb
from tkinter import messagebox
from logic.user import User
from db.db_handler import save_workout


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
        self.workoutframe.grid(row=0, column=0, sticky="n", padx=(115, 0))

        # Window settings
        self.root.geometry("490x630")
        self.root.title("ReHealth")

        self.exercise_name = None
        self.exercise_weight = None
        self.exercise_reps = None
        self.exercise_sets =None

        # Labels
        self.workout_label = tb.Label(
            self.workoutframe,
            text=f"{self.user.username}'s Workouts",
            font=("roboto", 18, "bold")
        )
        self.workout_label.grid(row=0, column=1, pady=(0, 0), columnspan=2, padx=(0, 0))

        self.name_label = tb.Label(
            self.workoutframe,
            text="Exercise Name:",
            font=("roboto", 14)
        )
        self.name_label.grid(row=1, column=1, pady=(30, 0))

        self.weight_label = tb.Label(
            self.workoutframe,
            text="Weight (kg):",
            font=("roboto", 14)
        )

        self.weight_label.grid(row=2, column=1, pady=(30, 0))

        self.sets_label = tb.Label(
            self.workoutframe,
            text="Sets:",
            font=("roboto", 14)
        )
        self.sets_label.grid(row=3, column=1, pady=(30, 0))

        self.reps_label = tb.Label(
            self.workoutframe,
            text="Reps:",
            font=("roboto", 14)
        )
        self.reps_label.grid(row=4, column=1, pady=(30, 0))

        # textboxes

        self.name_textbox = tb.Entry(self.workoutframe)
        self.name_textbox.grid(row=1, column=2, pady=(30, 0))

        self.weight_textbox = tb.Entry(self.workoutframe)
        self.weight_textbox.grid(row=2, column=2, pady=(30, 0))

        self.sets_textbox = tb.Entry(
            self.workoutframe,
        )
        self.sets_textbox.grid(row=3, column=2, pady=(30, 0))

        self.reps_textbox = tb.Entry(
            self.workoutframe,
        )
        self.reps_textbox.grid(row=4, column=2, pady=(30, 0))

        # Buttons

        self.exercise_add_button = tb.Button(
            self.workoutframe,
            text="Add Exercise",
            command=self.database_inc
        )
        self.exercise_add_button.grid(row=5, column=1, pady=(30, 0), padx=(40, 0), columnspan=2)

    def database_inc(self):
        self.exercise_name = self.name_textbox.get()
        if not self.exercise_name.strip() or not all(part.isalpha() for part in self.exercise_name.split()):
            messagebox.showerror("Error", "Exercise name can only consist of letters and cannot be blank.")
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
        save_workout(self.user.user_id, self.exercise_name, self.exercise_weight, self.exercise_sets, self.exercise_reps)
        messagebox.showinfo("Success",f"{self.exercise_name} logged successfully!")


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Workouts(root, test_user)
    root.mainloop()
