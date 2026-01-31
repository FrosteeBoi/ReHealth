"""Sleep Module - ReHealth"""

from tkinter import messagebox

import ttkbootstrap as tb

from db.db_handler import save_sleep, get_last_7_days_sleep_convert
from logic.calculations import sleep_calc
from logic.user import User
from ui.ui_handler import return_to_dashboard, GraphTemplate, BasePage


def validate_sleep_hours(hours_input: str) -> tuple[bool, float, str]:
    """
    Validates the sleep hours input from the user.

    Args:
        hours_input: The amount of hours inputted by the user representing how much they slept.

    Returns:
        A tuple of (is_valid, hours_value, error_message).
        Represents the validity of input, the value they inputted and a possible appropriate error message.
    """
    if not hours_input:
        return False, 0.0, "Please enter a valid number of hours (0-24)."

    # Check if input is a valid float value offer an appropriate response

    try:
        hours = float(hours_input)
        if hours < 0 or hours > 24:
            return False, 0.0, "Please enter a valid number of hours (0-24)."
        return True, hours, ""
    except ValueError:
        return False, 0.0, "Please enter a valid number of hours (0-24)."


def validate_sleep_quality(quality_input: str) -> tuple[bool, float, str]:
    """
    Validates the sleep quality input from the user.

    Args:
        quality_input: The subjective value entered by the user into the sleep quality field.

    Returns:
        A tuple of (is_valid, quality_value, error_message).
        Represents the validity of input, the value they inputted and a possible error message.
        If valid, error_message is empty.
    """
    if not quality_input:
        return False, 0, "Please enter a valid sleep quality (1-5)."

    try:
        quality = float(quality_input)
        if quality < 1 or quality > 5:
            return False, 0, "Please enter a valid positive sleep quality (1-5)."
        return True, quality, ""
    except ValueError:
        return False, 0, "Please enter a valid sleep quality (1-5)."


def calculate_sleep_rating(duration: float, quality: float) -> float:
    """
    Calculates a sleep rating based on duration and quality.

    Args:
        duration: Hours slept (0-24).
        quality: Sleep quality rating (1-5).

    Returns:
        A sleep rating between 0 and 1.
    """
    return sleep_calc(duration, quality)


def format_rating_percentage(rating: float) -> str:
    """
    Formats a sleep rating as a percentage string.

    Args:
        rating: Sleep rating between 0 and 1.

    Returns:
        Formatted string like "Sleep Rating: 85%"
    """
    return f"Sleep Rating: {round(rating * 100)}%"


class Sleep(BasePage):
    """Sleep tracking screen: records sleep inputs, calculates a rating and saves to the database."""

    def __init__(self, root: tb.Window, user: User) -> None:
        """
        Args:
            root: Main Sleep application window.
            user: Logged-in user
        """
        # Initialise 3 main attributes
        self.sleep_duration = None
        self.sleep_quality = None
        self.rating = None

        # Call parent constructor
        super().__init__(root, user, "Sleep")

    def _build_ui(self) -> None:
        """Build all UI components."""
        self._create_title()
        self._create_rating_display()
        self._create_input_section()
        self._create_calculate_button()
        self._create_graph_section()

    def _create_title(self) -> None:
        """Create the main title label."""
        self.sleep_label = tb.Label(
            self.frame,
            text=f"{self.user.username}'s Sleep",
            font=("roboto", 18, "bold")
        )
        self.sleep_label.grid(row=0, column=0, pady=(20, 30), columnspan=3, padx=20)

    def _create_rating_display(self) -> None:
        """Create the label that displays the calculated sleep rating."""
        self.rating_label = tb.Label(
            self.frame,
            text="Sleep Rating:",
            font=("roboto", 14)
        )
        self.rating_label.grid(row=1, column=0, pady=(10, 10), padx=20, columnspan=3)

    def _create_input_section(self) -> None:
        """Create the sleep hours and quality input fields."""
        # Sleep hours input
        self.sleep_hours_label = tb.Label(
            self.frame,
            text="Record your hours:",
            font=("roboto", 14)
        )
        self.sleep_hours_label.grid(row=2, column=0, pady=(20, 20), sticky="e", padx=(0, 10))

        self.sleep_entry = tb.Entry(self.frame)
        self.sleep_entry.grid(row=2, column=1, pady=(20, 20), columnspan=2)

        # Sleep quality input
        self.sleep_refresh_label = tb.Label(
            self.frame,
            text="Record how you feel (1-5):",
            font=("roboto", 14)
        )
        self.sleep_refresh_label.grid(row=3, column=0, pady=(20, 20), sticky="e", padx=(0, 10))

        self.refresh_entry = tb.Entry(self.frame)
        self.refresh_entry.grid(row=3, column=1, pady=(20, 20), columnspan=2)

    def _create_calculate_button(self) -> None:
        """Create the button to calculate and save sleep rating."""
        self.rating_button = tb.Button(
            self.frame,
            text="Calculate Rating",
            command=self.update_rating
        )
        self.rating_button.grid(row=4, column=0, columnspan=3)

    def _create_graph_section(self) -> None:
        """Create the graph frame and initialise the graph widget."""
        self.graph_frame = tb.Frame(self.frame)
        self.graph_frame.grid(row=5, column=0, columnspan=3, pady=0, padx=20)

        self.sleep_graph = SleepGraph(
            self.graph_frame,
            self.user,
            self.frame,
            self.root
        )

    def update_rating(self) -> None:
        """
        Validates inputs, calculates a sleep rating, saves to DB, updates UI, and refreshes the graph.
        """
        hours_input = self.sleep_entry.get().strip()
        quality_input = self.refresh_entry.get().strip()

        # Validate hours and sleep quality inputted by user
        hours_valid, hours_value, hours_error = validate_sleep_hours(hours_input)
        if not hours_valid:
            messagebox.showerror("Error", hours_error)
            self.sleep_entry.focus()
            return

        quality_valid, quality_value, quality_error = validate_sleep_quality(quality_input)
        if not quality_valid:
            messagebox.showerror("Error", quality_error)
            self.refresh_entry.focus()
            return

        # Store validated values
        self.sleep_duration = hours_value
        self.sleep_quality = quality_value

        try:
            self._calculate_and_save()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save to database: {str(e)}")

    def _calculate_and_save(self) -> None:
        """
        Calculates the sleep rating, saves to database, and updates UI.
        """
        # Calculate rating and update the display accordingly
        self.rating = calculate_sleep_rating(self.sleep_duration, self.sleep_quality)
        self.rating_label.config(text=format_rating_percentage(self.rating))

        # Save to database
        save_sleep(self.user.user_id, self.sleep_duration, self.rating)
        messagebox.showinfo(
            "Success",
            f"Sleep data saved! Rating: {round(self.rating * 100)}%"
        )

        # Clear inputs, refresh graph and prepare for next entry
        self.sleep_entry.delete(0, 'end')
        self.refresh_entry.delete(0, 'end')
        self.sleep_entry.focus()

        self.sleep_graph.refresh_graph()
        self.root.update_idletasks()


class SleepGraph(GraphTemplate):
    """
    Class for plotting a graph showing the user's sleep over the course of the last 7 years.
    """
    def plot_data(self) -> None:
        """
        Fetches sleep values and plot/style the graph
        """
        self.ax.clear()
        days, sleep_hours = get_last_7_days_sleep_convert(self.user.user_id)

        self.ax.plot(
            days,
            sleep_hours,
            marker='o',
            color='#4e73df',
            linewidth=2,
            markersize=8
        )

        self.style_axes("Days", "Hours", "Sleep Over Time")
        self.canvas.draw()

    def get_graph_filename(self) -> str:
        return f"{self.user.username}_sleep_graph_week.png"

    def return_to_dash(self) -> None:
        """
        Navigates back to the dashboard screen.
        """
        return_to_dashboard(self.parent_frame, self.root, self.user)


if __name__ == "__main__":
    """
    Allows testing to be made on this specific window.
    Only runs if the file is executed directly (not through imports)
    """
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Sleep(root, test_user)
    root.mainloop()
