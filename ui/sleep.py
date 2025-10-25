import ttkbootstrap as tb
from tkinter import messagebox
from logic.user import User
from logic.calculations import sleep_calc
from db.db_handler import save_sleep


class Sleep:
    """
    Class created to record user sleep and display it to the user
    """

    def __init__(self, root, user: User):
        """
        Main window for sleep tracking initialised
        """
        self.root = root
        self.user = user
        self.sleepframe = tb.Frame(self.root)
        self.sleepframe.grid(row=0, column=0, sticky="n")
        self.root.geometry("490x630")
        self.root.title("ReHealth")
        self.sleep_duration = None
        self.sleep_quality = None
        self.rating = None

        # Makes root expandable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Labels
        self.sleep_label = tb.Label(
            self.sleepframe,
            text=f"{self.user.username}'s Sleep",
            font=("roboto", 18, "bold")
        )
        self.sleep_label.grid(row=0, column=0, pady=(0, 0), columnspan=2, padx=(70, 0))

        self.rating_label = tb.Label(
            self.sleepframe,
            text="Sleep Rating:",
            font=("roboto", 18, "bold")
        )
        self.rating_label.grid(row=1, column=0, pady=(20, 20), padx=(70, 0), columnspan=2)

        self.sleep_hours_label = tb.Label(
            self.sleepframe,
            text="Record your hours:",
            font=("roboto", 18, "bold")
        )
        self.sleep_hours_label.grid(row=2, column=0, pady=(20, 20))

        self.sleep_entry = tb.Entry(self.sleepframe)
        self.sleep_entry.grid(row=2, column=1, pady=(20, 20))

        self.hours_button = tb.Button(
            self.sleepframe,
            text="Add",
            command=self.hours_inc
        )
        self.hours_button.grid(row=2, column=2, pady=(20, 20))

        self.sleep_refresh_label = tb.Label(
            self.sleepframe,
            text="Record how you feel(1-5):",
            font=("roboto", 18, "bold")
        )
        self.sleep_refresh_label.grid(row=3, column=0, pady=(20, 20))

        self.refresh_entry = tb.Entry(self.sleepframe)
        self.refresh_entry.grid(row=3, column=1, pady=(20, 20))

        self.refresh_button = tb.Button(
            self.sleepframe,
            text="Add",
            command=self.quality_inc
        )
        self.refresh_button.grid(row=3, column=2)

        self.rating_button = tb.Button(
            self.sleepframe,
            text="Calculate Rating",
            command=self.update_rating
        )
        self.rating_button.grid(row=4, column=0, pady=(20, 20), padx=(190, 0))

    def hours_inc(self):
        """Receive hours input from user to store"""
        try:
            hours = float(self.sleep_entry.get())
            if hours < 0 or hours > 24:
                raise ValueError
            self.sleep_duration = hours
            messagebox.showinfo("Success", f"Recorded {hours} hours of sleep.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of hours (0-24).")

    def quality_inc(self):
        """Get sleep quality input from user and store it."""
        try:
            quality = int(self.refresh_entry.get())
            if quality < 1 or quality > 5:
                raise ValueError
            self.sleep_quality = quality
            messagebox.showinfo("Success", f"Recorded sleep quality: {quality}/5.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid sleep quality (1-5).")

    def update_rating(self):
        """Calculates and displays sleep rating."""
        if self.sleep_duration is not None and self.sleep_quality is not None:
            self.rating = sleep_calc(self.sleep_duration, self.sleep_quality)
            self.rating_label.config(text=f"Sleep Rating: {round(self.rating * 100)}%")
            save_sleep(self.user.user_id, self.sleep_duration, self.rating)


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Sleep(root, test_user)
    root.mainloop()
