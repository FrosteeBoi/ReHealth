import sqlite3


def save_user_to_db(user):
    """
    Saves a new user to the database. If the table doesn't exist
    (which it should) it creates the table
    :param user:
    :return:
    """
    connection = sqlite3.connect("rehealth_db.db")
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
            user.username = input("Enter a different username: ")

    connection.close()


