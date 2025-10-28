import sqlite3
from datetime import date
import os


def save_user_to_db(user):
    """
    Saves a new user to the database

    :param user: User object containing username, password, sex, date of birth, and join date
    """
    db_path = os.path.join(os.path.dirname(__file__), "..", "db", "rehealth_db.db")
    db_path = os.path.abspath(db_path)
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS User (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username VARCHAR(20) UNIQUE NOT NULL,
            Password VARCHAR(50) NOT NULL,
            Sex VARCHAR(10),
            DateOfBirth DATE,
            JoinDate DATE
        );
    """)

    while True:
        try:
            cursor.execute("""
                INSERT INTO User (Username, Password, Sex, DateOfBirth, JoinDate)
                VALUES (?, ?, ?, ?, ?);
            """, (user.username, user.password, user.sex, user.dob, user.join_date))
            connection.commit()
            print("User successfully saved to database.")
            break  # Exit loop on success
        except sqlite3.IntegrityError:
            print("Error: Username already exists. Please choose a different username.")

    connection.close()


def save_metrics(user_id, height, weight):
    """
    Saves user metrics to the database.

    :param user_id: ID of the user
    :param height: User's height
    :param weight: User's weight
    """
    db_path = os.path.join(os.path.dirname(__file__), "..", "db", "rehealth_db.db")
    db_path = os.path.abspath(db_path)
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = ON")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO MetricsTracking (UserID, Height, Weight, MetricDate)
        VALUES (?, ?, ?, ?)
    """, (user_id, height, weight, date.today()))

    connection.commit()
    connection.close()


def save_steps(user_id, step_count, step_goal):
    """
    Save the user's daily step data.

    :param user_id: ID of the user
    :param step_count: Number of steps taken
    :param step_goal: Daily step goal
    """
    db_path = os.path.join(os.path.dirname(__file__), "..", "db", "rehealth_db.db")
    db_path = os.path.abspath(db_path)
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = ON")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO Steps (UserID, Date, StepCount, StepsGoal)
        VALUES (?, ?, ?, ?)
    """, (user_id, date.today(), step_count, step_goal))

    connection.commit()
    connection.close()


def save_sleep(user_id, sleep_hours, sleep_quality=None):
    """
    Save the user's daily sleep data.

    :param user_id: ID of the user
    :param sleep_hours: Hours slept
    :param sleep_quality: Optional rating of sleep quality
    """
    db_path = os.path.join(os.path.dirname(__file__), "..", "db", "rehealth_db.db")
    db_path = os.path.abspath(db_path)
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = ON")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO Sleep (UserID, SleepDate, SleepRating, SleepDuration)
        VALUES (?, ?, ?, ?)
    """, (user_id, date.today(), sleep_hours, sleep_quality))

    connection.commit()
    connection.close()


def save_food(user_id, food_name, calories, meal_type):
    """
    Save a user's food entry to the database.

    :param user_id: ID of the user
    :param food_name: Name of the food
    :param calories: Number of calories
    :param meal_type: Type of meal (e.g., breakfast, lunch, dinner, snack)
    """
    db_path = os.path.join(os.path.dirname(__file__), "..", "db", "rehealth_db.db")
    db_path = os.path.abspath(db_path)

    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = ON")
    cursor = connection.cursor()

    # Create the Food table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Food (
            FoodID INTEGER PRIMARY KEY AUTOINCREMENT,
            UserID INTEGER NOT NULL,
            FoodName TEXT NOT NULL,
            Calories INTEGER NOT NULL,
            MealType TEXT NOT NULL,
            DateConsumed DATE NOT NULL,
            FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE
        )
    """)

    # Insert the food record
    cursor.execute("""
        INSERT INTO Food (UserID, FoodName, Calories, MealType, DateConsumed)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, food_name, calories, meal_type.lower(), date.today()))

    connection.commit()
    connection.close()
