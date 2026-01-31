"""Login Module - ReHealth"""

import random
import re
import sqlite3
from datetime import date
from tkinter import messagebox

import ttkbootstrap as tb

from db.db_handler import save_user_to_db, db_path, get_db_connection
from logic.user import User
from ui.dashboard import Dashboard


def get_random_quote():
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


def validate_username(username: str) -> tuple[bool, str]:
    """
    Validates username inpit, returns error messages.

    Args:
        username: The username inputted by the user.

    Returns:
        A tuple describing the validity of the input possibly accompanied by an error message.
    """
    if not re.match(r"^[A-Za-z0-9_.]{3,20}$", username):
        return False, "Username must be between 3-20 characters inclusive, letters, numbers, underscores, or dots."
    return True, ""


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validates password strength and returns error messages.

    Args:
        password: The password inputted by the user.

    Returns:
        A tuple describing the validity of the input possibly accompanied by an error message.
    """
    if len(password) < 8 or len(password) > 20:
        return False, "Password must be between 8 and 20 characters inclusive."

    password_score = 0
    if re.search(r"[A-Z]", password):
        password_score += 1
    if re.search(r"[a-z]", password):
        password_score += 1
    if re.search(r"[0-9]", password):
        password_score += 1
    if re.search(r"[^A-Za-z0-9]", password):
        password_score += 1

    if password_score < 3:
        return False, "Password should mix uppercase, lowercase, numbers, and special characters."

    return True, ""


def validate_sex(sex: str) -> tuple[bool, str]:
    """
    Validates The sex that the user inputs and returns a descriptive error message.

    Args:
        sex: Biological sex selected by the user

    Returns:
        A tuple describing the validity of the input possibly accompanied by an error message.
    """
    if not sex or sex not in ("Male", "Female"):
        return False, "Please select a biological sex."
    return True, ""


def validate_date_of_birth(day: int, month: int, year: int) -> tuple[bool, date, str]:
    """
    Validates the date of birth inputted by the user.

    Args:
        day: Day selected by the user
        month: Month selected by the user
        year: Year selected by the user

    Returns:
        A tuple containing whether the input is valid, the date the user inputted and a possible error message.
    """
    try:
        dob_date = date(year, month, day)

        if dob_date > date.today():
            return False, None, "Date of birth cannot be in the future."

        return True, dob_date, ""
    except ValueError:
        return False, None, "Please enter a valid date of birth."


def check_username_exists(username: str) -> bool:
    """
    Checks if a username already exists in the database.

    Args:
        username: Username to be checked

    Returns:
        True if username exists, False otherwise.
    """

    # Set up a db connection and look for a matching user
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT Username FROM User WHERE Username = ?", (username,))
    exists = cursor.fetchone() is not None
    connection.close()
    return exists


class App:
    """Class for authenticating users and validating inputs so they can login or register."""

    def __init__(self, root: tb.Window) -> None:
        """
        Args:
            root: Main application window.
        """
        self.root = root

        self._configure_window()
        self._create_main_frame()
        self._create_widgets()
        self._show_login_view()

    def _configure_window(self) -> None:
        """Configure the login/register window."""
        self.root.title("ReHealth")
        self.root.geometry("490x630")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def _create_main_frame(self) -> None:
        """Create and configure the main frame for the App class."""
        self.mainframe = tb.Frame(self.root)
        self.mainframe.grid(row=0, column=0, sticky="nsew")
        self.mainframe.grid_rowconfigure((2, 4, 6), weight=0)
        self.mainframe.grid_columnconfigure(0, weight=1)

    def _create_widgets(self) -> None:
        """Create all widgets needed for the page."""
        self._create_header_widgets()
        self._create_login_widgets()
        self._create_registration_widgets()

    def _create_header_widgets(self) -> None:
        """Creates the main title for the window and displays a quote from predefined list."""
        self.login_label = tb.Label(
            self.mainframe,
            text="ReHealth Login",
            font=("roboto", 15, "bold")
        )
        self.quote_label = tb.Label(
            self.mainframe,
            text=get_random_quote(),
            font=("roboto", 11, "italic"),
            justify="center"
        )

    def _create_login_widgets(self) -> None:
        """Create username and password input widgets/entries."""
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

    def _create_registration_widgets(self) -> None:
        """Widgets and dropdown displays for dob and bilogical sex."""
        self.sex_label = tb.Label(
            self.mainframe,
            text="Biological Sex",
            font=("roboto", 12, "bold")
        )

        # Set up dropdown display for sex
        self.sex_combobox = tb.Combobox(
            self.mainframe,
            values=["Male", "Female"],
            state="readonly",
            width=27
        )

        # Set up dropdown display for date of birth
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

    def _show_login_view(self) -> None:
        """Display the initial login-only view."""
        self.login_label.grid(row=0, column=0, pady=(10, 5))
        self.quote_label.grid(row=1, column=0, pady=(0, 15), padx=10)

        self.username_label.grid(row=2, column=0, sticky="w", padx=10, pady=(15, 0))
        self.username_entry.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 25))

        self.password_label.grid(row=4, column=0, sticky="w", padx=10, pady=(15, 0))
        self.password_entry.grid(row=5, column=0, sticky="ew", padx=10, pady=(0, 25))

        self.login_button.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

    def login_func(self) -> None:
        """
        Checks credentials against a user in the database and loads the dashboard on success.
        """
        username_attempt = self.username_entry.get()
        password_attempt = self.password_entry.get()

        connection = get_db_connection()
        cursor = connection.cursor()

        # Search for a matching user in the database

        cursor.execute(
            """
            SELECT UserID, Username, Password, Sex, DateOfBirth, JoinDate
            FROM User WHERE Username = ?
            """,
            (username_attempt,)
        )
        result = cursor.fetchone()
        connection.close()

        # Create a user object if a match is found

        if result:
            fetched_user = User(
                username=result[1],
                password=result[2],
                sex=result[3],
                dob=result[4],
                join_date=result[5],
                user_id=result[0]
            )

            # Checks input password against hash stored in database

            if fetched_user.password_check(password_attempt):
                messagebox.showinfo("Success", "Login successful!")
                self.mainframe.grid_forget()
                Dashboard(self.root, fetched_user)
            else:
                self._login_failed()
        else:
            self._login_failed()

    def _login_failed(self) -> None:
        """Handles failed login attempts."""
        response = messagebox.askretrycancel(
            "Login Failed",
            "Incorrect username or password.\n\n"
            "Would you like to try again? Press 'Retry'.\n"
            "Or press 'Cancel' to register a new account."
        )

        # Clears fields and opens the registration page if the user permits it

        if response:
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.username_entry.focus()
        else:
            self._show_register_view()

    def _show_register_view(self) -> None:
        """Switches the UI from login mode into registration mode, sets up widgets/labels"""
        messagebox.showinfo("Register", "Please fill in the fields to register a new account.")

        self._clear_all_fields()

        # Configure mainframe grid
        self.mainframe.grid_rowconfigure((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), weight=0)

        # Display all widgets including registration fields
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

        # Grid date of birth components
        self.day_label.grid(row=0, column=0, padx=(0, 5))
        self.day_spinbox.grid(row=1, column=0, padx=(0, 10))

        self.month_label.grid(row=0, column=1, padx=(0, 5))
        self.month_combobox.grid(row=1, column=1, padx=(0, 10))

        self.year_label.grid(row=0, column=2, padx=(0, 5))
        self.year_spinbox.grid(row=1, column=2)

        # Swap login button for register button
        self.login_button.grid_forget()
        self.register_button.grid(row=11, column=0, padx=10, pady=10, sticky="ew")

    def register_submit(self) -> None:
        """
        Validates registration inputs and creates a new user record for the database
        """
        username_input = self.username_entry.get().strip()
        password_input = self.password_entry.get().strip()
        sex_input = self.sex_combobox.get().strip()

        # Validate registration inputs
        username_valid, username_error = validate_username(username_input)
        if not username_valid:
            messagebox.showerror("Error", username_error)
            return

        password_valid, password_error = validate_password(password_input)
        if not password_valid:
            messagebox.showerror("Error", password_error)
            return

        sex_valid, sex_error = validate_sex(sex_input)
        if not sex_valid:
            messagebox.showerror("Error", sex_error)
            return

        try:
            day = int(self.day_spinbox.get())
            month = self.month_combobox.current() + 1
            year = int(self.year_spinbox.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid date values.")
            return

        dob_valid, dob_date, dob_error = validate_date_of_birth(day, month, year)
        if not dob_valid:
            messagebox.showerror("Error", dob_error)
            return

        if check_username_exists(username_input):
            messagebox.showerror("Error", "Username already exists. Please choose another.")
            return

        # Create a user object from registration information and catch db error(s)

        try:
            self._create_user(username_input, password_input, sex_input, dob_date)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register user: {e}")

    def _create_user(self, username: str, password: str, sex: str, dob: date) -> None:
        """
        Creates a new user and saves to database.

        Args:
            username: User's chosen username.
            password: User's password (will be hashed).
            sex: User's biological sex.
            dob: User's date of birth.
        """
        today = date.today()
        hashed_password = User.password_hasher(password)

        new_user = User(username, hashed_password, sex, dob, today)
        save_user_to_db(new_user)

        messagebox.showinfo("Success", "Registration complete! You can now log in.")

        # Return to login view
        self._hide_registration_fields()
        self._clear_all_fields()
        self.username_entry.focus()

    def _hide_registration_fields(self) -> None:
        """Hides registration-specific fields and shows login button."""
        self.sex_label.grid_forget()
        self.sex_combobox.grid_forget()
        self.dob_label.grid_forget()
        self.dob_frame.grid_forget()
        self.register_button.grid_forget()

        self.login_button.grid(row=6, column=0, pady=10, padx=10, sticky="ew")

    def _clear_all_fields(self) -> None:
        """Clears all input fields."""
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.sex_combobox.set('')
        self.day_spinbox.set(1)
        self.month_combobox.current(0)
        self.year_spinbox.set(2000)


if __name__ == "__main__":
    """
    Allows testing to be made on this specific window.
    Only runs if the file is executed directly (not through imports)
    """
    root = tb.Window(themename="darkly")
    app = App(root)
    root.mainloop()
