import tkinter
import ttkbootstrap as tb
from tkinter import messagebox
from logic.user import User



class Workouts:
    """
    Class created to manage and add user exercises
    """

    def __init__(self, root, user: User):
        """
        Main window for managing exercises initialised
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








if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025")
    app = Workouts(root, test_user)
    root.mainloop()
