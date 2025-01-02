from dotenv import load_dotenv
from flask import Flask, jsonify
import requests
import sqlite3
import os

load_dotenv()
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

app = Flask(__name__)

def get_fav_movies(user_id):
    con = sqlite3.connect("server/database/movies.db")
    cursor = con.cursor()

    search_id = """
       SELECT movie_id
       FROM fav_movies
       WHERE user_id = ?  # Fixed the column name to user_id
    """
    cursor.execute(search_id, (user_id,))
    movie_ids = cursor.fetchall()

    search_movie = """
        SELECT movie_name
        FROM movies
        WHERE movie_id = ?  # Fixed the column name to movie_id
    """
    movies = []
    for movie_id_tuple in movie_ids:
        movie_id = movie_id_tuple[0]  
        cursor.execute(search_movie, (movie_id,))
        movie = cursor.fetchone()
        if movie:
            movies.append(movie[0]) 

    cursor.close()
    con.close()

    return movies  

def movie_exist(check_id):
    con = sqlite3.connect("server/database/movies.db")
    cursor = con.cursor()

    check_movie = """
        SELECT 1
        FROM movies
        WHERE movie_id = ?
        LIMIT 1
    """
    cursor.execute(check_movie, (check_id,))
    result = cursor.fetchone()

    cursor.close()
    con.close()

    if result:
        return True
    else:
        return False

def fav_movie_exists(check_id):
    con = sqlite3.connect("server/database/movies.db")
    cursor = con.cursor()

    check_fav = """
        SELECT 1
        FROM fav_movies
        WHERE movie_id = ?
        LIMIT 1
    """
    cursor.execute(check_fav, (check_id,))
    result = cursor.fetchone()
    cursor.close()
    con.close()

    if result:
        return True
    else:
        return False

def add_movie(movie_name, movie_results):
    m_id = movie_results.get("id")
    if not movie_exist(m_id):  # Only add movie if it doesn't exist
        m_details = movie_results.get("overview")
        # m_reviews = fetch_movie_rating(m_id)
        # print(m_reviews)
        m_rdate = movie_results.get("release_date")

        try:
            with sqlite3.connect("server/database/movies.db") as con:
                cursor = con.cursor()
                import_data = """
                    INSERT INTO movies (
                        movie_name, movie_id, release_date, description
                    ) VALUES (?, ?, ?, ?)
                """
                cursor.execute(import_data, (movie_name, m_id, m_rdate, m_details))
                con.commit()
                print("Movie added successfully.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
    else:
        print("Movie already exists in the database.")

def add_fav_movie(movie_name, usr_id):
    url = "https://api.themoviedb.org/3/search/movie"
    headers = {
        "accept": "application/json",
        "Authorization": BEARER_TOKEN
    }
    params = {"query": movie_name}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        get_result = response.json().get("results", [])
        if get_result:  # Ensure there are results
            results = get_result[0]
            m_id = results.get("id")

            add_movie(movie_name, results)  # Add movie if not already in the database

            if not fav_movie_exists(m_id):  # Check if the movie is already a favorite
                try:
                    with sqlite3.connect("server/database/movies.db") as con:
                        cursor = con.cursor()
                        import_data = """
                            INSERT INTO fav_movies (
                                user_id, movie_id
                            ) VALUES (?, ?)
                        """
                        cursor.execute(import_data, (usr_id, m_id))
                        con.commit()
                        print("Movie added to favorites.")
                except sqlite3.Error as e:
                    print(f"Database error: {e}")
            else:
                return "Movie is already added to favorites."
        else:
            return "No movie found."
    else:
        return "Failed to fetch movie data."


def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "accept": "application/json",
        "Authorization": BEARER_TOKEN
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch details for movie_id {movie_id}"}

def fetch_movie_rating(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews"
    headers = {
        "accept": "application/json",
        "Authorization": BEARER_TOKEN
    }
    response = requests.get(url, headers=headers)
    

    if response.status_code == 200: #200 means it works
        return response.json()
    else:
        return {"error": f"Failed to fetch ratings for movie_id {movie_id}"}

def fetch_recomendations(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations"
    headers = {
        "accept": "application/json",
        "Authorization": BEARER_TOKEN
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch recommendations for movie_id {movie_id}"}