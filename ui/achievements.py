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
        self.achieveframe = tb.Frame(self.root)
        self.achieveframe.place(relx=0.5, rely=0, anchor="n")
        self.root.geometry("490x630")
        self.root.title("ReHealth")

        # Initialises measurement values as empty strings
        self.height_val = 0
        self.weight_val = 0
        self.bmi_val = 0

        # Labels initialised and placed
        self.measure_label = tb.Label(
            self.achieveframe,
            text=f"{self.user.username}'s Hall of Fame",
            font=("roboto", 18, "bold")
        )
        self.measure_label.grid(row=0, column=0, pady=(20, 30), columnspan=3,
                                padx=20)




















    def return_to_dash(self):
        """
        Returns to the dashboard screen.
        """
        return_to_dashboard(self.achieveframe, self.root, self.user)


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Measurement(root, test_user)
    root.mainloop()
