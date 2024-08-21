from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TMDB_API_KEY = 'bef42caefedbfca06c47dcd6b580bf73'
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

def fetch_movie_recommendations(movie_title):
    search_url = f'{TMDB_BASE_URL}/search/movie'
    search_params = {
        'api_key': TMDB_API_KEY,
        'query': movie_title
    }
    search_response = requests.get(search_url, params=search_params).json()
    movie_id = search_response['results'][0]['id'] if search_response['results'] else None

    if movie_id:
        recommend_url = f'{TMDB_BASE_URL}/movie/{movie_id}/recommendations'
        recommend_params = {
            'api_key': TMDB_API_KEY
        }
        recommend_response = requests.get(recommend_url, params=recommend_params).json()
        return [movie['title'] for movie in recommend_response['results']]
    else:
        return ['No recommendations found.']

@app.route('/')
def home():
    return 'Welcome to the Movie Recommendation App!'

@app.route('/recommend', methods=['POST'])
def recommend_movie():
    data = request.json
    movie_title = data.get('title', '')
    recommendations = fetch_movie_recommendations(movie_title)
    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)
