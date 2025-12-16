"""Steps Module - ReHealth"""

import os
from tkinter import messagebox

import ttkbootstrap as tb
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from db.db_handler import get_weight, save_steps, get_last_7_days_steps_convert
from logic.calculations import calories_burnt
from logic.user import User
from ui.ui_handler import return_to_dashboard


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


def _create_graph_figure() -> tuple[Figure, any]:
    """
    Creates and configures a matplotlib figure for the step graph.

    Returns:
        A tuple of (figure, axes) with dark theme styling applied.
    """
    fig = Figure(figsize=(6, 4), dpi=80, facecolor="#222222")
    ax = fig.add_subplot(111)
    ax.set_facecolor("#2b3e50")
    return fig, ax


def _style_graph_axes(ax: any) -> None:
    """
    Applies dark theme styling to the graph axes.

    Args:
        ax: The matplotlib axes object to style.
    """
    ax.set_xlabel("Days", color="#adb5bd")
    ax.set_ylabel("Steps", color="#adb5bd")
    ax.set_title("Steps Over Time", color="#ffffff")
    ax.tick_params(colors="#adb5bd")

    for spine in ax.spines.values():
        spine.set_color("#adb5bd")

    ax.grid(True, alpha=0.2, color="#adb5bd")


class Steps:
    """GUI screen for step input + calories + 7-day graph."""

    def __init__(self, root: tb.Window, user: User) -> None:
        """
        Args:
            root: Main application window.
            user: Logged-in user (used for user_id and username).
        """
        self.root = root
        self.user = user

        self._configure_window()
        self._create_main_frame()
        self._initialize_state()
        self._build_ui()

    def _configure_window(self) -> None:
        """Configure window size and title."""
        self.root.geometry("490x630")
        self.root.title("ReHealth")

    def _create_main_frame(self) -> None:
        """Create and position the main frame."""
        self.stepframe = tb.Frame(self.root)
        self.stepframe.place(relx=0.5, rely=0, anchor="n")

    def _initialize_state(self) -> None:
        """Initialize instance variables."""
        self.step_count: int = 0
        self.calorie_count: float = 0.0

    def _build_ui(self) -> None:
        """Build all UI components."""
        self._create_labels()
        self._create_input_section()
        self._create_graph_section()

    def _create_labels(self) -> None:
        """Create the title and display labels."""
        self.steps_label = tb.Label(
            self.stepframe,
            text=f"{self.user.username}'s Steps",
            font=("roboto", 18, "bold"),
        )
        self.steps_label.grid(row=0, column=0, pady=(20, 30), padx=20, columnspan=2)

        self.count_label = tb.Label(
            self.stepframe,
            text="Step Count: 0",
            font=("roboto", 14)
        )
        self.count_label.grid(row=1, column=0, pady=(10, 10), padx=20, columnspan=2)

        self.calorie_label = tb.Label(
            self.stepframe,
            text="Calories Burnt: 0 kcal",
            font=("roboto", 14)
        )
        self.calorie_label.grid(row=2, column=0, pady=(10, 30), padx=20, columnspan=2)

    def _create_input_section(self) -> None:
        """Create the step input entry and button."""
        self.step_entry = tb.Entry(self.stepframe, width=20)
        self.step_entry.grid(row=3, column=0, padx=(20, 10), pady=(10, 10))

        self.step_button = tb.Button(
            self.stepframe,
            text="Add Steps",
            command=self.steps_and_calories
        )
        self.step_button.grid(row=3, column=1, pady=(10, 10), padx=(10, 20))

    def _create_graph_section(self) -> None:
        """Create the graph frame and initialize the graph widget."""
        self.graph_frame = tb.Frame(self.stepframe)
        self.graph_frame.grid(row=4, column=0, columnspan=2, pady=0, padx=20)

        self.step_graph = StepGraph(
            graph_frame=self.graph_frame,
            user=self.user,
            stepframe=self.stepframe,
            root=self.root,
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


class StepGraph:
    """Embedded matplotlib graph showing the user's last 7 days of steps + export button."""

    def __init__(
            self,
            graph_frame: tb.Frame,
            user: User,
            stepframe: tb.Frame,
            root: tb.Window
    ) -> None:
        """
        Args:
            graph_frame: Parent frame that the graph and buttons are placed into.
            user: Logged-in user
            stepframe: Steps screen frame
            root: Main application window (used for navigation).
        """
        self.graph_frame = graph_frame
        self.user = user
        self.stepframe = stepframe
        self.root = root

        self._configure_frame()
        self._create_graph()
        self._create_buttons()

    def _configure_frame(self) -> None:
        """Configure the graph frame layout."""
        self.graph_frame.grid(row=4, column=0, sticky="s")
        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)

    def _create_graph(self) -> None:
        """Create the matplotlib figure and canvas."""
        self.fig, self.ax = _create_graph_figure()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas_widget = self.canvas.get_tk_widget()

        self.plot_data()
        self.canvas_widget.grid(row=0, column=0, pady=(0, 10))

    def _create_buttons(self) -> None:
        """Create the download and dashboard navigation buttons."""
        self.button_frame = tb.Frame(self.graph_frame)
        self.button_frame.grid(row=1, column=0, pady=(0, 20))

        self.save_btn = tb.Button(
            self.button_frame,
            text="Download",
            command=self.save_graph
        )
        self.save_btn.grid(row=0, column=0, padx=(0, 5))

        self.dash_button = tb.Button(
            self.button_frame,
            text="Back to Dashboard",
            command=self.return_to_dash
        )
        self.dash_button.grid(row=0, column=1, padx=(5, 0))

    def plot_data(self) -> None:
        """
        Queries the DB for the last 7 days and redraws the line plot.
        """
        self.ax.clear()

        days, steps = get_last_7_days_steps_convert(self.user.user_id)

        self.ax.plot(
            days,
            steps,
            marker="o",
            color="#4e73df",
            linewidth=2,
            markersize=8
        )

        _style_graph_axes(self.ax)
        self.canvas.draw()

    def refresh_graph(self) -> None:
        """
        Replots data after a new step record is saved.
        """
        self.plot_data()

    def save_graph(self) -> None:
        """
        Exports the current graph to /images as a PNG file.
        """
        try:
            images_folder = os.path.join(
                os.path.dirname(__file__),
                "..",
                "images"
            )
            images_folder = os.path.abspath(images_folder)

            if not os.path.exists(images_folder):
                os.makedirs(images_folder)

            filename = os.path.join(
                images_folder,
                f"{self.user.username}_steps_graph_week.png"
            )
            self.fig.savefig(filename, dpi=100, facecolor="#222222")

            messagebox.showinfo("Success", f"Graph saved to {filename}")

        except Exception as exc:
            messagebox.showerror("Error", f"Failed to save graph: {exc}")

    def return_to_dash(self) -> None:
        """
        Navigates back to the dashboard screen.
        """
        return_to_dashboard(self.stepframe, self.root, self.user)


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Steps(root, test_user)
    root.mainloop()
