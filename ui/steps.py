"""Steps Module - ReHealth"""

from tkinter import messagebox

import ttkbootstrap as tb

from db.db_handler import get_weight, save_steps, get_last_7_days_steps_convert
from logic.calculations import calories_burnt
from logic.user import User
from ui.ui_handler import return_to_dashboard, GraphTemplate, BasePage


def _validate_step_input(steps_text: str) -> tuple[bool, int, str]:
    """
    Validates the step input from the user.

    Args:
        steps_text: Raw text input from the step entry field.

    Returns:
        A tuple of (is_valid, steps_value, error_message).
        If valid, error_message is empty.
    """
    if not steps_text:
        return False, 0, "Please enter your steps."

    if not steps_text.isdigit():
        return False, 0, "Please enter your steps as a whole number."

    steps_value = int(steps_text)

    if steps_value < 0:
        return False, 0, "Steps cannot be negative."

    return True, steps_value, ""


def _check_milestone_achievement(steps: int, username: str) -> None:
    """
    Checks if the user has reached a step milestone and shows a congratulatory message.

    Args:
        steps: Number of steps recorded.
        username: User's username for personalized message.
    """
    if steps >= 10000:
        messagebox.showinfo(
            "Congratulations!",
            f"Well done {username}. You smashed 10,000 steps — go treat yourself!",
        )


class Steps(BasePage):
    """GUI screen for step input + calories + 7-day graph."""

    def __init__(self, root: tb.Window, user: User) -> None:
        """
        Args:
            root: Main application window.
            user: Logged-in user (used for user_id and username).
        """
        # Initialise attributes
        self.step_count: int = 0
        self.calorie_count: float = 0.0

        # Call parent constructor
        super().__init__(root, user, "Steps")

    def _build_ui(self) -> None:
        """Build all UI components."""
        self._create_labels()
        self._create_input_section()
        self._create_graph_section()

    def _create_labels(self) -> None:
        """Create the title and display labels."""
        self.steps_label = tb.Label(
            self.frame,
            text=f"{self.user.username}'s Steps",
            font=("roboto", 18, "bold"),
        )
        self.steps_label.grid(row=0, column=0, pady=(20, 30), padx=20, columnspan=2)

        self.count_label = tb.Label(
            self.frame,
            text="Step Count: 0",
            font=("roboto", 14)
        )
        self.count_label.grid(row=1, column=0, pady=(10, 10), padx=20, columnspan=2)

        self.calorie_label = tb.Label(
            self.frame,
            text="Calories Burnt: 0 kcal",
            font=("roboto", 14)
        )
        self.calorie_label.grid(row=2, column=0, pady=(10, 30), padx=20, columnspan=2)

    def _create_input_section(self) -> None:
        """Create the step input entry and button."""
        self.step_entry = tb.Entry(self.frame, width=20)
        self.step_entry.grid(row=3, column=0, padx=(20, 10), pady=(10, 10))

        self.step_button = tb.Button(
            self.frame,
            text="Add Steps",
            command=self.steps_and_calories
        )
        self.step_button.grid(row=3, column=1, pady=(10, 10), padx=(10, 20))

    def _create_graph_section(self) -> None:
        """Create the graph frame and initialise the graph widget."""
        self.graph_frame = tb.Frame(self.frame)
        self.graph_frame.grid(row=4, column=0, columnspan=2, pady=0, padx=20)

        self.step_graph = StepGraph(
            self.graph_frame,
            self.user,
            self.frame,
            self.root
        )

    def steps_and_calories(self) -> None:
        """
        Validates step input, saves to DB, updates UI, and refreshes the graph.
        Also shows an achievement message for 10,000+ steps.
        """
        steps_text = self.step_entry.get().strip()

        is_valid, steps_value, error_msg = _validate_step_input(steps_text)

        if not is_valid:
            messagebox.showerror("Invalid Input", error_msg)
            self.step_entry.focus()
            return

        try:
            self._save_and_update(steps_value)
            _check_milestone_achievement(steps_value, self.user.username)

        except Exception as exc:
            messagebox.showerror("Database Error", f"Failed to save to database: {exc}")
            self.step_entry.focus()

    def _save_and_update(self, steps_value: int) -> None:
        """
        Saves steps to database and updates all UI elements.

        Args:
            steps_value: Number of steps to save.
        """
        save_steps(self.user.user_id, str(steps_value), 10000)

        self.step_count = steps_value
        self.count_label.config(text=f"Step Count: {self.step_count}")

        weight = get_weight(self.user.user_id)
        self.calorie_count = calories_burnt(steps_value, weight)
        self.calorie_label.config(
            text=f"Calories Burnt: {round(self.calorie_count)} kcal"
        )

        messagebox.showinfo("Success", f"Steps saved! {self.step_count} steps recorded.")

        self.step_entry.delete(0, "end")
        self.step_entry.focus()

        self.step_graph.refresh_graph()


class StepGraph(GraphTemplate):
    def plot_data(self) -> None:
        self.ax.clear()
        days, steps = get_last_7_days_steps_convert(self.user.user_id)

        self.ax.plot(days, steps, marker='o', color='#4e73df',
                     linewidth=2, markersize=8)
        self.style_axes('Days', 'Steps', 'Steps Over Time')
        self.canvas.draw()

    def get_graph_filename(self) -> str:
        return f"{self.user.username}_steps_graph_week.png"

    def return_to_dash(self) -> None:
        """
        Navigates back to the dashboard screen.
        """
        return_to_dashboard(self.parent_frame, self.root, self.user)


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Steps(root, test_user)
    root.mainloop()