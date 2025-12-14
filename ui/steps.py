"""
ReHealth – Steps page

AQA A-Level Computer Science (NEA) style notes:
- Clear class structure and method responsibilities.
- Input validation with user-friendly error messages.
- Database writes wrapped in try/except for robustness.
- Separation of concerns: UI (Steps/StepGraph) vs logic/db modules.
"""

import os
from tkinter import messagebox

import ttkbootstrap as tb
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from db.db_handler import (
    get_weight,
    save_steps,
    get_last_7_days_steps_convert
)
from logic.calculations import calories_burnt
from logic.user import User
from ui.ui_handler import return_to_dashboard


class Steps:
    """
    UI controller for recording a user's steps and showing calories burnt.

    Responsibilities:
    - Build the steps input UI (labels, entry, button).
    - Validate user input.
    - Save steps to the database.
    - Update labels and refresh the graph after a successful save.
    """

    def __init__(self, root: tb.Window, user: User) -> None:
        """
        Initialise the Steps screen.

        Args:
            root: Tkinter root window.
            user: Currently logged-in user object.
        """
        self.root = root
        self.user = user

        # ---- Window / layout configuration ----
        self.stepframe = tb.Frame(self.root)
        self.stepframe.place(relx=0.5, rely=0, anchor="n")

        self.root.geometry("490x630")
        self.root.title("ReHealth")

        # ---- State variables (UI-friendly values) ----
        self.step_count: int = 0
        self.calorie_count: float = 0.0

        # ---- Headings / labels ----
        self.steps_label = tb.Label(
            self.stepframe,
            text=f"{self.user.username}'s Steps",
            font=("roboto", 18, "bold")
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

        # ---- Input controls ----
        self.step_entry = tb.Entry(self.stepframe, width=20)
        self.step_entry.grid(row=3, column=0, padx=(20, 10), pady=(10, 10))

        self.step_button = tb.Button(
            self.stepframe,
            text="Add Steps",
            command=self.steps_and_calories
        )
        self.step_button.grid(row=3, column=1, pady=(10, 10), padx=(10, 20))

        # ---- Graph widget ----
        self.graph_frame = tb.Frame(self.stepframe)
        self.graph_frame.grid(row=4, column=0, columnspan=2, pady=0, padx=20)

        self.step_graph = StepGraph(
            graph_frame=self.graph_frame,
            user=self.user,
            stepframe=self.stepframe,
            root=self.root
        )

    def steps_and_calories(self) -> None:
        """
        Validate input, save steps, update labels, and refresh graph.

        Design choice:
        - The graph refresh happens ONLY after a successful database save,
          so the UI always matches stored data.
        """
        steps_text = self.step_entry.get().strip()

        # ---- Validation (presence + integer + non-negative) ----
        if not steps_text:
            messagebox.showerror("Missing Information", "Please enter your steps.")
            self.step_entry.focus()
            return

        # isdigit() rejects negatives and decimals (which we don't want anyway).
        if not steps_text.isdigit():
            messagebox.showerror("Invalid Input", "Please enter your steps as a whole number.")
            self.step_entry.focus()
            return

        steps_value = int(steps_text)

        # Defensive check (kept for clarity even though isdigit() blocks negatives)
        if steps_value < 0:
            messagebox.showerror("Invalid Input", "Steps cannot be negative.")
            self.step_entry.focus()
            return

        # ---- Save and update UI ----
        try:
            # Persist steps to the database. Goal is set to 10,000.
            save_steps(self.user.user_id, str(steps_value), 10000)

            # Update step label.
            self.step_count = steps_value
            self.count_label.config(text=f"Step Count: {self.step_count}")

            # Calculate calories burnt using user's weight (from DB).
            weight = get_weight(self.user.user_id)
            self.calorie_count = calories_burnt(steps_value, weight)
            self.calorie_label.config(
                text=f"Calories Burnt: {round(self.calorie_count)} kcal"
            )

            messagebox.showinfo("Success", f"Steps saved! {self.step_count} steps recorded.")

            # Clear entry to improve usability.
            self.step_entry.delete(0, "end")
            self.step_entry.focus()

            # Refresh graph to reflect latest stored values.
            self.step_graph.refresh_graph()

            # Optional motivational message if user hits goal.
            if steps_value >= 10000:
                messagebox.showinfo(
                    "Congratulations!",
                    f"Well done {self.user.username}. You smashed 10,000 steps — go treat yourself!"
                )

        except Exception as exc:
            # Generic catch ensures the UI doesn't crash on database errors.
            messagebox.showerror("Database Error", f"Failed to save to database: {exc}")
            self.step_entry.focus()


class StepGraph:
    """
    Graph widget displaying the user's last 7 days of steps.

    Responsibilities:
    - Fetch data for the last 7 days from the database layer.
    - Plot steps as a line chart embedded into Tkinter via FigureCanvasTkAgg.
    - Allow the user to download the chart and return to the dashboard.
    """

    def __init__(self, graph_frame: tb.Frame, user: User, stepframe: tb.Frame, root: tb.Window) -> None:
        """
        Initialise the graph widget.

        Args:
            graph_frame: Parent frame to contain the matplotlib canvas + buttons.
            user: Current user object.
            stepframe: Current page frame (needed for navigation).
            root: Tkinter root window (needed for navigation).
        """
        self.graph_frame = graph_frame
        self.user = user
        self.stepframe = stepframe
        self.root = root

        # Configure layout so canvas can expand nicely if needed.
        self.graph_frame.grid(row=4, column=0, sticky="s")
        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)

        # Create matplotlib Figure/Axes for embedding.
        self.fig = Figure(figsize=(6, 4), dpi=80, facecolor="#222222")
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#2b3e50")

        # Create canvas widget that hosts the matplotlib figure.
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas_widget = self.canvas.get_tk_widget()

        # Initial render.
        self.plot_data()
        self.canvas_widget.grid(row=0, column=0, pady=(0, 10))

        # Buttons beneath the graph.
        self.button_frame = tb.Frame(self.graph_frame)
        self.button_frame.grid(row=1, column=0, pady=(0, 20))

        self.save_btn = tb.Button(self.button_frame, text="Download", command=self.save_graph)
        self.save_btn.grid(row=0, column=0, padx=(0, 5))

        self.dash_button = tb.Button(
            self.button_frame,
            text="Back to Dashboard",
            command=self.return_to_dash
        )
        self.dash_button.grid(row=0, column=1, padx=(5, 0))

    def plot_data(self) -> None:
        """
        Fetch the last 7 days of step data and draw the graph.

        Data source:
        - get_last_7_days_steps_convert() returns (days, steps) lists/arrays.
        """
        self.ax.clear()

        days, steps = get_last_7_days_steps_convert(self.user.user_id)

        # Plot line chart with markers to highlight each day.
        self.ax.plot(days, steps, marker="o", color="#4e73df", linewidth=2, markersize=8)

        # Axis labels and styling (readable on dark theme).
        self.ax.set_xlabel("Days", color="#adb5bd")
        self.ax.set_ylabel("Steps", color="#adb5bd")
        self.ax.set_title("Steps Over Time", color="#ffffff")

        self.ax.tick_params(colors="#adb5bd")
        for spine in self.ax.spines.values():
            spine.set_color("#adb5bd")

        self.ax.grid(True, alpha=0.2, color="#adb5bd")

        # Redraw the canvas to display updates.
        self.canvas.draw()

    def refresh_graph(self) -> None:
        """
        Re-plot data and redraw the canvas.
        Called after a successful database update to keep UI consistent with stored data.
        """
        self.plot_data()

    def save_graph(self) -> None:
        """
        Save the current graph as a PNG into the project's images folder.

        Implementation notes:
        - Uses a path relative to this file so it works on different machines.
        - Creates the folder if it doesn't exist.
        """
        try:
            images_folder = os.path.join(os.path.dirname(__file__), "..", "images")
            images_folder = os.path.abspath(images_folder)

            if not os.path.exists(images_folder):
                os.makedirs(images_folder)

            filename = os.path.join(images_folder, f"{self.user.username}_steps_graph_week.png")
            self.fig.savefig(filename, dpi=100, facecolor="#222222")

            messagebox.showinfo("Success", f"Graph saved to {filename}")

        except Exception as exc:
            messagebox.showerror("Error", f"Failed to save graph: {exc}")

    def return_to_dash(self) -> None:
        """
        Navigate back to the dashboard screen.
        """
        return_to_dashboard(self.stepframe, self.root, self.user)


if __name__ == "__main__":
    # Manual test harness (useful for development/testing outside the full app).
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Steps(root, test_user)
    root.mainloop()
