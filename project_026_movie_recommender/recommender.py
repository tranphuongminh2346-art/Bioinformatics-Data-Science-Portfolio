"""
Movie Recommender System (Collaborative Filtering)
Author: Portfolio Creator
Description: Implements item-based collaborative filtering recommender systems,
             calculates cosine similarity matrix profiles, and outputs top N recommendations.
Language: English (100%)
"""

import os
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class MovieRecommender:
    """Item-based Collaborative Filtering Recommender using cosine similarities."""
    
    def __init__(self, ratings_path: str):
        self.ratings_path = ratings_path
        self.df = None
        self.user_item_matrix = None
        self.similarity_df = None
        self.load_data()

    def load_data(self):
        """Loads rating CSV records."""
        if not os.path.exists(self.ratings_path):
            raise FileNotFoundError(f"Ratings file not found: {self.ratings_path}")
        self.df = pd.read_csv(self.ratings_path)

    def build_similarity_matrix(self):
        """Pivots user ratings and calculates the item-item cosine similarity matrix."""
        # Pivot: rows = users, cols = movies
        self.user_item_matrix = self.df.pivot_table(
            index='user_id',
            columns='movie_title',
            values='rating'
        ).fillna(0.0)
        
        # Calculate cosine similarity between columns (movies)
        # Transpose to get movie vs movie similarities
        movie_similarities = cosine_similarity(self.user_item_matrix.T)
        
        # Create a DataFrame wrapper
        self.similarity_df = pd.DataFrame(
            movie_similarities,
            index=self.user_item_matrix.columns,
            columns=self.user_item_matrix.columns
        )

    def get_similar_movies(self, movie_title: str, limit: int = 3) -> list:
        """
        Retrieves similar movies for a given target title.
        
        Returns:
            list: List of tuples (movie_title: str, similarity_score: float).
        """
        if self.similarity_df is None:
            self.build_similarity_matrix()
            
        if movie_title not in self.similarity_df.index:
            raise KeyError(f"Movie title '{movie_title}' not found in training dataset.")
            
        # Get similarities for movie, sort descending, exclude the self movie
        movie_scores = self.similarity_df[movie_title].drop(labels=[movie_title])
        top_similar = movie_scores.sort_values(ascending=False).head(limit)
        
        return list(zip(top_similar.index, top_similar.values))
