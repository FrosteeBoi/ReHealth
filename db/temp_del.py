"""FILE FOR DELETING DATABASE RECORDS AFTER TESTING"""

import sqlite3

# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect("health_app.db")
cursor = conn.cursor()

# Create a table for user health data
cursor.execute("""
CREATE TABLE IF NOT EXISTS health_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    weight REAL,
    steps INTEGER
)
""")

# Get user input
name = input("Enter your name: ")
age = int(input("Enter your age: "))
weight = float(input("Enter your weight (kg): "))
steps = int(input("Enter today's step count: "))

# Insert data into the database (parameterised query)
cursor.execute("""
INSERT INTO health_data (name, age, weight, steps)
VALUES (?, ?, ?, ?)
""", (name, age, weight, steps))

# Save changes and close connection
conn.commit()
conn.close()

print("Health data saved successfully.")
