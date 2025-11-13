import os
import sqlite3
from datetime import date, datetime, timedelta


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
    """, (user_id, date.today(), sleep_quality, sleep_hours))

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

    cursor.execute("""
        INSERT INTO Food (UserID, FoodName, Calories, MealType, DateConsumed)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, food_name, calories, meal_type.lower(), date.today()))

    connection.commit()
    connection.close()


def save_workout(user_id, exercise_name, weight, sets, reps):
    """
    Save a user's workout entry to the database.

    :param user_id: ID of the user
    :param exercise_name: Name of the exercise
    :param weight: Weight lifted in kg
    :param sets: Number of sets performed
    :param reps: Number of reps per set
    """
    db_path = os.path.join(os.path.dirname(__file__), "..", "db", "rehealth_db.db")
    db_path = os.path.abspath(db_path)

    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = ON")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO Exercises (UserID, ExerciseName, Weight, Sets, Reps, DatePerformed)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, exercise_name, weight, sets, reps, date.today()))

    connection.commit()
    connection.close()


def get_weight(user_id):
    db_path = os.path.join(os.path.dirname(__file__), "..", "db", "rehealth_db.db")
    db_path = os.path.abspath(db_path)
    connection = sqlite3.connect(db_path)
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
    Fetches steps data for the last 7 days for a given user.
    """
    db_path = os.path.join(os.path.dirname(__file__), "rehealth_db.db")
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Gets today's date and calculate 7 days ago
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

    # Creates a dictionary of dates and steps from database results
    steps_dict = {}
    for row in results:
        date_obj = datetime.strptime(row[0], '%Y-%m-%d').date()
        steps_dict[date_obj] = row[1]

    # Fill in all 7 days (including days with no data)
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
    """
    db_path = os.path.join(os.path.dirname(__file__), "rehealth_db.db")
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Gets today's date and calculate 7 days ago
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

    # Fill in all 7 days (including days with no data)
    dates = []
    sleep_hours = []

    for i in range(7):
        current_date = seven_days_ago + timedelta(days=i)
        dates.append(current_date.strftime('%m/%d'))  # Formats as MM/DD for display
        sleep_hours.append(sleep_dict.get(current_date, 0))  # Value is 0 if no data for that day is found

    return dates, sleep_hours


def get_last_7_days_sleep_convert(user_id):
    """
    Converts dates to numbers for graph
    Returns day numbers (1-7) and sleep hours.
    """
    dates, sleep_hours = get_last_7_days_sleep(user_id)
    day_numbers = list(range(1, 8))
    return day_numbers, sleep_hours


def get_last_7_days_calories(user_id):
    """
    Fetches calorie data for the last 7 days for a given user.
    """
    db_path = os.path.join(os.path.dirname(__file__), "rehealth_db.db")
    connection = sqlite3.connect(db_path)
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

    # Fill in all 7 days (including days with no data)
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
        # Connect to database
        db_path = os.path.join(os.path.dirname(__file__), "..", "db", "rehealth_db.db")
        db_path = os.path.abspath(db_path)
        connection = sqlite3.connect(db_path)
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
        # Connect to database
        db_path = os.path.join(os.path.dirname(__file__), "..", "db", "rehealth_db.db")
        db_path = os.path.abspath(db_path)
        connection = sqlite3.connect(db_path)
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
