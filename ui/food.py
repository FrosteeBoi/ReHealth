import tkinter
import ttkbootstrap as tb
from tkinter import messagebox
from logic.user import User
from db.db_handler import save_steps
from


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
        self.foodframe.grid(row=0, column=0, sticky="n")

        # Window settings
        self.root.geometry("490x630")
        self.root.title("ReHealth")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.meal_type_options = ["breakfast", "lunch", "dinner", "snack"]

        # Labels
        self.food_label = tb.Label(
            self.foodframe,
            text=f"{self.user.username}'s Food",
            font=("roboto", 18, "bold")
        )
        self.food_label.grid(row=0, column=1, pady=(0, 0), columnspan=2, padx=(50, 0))

        self.food_entry_label = tb.Label(
            self.foodframe,
            text="Add Food Name:",
            font=("roboto", 14)
        )
        self.food_entry_label.grid(row=1, column=1, pady=(30, 0))

        self.calorie_label = tb.Label(
            self.foodframe,
            text="Add Calorie Amount:",
            font=("roboto", 14)
        )
        self.calorie_label.grid(row=2, column=1, pady=(30, 0))

        self.meal_type_label = tb.Label(
            self.foodframe,
            text="Add Meal Type:",
            font=("roboto", 14)
        )
        self.meal_type_label.grid(row=3, column=1, pady=(30, 0))

        # Entry boxes
        self.food_textbox = tb.Entry(self.foodframe)
        self.food_textbox.grid(row=1, column=2, pady=(30, 0))

        self.calorie_textbox = tb.Entry(self.foodframe)
        self.calorie_textbox.grid(row=2, column=2, pady=(30, 0))

        self.meal_type_combobox = tb.Combobox(self.foodframe, values=self.meal_type_options)
        self.meal_type_combobox.grid(row=3, column=2, pady=(30, 0))

        # Buttons
        self.food_add_button = tb.Button(self.foodframe, text="Add", command=self.food_name_inc)
        self.food_add_button.grid(row=1, column=3, pady=(30, 0))

        self.calorie_add_button = tb.Button(self.foodframe, text="Add", command=self.calorie_name_inc)
        self.calorie_add_button.grid(row=2, column=3, pady=(30, 0))

        self.meal_type_button = tb.Button(self.foodframe, text="Add", command=self.meal_type_inc)
        self.meal_type_button.grid(row=3, column=3, pady=(30, 0))

        self.db_add_button = tb.Button(self.foodframe, text="Add to database")
        self.db_add_button.grid(row=4, column=1, pady=(30, 0), padx=(75, 0), columnspan=2)

    def food_name_inc(self):
        try:
            self.foodname = self.food_textbox.get()
            if not self.foodname.strip():
                raise ValueError
            messagebox.showinfo("Success", f"Food: {self.foodname} recorded!")
        except ValueError:
            messagebox.showerror("Error", "Input cannot be empty space.")

    def calorie_name_inc(self):
        try:
            self.calorie_amount = self.calorie_textbox.get()
            if not self.calorie_amount.strip():
                raise ValueError
            if not self.calorie_amount.isdigit():
                raise ValueError
            messagebox.showinfo("Success", f"{self.calorie_amount} cals recorded!")
        except ValueError:
            messagebox.showerror("Error", "Input calories as digits only.")
    def meal_type_inc(self):
        try:
            self.meal_type = self.meal_type_combobox.get()
            if not self.meal_type.strip():
                raise ValueError
            messagebox.showinfo("Success", f"Food: {self.meal_type} recorded!")
        except ValueError:
            messagebox.showerror("Error", "Enter an meal option given below.")

    def database_inc(self):
        if self.foodname is not None and self.calorie_amount is not None and self.meal_type is not None:
            save_food


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Food(root, test_user)
    root.mainloop()
