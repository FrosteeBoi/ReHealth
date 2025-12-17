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


class Dashboard:
    """
    Dashboard class that displays user metrics and allows navigation to other windows.
    """

    def __init__(self, root: tb.Window, user: User) -> None:
        """
        Initializes the dashboard GUI.

        Args:
            root: Main application window.
            user: Logged-in user (used for user_id and username).
        """
        self.root = root
        self.user = user

        self._configure_window()
        self._create_main_frame()
        self._build_ui()

    def _configure_window(self) -> None:
        """Configure window size and title."""
        self.root.geometry("490x630")
        self.root.title("ReHealth")

    def _create_main_frame(self) -> None:
        """Create and position the main frame."""
        self.dashframe = tb.Frame(self.root)
        self.dashframe.place(relx=0.5, rely=0, anchor="n")

    def _build_ui(self) -> None:
        """Build all UI components."""
        self._create_welcome_label()
        self._create_metric_displays()
        self._create_achievements_button()
        self._create_navigation_tabs()

    def _create_welcome_label(self) -> None:
        """Create the welcome label with username."""
        self.dash_label = tb.Label(
            self.dashframe,
            text=f"Hello {self.user.username}",
            font=("roboto", 18, "bold")
        )
        self.dash_label.grid(row=0, column=0, pady=(20, 30))

    def _create_metric_displays(self) -> None:
        """Create the metric display labels (steps, calories, sleep)."""
        # Fetch current metrics
        steps = get_steps(self.user.user_id)
        calories = get_calories(self.user.user_id)
        sleep = get_sleep(self.user.user_id)

        # Steps display
        self.dash_steps = tb.Label(
            self.dashframe,
            text=f"Steps: {steps}",
            font=("roboto", 14)
        )
        self.dash_steps.grid(row=1, column=0, pady=(5, 5))

        # Calories display
        self.dash_cals = tb.Label(
            self.dashframe,
            text=f"Calories: {calories}",
            font=("roboto", 14)
        )
        self.dash_cals.grid(row=2, column=0, pady=(5, 5))

        # Sleep score display
        self.dash_sleep = tb.Label(
            self.dashframe,
            text=f"SleepScore: {round(sleep, 2) * 100}%",
            font=("roboto", 14)
        )
        self.dash_sleep.grid(row=3, column=0, pady=(5, 5))

    def _create_achievements_button(self) -> None:
        """Create the achievements button."""
        self.achievements_button = tb.Button(
            self.dashframe,
            text="Achievements",
            command=self.show_achievements,
            width=13
        )
        self.achievements_button.grid(row=4, pady=(0, 400), column=0)

    def _create_navigation_tabs(self) -> None:
        """Create the navigation tab buttons at the bottom."""
        # Create tab frame
        self.tab_frame = tb.Frame(self.dashframe)
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
        self.dashframe.destroy()
        Measurement(self.root, self.user)

    def show_food(self) -> None:
        """Opens the Food tab."""
        self.dashframe.destroy()
        Food(self.root, self.user)

    def show_workouts(self) -> None:
        """Display the Workouts tab."""
        self.dashframe.destroy()
        Workouts(self.root, self.user)

    def show_sleep(self) -> None:
        """Opens the Sleep tab."""
        self.dashframe.destroy()
        Sleep(self.root, self.user)

    def show_steps(self) -> None:
        """Opens the steps tab."""
        self.dashframe.destroy()
        Steps(self.root, self.user)

    def show_achievements(self) -> None:
        """Opens the Achievements tab."""
        self.dashframe.destroy()
        Achievements(self.root, self.user)


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Dashboard(root, test_user)
    root.mainloop()