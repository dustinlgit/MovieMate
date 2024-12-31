import sqlite3

con = sqlite3.connect("server/database/recommendations.db")
cursor = con.cursor()

users_table = """ 
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(225) UNIQUE NOT NULL,
        hashed_pass VARCHAR(225) NOT NULL
    ); """

movies_table = """
    CREATE TABLE IF NOT EXISTS movies(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_name VARCHAR(500) NOT NULL,
        release_date DATE,
        description TEXT,
        rating FLOAT
    ); """

fav_movies_table = """
    CREATE TABLE IF NOT EXISTS fav_movies(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        movie_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (movie_id) REFERENCES movies(id)
        UNIQUE(user_id, movie_id)
    );"""

cursor.execute(users_table)
cursor.execute(movies_table)
cursor.execute(fav_movies_table)
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