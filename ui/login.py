from logic.user import User
import re
from datetime import datetime
from datetime import date
from db.db_handler import save_user_to_db
import sqlite3


def login_menu():
    """
    Menu that allows the user to register or login to an account
    """
    while True:
        try:
            menu_choice = int(input("Would you like to:\n"
                                    "1: Login \n"
                                    "2: Register \n"))
            if menu_choice == 1:
                print(f"You selected {menu_choice}: Login.")
                break
            elif menu_choice == 2:
                print(f"You selected {menu_choice}: Register.")
                register()
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
        except ValueError:
            print("Invalid choice. Please enter 1 or 2.")


def register():
    today = date.today()
    """
    Allows the user to register a new account.
    """
    while True:
        username_input = input("Please enter a username of your choice: ")
        if re.match("^[A-Za-z0-9_.]{3,20}$", username_input):
            break
        else:
            print(
                "Invalid choice. Please enter a username between 3 and 20 characters long using only letters, "
                "numbers, underscores or dots.")

    while True:
        # Checks if the password has the recommended amount of characters
        password_input = input("Please enter a password of your choice: ")
        if len(password_input) < 8 or len(password_input) > 20:
            print("Password must be between 8 and 20 characters.")
            continue

        password_score = 0
        # Checks if the password is strong enough

        if re.search(r"[A-Z]", password_input):
            password_score += 1
        if re.search(r"[a-z]", password_input):
            password_score += 1
        if re.search(r"[0-9]", password_input):
            password_score += 1
        if re.search(r"[^A-Za-z0-9]", password_input):
            password_score += 1

        if password_score >= 3:
            print("Password accepted.")
            break
        else:
            print("Try using a mix of upper/lowercase, numbers, and special characters.")

    while True:
        sex_input = input("Please enter your biological sex ('Male' or 'Female'): ").strip().upper()
        if sex_input == "MALE" or sex_input == "FEMALE":
            break
        else:
            print("Please enter 'Male' or 'Female'")

    while True:
        dob_input = input("Enter your date of birth (DD/MM/YYYY): ").strip()
        try:
            dob_input = datetime.strptime(dob_input, "%d/%m/%Y").date()
            break
        except ValueError:
            print("Invalid format. Please enter in DD/MM/YYYY format.")

    password_input = User.password_hasher(password_input)

    new_user = User(username_input, password_input, sex_input, dob_input, today)
    # Creates a User object based on data provided by the user

    save_user_to_db(new_user)

    print("Registration complete! You can now log in.")


def login():
    """
    The user can log in and access the application
    """
    connection = sqlite3.connect("../db/rehealth_db.db")
    cursor = connection.cursor()
    print("")

    while True:
        username_attempt = input("Username: ")
        password_attempt = input("Password: ")

        # Fetch all relevant user info
        cursor.execute("""
            SELECT Username, Password, Sex, DateOfBirth, JoinDate
            FROM User WHERE Username = ?
        """, (username_attempt,))
        result = cursor.fetchone()

        if result:
            # Create a User object using the fetched data
            fetched_user = User(
                username=result[0],
                password=result[1],
                sex=result[2],
                dob=result[3],
                join_date=result[4]
            )

            if fetched_user.password_check(password_attempt):
                print("Login successful!")
                break
            else:
                print("Incorrect password.\n")
        else:
            print("Username not found.\n")

    connection.close()


login_menu()
