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
