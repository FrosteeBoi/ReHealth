import ttkbootstrap as tb
from tkinter import messagebox
from logic.user import User
from db.db_handler import save_steps
from logic.calculations import calories_burnt
from db.db_handler import get_weight


class Steps:
    """
    Class created to record steps and display them to the user
    """

    def __init__(self, root, user: User):
        """
        Main window for measurement initialised
        """
        self.root = root
        self.user = user
        self.stepframe = tb.Frame(self.root)
        self.stepframe.grid(row=0, column=0, sticky="n")
        self.root.geometry("490x630")
        self.root.title("ReHealth")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # initialises variables
        self.step_count = 0
        self.calorie_count = 0

        # Labels
        self.steps_label = tb.Label(
            self.stepframe,
            text=f"{self.user.username}'s Steps",
            font=("roboto", 18, "bold")
        )
        self.steps_label.grid(row=0, column=0, pady=(20, 30), padx=20, columnspan=2)

        self.count_label = tb.Label(
            self.stepframe,
            text=f"Step Count: 0",
            font=("roboto", 14)
        )
        self.count_label.grid(row=1, column=0, pady=(10, 10), padx=20, columnspan=2)

        self.calorie_label = tb.Label(
            self.stepframe,
            text=f"Calories Burnt: 0 kcal",
            font=("roboto", 14)
        )
        self.calorie_label.grid(row=2, column=0, pady=(10, 30), padx=20, columnspan=2)

        # Entry and Button initialised
        self.step_entry = tb.Entry(self.stepframe, width=20)
        self.step_entry.grid(row=3, column=0, padx=(20, 10), pady=(10, 10))

        self.step_button = tb.Button(self.stepframe, text="Add Steps", command=self.steps_and_calories)
        self.step_button.grid(row=3, column=1, pady=(10, 10), padx=(10, 20))


    def step_inc(self):
        """
        Increments the amount of steps
        """
        try:
            value = int(self.step_entry.get())
            self.step_count = str(value)
            self.step_entry.delete(0, 'end')
            self.count_label.config(text=f"Step Count: {self.step_count}")

            # Saves steps to the database
            save_steps(self.user.user_id, self.step_count, 10000)
        except ValueError:
            messagebox.showerror("Failed input", "Please enter your steps as an integer.")

    def calorie_inc(self):
        """
        Calculates and updates calories burnt only if steps are recorded.
        """
        if self.step_count and str(self.step_count).isdigit():
            weight = get_weight(self.user.user_id)
            steps = int(self.step_count)
            self.calorie_count = calories_burnt(steps, weight)
            self.calorie_label.config(text=f"Calories Burnt: {round(self.calorie_count)} kcal")
        else:
            messagebox.showinfo("No Steps", "Please enter your steps first before calculating calories.")

    def steps_and_calories(self):
        self.step_inc()
        self.calorie_inc()


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Steps(root, test_user)
    root.mainloop()