import ttkbootstrap as tb
import random
from tkinter import messagebox
from logic.user import User
import re
from datetime import datetime, date
from db.db_handler import save_user_to_db
import sqlite3


def quote_maker():
    quote_list = [
        "'Your body is a temple.'",
        "'Health is wealth.'",
        "'Giving up is way harder than trying.'",
        "'Remember to take breaks.'",
        "'A lesson without pain is meaningless.'",
        "'Welcome back.'",
        "'Make your dreams a reality.'",
        "'Just do it.'",
        "'One day or day one.'"
    ]
    return random.choice(quote_list)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("ReHealth")
        self.root.geometry("340x440")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.mainframe = tb.Frame(self.root)
        self.mainframe.grid(row=0, column=0, sticky="nsew")

        self.mainframe.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.mainframe.grid_columnconfigure(0, weight=1)

        # Login widgets
        self.login_label = tb.Label(self.mainframe, text="ReHealth Login", font=("roboto", 12, "bold"))
        self.quote_label = tb.Label(self.mainframe, text=quote_maker(), font=("roboto", 11, "italic"), wraplength=300,
                                    justify="center")
        self.username_label = tb.Label(self.mainframe, text="Username", font=("roboto", 12, "bold"))
        self.username_entry = tb.Entry(self.mainframe)

        self.password_label = tb.Label(self.mainframe, text="Password", font=("roboto", 12, "bold"))
        self.password_entry = tb.Entry(self.mainframe, show="*")

        self.login_button = tb.Button(self.mainframe, text="REVOLUTIONISE FITNESS", command=self.login_func)

        # Registration widgets that are called upon after failing login once
        self.sex_label = tb.Label(self.mainframe, text="Biological Sex (Male/Female)", font=("roboto", 12, "bold"))
        self.sex_entry = tb.Entry(self.mainframe)

        self.dob_label = tb.Label(self.mainframe, text="Date of Birth (DD/MM/YYYY)", font=("roboto", 12, "bold"))
        self.dob_entry = tb.Entry(self.mainframe)

        self.register_button = tb.Button(self.mainframe, text="REVOLUTIONISE FITNESS", command=self.register_submit)

        # Places all the widgets excluding registration ones
        self.login_label.grid(row=0, column=0, pady=(10, 10))
        self.quote_label.grid(row=1, column=0, pady=(0, 15), padx=10)
        self.username_label.grid(row=2, column=0, sticky="w", padx=20)
        self.username_entry.grid(row=3, column=0, padx=20, sticky="ew")

        self.password_label.grid(row=4, column=0, sticky="w", padx=20, pady=(10, 0))
        self.password_entry.grid(row=5, column=0, padx=20, sticky="ew")

        self.login_button.grid(row=6, column=0, pady=20, padx=20, sticky="ew")

    def login_func(self):
        username_attempt = self.username_entry.get()
        password_attempt = self.password_entry.get()

        connection = sqlite3.connect(r"C:\Users\frost\PycharmProjects\ReHealth\db\rehealth_db.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT Username, Password, Sex, DateOfBirth, JoinDate
            FROM User WHERE Username = ?
        """, (username_attempt,))
        result = cursor.fetchone()

        connection.close()

        if result:
            fetched_user = User(
                username=result[0],
                password=result[1],
                sex=result[2],
                dob=result[3],
                join_date=result[4]
            )

            if fetched_user.password_check(password_attempt):
                messagebox.showinfo("Success", "Login successful!")
            else:
                self.login_failed()
        else:
            self.login_failed()

    def login_failed(self):
        response = messagebox.askretrycancel(
            "Login Failed",
            "Incorrect username or password.\n\n"
            "Would you like to try again? Press 'Retry'.\n"
            "Or press 'Cancel' to register a new account."
        )
        if response:  # Retry
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.username_entry.focus()
        else:
            self.show_register_fields()

    def show_register_fields(self):
        messagebox.showinfo("Register", "Please fill in the fields to register a new account.")

        # Clears all the user entries
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.sex_entry.delete(0, 'end')
        self.dob_entry.delete(0, 'end')

        # Shows registration widgets
        self.sex_label.grid(row=7, column=0, sticky="w", padx=20, pady=(10, 0))
        self.sex_entry.grid(row=8, column=0, padx=20, sticky="ew")

        self.dob_label.grid(row=9, column=0, sticky="w", padx=20, pady=(10, 0))
        self.dob_entry.grid(row=10, column=0, padx=20, sticky="ew")

        # Hides login button and shows register button
        self.login_button.grid_forget()
        self.register_button.grid(row=11, column=0, pady=20, padx=20, sticky="ew")

    def register_submit(self):
        username_input = self.username_entry.get().strip()
        password_input = self.password_entry.get().strip()
        sex_input = self.sex_entry.get().strip().capitalize()
        dob_input = self.dob_entry.get().strip()

        # Validate username
        if not re.match(r"^[A-Za-z0-9_.]{3,20}$", username_input):
            messagebox.showerror("Error", "Username must be 3-20 characters, letters, numbers, underscores, or dots.")
            return

        # Validate password length
        if len(password_input) < 8 or len(password_input) > 20:
            messagebox.showerror("Error", "Password must be between 8 and 20 characters.")
            return

        # Validate password strength
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
            messagebox.showerror("Error", "Password should mix uppercase, lowercase, numbers, and special characters.")
            return

        # Validates sex format
        if sex_input not in ("Male", "Female"):
            messagebox.showerror("Error", "Sex must be 'Male' or 'Female'.")
            return

        # Validates date of birth format
        try:
            dob_date = datetime.strptime(dob_input, "%d/%m/%Y").date()
        except ValueError:
            messagebox.showerror("Error", "Date of birth must be in DD/MM/YYYY format.")
            return

        today = date.today()
        hashed_password = User.password_hasher(password_input)

        # Checks if username already exists
        connection = sqlite3.connect(r"C:\Users\frost\PycharmProjects\ReHealth\db\rehealth_db.db")
        cursor = connection.cursor()
        cursor.execute("SELECT Username FROM User WHERE Username = ?", (username_input,))
        if cursor.fetchone():
            messagebox.showerror("Error", "Username already exists. Please choose another.")
            connection.close()
            return

        # Creates a new user and saves it to the database
        new_user = User(username_input, hashed_password, sex_input, dob_date, today)

        try:
            save_user_to_db(new_user)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register user: {e}")
            connection.close()
            return

        connection.close()

        messagebox.showinfo("Success", "Registration complete! You can now log in.")

        # Clears registration fields and reset UI to allow the user to login
        self.sex_label.grid_forget()
        self.sex_entry.grid_forget()
        self.dob_label.grid_forget()
        self.dob_entry.grid_forget()
        self.register_button.grid_forget()

        self.login_button.grid(row=6, column=0, pady=20, padx=20, sticky="ew")
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.sex_entry.delete(0, 'end')
        self.dob_entry.delete(0, 'end')
        self.username_entry.focus()


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    app = App(root)
    root.mainloop()
