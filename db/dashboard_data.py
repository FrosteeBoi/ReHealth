import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "rehealth_db.db")


def get_steps(user_id):
    """Return the steps by user."""
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT StepCount FROM Steps WHERE UserID = ? ORDER BY Date DESC LIMIT 1", (user_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else 0


def get_calories(user_id):
    """Returns calories consumed by user."""
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT SUM(Calories) FROM Food WHERE UserID = ? AND DateConsumed = DATE('now')", (user_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result and result[0] is not None else 0


def get_sleep(user_id):
    """Returns sleep obtained from user."""
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT SleepDuration FROM Sleep WHERE UserID = ? ORDER BY SleepDate DESC LIMIT 1", (user_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else 0
