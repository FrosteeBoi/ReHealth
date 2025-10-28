import ttkbootstrap as tb
from logic.user import User
from ui.measurement import Measurement
from ui.steps import Steps
from ui.sleep import Sleep
from ui.food import Food
from ui.workout import Workouts


class Dashboard:
    """
    Create a class for a dashboard gui that can access other parts of the application
    """

    def __init__(self, root, user: User):
        """
        initialises the dashboard gui
        """
        self.root = root
        self.user = user
        self.dashframe = tb.Frame(self.root)
        self.dashframe.grid(row=0, column=0, sticky="n")
        self.root.geometry("490x630")
        self.root.title("ReHealth")

        # Makes root expandable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Welcome label created
        self.dash_label = tb.Label(
            self.dashframe,
            text=f"Hello {self.user.username}",
            font=("roboto", 18, "bold")
        )
        self.dash_label.grid(row=0, column=0, pady=(20, 50), sticky="n")

        # Bottom frame made for tab buttons
        self.tab_frame = tb.Frame(self.dashframe)
        self.tab_frame.grid(row=4, column=0, sticky="n", pady=(420, 20), padx=5)

        # Tab buttons made
        self.measurements_button = tb.Button(
            self.tab_frame,
            text="Measurements",
            command=self.show_measurements
        )
        self.food_button = tb.Button(
            self.tab_frame,
            text="Food",
            command=self.show_food
        )
        self.workout_button = tb.Button(
            self.tab_frame,
            text="Workouts",
            command=self.show_workouts
        )
        self.sleep_button = tb.Button(
            self.tab_frame,
            text="Sleep",
            command=self.show_sleep
        )
        self.steps_button = tb.Button(
            self.tab_frame,
            text="Steps",
            command=self.show_steps
        )

        # Visual displays
        self.dash_steps = tb.Label(self.dashframe, text="Steps: 6767")
        self.dash_cals = tb.Label(self.dashframe, text="Calories: 6767")
        self.dash_sleep = tb.Label(self.dashframe, text="Sleep: 6767")

        # Grids the buttons
        self.measurements_button.grid(row=0, column=0, padx=5)
        self.food_button.grid(row=0, column=1, padx=5)
        self.workout_button.grid(row=0, column=2, padx=5)
        self.sleep_button.grid(row=0, column=3, padx=5)
        self.steps_button.grid(row=0, column=4, padx=5)

        # Grids the  visual displays
        self.dash_steps.grid(row=1, column=0)
        self.dash_cals.grid(row=2, column=0)
        self.dash_sleep.grid(row=3, column=0)

    # Placeholder methods for each tab
    def show_measurements(self):
        """Opens the measurement tab"""
        Measurement(self.root, self.user)

    def show_food(self):
        """Display the Food tab."""
        Food(self.root, self.user)

    def show_workouts(self):
        """Display the Workouts tab"""
        Workouts(self.root, self.user)

    def show_sleep(self):
        Sleep(self.root, self.user)


    def show_steps(self):
        """Opens the steps tab"""
        Steps(self.root, self.user)


class TestUser:
    """
    A simple test user class for standalone testing of the Dashboard.
    """

    def __init__(self, username):
        self.username = username


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = TestUser("TestUser")
    app = Dashboard(root, test_user)
    root.mainloop()
