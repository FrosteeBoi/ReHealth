import os
from tkinter import messagebox

import ttkbootstrap as tb
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from db.db_handler import save_food, get_last_7_days_calories_convert
from logic.user import User
from ui.ui_handler import return_to_dashboard


class Food:
    """
    Class created to manage the food interface and user input.
    """

    def __init__(self, root, user: User):
        """
        Main window for food input initialised.
        """
        self.root = root
        self.user = user

        # Main frame
        self.foodframe = tb.Frame(self.root)
        self.foodframe.place(relx=0.5, rely=0, anchor="n")

        # Window settings
        self.root.geometry("490x630")
        self.root.title("ReHealth")

        self.meal_type_options = ["breakfast", "lunch", "dinner", "snack"]

        # Title Label
        self.food_label = tb.Label(
            self.foodframe,
            text=f"{self.user.username}'s Food",
            font=("roboto", 18, "bold")
        )
        self.food_label.grid(row=0, column=0, pady=(20, 30), columnspan=2,
                             padx=20)

        # Food Name Section
        self.food_entry_label = tb.Label(
            self.foodframe,
            text="Food Name:",
            font=("roboto", 14)
        )
        self.food_entry_label.grid(row=1, column=0, pady=(10, 10),
                                   padx=(20, 10), sticky="e")

        self.food_textbox = tb.Entry(self.foodframe, width=25)
        self.food_textbox.grid(row=1, column=1, pady=(10, 10), padx=(10, 20),
                               sticky="w")

        # Calorie Section
        self.calorie_label = tb.Label(
            self.foodframe,
            text="Calorie Amount:",
            font=("roboto", 14)
        )
        self.calorie_label.grid(row=2, column=0, pady=(10, 10),
                                padx=(20, 10), sticky="e")

        self.calorie_textbox = tb.Entry(self.foodframe, width=25)
        self.calorie_textbox.grid(row=2, column=1, pady=(10, 10),
                                  padx=(10, 20), sticky="w")

        # Meal Type Section
        self.meal_type_label = tb.Label(
            self.foodframe,
            text="Meal Type:",
            font=("roboto", 14)
        )
        self.meal_type_label.grid(row=3, column=0, pady=(10, 10),
                                  padx=(20, 10), sticky="e")

        self.meal_type_combobox = tb.Combobox(
            self.foodframe,
            values=self.meal_type_options,
            width=23
        )
        self.meal_type_combobox.grid(row=3, column=1, pady=(10, 10),
                                     padx=(10, 20), sticky="w")

        # Database Button
        self.db_add_button = tb.Button(
            self.foodframe,
            text="Add to Database",
            command=self.database_inc
        )
        self.db_add_button.grid(row=4, column=0, pady=(30, 10), columnspan=2)

        # Add graph frame
        self.graph_frame = tb.Frame(self.foodframe)
        self.graph_frame.grid(row=5, column=0, columnspan=2, pady=0, padx=20)
        self.calorie_graph = CalorieGraph(self.graph_frame, self.user,
                                          self.foodframe, self.root)

    def database_inc(self):
        """
        Validates all fields and saves food to database
        """
        # Get values from entries
        foodname = self.food_textbox.get().strip()
        calorie_amount = self.calorie_textbox.get().strip()
        meal_type = self.meal_type_combobox.get().strip()

        # Validate food name
        if not foodname:
            messagebox.showerror(
                "Missing Information",
                "Please enter the food name."
            )
            self.food_textbox.focus()
            return

        # Validate calorie amount
        if not calorie_amount:
            messagebox.showerror(
                "Missing Information",
                "Please enter a calorie amount."
            )
            self.calorie_textbox.focus()
            return

        if not calorie_amount.isdigit():
            messagebox.showerror(
                "Invalid Input",
                "Calorie amount must be a number."
            )
            self.calorie_textbox.focus()
            return

        # Validate meal type
        if not meal_type:
            messagebox.showerror(
                "Missing Information",
                "Please select a meal type."
            )
            self.meal_type_combobox.focus()
            return

        if meal_type.lower() not in self.meal_type_options:
            messagebox.showerror(
                "Invalid Input",
                "Please select a valid meal type from the dropdown."
            )
            self.meal_type_combobox.focus()
            return

        # All fields are valid, save to database
        try:
            save_food(
                self.user.user_id,
                foodname,
                calorie_amount,
                meal_type.lower()
            )
            messagebox.showinfo(
                "Success",
                f"{foodname} ({calorie_amount} cals) saved as {meal_type}!"
            )

            # Clear all fields after successful save
            self.food_textbox.delete(0, 'end')
            self.calorie_textbox.delete(0, 'end')
            self.meal_type_combobox.set('')
            self.food_textbox.focus()

            # Refresh the graph to show updated data
            self.calorie_graph.refresh_graph()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"Failed to save to database: {str(e)}"
            )


class CalorieGraph:
    """
    Graph widget to display calories over time
    """

    def __init__(self, graph_frame, user: User, foodframe, root):
        """
        Initialises graph
        graph_frame: frame to place graph
        user: user id whose calories are recorded
        foodframe: main food frame for navigation
        root: root window
        """
        self.graph_frame = graph_frame
        self.user = user
        self.foodframe = foodframe
        self.root = root

        self.graph_frame.grid(row=5, column=0, sticky="s")

        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)

        self.fig = Figure(figsize=(6, 4), dpi=67, facecolor='#222222')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#2b3e50')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas_widget = self.canvas.get_tk_widget()

        # Initial plot
        self.plot_data()

        # Packs the canvas
        self.canvas_widget.grid(row=0, column=0, pady=(0, 10))

        # Frame for Download and Back to Dashboard buttons initialised
        self.button_frame = tb.Frame(self.graph_frame)
        self.button_frame.grid(row=1, column=0, pady=(0, 10))

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

    def plot_data(self):
        """
        Plots calorie data on the graph
        """
        # Clear previous plot
        self.ax.clear()

        # Grabs calorie data
        days, calories = get_last_7_days_calories_convert(self.user.user_id)

        # Plots the data
        self.ax.plot(days, calories, marker='o', color='#4e73df',
                     linewidth=2, markersize=8)
        self.ax.set_xlabel('Days', color='#adb5bd')
        self.ax.set_ylabel('Calories', color='#adb5bd')
        self.ax.set_title('Calories Over Time', color='#ffffff')

        # Graph styling
        self.ax.tick_params(colors='#adb5bd')
        self.ax.spines['bottom'].set_color('#adb5bd')
        self.ax.spines['top'].set_color('#adb5bd')
        self.ax.spines['left'].set_color('#adb5bd')
        self.ax.spines['right'].set_color('#adb5bd')

        self.ax.grid(True, alpha=0.2, color='#adb5bd')

        # Redraw the canvas
        self.canvas.draw()

    def refresh_graph(self):
        """
        Refreshes the graph with updated data
        """
        self.plot_data()

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
                f'{self.user.username}_calories_graph_week.png'
            )

            self.fig.savefig(filename, dpi=100, facecolor='#222222')

            messagebox.showinfo("Success", f"Graph saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save graph: {str(e)}")

    def return_to_dash(self):
        """
        Returns to the dashboard screen
        """
        return_to_dashboard(self.foodframe, self.root, self.user)


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007",
                     "29/08/2025")
    app = Food(root, test_user)
    root.mainloop()
