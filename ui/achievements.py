import os
from datetime import datetime
from tkinter import messagebox
import ttkbootstrap as tb
from db.db_handler import get_total_steps, get_total_calories, get_total_sleep_hours
from logic.calculations import bmi_calc, bmi_status
from logic.user import User
from ui.ui_handler import return_to_dashboard


class Achievements:
    """
    Class created to view user achievements.
    """

    def __init__(self, root, user: User):
        """
        Main window for achievements initialised.
        """
        self.root = root
        self.user = user
        self.root.geometry("490x630")
        self.root.title("ReHealth")

        # --- Main frame (centred) ---
        self.achieveframe = tb.Frame(self.root)
        self.achieveframe.place(relx=0.5, rely=0.05, anchor="n")

        # --- Fetch totals ---
        total_steps = get_total_steps(self.user.user_id)
        total_cals = get_total_calories(self.user.user_id)
        total_sleep = get_total_sleep_hours(self.user.user_id)

        # --- Title ---
        self.achieve_label = tb.Label(
            self.achieveframe,
            text=f"{self.user.username}'s Hall of Fame",
            font=("roboto", 18, "bold")
        )
        self.achieve_label.grid(row=0, column=0, pady=(10, 20), sticky="n")

        # --- Achievements Items (all centred) ---

        self.steps_label = tb.Label(
            self.achieveframe,
            text=f"Total Steps Taken: {total_steps:,}",
            font=("roboto", 14, "bold")
        )
        self.steps_label.grid(row=1, column=0, pady=10, sticky="n")

        self.cals_label = tb.Label(
            self.achieveframe,
            text=f"Total Calories Burnt: {total_cals:,}",
            font=("roboto", 14, "bold")
        )
        self.cals_label.grid(row=2, column=0, pady=10, sticky="n")

        self.sleep_label = tb.Label(
            self.achieveframe,
            text=f"Total Hours Slept: {total_sleep:.1f}",
            font=("roboto", 14, "bold")
        )
        self.sleep_label.grid(row=3, column=0, pady=10, sticky="n")

        # --- Button (centred) ---
        self.dash_button = tb.Button(
            self.achieveframe,
            text="Back to Dashboard",
            command=self.return_to_dash,
            width=22
        )
        self.dash_button.grid(row=4, column=0, pady=(340, 10), sticky="n")

        # Extra spacing at bottom
        self.achieveframe.grid_rowconfigure(5, minsize=200)

    def return_to_dash(self):
        """
        Returns to the dashboard screen.
        """
        return_to_dashboard(self.achieveframe, self.root, self.user)


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    test_user.user_id = 1  # TEMP for testing
    app = Achievements(root, test_user)
    root.mainloop()
