import os
import sqlite3
from db.db_handler import get_db_connection

db_path = os.path.join(os.path.dirname(__file__), "rehealth_db.db")


def get_steps(user_id):
    """Return the steps for today by user."""
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT SUM(StepCount) FROM Steps WHERE UserID = ? AND Date = DATE('now')", (user_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result and result[0] else 0


def get_calories(user_id):
    """Returns calories consumed by user."""
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT SUM(Calories) FROM Food WHERE UserID = ? AND DateConsumed = DATE('now')", (user_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result and result[0] is not None else 0


def get_sleep(user_id):
    """Returns sleep rating for today by user."""
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT SleepRating FROM Sleep WHERE UserID = ? AND SleepDate = DATE('now')", (user_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result and result[0] else 0
