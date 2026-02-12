import os
import sqlite3
from datetime import date, datetime, timedelta

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "db", "rehealth_db.db"))


def get_db_connection(enable_foreign_keys=False):
    """Sets up database connection"""
    connection = sqlite3.connect(DB_PATH)
    if enable_foreign_keys:
        connection.execute("PRAGMA foreign_keys = ON")
    return connection


def save_user_to_db(user):
    """
    Saves a new user to the database

    Args: user_id (int): The user's ID.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    # Sets up database connection

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS User (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username VARCHAR(20) UNIQUE NOT NULL,
            Password VARCHAR(64) NOT NULL,
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
            break  # Exit loop if user successfully saved
        except sqlite3.IntegrityError:
            # Check for duplicate username
            print("Error: Username already exists. Please choose a different username.")

    connection.close()


def save_metrics(user_id, height, weight):
    """
    Saves user metrics to the database.

    Args:

    user_id: The user's ID.
    height: The user's height
    weight: The user's weight
    """
    connection = get_db_connection(enable_foreign_keys=True)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO MetricsTracking (UserID, Height, Weight, MetricDate)
        VALUES (?, ?, ?, ?)
    """, (user_id, height, weight, date.today()))

    connection.commit()
    connection.close()


def save_steps(user_id, step_count, step_goal):
    """
    Save the user's daily step data to the database.

    Args:

    user_id: The user's ID.
    step_count: Number of steps taken by the user
    step_goal: Daily step goal
    """
    connection = get_db_connection(enable_foreign_keys=True)
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

    Args:

    user_id: The user's ID
    sleep_hours: Hours slept by the user
    sleep_quality: User's objective sleep quality
    """
    connection = get_db_connection(enable_foreign_keys=True)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO Sleep (UserID, SleepDate, SleepRating, SleepDuration)
        VALUES (?, ?, ?, ?)
    """, (user_id, date.today(), sleep_quality, sleep_hours))

    connection.commit()
    connection.close()


def save_food(user_id, food_name, calories, meal_type):
    """
    Save a user's food entry to the database.

    Args:

    user_id: The user's ID
    food_name: Name of the food
    calories: Number of calories
    meal_type: Type of meal
    """
    connection = get_db_connection(enable_foreign_keys=True)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO Food (UserID, FoodName, Calories, MealType, DateConsumed)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, food_name, calories, meal_type.lower(), date.today()))

    connection.commit()
    connection.close()


def save_workout(user_id, exercise_name, weight, sets, reps):
    """
    Save a user's workout entry to the database.

    Args:

    user_id: The user's ID
    exercise_name: Name of the exercise
    weight: Amount of weight lifted
    sets: Number of sets performed
    reps: Number of reps performed
    """
    connection = get_db_connection(enable_foreign_keys=True)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO Exercises (UserID, ExerciseName, Weight, Sets, Reps, DatePerformed)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, exercise_name, weight, sets, reps, date.today()))

    connection.commit()
    connection.close()


def get_weight(user_id):
    """
    Fetches weight from the database

    Args:
    user_id:  The user's ID

    Returns: The weight the user recorded in the database
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
           SELECT Weight 
           FROM MetricsTracking
           WHERE UserID = ?
           ORDER BY MetricDate DESC
           LIMIT 1
       """, (user_id,))
    result = cursor.fetchone()
    connection.close()
    return float(result[0]) if result and result[0] is not None else 0.0


def get_last_7_days_steps(user_id):
    """
    Fetches steps data for the last 7 days for the user
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    # Gets today's date and calculates when 7 days ago was
    today = datetime.now().date()
    seven_days_ago = today - timedelta(days=6)

    # Queries steps for the last 7 days
    cursor.execute("""
        SELECT Date, SUM(StepCount) as TotalSteps
        FROM Steps
        WHERE UserID = ? AND Date >= ? AND Date <= ?
        GROUP BY Date
        ORDER BY Date ASC
    """, (user_id, seven_days_ago, today))

    results = cursor.fetchall()
    connection.close()

    # Creates a dictionary and places dates and corresponding step counts
    steps_dict = {}
    for row in results:
        date_obj = datetime.strptime(row[0], '%Y-%m-%d').date()
        steps_dict[date_obj] = row[1]

    # list of dates and steps each filled from dictionary
    dates = []
    steps = []

    for i in range(7):
        current_date = seven_days_ago + timedelta(days=i)
        dates.append(current_date.strftime('%m/%d'))  # Formats as MM/DD for display
        steps.append(steps_dict.get(current_date, 0))  # Value is 0 if no data for that day is found

    return dates, steps


def get_last_7_days_steps_convert(user_id):
    """
    Converts dates to numbers for graph
    Returns day numbers (1-7) and steps.
    """
    dates, steps = get_last_7_days_steps(user_id)
    day_numbers = list(range(1, 8))
    return day_numbers, steps


def get_last_7_days_sleep(user_id):
    """
    Fetches sleep data for the last 7 days for a given user.

    Args:
        user_id: The user's ID

    Returns:
        numbers (1-7) and sleep
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    # Calculates the date that that was 7 days ago
    today = datetime.now().date()
    seven_days_ago = today - timedelta(days=6)

    # Queries sleep for the last 7 days
    cursor.execute("""
        SELECT SleepDate, SleepDuration
        FROM Sleep
        WHERE UserID = ? AND SleepDate >= ? AND SleepDate <= ?
        ORDER BY SleepDate ASC
    """, (user_id, seven_days_ago, today))

    results = cursor.fetchall()
    connection.close()

    # Creates a dictionary of dates and sleep hours from database results
    sleep_dict = {}
    for row in results:
        date_obj = datetime.strptime(row[0], '%Y-%m-%d').date()
        sleep_dict[date_obj] = row[1]

    # places dictionary values in two lists
    dates = []
    sleep_hours = []

    for i in range(7):
        current_date = seven_days_ago + timedelta(days=i)
        dates.append(current_date.strftime('%m/%d'))  # Formats as MM/DD for display
        sleep_hours.append(sleep_dict.get(current_date, 0))  # Value is 0 if no data for that day is found

    return dates, sleep_hours


def get_last_7_days_sleep_convert(user_id):
    """
    Converts dates to numbers for the graph
    Returns day numbers (1-7) and sleep hours.
    """
    dates, sleep_hours = get_last_7_days_sleep(user_id)
    day_numbers = list(range(1, 8))
    return day_numbers, sleep_hours


def get_last_7_days_calories(user_id):
    """
    Fetches calorie data for the last 7 days for a given user.
    Returns days 1-7 and calories
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    # Gets today's date and calculate 7 days ago
    today = datetime.now().date()
    seven_days_ago = today - timedelta(days=6)

    # Queries calories for the last 7 days
    cursor.execute("""
        SELECT DateConsumed, SUM(Calories) as TotalCalories
        FROM Food
        WHERE UserID = ? AND DateConsumed >= ? AND DateConsumed <= ?
        GROUP BY DateConsumed
        ORDER BY DateConsumed ASC
    """, (user_id, seven_days_ago, today))

    results = cursor.fetchall()
    connection.close()

    # Creates a dictionary of dates and calories from database results
    calories_dict = {}
    for row in results:
        date_obj = datetime.strptime(row[0], '%Y-%m-%d').date()
        calories_dict[date_obj] = row[1]

    # Dictionary values are placed in two lists
    dates = []
    calories = []

    for i in range(7):
        current_date = seven_days_ago + timedelta(days=i)
        dates.append(current_date.strftime('%m/%d'))  # Formats as MM/DD for display
        calories.append(calories_dict.get(current_date, 0))  # Value is 0 if no data for that day is found

    return dates, calories


def get_last_7_days_calories_convert(user_id):
    """
    Converts dates to numbers for graph
    Returns day numbers (1-7) and calories.
    """
    dates, calories = get_last_7_days_calories(user_id)
    day_numbers = list(range(1, 8))
    return day_numbers, calories


def get_all_days_metrics(user_id):
    """
    Gets a list of all the measurement information
    stored by the user from the database
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Fetch all metrics for the user
        cursor.execute("""
                   SELECT MetricDate, Height, Weight
                   FROM MetricsTracking
                   WHERE UserID = ?
                   ORDER BY MetricDate DESC
               """, (user_id,))

        records = cursor.fetchall()
        connection.close()
        return records
    except Exception as e:
        print(f"Error fetching user metrics: {e}")
        return []


def get_all_workouts(user_id):
    """
    Gets a list of all the workout information
    stored by the user from the database
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Fetch all workouts for the user
        cursor.execute("""
            SELECT DatePerformed, ExerciseName, Weight, Sets, Reps
            FROM Exercises
            WHERE UserID = ?
            ORDER BY DatePerformed DESC
        """, (user_id,))

        records = cursor.fetchall()
        connection.close()

        return records

    except Exception as e:
        print(f"Error fetching workouts: {e}")
        return []


def get_total_steps(user_id):
    """
    Returns the user's lifetime total steps.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT SUM(StepCount)
        FROM Steps
        WHERE UserID = ?
    """, (user_id,))

    result = cursor.fetchone()
    connection.close()

    return result[0] if result and result[0] is not None else 0


def get_total_calories(user_id):
    """
    Returns the user's lifetime total calories.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT SUM(Calories)
        FROM Food
        WHERE UserID = ?
    """, (user_id,))

    result = cursor.fetchone()
    connection.close()

    return result[0] if result and result[0] is not None else 0


def get_total_sleep_hours(user_id):
    """
    Returns the user's lifetime total hours slept.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT SUM(SleepDuration)
        FROM Sleep
        WHERE UserID = ?
    """, (user_id,))

    result = cursor.fetchone()
    connection.close()

    return float(result[0]) if result and result[0] is not None else 0.0


def get_total_weight_lifted(user_id):
    """
    Returns lifetime weight lifted.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
            SELECT SUM(Weight * Sets * Reps)
            FROM Exercises
            WHERE UserID = ?
        """, (user_id,))

    result = cursor.fetchone()
    connection.close()

    return float(result[0] if result and result[0] is not None else 0.0)
