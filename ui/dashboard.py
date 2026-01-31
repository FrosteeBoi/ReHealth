"""Dashboard Module - ReHealth"""

import ttkbootstrap as tb

from db.dashboard_data import get_sleep, get_steps, get_calories
from logic.user import User
from ui.food import Food
from ui.measurement import Measurement
from ui.sleep import Sleep
from ui.steps import Steps
from ui.workout import Workouts
from ui.achievements import Achievements
from ui.ui_handler import BasePage


class Dashboard(BasePage):
    """
    Dashboard class that displays user metrics and allows navigation to other windows.
    """

    def __init__(self, root: tb.Window, user: User) -> None:
        """
        Initialises the dashboard GUI.

        Args:
            root: Main application window.
            user: Logged-in user
        """
        # Call parent constructor
        super().__init__(root, user, "Dashboard")

    def _build_ui(self) -> None:
        """Build all UI components."""
        self._create_welcome_label()
        self._create_metric_displays()
        self._create_achievements_button()
        self._create_navigation_tabs()

    def _create_welcome_label(self) -> None:
        """Create a welcome label to initially greet the user."""
        self.dash_label = tb.Label(
            self.frame,
            text=f"Hello {self.user.username}",
            font=("roboto", 18, "bold")
        )
        self.dash_label.grid(row=0, column=0, pady=(20, 30))

    def _create_metric_displays(self) -> None:
        """Create labels for the user's: steps, calories, sleep."""
        # Fetch current metrics
        steps = get_steps(self.user.user_id)
        calories = get_calories(self.user.user_id)
        sleep = get_sleep(self.user.user_id)

        # Steps display
        self.dash_steps = tb.Label(
            self.frame,
            text=f"Steps: {steps}",
            font=("roboto", 14)
        )
        self.dash_steps.grid(row=1, column=0, pady=(5, 5))

        # Calories display
        self.dash_cals = tb.Label(
            self.frame,
            text=f"Calories: {calories}",
            font=("roboto", 14)
        )
        self.dash_cals.grid(row=2, column=0, pady=(5, 5))

        # Sleep score display
        self.dash_sleep = tb.Label(
            self.frame,
            text=f"SleepScore: {round(sleep, 2) * 100}%",
            font=("roboto", 14)
        )
        self.dash_sleep.grid(row=3, column=0, pady=(5, 5))

    def _create_achievements_button(self) -> None:
        """Create the button to go to achievements in the menu."""
        self.achievements_button = tb.Button(
            self.frame,
            text="Achievements",
            command=self.show_achievements,
            width=13
        )
        self.achievements_button.grid(row=4, pady=(0, 400), column=0)

    def _create_navigation_tabs(self) -> None:
        """Create the navigation tab buttons at the bottom."""
        # Create tab frame
        self.tab_frame = tb.Frame(self.frame)
        self.tab_frame.grid(row=4, column=0, pady=(390, 20))

        # Create individual tab buttons
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

        # Grid all tab buttons
        self.measurements_button.grid(row=1, column=0, padx=4)
        self.food_button.grid(row=1, column=1, padx=4)
        self.workout_button.grid(row=1, column=2, padx=4)
        self.sleep_button.grid(row=1, column=3, padx=4)
        self.steps_button.grid(row=1, column=4, padx=4)

    def show_measurements(self) -> None:
        """Opens the measurement tab."""
        self.frame.destroy()
        Measurement(self.root, self.user)

    def show_food(self) -> None:
        """Opens the Food tab."""
        self.frame.destroy()
        Food(self.root, self.user)

    def show_workouts(self) -> None:
        """Display the Workouts tab."""
        self.frame.destroy()
        Workouts(self.root, self.user)

    def show_sleep(self) -> None:
        """Opens the Sleep tab."""
        self.frame.destroy()
        Sleep(self.root, self.user)

    def show_steps(self) -> None:
        """Opens the steps tab."""
        self.frame.destroy()
        Steps(self.root, self.user)

    def show_achievements(self) -> None:
        """Opens the Achievements tab."""
        self.frame.destroy()
        Achievements(self.root, self.user)


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Dashboard(root, test_user)
    root.mainloop()