"""
Unit Tests for Movie Recommender
Author: Portfolio Creator
Description: Verify user-item pivot tables, cosine similarities, and recommendations lists sorting.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from recommender import MovieRecommender

class TestMovieRecommender(unittest.TestCase):

    def setUp(self):
        # Create a mock ratings dataset
        # 3 users, 4 movies
        # Movies: M1, M2 (highly similar for U1/U2) and M3, M4 (highly similar for U3)
        self.mock_data = pd.DataFrame({
            "user_id": [1, 1, 2, 2, 3, 3],
            "movie_title": ["M1", "M2", "M1", "M2", "M3", "M4"],
            "rating": [5.0, 5.0, 4.0, 4.0, 5.0, 5.0]
        })
        
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        self.mock_data.to_csv(self.temp_csv_path, index=False)
        self.recommender = MovieRecommender(self.temp_csv_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_csv_path):
            os.remove(self.temp_csv_path)

    def test_pivot_matrix(self):
        self.recommender.build_similarity_matrix()
        
        # 3 users, 4 movies
        self.assertEqual(self.recommender.user_item_matrix.shape, (3, 4))
        self.assertEqual(list(self.recommender.user_item_matrix.columns), ["M1", "M2", "M3", "M4"])

    def test_cosine_similarity(self):
        self.recommender.build_similarity_matrix()
        
        # Self-similarity should be 1.0
        self.assertAlmostEqual(self.recommender.similarity_df.loc["M1", "M1"], 1.0)
        
        # M1 and M2 should have high similarity (both users 1 and 2 rated them identically)
        self.assertAlmostEqual(self.recommender.similarity_df.loc["M1", "M2"], 1.0)
        
        # M1 and M3 should have low similarity (user 3 rated M3, but user 3 did not rate M1/M2)
        self.assertAlmostEqual(self.recommender.similarity_df.loc["M1", "M3"], 0.0)

    def test_recommendation_sorting(self):
        self.recommender.build_similarity_matrix()
        recs = self.recommender.get_similar_movies("M1", limit=2)
        
        # Best recommendation for M1 should be M2 (similarity = 1.0)
        self.assertEqual(recs[0][0], "M2")
        self.assertAlmostEqual(recs[0][1], 1.0)

if __name__ == "__main__":
    unittest.main()
