import ttkbootstrap as tb
from tkinter import messagebox
from logic.user import User
from db.db_handler import save_steps


class Steps:
    """
    Class created to record measurements like user height, weight,
    and calculate BMI
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

        # Labels
        self.steps_label = tb.Label(
            self.stepframe,
            text=f"{self.user.username}'s Steps",
            font=("roboto", 18, "bold")
        )
        self.steps_label.grid(row=0, column=0, pady=(0, 0), columnspan=2, padx=(15, 0))

        self.count_label = tb.Label(
            self.stepframe,
            text=f"{self.step_count}",
            font=("roboto", 18, "bold")
        )
        self.count_label.grid(row=1, column=0, pady=(50, 50), padx=(15, 0), columnspan=2)

        self.step_record = tb.Label(
            self.stepframe,
            text="Record Your Steps:",
            font=("roboto", 18, "bold")
        )
        self.step_record.grid(row=2, column=0, pady=(0, 50))

        # Entry and Button initialised
        self.step_entry = tb.Entry(self.stepframe)
        self.step_entry.grid(row=2, column=1, padx=(10, 0), pady=(0, 50))

        self.step_button = tb.Button(self.stepframe, text="Add", command=self.step_inc)
        self.step_button.grid(row=2, column=2, pady=(0, 50))

    def step_inc(self):
        """
        Increments the amount of steps
        """
        try:
            value = int(self.step_entry.get())
            self.step_count = str(value)
            self.step_entry.delete(0, 'end')
            self.count_label.config(text=f"{self.step_count}")

            # Saves steps to the database
            save_steps(self.user.user_id, self.step_count, 10000)
        except ValueError:
            messagebox.showerror("Failed input", "Please enter your steps as an integer.")


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Steps(root, test_user)
    root.mainloop()
