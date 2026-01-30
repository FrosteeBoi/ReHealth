"""
Dashboard_Data Module - ReHealth
"""

import os
import sqlite3
from db.db_handler import get_db_connection

db_path = os.path.join(os.path.dirname(__file__), "rehealth_db.db")
# database path set up


def get_steps(user_id: int) -> int:
    """
    Fetch the user's total steps for today's date from the database.

    Args: user_id (int): The user's ID.

    Returns: The total number of steps the user took today.

    Raises: DatabaseError: If a database error occurs.
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT SUM(StepCount) FROM Steps WHERE UserID = ? AND Date = DATE('now')",
        (user_id,)
    )
    result = cursor.fetchone()
    connection.close()
    if result[0] is None:
        return 0
    else:
        return result[0]
    # Return zero if no results are found


def get_calories(user_id: int) -> int:
    """
    Fetch the user's calories for today's date from the database.

    Args: user_id (int): The user's ID.

    Returns: The total amount of calories the user logged  today.

    Raises: DatabaseError: If a database error occurs.
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT SUM(Calories) FROM Food WHERE UserID = ? AND DateConsumed = DATE('now')",
        (user_id,)
    )
    result = cursor.fetchone()
    connection.close()
    if result[0] is None:
        return 0
    else:
        return result[0]


def get_sleep(user_id: int) -> int:
    """
    Fetch the user's sleep rating that they logged today.

    Args: user_id (int): The user's ID.

    Returns: The sleep rating that the user recorded on today's date.

    Raises: DatabaseError: If a database error occurs.
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT SleepRating FROM Sleep WHERE UserID = ? AND SleepDate = DATE('now')",
        (user_id,)
    )
    result = cursor.fetchone()
    connection.close()
    if result[0] is None:
        return 0
    else:
        return result[0]
