"""
Unit Tests for Microarray Clusterer
Author: Portfolio Creator
Description: Verify row-wise Z-score normalization means and linkage matrix sizes.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clustering import MicroarrayClusterer

class TestMicroarrayClusterer(unittest.TestCase):

    def setUp(self):
        # Create a mock expression CSV containing 4 genes and 5 samples
        self.mock_data = pd.DataFrame({
            "gene_name": ["G1", "G2", "G3", "G4"],
            "S1": [10.0, 20.0, 30.0, 40.0],
            "S2": [12.0, 18.0, 32.0, 38.0],
            "S3": [11.0, 21.0, 29.0, 41.0],
            "S4": [9.0,  19.0, 31.0, 39.0],
            "S5": [10.5, 20.5, 29.5, 40.5]
        })
        
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        os.close(self.db_fd)
        self.mock_data.to_csv(self.temp_csv_path, index=False)
        self.clusterer = MicroarrayClusterer(self.temp_csv_path)

    def tearDown(self):
        if os.path.exists(self.temp_csv_path):
            try:
                os.remove(self.temp_csv_path)
            except PermissionError:
                pass

    def test_load(self):
        self.assertEqual(len(self.clusterer.genes), 4)
        self.assertEqual(len(self.clusterer.samples), 5)
        self.assertEqual(self.clusterer.data_matrix.shape, (4, 5))

    def test_zscore_standardization(self):
        norm = self.clusterer.standardize_rows()
        
        # Verify Z-scores for each row have mean = 0 and std = 1
        for i in range(4):
            self.assertAlmostEqual(np.mean(norm[i, :]), 0.0, places=5)
            self.assertAlmostEqual(np.std(norm[i, :]), 1.0, places=5)

    def test_linkage_dimensions(self):
        # For N genes, linkage matrix shape is (N-1) x 4
        linkage = self.clusterer.compute_linkage(method='average')
        self.assertEqual(linkage.shape, (3, 4))

if __name__ == "__main__":
    unittest.main()
