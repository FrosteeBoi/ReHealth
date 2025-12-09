import os
from tkinter import messagebox

import ttkbootstrap as tb
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from db.db_handler import (get_weight, save_steps,
                           get_last_7_days_steps_convert)
from logic.calculations import calories_burnt
from logic.user import User
from ui.ui_handler import return_to_dashboard


class Steps:
    """
    Class created to record steps and display them to the user
    """

    def __init__(self, root, user: User):
        """
        Main window for measurement initialised
        """
        self.root = root
        self.user = user
        self.stepframe = tb.Frame(self.root)
        self.stepframe.place(relx=0.5, rely=0, anchor="n")
        self.root.geometry("490x630")
        self.root.title("ReHealth")

        # Initialises variables
        self.step_count = 0
        self.calorie_count = 0

        # Labels
        self.steps_label = tb.Label(
            self.stepframe,
            text=f"{self.user.username}'s Steps",
            font=("roboto", 18, "bold")
        )
        self.steps_label.grid(row=0, column=0, pady=(20, 30), padx=20,
                              columnspan=2)

        self.count_label = tb.Label(
            self.stepframe,
            text=f"Step Count: 0",
            font=("roboto", 14)
        )
        self.count_label.grid(row=1, column=0, pady=(10, 10), padx=20,
                              columnspan=2)

        self.calorie_label = tb.Label(
            self.stepframe,
            text=f"Calories Burnt: 0 kcal",
            font=("roboto", 14)
        )
        self.calorie_label.grid(row=2, column=0, pady=(10, 30), padx=20,
                                columnspan=2)

        # Entry and Button initialised
        self.step_entry = tb.Entry(self.stepframe, width=20)
        self.step_entry.grid(row=3, column=0, padx=(20, 10), pady=(10, 10))

        self.step_button = tb.Button(
            self.stepframe,
            text="Add Steps",
            command=self.steps_and_calories
        )
        self.step_button.grid(row=3, column=1, pady=(10, 10), padx=(10, 20))

        self.graph_frame = tb.Frame(self.stepframe)
        self.graph_frame.grid(row=4, column=0, columnspan=2, pady=0, padx=20)
        self.step_graph = StepGraph(self.graph_frame, self.user,
                                    self.stepframe, self.root)

    def step_inc(self):
        try:
            value = int(self.step_entry.get())
            if value < 0:
                messagebox.showerror("Invalid Input", "Steps cannot be negative.")
                return
            self.step_count = str(value)
            self.step_entry.delete(0, 'end')
            self.count_label.config(text=f"Step Count: {self.step_count}")

            save_steps(self.user.user_id, self.step_count, 10000)

            if value >= 10000:
                messagebox.showinfo(
                    "Congratulations!",
                    f"Well done {self.user.username}. You smashed 10,000 steps go treat yourself!"
                )

        except ValueError:
            messagebox.showerror(
                "Failed input",
                "Please enter your steps as an integer."
            )

    def calorie_inc(self):
        """
        Calculates and updates calories burnt only if steps are recorded
        """
        if self.step_count and str(self.step_count).isdigit():
            weight = get_weight(self.user.user_id)
            steps = int(self.step_count)
            self.calorie_count = calories_burnt(steps, weight)
            self.calorie_label.config(
                text=f"Calories Burnt: {round(self.calorie_count)} kcal"
            )

    def steps_and_calories(self):
        """
        Adds steps and calculates calories burnt
        """
        self.step_inc()
        self.calorie_inc()


class StepGraph:
    """
    Graph widget to display steps over time
    """

    def __init__(self, graph_frame, user: User, stepframe, root):
        """
        Initialises graph
        graph_frame: frame to place graph
        user: user id whose steps are recorded
        stepframe: main step frame for navigation
        root: root window
        """
        self.graph_frame = graph_frame
        self.user = user
        self.stepframe = stepframe
        self.root = root

        self.graph_frame.grid(row=4, column=0, sticky="s")

        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)

        self.fig = Figure(figsize=(6, 4), dpi=80, facecolor='#222222')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#2b3e50')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas_widget = self.canvas.get_tk_widget()

        # Grabs steps data
        days, steps = get_last_7_days_steps_convert(self.user.user_id)

        # Plot the data
        self.ax.plot(days, steps, marker='o', color='#4e73df',
                     linewidth=2, markersize=8)
        self.ax.set_xlabel('Days', color='#adb5bd')
        self.ax.set_ylabel('Steps', color='#adb5bd')
        self.ax.set_title('Steps Over Time', color='#ffffff')

        # Graph styling
        self.ax.tick_params(colors='#adb5bd')
        self.ax.spines['bottom'].set_color('#adb5bd')
        self.ax.spines['top'].set_color('#adb5bd')
        self.ax.spines['left'].set_color('#adb5bd')
        self.ax.spines['right'].set_color('#adb5bd')

        self.ax.grid(True, alpha=0.2, color='#adb5bd')

        # Pack the canvas
        self.canvas_widget.grid(row=0, column=0, pady=(0, 10))

        # Frame for Download and Back to Dashboard buttons initialised
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

    def save_graph(self):
        """
        Saves image of graph to images folder
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
                f'{self.user.username}_steps_graph_week.png'
            )

            self.fig.savefig(filename, dpi=100, facecolor='#222222')

            messagebox.showinfo("Success", f"Graph saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save graph: {str(e)}")

    def return_to_dash(self):
        """
        Returns to the dashboard screen
        """
        return_to_dashboard(self.stepframe, self.root, self.user)


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007",
                     "29/08/2025")
    app = Steps(root, test_user)
    root.mainloop()
