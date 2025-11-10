import os
import ttkbootstrap as tb
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from logic.user import User
from logic.calculations import sleep_calc
from db.db_handler import save_sleep, get_last_7_days_sleep_convert


class Sleep:
    """
    Class created to record user sleep and display it to the user
    """

    def __init__(self, root, user: User):
        """
        Main window for sleep tracking initialised
        """
        self.root = root
        self.user = user
        self.sleepframe = tb.Frame(self.root)
        self.sleepframe.place(relx=0.5, rely=0, anchor="n")
        self.root.geometry("490x630")
        self.root.title("ReHealth")
        self.sleep_duration = None
        self.sleep_quality = None
        self.rating = None

        # Labels
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
        self.sleep_entry.grid(row=2, column=1, pady=(20, 20))

        self.hours_button = tb.Button(
            self.sleepframe,
            text="Add",
            command=self.hours_inc
        )
        self.hours_button.grid(row=2, column=2, pady=(20, 20), padx=(10, 0))

        self.sleep_refresh_label = tb.Label(
            self.sleepframe,
            text="Record how you feel(1-5):",
            font=("roboto", 14)
        )
        self.sleep_refresh_label.grid(row=3, column=0, pady=(20, 20), sticky="e", padx=(0, 10))

        self.refresh_entry = tb.Entry(self.sleepframe)
        self.refresh_entry.grid(row=3, column=1, pady=(20, 20))

        self.refresh_button = tb.Button(
            self.sleepframe,
            text="Add",
            command=self.quality_inc
        )
        self.refresh_button.grid(row=3, column=2, pady=(20, 20), padx=(10, 0))

        self.rating_button = tb.Button(
            self.sleepframe,
            text="Calculate Rating",
            command=self.update_rating
        )
        self.rating_button.grid(row=4, column=0, pady=(0, 20), columnspan=3)

        # Adds graph frame
        self.graph_frame = tb.Frame(self.sleepframe)
        self.graph_frame.grid(row=5, column=0, columnspan=3, pady=(0, 20), padx=20)
        self.sleep_graph = SleepGraph(self.graph_frame, self.user)

    def hours_inc(self):
        """Receive hours input from user to store"""
        try:
            hours = float(self.sleep_entry.get())
            if hours < 0 or hours > 24:
                raise ValueError
            self.sleep_duration = hours
            self.sleep_entry.delete(0, 'end')
            messagebox.showinfo("Success", f"Recorded {hours} hours of sleep!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of hours (0-24).")

    def quality_inc(self):
        """Get sleep quality input from user and store it."""
        try:
            quality = int(self.refresh_entry.get())
            if quality < 1 or quality > 5:
                raise ValueError
            self.sleep_quality = quality
            self.refresh_entry.delete(0, 'end')
            messagebox.showinfo("Success", f"Recorded sleep quality: {quality}/5.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid sleep quality (1-5).")

    def update_rating(self):
        """Calculates and displays sleep rating."""
        if self.sleep_duration is not None and self.sleep_quality is not None:
            self.rating = sleep_calc(self.sleep_duration, self.sleep_quality)
            self.rating_label.config(text=f"Sleep Rating: {round(self.rating * 100)}%")
            save_sleep(self.user.user_id, self.sleep_duration, self.rating)


class SleepGraph:
    """
    graph widget to display sleep hours over time
    """

    def __init__(self, graph_frame, user: User):
        """
        initialises graph
        graph_frame: frame to place graph
        user: user id whose sleep is recorded
        """
        self.graph_frame = graph_frame
        self.user = user

        self.graph_frame.grid(row=5, column=0, sticky="s")

        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)

        self.fig = Figure(figsize=(6, 4), dpi=67, facecolor='#222222')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#2b3e50')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas_widget = self.canvas.get_tk_widget()

        # grabs sleep data
        days, sleep_hours = get_last_7_days_sleep_convert(self.user.user_id)

        # Plot the data
        self.ax.plot(days, sleep_hours, marker='o', color='#4e73df', linewidth=2, markersize=8)
        self.ax.set_xlabel('Days', color='#adb5bd')
        self.ax.set_ylabel('Hours', color='#adb5bd')
        self.ax.set_title('Sleep Over Time', color='#ffffff')

        # Graph styling
        self.ax.tick_params(colors='#adb5bd')
        self.ax.spines['bottom'].set_color('#adb5bd')
        self.ax.spines['top'].set_color('#adb5bd')
        self.ax.spines['left'].set_color('#adb5bd')
        self.ax.spines['right'].set_color('#adb5bd')

        self.ax.grid(True, alpha=0.2, color='#adb5bd')

        # Pack the canvas
        self.canvas_widget.grid(row=0, column=0, pady=(0, 10))

        self.save_btn = tb.Button(
            self.graph_frame,
            text="Download",
            command=self.save_graph
        )
        self.save_btn.grid(row=1, column=0, pady=(0, 10))

    def save_graph(self):
        """
        Saves image of graph to images folder
        """
        try:
            images_folder = os.path.join(os.path.dirname(__file__), "..", "images")
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


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Sleep(root, test_user)
    root.mainloop()