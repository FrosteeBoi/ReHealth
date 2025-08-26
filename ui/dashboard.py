import ttkbootstrap as tb
import random
from tkinter import messagebox
from logic.user import User
import re
from datetime import datetime, date
from db.db_handler import save_user_to_db
import sqlite3
from ui.login import App


class Dashboard:
    def __init__(self, root, user: User):
        self.root = root
        self.user = user
        self.dashframe = tb.Frame(self.root)
        self.dashframe.grid(row=0, column = 0, sticky="nsew")

        # Dashboard widgets
        self.dash_label = tb.Label(self.dashframe, text=f"Hello {self.user.username}", font=("roboto", 15, "bold"))

        self.metrics_label = tb.Label(self.dashframe, text="Measurements", font=("roboto", 12, "bold"))

        self.food_label = tb.Label(self.dashframe, text="Food", font=("roboto", 12, "bold"))

        self.workout_label = tb.Label(self.dashframe, text="Workouts", font=("roboto", 12, "bold"))

        self.sleep_label = tb.Label(self.dashframe, text="Sleep", font=("roboto", 12, "bold"))

        self.steps_label = tb.Label(self.dashframe, text="Steps", font=("roboto", 12, "bold"))


root = tb.Window(themename="darkly")
app = Dashboard(root)
root.mainloop()



