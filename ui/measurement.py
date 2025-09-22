import ttkbootstrap as tb
import random
from tkinter import messagebox
from logic.user import User
import re
from datetime import datetime, date
from db.db_handler import save_user_to_db
import sqlite3


"""
This module contains the Measurement class for recording user height,
weight, and calculating BMI in a tkinter-based GUI.
"""


class Measurement:
    """
    Class created to record measurements like user height.
    """

    def __init__(self, root, user: User):
        """
        Measurement gui is created
        """
        self.root = root
        self.user = user
        self.measureframe = tb.Frame(self.root)
        self.measureframe.grid(row=0, column=0, sticky="n")
        self.root.geometry("490x630")

        # Makes root expandable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Label that welcomes user
        self.measure_label = tb.Label(
            self.measureframe,
            text=f"{self.user.username}'s Measurements",
            font=("roboto", 18, "bold")
        )
        self.measure_label.grid(row=0, column=0, pady=(0, 0), padx=(0, 0), sticky="n")

        # Height, weight and BMI labels
        self.height_label = tb.Label(
            self.measureframe,
            text="Record Your Height:",
            font=("roboto", 18, "bold")
        )
        self.height_label.grid(row=1, column=0, pady=(50, 50), padx=(0, 0))

        self.weight_label = tb.Label(
            self.measureframe,
            text="Record Your Weight:",
            font=("roboto", 18, "bold")
        )
        self.weight_label.grid(row=2, column=0, padx=(0, 0), pady=(0, 50))

        self.bmi_label = tb.Label(
            self.measureframe,
            text="Body Mass Index:",
            font=("roboto", 18, "bold")
        )
        self.bmi_label.grid(row=3, column=0, pady=(0, 50))

        # Entries for user input
        self.height_entry = tb.Entry(self.measureframe)
        self.height_entry.grid(row=1, column=1, padx=(0, 0), pady=(50, 50))

        self.weight_entry = tb.Entry(self.measureframe)
        self.weight_entry.grid(row=2, column=1, padx=(0, 0), pady=(0, 50))

        # Buttons and BMI display
        self.bmi_display = tb.Label(self.measureframe, text="BMI")
        self.bmi_display.grid(row=3, column=1, padx=(0, 0), pady=(0, 50))

        self.height_button = tb.Button(self.measureframe, text="Add")
        self.height_button.grid(row=1, column=2)

        self.weight_button = tb.Button(self.measureframe, text="Add")
        self.weight_button.grid(row=2, column=2, pady=(0, 50))


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/082025")
    app = Measurement(root, test_user)
    root.mainloop()
