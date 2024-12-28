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

# cursor.execute("DROP TABLE users")


con.commit()
cursor.close()
con.close()