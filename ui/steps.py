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

        self.stepframe = tb.Frame(self.root)
        self.stepframe.place(relx=0.5, rely=0, anchor="n")

        self.root.geometry("490x630")
        self.root.title("ReHealth")

        self.step_count: int = 0
        self.calorie_count: float = 0.0

        self.steps_label = tb.Label(
            self.stepframe,
            text=f"{self.user.username}'s Steps",
            font=("roboto", 18, "bold"),
        )
        self.steps_label.grid(row=0, column=0, pady=(20, 30), padx=20, columnspan=2)

        self.count_label = tb.Label(self.stepframe, text="Step Count: 0", font=("roboto", 14))
        self.count_label.grid(row=1, column=0, pady=(10, 10), padx=20, columnspan=2)

        self.calorie_label = tb.Label(self.stepframe, text="Calories Burnt: 0 kcal", font=("roboto", 14))
        self.calorie_label.grid(row=2, column=0, pady=(10, 30), padx=20, columnspan=2)

        self.step_entry = tb.Entry(self.stepframe, width=20)
        self.step_entry.grid(row=3, column=0, padx=(20, 10), pady=(10, 10))

        self.step_button = tb.Button(self.stepframe, text="Add Steps", command=self.steps_and_calories)
        self.step_button.grid(row=3, column=1, pady=(10, 10), padx=(10, 20))

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

        Raises:
            None. Any database or runtime errors are caught and shown to the user via a messagebox.
        """
        steps_text = self.step_entry.get().strip()

        if not steps_text:
            messagebox.showerror("Missing Information", "Please enter your steps.")
            self.step_entry.focus()
            return

        if not steps_text.isdigit():
            messagebox.showerror("Invalid Input", "Please enter your steps as a whole number.")
            self.step_entry.focus()
            return

        steps_value = int(steps_text)

        if steps_value < 0:
            messagebox.showerror("Invalid Input", "Steps cannot be negative.")
            self.step_entry.focus()
            return

        try:
            save_steps(self.user.user_id, str(steps_value), 10000)

            self.step_count = steps_value
            self.count_label.config(text=f"Step Count: {self.step_count}")

            weight = get_weight(self.user.user_id)
            self.calorie_count = calories_burnt(steps_value, weight)
            self.calorie_label.config(text=f"Calories Burnt: {round(self.calorie_count)} kcal")

            messagebox.showinfo("Success", f"Steps saved! {self.step_count} steps recorded.")

            self.step_entry.delete(0, "end")
            self.step_entry.focus()

            self.step_graph.refresh_graph()

            if steps_value >= 10000:
                messagebox.showinfo(
                    "Congratulations!",
                    f"Well done {self.user.username}. You smashed 10,000 steps — go treat yourself!",
                )

        except Exception as exc:
            messagebox.showerror("Database Error", f"Failed to save to database: {exc}")
            self.step_entry.focus()


class StepGraph:
    """Embedded matplotlib graph showing the user's last 7 days of steps + export button."""

    def __init__(self, graph_frame: tb.Frame, user: User, stepframe: tb.Frame, root: tb.Window) -> None:
        """
        Args:
            graph_frame: Parent frame that the graph and buttons are placed into.
            user: Logged-in user (used for user_id and export filename).
            stepframe: Steps screen frame (used for navigation back to dashboard).
            root: Main application window (used for navigation).
        """
        self.graph_frame = graph_frame
        self.user = user
        self.stepframe = stepframe
        self.root = root

        self.graph_frame.grid(row=4, column=0, sticky="s")
        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)

        self.fig = Figure(figsize=(6, 4), dpi=80, facecolor="#222222")
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#2b3e50")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas_widget = self.canvas.get_tk_widget()

        self.plot_data()
        self.canvas_widget.grid(row=0, column=0, pady=(0, 10))

        self.button_frame = tb.Frame(self.graph_frame)
        self.button_frame.grid(row=1, column=0, pady=(0, 20))

        self.save_btn = tb.Button(self.button_frame, text="Download", command=self.save_graph)
        self.save_btn.grid(row=0, column=0, padx=(0, 5))

        self.dash_button = tb.Button(self.button_frame, text="Back to Dashboard", command=self.return_to_dash)
        self.dash_button.grid(row=0, column=1, padx=(5, 0))

    def plot_data(self) -> None:
        """
        Queries the DB for the last 7 days and redraws the line plot.
        """
        self.ax.clear()

        days, steps = get_last_7_days_steps_convert(self.user.user_id)

        self.ax.plot(days, steps, marker="o", color="#4e73df", linewidth=2, markersize=8)

        self.ax.set_xlabel("Days", color="#adb5bd")
        self.ax.set_ylabel("Steps", color="#adb5bd")
        self.ax.set_title("Steps Over Time", color="#ffffff")
        self.ax.tick_params(colors="#adb5bd")

        for spine in self.ax.spines.values():
            spine.set_color("#adb5bd")

        self.ax.grid(True, alpha=0.2, color="#adb5bd")
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
        Navigates back to the dashboard screen.
        """
        return_to_dashboard(self.stepframe, self.root, self.user)


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Steps(root, test_user)
    root.mainloop()
