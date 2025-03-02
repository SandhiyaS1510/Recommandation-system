import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Sample user-movie rating matrix
data = {
    "User": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "Inception": [5, 4, np.nan, 2, np.nan],
    "Interstellar": [4, np.nan, 5, 1, 3],
    "The Matrix": [np.nan, 3, 4, 5, 2],
    "Titanic": [2, np.nan, 3, 4, 5]
}

df = pd.DataFrame(data).set_index("User")  # Convert to DataFrame

# Fill missing ratings with 0 (or you can use other methods like mean substitution)
df_filled = df.fillna(0)

# Compute similarity between users
similarity_matrix = cosine_similarity(df_filled)
similarity_df = pd.DataFrame(similarity_matrix, index=df.index, columns=df.index)

def recommend_movie_for_user(user_name):
    if user_name not in df.index:
        return "User not found."

    similar_users = similarity_df[user_name].sort_values(ascending=False)[1:3]  # Top 2 similar users
    user_ratings = df.loc[similar_users.index].mean(axis=0)  # Average ratings of similar users

    recommendations = user_ratings[user_ratings > 3].index.tolist()  # Recommend movies with avg rating > 3
    return recommendations

# Test recommendation
user_to_search = "Alice"
recommended_movies = recommend_movie_for_user(user_to_search)
print(f"Recommended movies for {user_to_search}: {recommended_movies}")
