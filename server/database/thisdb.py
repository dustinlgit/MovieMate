import sqlite3

con = sqlite3.connect("server/database/recommendations.db")
cursor = con.cursor()

users_column = """ 
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(225) UNIQUE NOT NULL,
        hashed_pass VARCHAR(225) NOT NULL
    ); """

cursor.execute(users_column)
# cursor.execute("INSERT INTO users(username, hashed_pass) VALUES(?, ?)", ("user1", "hashed_password1"))
# cursor.execute("INSERT INTO users(username, hashed_pass) VALUES(?, ?)", ("user2", "hashed_password2"))

# # Checking inserted rows
# cursor.execute("SELECT * FROM users")
# rows = cursor.fetchall()
# print(rows)

# cursor.execute("DROP TABLE users")


con.commit()
cursor.close()
con.close()