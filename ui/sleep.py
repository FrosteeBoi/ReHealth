"""Sleep Module - ReHealth"""

import os
from tkinter import messagebox

import ttkbootstrap as tb
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from db.db_handler import save_sleep, get_last_7_days_sleep_convert
from logic.calculations import sleep_calc
from logic.user import User
from ui.ui_handler import return_to_dashboard


def validate_sleep_hours(hours_input: str) -> tuple[bool, float, str]:
    """
    Validates the sleep hours input from the user.

    Args:
        hours_input: Raw text input from the hours entry field.

    Returns:
        A tuple of (is_valid, hours_value, error_message).
        If valid, error_message is empty.
    """
    if not hours_input:
        return False, 0.0, "Please enter a valid number of hours (0-24)."

    try:
        hours = float(hours_input)
        if hours < 0 or hours > 24:
            return False, 0.0, "Please enter a valid number of hours (0-24)."
        return True, hours, ""
    except ValueError:
        return False, 0.0, "Please enter a valid number of hours (0-24)."


def validate_sleep_quality(quality_input: str) -> tuple[bool, int, str]:
    """
    Validates the sleep quality input from the user.

    Args:
        quality_input: Raw text input from the quality entry field.

    Returns:
        A tuple of (is_valid, quality_value, error_message).
        If valid, error_message is empty.
    """
    if not quality_input:
        return False, 0, "Please enter a valid sleep quality (1-5)."

    try:
        quality = int(quality_input)
        if quality < 1 or quality > 5:
            return False, 0, "Please enter a valid sleep quality (1-5)."
        return True, quality, ""
    except ValueError:
        return False, 0, "Please enter a valid sleep quality (1-5)."


def calculate_sleep_rating(duration: float, quality: int) -> float:
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


def create_graph_figure() -> tuple[Figure, any]:
    """
    Creates and configures a matplotlib figure for the sleep graph.

    Returns:
        A tuple of (figure, axes) with dark theme styling applied.
    """
    fig = Figure(figsize=(6, 4), dpi=67, facecolor='#222222')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#2b3e50')
    return fig, ax


def style_graph_axes(ax: any) -> None:
    """
    Applies dark theme styling to the graph axes.

    Args:
        ax: The matplotlib axes object to style.
    """
    ax.set_xlabel('Days', color='#adb5bd')
    ax.set_ylabel('Hours', color='#adb5bd')
    ax.set_title('Sleep Over Time', color='#ffffff')
    ax.tick_params(colors='#adb5bd')

    for spine in ax.spines.values():
        spine.set_color('#adb5bd')

    ax.grid(True, alpha=0.2, color='#adb5bd')


class Sleep:
    """Sleep tracking screen: records sleep inputs, calculates a rating, saves to DB, and displays a 7-day graph."""

    def __init__(self, root: tb.Window, user: User) -> None:
        """
        Args:
            root: Main application window.
            user: Logged-in user (used for user_id and username).
        """
        self.root = root
        self.user = user

        self.__configure_window()
        self.__create_main_frame()
        self.__initialize_state()
        self.__build_ui()

    def __configure_window(self) -> None:
        """Configure window size and title."""
        self.root.geometry("490x630")
        self.root.title("ReHealth")

    def __create_main_frame(self) -> None:
        """Create and position the main frame."""
        self.sleepframe = tb.Frame(self.root)
        self.sleepframe.place(relx=0.5, rely=0, anchor="n")

    def __initialize_state(self) -> None:
        """Initialize instance variables for tracking sleep data."""
        self.sleep_duration = None
        self.sleep_quality = None
        self.rating = None

    def __build_ui(self) -> None:
        """Build all UI components."""
        self.__create_title()
        self.__create_rating_display()
        self.__create_input_section()
        self.__create_calculate_button()
        self.__create_graph_section()

    def __create_title(self) -> None:
        """Create the main title label."""
        self.sleep_label = tb.Label(
            self.sleepframe,
            text=f"{self.user.username}'s Sleep",
            font=("roboto", 18, "bold")
        )
        self.sleep_label.grid(row=0, column=0, pady=(20, 30), columnspan=3, padx=20)

    def __create_rating_display(self) -> None:
        """Create the label that displays the calculated sleep rating."""
        self.rating_label = tb.Label(
            self.sleepframe,
            text="Sleep Rating:",
            font=("roboto", 14)
        )
        self.rating_label.grid(row=1, column=0, pady=(10, 10), padx=20, columnspan=3)

    def __create_input_section(self) -> None:
        """Create the sleep hours and quality input fields."""
        # Sleep hours input
        self.sleep_hours_label = tb.Label(
            self.sleepframe,
            text="Record your hours:",
            font=("roboto", 14)
        )
        self.sleep_hours_label.grid(row=2, column=0, pady=(20, 20), sticky="e", padx=(0, 10))

        self.sleep_entry = tb.Entry(self.sleepframe)
        self.sleep_entry.grid(row=2, column=1, pady=(20, 20), columnspan=2)

        # Sleep quality input
        self.sleep_refresh_label = tb.Label(
            self.sleepframe,
            text="Record how you feel (1-5):",
            font=("roboto", 14)
        )
        self.sleep_refresh_label.grid(row=3, column=0, pady=(20, 20), sticky="e", padx=(0, 10))

        self.refresh_entry = tb.Entry(self.sleepframe)
        self.refresh_entry.grid(row=3, column=1, pady=(20, 20), columnspan=2)

    def __create_calculate_button(self) -> None:
        """Create the button to calculate and save sleep rating."""
        self.rating_button = tb.Button(
            self.sleepframe,
            text="Calculate Rating",
            command=self.update_rating
        )
        self.rating_button.grid(row=4, column=0, columnspan=3)

    def __create_graph_section(self) -> None:
        """Create the graph frame and initialize the graph widget."""
        self.graph_frame = tb.Frame(self.sleepframe)
        self.graph_frame.grid(row=5, column=0, columnspan=3, pady=0, padx=20)

        self.sleep_graph = SleepGraph(
            graph_frame=self.graph_frame,
            user=self.user,
            sleepframe=self.sleepframe,
            root=self.root
        )

    def update_rating(self) -> None:
        """
        Validates inputs, calculates a sleep rating, saves to DB, updates UI, and refreshes the graph.
        """
        hours_input = self.sleep_entry.get().strip()
        quality_input = self.refresh_entry.get().strip()

        # Validate hours input
        hours_valid, hours_value, hours_error = validate_sleep_hours(hours_input)
        if not hours_valid:
            messagebox.showerror("Error", hours_error)
            self.sleep_entry.focus()
            return

        # Validate quality input
        quality_valid, quality_value, quality_error = validate_sleep_quality(quality_input)
        if not quality_valid:
            messagebox.showerror("Error", quality_error)
            self.refresh_entry.focus()
            return

        # Store validated values
        self.sleep_duration = hours_value
        self.sleep_quality = quality_value

        try:
            self.__calculate_and_save()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save to database: {str(e)}")

    def __calculate_and_save(self) -> None:
        """
        Calculates the sleep rating, saves to database, and updates UI.
        """
        # Calculate rating
        self.rating = calculate_sleep_rating(self.sleep_duration, self.sleep_quality)

        # Update rating display
        self.rating_label.config(text=format_rating_percentage(self.rating))

        # Save to database
        save_sleep(self.user.user_id, self.sleep_duration, self.rating)

        # Show success message
        messagebox.showinfo(
            "Success",
            f"Sleep data saved! Rating: {round(self.rating * 100)}%"
        )

        # Clear inputs and prepare for next entry
        self.sleep_entry.delete(0, 'end')
        self.refresh_entry.delete(0, 'end')
        self.sleep_entry.focus()

        # Refresh graph to show new data
        self.sleep_graph.refresh_graph()
        self.root.update_idletasks()


class SleepGraph:
    """Embedded matplotlib graph showing the user's last 7 days of sleep hours with export + navigation buttons."""

    def __init__(
        self,
        graph_frame: tb.Frame,
        user: User,
        sleepframe: tb.Frame,
        root: tb.Window
    ) -> None:
        """
        Args:
            graph_frame: Parent frame that the graph and buttons are placed into.
            user: Logged-in user.
            sleepframe: Sleep screen frame.
            root: Main application window (used for navigation).
        """
        self.graph_frame = graph_frame
        self.user = user
        self.sleepframe = sleepframe
        self.root = root

        self.__configure_frame()
        self.__create_graph()
        self.__create_buttons()

    def __configure_frame(self) -> None:
        """Configure the graph frame layout."""
        self.graph_frame.grid(row=5, column=0, sticky="s")
        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)

    def __create_graph(self) -> None:
        """Create the matplotlib figure and canvas."""
        self.fig, self.ax = create_graph_figure()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas_widget = self.canvas.get_tk_widget()

        self.plot_data()
        self.canvas_widget.grid(row=0, column=0, pady=(0, 10))

    def __create_buttons(self) -> None:
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
        Fetches the last 7 days of sleep hours and redraws the line plot.
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

        style_graph_axes(self.ax)
        self.canvas.draw()

    def refresh_graph(self) -> None:
        """Replots data after a new sleep record is saved."""
        self.plot_data()

    def save_graph(self) -> None:
        """
        Exports the current graph image to the project's /images folder.
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
                f'{self.user.username}_sleep_graph_week.png'
            )

            self.fig.savefig(filename, dpi=100, facecolor='#222222')

            messagebox.showinfo("Success", f"Graph saved to {filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save graph: {str(e)}")

    def return_to_dash(self) -> None:
        """Returns to the dashboard screen."""
        return_to_dashboard(self.sleepframe, self.root, self.user)


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Sleep(root, test_user)
    root.mainloop()