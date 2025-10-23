import ttkbootstrap as tb
from tkinter import messagebox
from logic.user import User


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
        self.sleepframe.grid(row=0, column=0, sticky="n")
        self.root.geometry("490x630")
        self.root.title("ReHealth")

        # Makes root expandable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Labels

        self.rating_label = tb.Label(self.sleepframe, text="Sleep Rating")
        self.rating_label.grid


        self.sleep_label = tb.Label(
            self.sleepframe,
            text=f"{self.user.username}'s Sleep",
            font=("roboto", 18, "bold")
        )
        self.sleep_label.grid(row=0, column=0, pady=(0, 0), columnspan=2, padx=(50, 50))

        self.sleep_hours_label = tb.Label(self.sleepframe, text="Record your hours:",
                                          font=("roboto", 18, "bold"))
        self.sleep_hours_label.grid(row=1, column=0, pady=(20, 20))

        self.sleep_entry = tb.Entry(self.sleepframe)
        self.sleep_entry.grid(row=1, column=1, pady=(20, 20))

        self.sleep_refresh_label = tb.Label(self.sleepframe, text="Record your tiredness:", font=("roboto", 18, "bold"))
        self.sleep_refresh_label.grid(row=2, column=0, pady=(20, 20))

        self.refresh_entry = tb.Entry(self.sleepframe)
        self.refresh_entry.grid(row=2, column=1, pady=(20, 20))




if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    test_user = User("TestUser", "1234567", "Male", "26/12/2007", "29/08/2025", )
    app = Sleep(root, test_user)
    root.mainloop()
