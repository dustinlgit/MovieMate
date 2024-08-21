document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('search-form');
    const resultsDiv = document.getElementById('results');

    form.addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent the default form submission

        const movieTitle = document.getElementById('movie-title').value;

        if (movieTitle.trim() === '') {
            resultsDiv.innerHTML = 'Please enter a movie title.';
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:5000/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title: movieTitle })
            });

            const data = await response.json();
            if (data.recommendations.length > 0) {
                resultsDiv.innerHTML = `<ul>${data.recommendations.map(movie => `<li>${movie}</li>`).join('')}</ul>`;
            } else {
                resultsDiv.innerHTML = 'No recommendations found.';
            }
        } catch (error) {
            resultsDiv.innerHTML = 'An error occurred. Please try again.';
        }
    });
});
