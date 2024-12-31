from dotenv import load_dotenv
from flask import Flask, requests, jsonify
import sqlite3
import os

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

app = Flask(__name__)

def get_fav_movies(id):
    con = sqlite3.connect("server/database/recommendations.db")
    cursor = con.cursor()

    search_fav = """
       SELECT movie_id
       FROM fav_movies
       WHERE id = ?
    """

    cursor.execute(search_fav, (id,))
    favorite_movies = cursor.fetchall()

    cursor.close()
    con.close()

    movie_in_tuple = []
    for movie in favorite_movies:
        movie_in_tuple.append(movie[0])
    
    return movie_in_tuple

def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch details for movie_id {movie_id}"}

def fetch_movie_rating(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews"
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(url, params=params)

    if response.status_code == 200: #200 means it works
        return response.json()
    else:
        return {"error": f"Failed to fetch ratings for movie_id {movie_id}"}

def fetch_recomendations(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations"
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch recommendations for movie_id {movie_id}"}