import ttkbootstrap as tb
import random
from tkinter import messagebox
from logic.user import User
import re
from datetime import datetime, date
from db.db_handler import save_user_to_db
from measurement import Measurement


class Dashboard:
    def __init__(self, root, user: User):
        self.root = root
        self.user = user
        self.dashframe = tb.Frame(self.root)
        self.dashframe.grid(row=0, column=0, sticky="n")
        self.root.geometry("490x630")

        # Makes root expandable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Label that welcomes user
        self.dash_label = tb.Label(self.dashframe, text=f"Hello {self.user.username}", font=("roboto", 18, "bold"))
        self.dash_label.grid(row=0, column=0, pady=(20, 50), sticky="n")

        # Bottom frame for tabs
        self.tab_frame = tb.Frame(self.dashframe)
        self.tab_frame.grid(row=4, column=0, sticky="n", pady=(420, 20), padx=5)

        # Creates buttons for the tabs
        self.measurements_button = tb.Button(self.tab_frame, text="Measurements", command=self.show_measurements)
        self.food_button = tb.Button(self.tab_frame, text="Food", command=self.show_food)
        self.workout_button = tb.Button(self.tab_frame, text="Workouts", command=self.show_workouts)
        self.sleep_button = tb.Button(self.tab_frame, text="Sleep", command=self.show_sleep)
        self.steps_button = tb.Button(self.tab_frame, text="Steps", command=self.show_steps)

        # Creates the visual displays
        self.dash_steps = tb.Label(self.dashframe, text="Steps: 6767")
        self.dash_cals = tb.Label(self.dashframe, text="Calories: 6767")
        self.dash_sleep = tb.Label(self.dashframe, text="Sleep: 6767")

        # Grids the buttons
        self.measurements_button.grid(row=0, column=0, padx=5)
        self.food_button.grid(row=0, column=1, padx=5)
        self.workout_button.grid(row=0, column=2, padx=5)
        self.sleep_button.grid(row=0, column=3, padx=5)
        self.steps_button.grid(row=0, column=4, padx=5)

        # Grids the visual displays:
        self.dash_steps.grid(row=1, column=0)
        self.dash_cals.grid(row=2, column=0)
        self.dash_sleep.grid(row=3, column=0)

    # Placeholder methods for each tab
    def show_measurements(self):
        Measurement(self.root, self.user)

    def show_food(self):
        print("Show food")

    def show_workouts(self):
        print("Show workouts")

    def show_sleep(self):
        print("Show sleep")

    def show_steps(self):
        print("Show steps")


class TestUser:
    def __init__(self, username):
        self.username = username


if __name__ == "__main__":

    root = tb.Window(themename="darkly")
    test_user = TestUser("TestUser")
    app = Dashboard(root, test_user)
    root.mainloop()
