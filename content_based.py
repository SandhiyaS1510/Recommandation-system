import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample dataset (Movie titles + Genres)
data = {
    "Movie": ["Inception", "Interstellar", "The Matrix", "The Dark Knight", "Titanic"],
    "Genre": ["Sci-Fi Thriller", "Sci-Fi Drama", "Sci-Fi Action", "Action Crime", "Romance Drama"]
}

df = pd.DataFrame(data)

# Convert genres into numerical vectors using TF-IDF
vectorizer = TfidfVectorizer()
genre_vectors = vectorizer.fit_transform(df["Genre"])

# Compute similarity between movies
similarity_matrix = cosine_similarity(genre_vectors)

def recommend_movie(movie_name):
    if movie_name not in df["Movie"].values:
        return "Movie not found in database."

    idx = df[df["Movie"] == movie_name].index[0]  # Find movie index
    similar_movies = list(enumerate(similarity_matrix[idx]))  # Get similarity scores
    similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:4]  # Sort and get top 3

    recommendations = [df["Movie"][i[0]] for i in similar_movies]
    return recommendations

# Test recommendation
movie_to_search = "Inception"
recommended_movies = recommend_movie(movie_to_search)
print(f"Movies similar to '{movie_to_search}': {recommended_movies}")
