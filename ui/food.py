import tkinter
import ttkbootstrap as tb
from tkinter import messagebox
from logic.user import User
from db.db_handler import save_steps


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
        self.foodframe.grid(row=0, column=0, sticky="n")

        # Window settings
        self.root.geometry("490x630")
        self.root.title("ReHealth")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

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
        self.food_entry_label.grid(row=1, column=1, pady=(50, 0))

        self.calorie_label = tb.Label(
            self.foodframe,
            text="Add Calorie Amount:",
            font=("roboto", 14)
        )
        self.calorie_label.grid(row=2, column=1, pady=(50, 0))

        # Entry boxes
        self.food_textbox = tb.Entry(self.foodframe)
        self.food_textbox.grid(row=1, column=2, pady=(50, 0))

        self.calorie_textbox = tb.Entry(self.foodframe)
        self.calorie_textbox.grid(row=2, column=2, pady=(50, 0))

        # Buttons
        self.food_add_button = tb.Button(self.foodframe, text="Add")
        self.food_add_button.grid(row=1, column=3, pady=(50, 0))

        self.calorie_add_button = tb.Button(self.foodframe, text="Add")
        self.calorie_add_button.grid(row=2, column=3, pady=(50, 0))


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Food(root, test_user)
    root.mainloop()
