"""
import sqlite3

connection = sqlite3.connect("rehealth_db.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM User")
rows = cursor.fetchall()

if not rows:
    print("No users found.")
else:
    for row in rows:
        print(row)

connection.close()
"""

import os
import sqlite3


def initialize_db():
    db_path = os.path.join(os.path.dirname(__file__), "rehealth_db.db")
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = ON")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS User (
      UserID INTEGER PRIMARY KEY AUTOINCREMENT,
      Username VARCHAR(20) UNIQUE NOT NULL,
      Password VARCHAR(50) NOT NULL,
      Gender VARCHAR(10),
      DateOfBirth DATE,
      JoinDate DATE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS MetricsTracking (
      UserID INTEGER,
      Height DECIMAL(4,1),
      Weight DECIMAL(4,1),
      MetricDate DATE,
      FOREIGN KEY (UserID) REFERENCES User(UserID)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Steps (
      StepID INTEGER PRIMARY KEY AUTOINCREMENT,
      UserID INTEGER,
      Date DATE,
      StepCount INTEGER,
      StepsGoal INTEGER,
      FOREIGN KEY (UserID) REFERENCES User(UserID)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Exercises (
      ExerciseID INTEGER PRIMARY KEY AUTOINCREMENT,
      UserID INTEGER,
      ExerciseName VARCHAR(50),
      Weight DECIMAL(5,1),
      Sets INTEGER,
      Reps INTEGER,
      DatePerformed DATE NOT NULL,
      FOREIGN KEY (UserID) REFERENCES User(UserID)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Sleep (
      SleepID INTEGER PRIMARY KEY AUTOINCREMENT,
      UserID INTEGER,
      SleepDate DATE,
      SleepRating DECIMAL(3,2),
      SleepDuration DECIMAL(4,1),
      FOREIGN KEY (UserID) REFERENCES User(UserID)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Food (
      FoodID INTEGER PRIMARY KEY AUTOINCREMENT,
      UserID INTEGER,
      FoodName VARCHAR(50),
      Calories INTEGER,
      MealType VARCHAR(10),
      DateConsumed DATE,
      FOREIGN KEY (UserID) REFERENCES User(UserID)
    );
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_db()
