import sqlite3
from datetime import date
import os


def save_user_to_db(user):
    """
    Saves a new user to the database. If the table doesn't exist
    (which it should) it creates the table
    :param user:
    :return:
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
    Saves the user's daily step data into the Steps table

    :param user_id:
    :param step_count:
    :param step_goal:
    :return:
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
