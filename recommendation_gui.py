import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

# GUI Setup
def on_recommend():
    selected_movie = movie_dropdown.get()
    recommendations = recommend_movie(selected_movie)
    result_label.config(text="Recommendations: " + ", ".join(recommendations))

# Create Window
root = tk.Tk()
root.title("Movie Recommendation System")
root.geometry("400x300")

# Label
label = tk.Label(root, text="Select a Movie:", font=("Arial", 12))
label.pack(pady=10)

# Dropdown
movie_dropdown = ttk.Combobox(root, values=df["Movie"].tolist())
movie_dropdown.pack(pady=5)
movie_dropdown.current(0)

# Button
recommend_button = tk.Button(root, text="Get Recommendations", command=on_recommend)
recommend_button.pack(pady=10)

# Result Label
result_label = tk.Label(root, text="Recommendations will appear here.", font=("Arial", 12))
result_label.pack(pady=10)

# Run the app
root.mainloop()
