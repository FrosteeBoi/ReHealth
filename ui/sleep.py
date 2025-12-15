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


class Sleep:
    """Sleep tracking screen: records sleep inputs, calculates a rating, saves to DB, and displays a 7-day graph."""

    def __init__(self, root, user: User):
        """
        Args:
            root: Main application window.
            user: Logged-in user (used for user_id and username).
        """
        self.root = root
        self.user = user

        self.sleepframe = tb.Frame(self.root)
        self.sleepframe.place(relx=0.5, rely=0, anchor="n")

        self.root.geometry("490x630")
        self.root.title("ReHealth")

        # Stored values used for calculation and database saving
        self.sleep_duration = None
        self.sleep_quality = None
        self.rating = None

        self.sleep_label = tb.Label(
            self.sleepframe,
            text=f"{self.user.username}'s Sleep",
            font=("roboto", 18, "bold")
        )
        self.sleep_label.grid(row=0, column=0, pady=(20, 30), columnspan=3, padx=20)

        self.rating_label = tb.Label(
            self.sleepframe,
            text="Sleep Rating:",
            font=("roboto", 14)
        )
        self.rating_label.grid(row=1, column=0, pady=(10, 10), padx=20, columnspan=3)

        self.sleep_hours_label = tb.Label(
            self.sleepframe,
            text="Record your hours:",
            font=("roboto", 14)
        )
        self.sleep_hours_label.grid(row=2, column=0, pady=(20, 20), sticky="e", padx=(0, 10))

        self.sleep_entry = tb.Entry(self.sleepframe)
        self.sleep_entry.grid(row=2, column=1, pady=(20, 20), columnspan=2)

        self.sleep_refresh_label = tb.Label(
            self.sleepframe,
            text="Record how you feel (1-5):",
            font=("roboto", 14)
        )
        self.sleep_refresh_label.grid(row=3, column=0, pady=(20, 20), sticky="e", padx=(0, 10))

        self.refresh_entry = tb.Entry(self.sleepframe)
        self.refresh_entry.grid(row=3, column=1, pady=(20, 20), columnspan=2)

        self.rating_button = tb.Button(
            self.sleepframe,
            text="Calculate Rating",
            command=self.update_rating
        )
        self.rating_button.grid(row=4, column=0, columnspan=3)

        # Container for the embedded graph widget
        self.graph_frame = tb.Frame(self.sleepframe)
        self.graph_frame.grid(row=5, column=0, columnspan=3, pady=0, padx=20)

        self.sleep_graph = SleepGraph(self.graph_frame, self.user, self.sleepframe, self.root)

    def update_rating(self):
        """
        Validates inputs, calculates a sleep rating, saves to DB, updates UI, and refreshes the graph.
        """
        hours_input = self.sleep_entry.get().strip()
        quality_input = self.refresh_entry.get().strip()

        # Presence + type + range check for sleep hours (float allows half-hours, etc.)
        if not hours_input:
            messagebox.showerror("Error", "Please enter a valid number of hours (0-24).")
            self.sleep_entry.focus()
            return

        try:
            hours = float(hours_input)
            if hours < 0 or hours > 24:
                messagebox.showerror("Error", "Please enter a valid number of hours (0-24).")
                self.sleep_entry.focus()
                return
            self.sleep_duration = hours
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of hours (0-24).")
            self.sleep_entry.focus()
            return

        # Presence + type + range check for sleep quality (must be integer 1–5)
        if not quality_input:
            messagebox.showerror("Error", "Please enter a valid sleep quality (1-5).")
            self.refresh_entry.focus()
            return

        try:
            quality = int(quality_input)
            if quality < 1 or quality > 5:
                messagebox.showerror("Error", "Please enter a valid sleep quality (1-5).")
                self.refresh_entry.focus()
                return
            self.sleep_quality = quality
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid sleep quality (1-5).")
            self.refresh_entry.focus()
            return

        # Rating algorithm is kept in a separate logic function for modularity
        self.rating = sleep_calc(self.sleep_duration, self.sleep_quality)
        self.rating_label.config(text=f"Sleep Rating: {round(self.rating * 100)}%")

        try:
            # Save record to database linked to the logged-in user
            save_sleep(self.user.user_id, self.sleep_duration, self.rating)

            messagebox.showinfo(
                "Success",
                f"Sleep data saved! Rating: {round(self.rating * 100)}%"
            )

            # Reset inputs for the next entry
            self.sleep_entry.delete(0, 'end')
            self.refresh_entry.delete(0, 'end')
            self.sleep_entry.focus()

            # Refresh graph so the new DB record is visible immediately
            self.sleep_graph.refresh_graph()
            self.root.update_idletasks()

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save to database: {str(e)}")


class SleepGraph:
    """Embedded matplotlib graph showing the user's last 7 days of sleep hours with export + navigation buttons."""

    def __init__(self, graph_frame, user: User, sleepframe, root):
        """
        Args:
            graph_frame: Parent frame that the graph and buttons are placed into.
            user: Logged-in user (used for user_id and export filename).
            sleepframe: Sleep screen frame (used for navigation back to dashboard).
            root: Main application window (used for navigation).
        """
        self.graph_frame = graph_frame
        self.user = user
        self.sleepframe = sleepframe
        self.root = root

        self.graph_frame.grid(row=5, column=0, sticky="s")
        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)

        # Matplotlib setup (dark theme to match ttkbootstrap "darkly")
        self.fig = Figure(figsize=(6, 4), dpi=67, facecolor='#222222')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#2b3e50')

        # Embed the matplotlib figure into tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas_widget = self.canvas.get_tk_widget()

        self.plot_data()
        self.canvas_widget.grid(row=0, column=0, pady=(0, 10))

        # Button bar under the graph
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

    def plot_data(self):
        """
        Fetches the last 7 days of sleep hours and redraws the line plot.
        """
        self.ax.clear()

        days, sleep_hours = get_last_7_days_sleep_convert(self.user.user_id)

        self.ax.plot(days, sleep_hours, marker='o', color='#4e73df', linewidth=2, markersize=8)

        self.ax.set_xlabel('Days', color='#adb5bd')
        self.ax.set_ylabel('Hours', color='#adb5bd')
        self.ax.set_title('Sleep Over Time', color='#ffffff')

        # Styling for readability on a dark background
        self.ax.tick_params(colors='#adb5bd')
        for spine in self.ax.spines.values():
            spine.set_color('#adb5bd')

        self.ax.grid(True, alpha=0.2, color='#adb5bd')
        self.canvas.draw()

    def refresh_graph(self):
        """Replots data after a new sleep record is saved."""
        self.plot_data()

    def save_graph(self):
        """
        Exports the current graph image to the project's /images folder.
        """
        try:
            images_folder = os.path.join(os.path.dirname(__file__), "..", "images")
            images_folder = os.path.abspath(images_folder)

            # Ensure export folder exists before saving
            if not os.path.exists(images_folder):
                os.makedirs(images_folder)

            filename = os.path.join(images_folder, f'{self.user.username}_sleep_graph_week.png')

            # facecolor keeps the dark theme in the saved file
            self.fig.savefig(filename, dpi=100, facecolor='#222222')

            messagebox.showinfo("Success", f"Graph saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save graph: {str(e)}")

    def return_to_dash(self):
        """Returns to the dashboard screen."""
        return_to_dashboard(self.sleepframe, self.root, self.user)


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Sleep(root, test_user)
    root.mainloop()
