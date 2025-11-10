import os
import ttkbootstrap as tb
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from logic.user import User
from db.db_handler import save_food, get_last_7_days_calories_convert


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

        # Variables
        self.foodname = None
        self.calorie_amount = None
        self.meal_type = None

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
        self.food_label.grid(row=0, column=0, pady=(20, 30), columnspan=3, padx=20)

        # Food Name Section
        self.food_entry_label = tb.Label(
            self.foodframe,
            text="Add Food Name:",
            font=("roboto", 14)
        )
        self.food_entry_label.grid(row=1, column=0, pady=(10, 10), padx=(20, 10), sticky="e")

        self.food_textbox = tb.Entry(self.foodframe, width=20)
        self.food_textbox.grid(row=1, column=1, pady=(10, 10), padx=(10, 10))

        self.food_add_button = tb.Button(
            self.foodframe,
            text="Add",
            command=self.food_name_inc,
            width=8
        )
        self.food_add_button.grid(row=1, column=2, pady=(10, 10), padx=(10, 20))

        # Calorie Section
        self.calorie_label = tb.Label(
            self.foodframe,
            text="Add Calorie Amount:",
            font=("roboto", 14)
        )
        self.calorie_label.grid(row=2, column=0, pady=(10, 10), padx=(20, 10), sticky="e")

        self.calorie_textbox = tb.Entry(self.foodframe, width=20)
        self.calorie_textbox.grid(row=2, column=1, pady=(10, 10), padx=(10, 10))

        self.calorie_add_button = tb.Button(
            self.foodframe,
            text="Add",
            command=self.calorie_name_inc,
            width=8
        )
        self.calorie_add_button.grid(row=2, column=2, pady=(10, 10), padx=(10, 20))

        # Meal Type Section
        self.meal_type_label = tb.Label(
            self.foodframe,
            text="Add Meal Type:",
            font=("roboto", 14)
        )
        self.meal_type_label.grid(row=3, column=0, pady=(10, 10), padx=(20, 10), sticky="e")

        self.meal_type_combobox = tb.Combobox(
            self.foodframe,
            values=self.meal_type_options,
            width=18
        )
        self.meal_type_combobox.grid(row=3, column=1, pady=(10, 10), padx=(10, 10))

        self.meal_type_button = tb.Button(
            self.foodframe,
            text="Add",
            command=self.meal_type_inc,
            width=8
        )
        self.meal_type_button.grid(row=3, column=2, pady=(10, 10), padx=(10, 20))

        # Database Button
        self.db_add_button = tb.Button(
            self.foodframe,
            text="Add to Database",
            command=self.database_inc
        )
        self.db_add_button.grid(row=4, column=0, pady=(30, 10), columnspan=3)

        # Add graph frame
        self.graph_frame = tb.Frame(self.foodframe)
        self.graph_frame.grid(row=5, column=0, columnspan=3, pady=20, padx=20)
        self.calorie_graph = CalorieGraph(self.graph_frame, self.user)

    def food_name_inc(self):
        """
        Records name of food
        :return:
        """
        self.foodname = self.food_textbox.get()
        if not self.foodname.strip():
            messagebox.showerror("Error", "Input cannot be empty space.")
            return
        self.food_textbox.delete(0, 'end')
        messagebox.showinfo("Success", f"Food: {self.foodname} recorded!")

    def calorie_name_inc(self):
        """
        Records calorie amount
        """
        self.calorie_amount = self.calorie_textbox.get()
        if not self.calorie_amount.strip() or not self.calorie_amount.isdigit():
            messagebox.showerror("Error", "Input calories as digits only.")
            return
        self.calorie_textbox.delete(0, 'end')
        messagebox.showinfo("Success", f"{self.calorie_amount} cals recorded!")

    def meal_type_inc(self):
        """
        Records type of meal recorded by user
        """
        self.meal_type = self.meal_type_combobox.get()
        if not self.meal_type.strip():
            messagebox.showerror("Error", "Enter a meal option given below.")
            return
        messagebox.showinfo("Success", f"Meal type: {self.meal_type} recorded!")

    def database_inc(self):
        """
        Saves food to database
        """
        if self.foodname is not None and self.calorie_amount is not None and self.meal_type is not None:
            save_food(
                self.user.user_id,
                self.foodname,
                self.calorie_amount,
                self.meal_type
            )
            messagebox.showinfo(
                "Success",
                f"{self.foodname} saved to database as {self.meal_type}"
            )


class CalorieGraph:
    """
    graph widget to display calories over time
    """

    def __init__(self, graph_frame, user: User):
        """
        initialises graph
        graph_frame: frame to place graph
        user: user id whose calories are recorded
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

        # grabs calorie data
        days, calories = get_last_7_days_calories_convert(self.user.user_id)

        # Plot the data
        self.ax.plot(days, calories, marker='o', color='#4e73df', linewidth=2, markersize=8)
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
                f'{self.user.username}_calories_graph_week.png'
            )

            self.fig.savefig(filename, dpi=100, facecolor='#222222')

            messagebox.showinfo("Success", f"Graph saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save graph: {str(e)}")


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Food(root, test_user)
    root.mainloop()