from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to the Movie Recommendation App!'

@app.route('/recommend', methods=['POST'])
def recommend_movie():
    data = request.json
    movie_title = data.get('title', '')
    # Placeholder for recommendation logic
    return jsonify({'message': f'Recommendations for {movie_title}'})

if __name__ == '__main__':
    app.run(debug=True)
