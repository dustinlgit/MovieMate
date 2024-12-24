import sqlite3

con = sqlite3.connect("server/database/recommendations.db")
cursor = con.cursor()

table = """ CREATE TABLE users(
            id INT PRIMARY KEY,
            username VARCHAR(225) UNIQUE NOT NULL,
            hashed_pass VARCHAR(225) NOT NULL
        ); """

cursor.execute(table)



cursor.close()