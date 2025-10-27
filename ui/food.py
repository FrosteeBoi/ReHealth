import ttkbootstrap as tb
from tkinter import messagebox
from logic.user import User
from db.db_handler import save_steps

class Food:
    """
    Class created to
    """

    def __init__(self, root, user: User):
        """
        Main window for measurement initialised
        """
        self.root = root
        self.user = user
        self.foodframe = tb.Frame(self.root)
        self.foodframe.grid(row=0, column=0, sticky="n")
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
        self.food_label.grid(row=0, column=0, pady=(0, 0), columnspan=2, padx=(15, 0))



if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Food(root, test_user)
    root.mainloop()
