"""
Unit Tests for Customer Segmentation Engine
Author: Portfolio Creator
Description: Verify data preprocessing scaling, cluster model dimensions, and inertia properties.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from segmentation import CustomerSegmenter

class TestCustomerSegmenter(unittest.TestCase):

    def setUp(self):
        # Create a mock customer dataset with 9 entries
        self.mock_data = pd.DataFrame({
            "CustomerID": list(range(1, 10)),
            "AnnualIncome": [15, 16, 18, 50, 52, 54, 90, 92, 95],
            "SpendingScore": [10, 12, 11, 48, 50, 51, 88, 90, 92]
        })
        
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        self.mock_data.to_csv(self.temp_csv_path, index=False)
        self.segmenter = CustomerSegmenter(self.temp_csv_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_csv_path):
            os.remove(self.temp_csv_path)

    def test_data_loading(self):
        self.assertEqual(len(self.segmenter.df), 9)
        self.assertIn("AnnualIncome", self.segmenter.df.columns)

    def test_clustering_fit(self):
        # Fit K=3 clusters
        labels = self.segmenter.fit_clusters(n_clusters=3)
        
        self.assertTrue(self.segmenter.is_fit)
        self.assertEqual(len(labels), 9)
        self.assertEqual(len(np.unique(labels)), 3)
        self.assertIn("Cluster", self.segmenter.df.columns)

    def test_elbow_inertia(self):
        inertias = self.segmenter.compute_elbow_curve(max_k=3)
        
        self.assertEqual(len(inertias), 3)
        # Inertia must decrease or stay same as K increases
        self.assertTrue(inertias[0] >= inertias[1])
        self.assertTrue(inertias[1] >= inertias[2])

if __name__ == "__main__":
    unittest.main()
