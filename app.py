from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Sample dataset
data = {
    "Movie": ["Inception", "Interstellar", "The Matrix", "The Dark Knight", "Titanic"],
    "Genre": ["Sci-Fi Thriller", "Sci-Fi Drama", "Sci-Fi Action", "Action Crime", "Romance Drama"]
}

df = pd.DataFrame(data)

# Convert genres into numerical vectors using TF-IDF
vectorizer = TfidfVectorizer()
genre_vectors = vectorizer.fit_transform(df["Genre"])
similarity_matrix = cosine_similarity(genre_vectors)

def recommend_movie(movie_name):
    if movie_name not in df["Movie"].values:
        return ["Movie not found in database."]

    idx = df[df["Movie"] == movie_name].index[0]
    similar_movies = list(enumerate(similarity_matrix[idx]))
    similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:4]

    recommendations = [df["Movie"][i[0]] for i in similar_movies]
    return recommendations

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        selected_movie = request.form["movie"]
        recommendations = recommend_movie(selected_movie)
        return render_template("index.html", movies=df["Movie"].tolist(), recommendations=recommendations, selected_movie=selected_movie)

    return render_template("index.html", movies=df["Movie"].tolist(), recommendations=None)

if __name__ == "__main__":
    app.run(debug=True)
