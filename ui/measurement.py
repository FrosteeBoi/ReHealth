import ttkbootstrap as tb
import random
from tkinter import messagebox
from logic.user import User
import re
from datetime import datetime, date
from db.db_handler import save_user_to_db
import sqlite3


class Measurement:
    def __init__(self, root, user: User):
        self.root = root
        self.user = user
        self.measureframe = tb.Frame(self.root)
        self.measureframe.grid(row=0, column=0, sticky="n")
        self.root.geometry("490x630")

        # Makes root expandable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Label that welcomes user
        self.measure_label = tb.Label(self.measureframe, text=f"{self.user.username}'s Measurements",
                                      font=("roboto", 18, "bold"))
        self.measure_label.grid(row=0, column=0, pady=(50, 50), padx=(100, 0), sticky="n")

        # Height, weight and bmi labels and entries
        self.height_label = tb.Label(self.measureframe, text="Height: \n 174cm", font=("roboto", 18, "bold"))
        self.height_label.grid(row=1, column=0, pady=(50, 0), sticky="w")

        self.weight_label = tb.Label(self.measureframe, text="Weight: \n 69kg", font=("roboto", 18, "bold"))
        self.weight_label.grid(row=1, column=1, pady=(50, 50), sticky="n")

        self.bmi_label = tb.Label(self.measureframe, text="Body Mass Index: \n 22.8", font=("roboto", 18, "bold"))
        self.bmi_label.grid(row=3, column=0, pady=(50, 50), sticky="n")

        self.height_entry = tb.Entry(self.measureframe)
        self.height_entry.grid(row=2, column=0, sticky="w", pady=(0, 50))

        self.weight_entry = tb.Entry(self.measureframe)
        self.weight_entry.grid(row=2, column=1, sticky="n", pady=(0, 50))



if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/082025")
    app = Measurement(root, test_user)
    root.mainloop()
