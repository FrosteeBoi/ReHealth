import ttkbootstrap as tb
from logic.user import User
from ui.measurement import Measurement
from ui.steps import Steps
from ui.sleep import Sleep
from ui.food import Food
from ui.workout import Workouts
from db.dashboard_data import get_sleep, get_steps, get_calories


class Dashboard:
    """
    Create a dashboard class inherited from a base page
    that allows navigation to other windows
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

        # Initial welcome label created
        self.dash_label = tb.Label(
            self.dashframe,
            text=f"Hello {self.user.username}",
            font=("roboto", 18, "bold")
        )
        self.dash_label.grid(row=0, column=0, pady=(20, 30), sticky="n")

        # Bottom frame made for tab buttons
        self.tab_frame = tb.Frame(self.dashframe)
        self.tab_frame.grid(row=4, column=0, sticky="n", pady=(390, 20), padx=5)

        # Tab buttons made
        self.measurements_button = tb.Button(
            self.tab_frame,
            text="Body",
            command=self.show_measurements,
            width=9
        )
        self.food_button = tb.Button(
            self.tab_frame,
            text="Food",
            command=self.show_food,
            width=9
        )
        self.workout_button = tb.Button(
            self.tab_frame,
            text="Workouts",
            command=self.show_workouts,
            width=9
        )
        self.sleep_button = tb.Button(
            self.tab_frame,
            text="Sleep",
            command=self.show_sleep,
            width=9
        )
        self.steps_button = tb.Button(
            self.tab_frame,
            text="Steps",
            command=self.show_steps,
            width=9
        )

        # Visual displays
        self.dash_steps = tb.Label(
            self.dashframe,
            text=f"Steps: {get_steps(user.user_id)}",
            font=("roboto", 14)
        )
        self.dash_cals = tb.Label(
            self.dashframe,
            text=f"Calories: {get_calories(user.user_id)}",
            font=("roboto", 14)
        )
        self.dash_sleep = tb.Label(
            self.dashframe,
            text=f"SleepScore: {round(get_sleep(user.user_id), 2) * 100}%",
            font=("roboto", 14)
        )

        # Grids the buttons
        self.measurements_button.grid(row=0, column=0, padx=4)
        self.food_button.grid(row=0, column=1, padx=4)
        self.workout_button.grid(row=0, column=2, padx=4)
        self.sleep_button.grid(row=0, column=3, padx=4)
        self.steps_button.grid(row=0, column=4, padx=4)

        # Grids the visual displays
        self.dash_steps.grid(row=1, column=0, pady=(5, 5))
        self.dash_cals.grid(row=2, column=0, pady=(5, 5))
        self.dash_sleep.grid(row=3, column=0, pady=(5, 5))

    def show_measurements(self):
        """Opens the measurement tab"""
        Measurement(self.root, self.user)

    def show_food(self):
        """Opens the Food tab."""
        Food(self.root, self.user)

    def show_workouts(self):
        """Display the Workouts tab"""
        Workouts(self.root, self.user)

    def show_sleep(self):
        """
        Opens the Sleep tab
        :return:
        """
        Sleep(self.root, self.user)

    def show_steps(self):
        """Opens the steps tab"""
        Steps(self.root, self.user)


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Dashboard(root, test_user)
    root.mainloop()