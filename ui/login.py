""" Login Module - ReHealth"""

import random
import re
import sqlite3
from datetime import date
from tkinter import messagebox

import ttkbootstrap as tb

from db.db_handler import save_user_to_db, db_path, get_db_connection
from logic.user import User
from ui.dashboard import Dashboard


def quote_maker():
    """
    Returns a random motivational quote for the login screen.

    Returns:
        str: A randomly selected quote.
    """
    quote_list = [
        "'Your body is a temple.'", "'Health is wealth.'",
        "'Giving up is way harder than trying.'", "'Remember to take breaks.'",
        "'A lesson without pain is meaningless.'", "'Welcome back.'",
        "'Make your dreams a reality.'", "'Just do it.'",
        "'One day or day one.'"
    ]
    return random.choice(quote_list)


class App:
    """Login + registration screen controller. Creates widgets and handles user authentication."""

    def __init__(self, root):
        """
        Args:
            root: Main application window.
        """
        self.root = root
        self.root.title("ReHealth")
        self.root.geometry("490x630")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.mainframe = tb.Frame(self.root)
        self.mainframe.grid(row=0, column=0, sticky="nsew")

        self.mainframe.grid_rowconfigure((2, 4, 6), weight=0)
        self.mainframe.grid_columnconfigure(0, weight=1)

        # Login widgets (Shown by default)
        self.login_label = tb.Label(
            self.mainframe,
            text="ReHealth Login",
            font=("roboto", 15, "bold")
        )
        self.quote_label = tb.Label(
            self.mainframe,
            text=quote_maker(),
            font=("roboto", 11, "italic"),
            justify="center"
        )
        self.username_label = tb.Label(
            self.mainframe,
            text="Username",
            font=("roboto", 12, "bold")
        )
        self.username_entry = tb.Entry(self.mainframe)

        self.password_label = tb.Label(
            self.mainframe,
            text="Password",
            font=("roboto", 12, "bold")
        )
        self.password_entry = tb.Entry(self.mainframe, show="*")

        self.login_button = tb.Button(
            self.mainframe,
            text="REVOLUTIONISE FITNESS",
            command=self.login_func
        )

        # Registration widgets (only shown after user chooses to register)
        self.sex_label = tb.Label(
            self.mainframe,
            text="Biological Sex",
            font=("roboto", 12, "bold")
        )
        self.sex_combobox = tb.Combobox(
            self.mainframe,
            values=["Male", "Female"],
            state="readonly",
            width=27
        )

        self.dob_label = tb.Label(
            self.mainframe,
            text="Date of Birth",
            font=("roboto", 12, "bold")
        )

        self.dob_frame = tb.Frame(self.mainframe)

        self.day_label = tb.Label(self.dob_frame, text="Day", font=("roboto", 10))
        self.day_spinbox = tb.Spinbox(
            self.dob_frame,
            from_=1,
            to=31,
            width=5,
            format="%02.0f"
        )
        self.day_spinbox.set(1)

        self.month_label = tb.Label(self.dob_frame, text="Month", font=("roboto", 10))
        self.month_combobox = tb.Combobox(
            self.dob_frame,
            values=["January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"],
            state="readonly",
            width=10
        )
        self.month_combobox.current(0)

        current_year = date.today().year
        self.year_label = tb.Label(self.dob_frame, text="Year", font=("roboto", 10))
        self.year_spinbox = tb.Spinbox(
            self.dob_frame,
            from_=1900,
            to=current_year,
            width=7
        )
        self.year_spinbox.set(2000)

        self.register_button = tb.Button(
            self.mainframe,
            text="REVOLUTIONISE FITNESS",
            command=self.register_submit
        )

        # Initial layout: login-only view
        self.login_label.grid(row=0, column=0, pady=(10, 5))
        self.quote_label.grid(row=1, column=0, pady=(0, 15), padx=10)

        self.username_label.grid(row=2, column=0, sticky="w", padx=10, pady=(15, 0))
        self.username_entry.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 25))

        self.password_label.grid(row=4, column=0, sticky="w", padx=10, pady=(15, 0))
        self.password_entry.grid(row=5, column=0, sticky="ew", padx=10, pady=(0, 25))

        self.login_button.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

    def login_func(self):
        """
        Checks credentials against the database and loads the dashboard on success.
        """
        username_attempt = self.username_entry.get()
        password_attempt = self.password_entry.get()

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT UserID, Username, Password, Sex, DateOfBirth, JoinDate
            FROM User WHERE Username = ?
            """,
            (username_attempt,)
        )
        result = cursor.fetchone()
        connection.close()

        if result:
            fetched_user = User(
                username=result[1],
                password=result[2],
                sex=result[3],
                dob=result[4],
                join_date=result[5],
                user_id=result[0]
            )

            if fetched_user.password_check(password_attempt):
                messagebox.showinfo("Success", "Login successful!")
                self.mainframe.grid_forget()
                Dashboard(self.root, fetched_user)
            else:
                self.login_failed()
        else:
            self.login_failed()

    def login_failed(self):
        """Handles failed login attempts."""
        response = messagebox.askretrycancel(
            "Login Failed",
            "Incorrect username or password.\n\n"
            "Would you like to try again? Press 'Retry'.\n"
            "Or press 'Cancel' to register a new account."
        )
        if response:
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.username_entry.focus()
        else:
            self.show_register_fields()

    def show_register_fields(self):
        """Switches the UI from login mode into registration mode."""
        messagebox.showinfo("Register", "Please fill in the fields to register a new account.")

        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.sex_combobox.set('')
        self.day_spinbox.set(1)
        self.month_combobox.current(0)
        self.year_spinbox.set(2000)

        self.mainframe.grid_rowconfigure((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), weight=0)

        self.login_label.grid(row=0, column=0, pady=(10, 5))
        self.quote_label.grid(row=1, column=0, pady=(0, 15), padx=10)

        self.username_label.grid(row=2, column=0, sticky="w", padx=10, pady=(15, 0))
        self.username_entry.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 25))

        self.password_label.grid(row=4, column=0, sticky="w", padx=10, pady=(15, 0))
        self.password_entry.grid(row=5, column=0, sticky="ew", padx=10, pady=(0, 25))

        self.sex_label.grid(row=7, column=0, sticky="w", padx=10, pady=(15, 0))
        self.sex_combobox.grid(row=8, column=0, padx=10, pady=(0, 25), sticky="ew")

        self.dob_label.grid(row=9, column=0, sticky="w", padx=10, pady=(15, 0))
        self.dob_frame.grid(row=10, column=0, padx=10, pady=(0, 25), sticky="ew")

        self.day_label.grid(row=0, column=0, padx=(0, 5))
        self.day_spinbox.grid(row=1, column=0, padx=(0, 10))

        self.month_label.grid(row=0, column=1, padx=(0, 5))
        self.month_combobox.grid(row=1, column=1, padx=(0, 10))

        self.year_label.grid(row=0, column=2, padx=(0, 5))
        self.year_spinbox.grid(row=1, column=2)

        self.login_button.grid_forget()
        self.register_button.grid(row=11, column=0, padx=10, pady=10, sticky="ew")

    def register_submit(self):
        """
        Validates registration inputs and creates a new user record.

        Raises:
            None. Validation failures and database errors are shown via messageboxes.
        """
        username_input = self.username_entry.get().strip()
        password_input = self.password_entry.get().strip()
        sex_input = self.sex_combobox.get().strip()

        if not re.match(r"^[A-Za-z0-9_.]{3,20}$", username_input):
            messagebox.showerror(
                "Error",
                "Username must be 3-20 characters, letters, numbers, underscores, or dots."
            )
            return

        if len(password_input) < 8 or len(password_input) > 20:
            messagebox.showerror("Error", "Password must be between 8 and 20 characters.")
            return

        password_score = 0
        if re.search(r"[A-Z]", password_input):
            password_score += 1
        if re.search(r"[a-z]", password_input):
            password_score += 1
        if re.search(r"[0-9]", password_input):
            password_score += 1
        if re.search(r"[^A-Za-z0-9]", password_input):
            password_score += 1

        if password_score < 3:
            messagebox.showerror(
                "Error",
                "Password should mix uppercase, lowercase, numbers, and special characters."
            )
            return

        if not sex_input or sex_input not in ("Male", "Female"):
            messagebox.showerror("Error", "Please select a biological sex.")
            return

        try:
            day = int(self.day_spinbox.get())
            month = self.month_combobox.current() + 1
            year = int(self.year_spinbox.get())

            dob_date = date(year, month, day)

            if dob_date > date.today():
                messagebox.showerror("Error", "Date of birth cannot be in the future.")
                return

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid date of birth.")
            return

        today = date.today()
        hashed_password = User.password_hasher(password_input)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT Username FROM User WHERE Username = ?", (username_input,))
        if cursor.fetchone():
            messagebox.showerror("Error", "Username already exists. Please choose another.")
            connection.close()
            return

        new_user = User(username_input, hashed_password, sex_input, dob_date, today)

        try:
            save_user_to_db(new_user)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register user: {e}")
            connection.close()
            return

        connection.close()

        messagebox.showinfo("Success", "Registration complete! You can now log in.")

        self.sex_label.grid_forget()
        self.sex_combobox.grid_forget()
        self.dob_label.grid_forget()
        self.dob_frame.grid_forget()
        self.register_button.grid_forget()

        self.login_button.grid(row=6, column=0, pady=10, padx=10, sticky="ew")

        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.sex_combobox.set('')
        self.day_spinbox.set(1)
        self.month_combobox.current(0)
        self.year_spinbox.set(2000)
        self.username_entry.focus()


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    app = App(root)
    root.mainloop()
