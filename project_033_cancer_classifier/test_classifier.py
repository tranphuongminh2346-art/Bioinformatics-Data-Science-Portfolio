"""
Unit Tests for Cancer Classifier Model
Author: Portfolio Creator
Description: Verify dataset splits, SVM fits, and diagnostic classification predictions.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cancer_classifier import CancerClassifier

class TestCancerClassifier(unittest.TestCase):

    def setUp(self):
        # Create a mock cancer dataset of 10 entries (5 benign, 5 malignant)
        self.mock_data = pd.DataFrame({
            "mean_radius": [10.0, 11.0, 12.0, 13.0, 14.0, 18.0, 19.0, 20.0, 21.0, 22.0],
            "mean_texture": [12.0, 13.0, 14.0, 15.0, 16.0, 22.0, 23.0, 24.0, 25.0, 26.0],
            "mean_perimeter": [65.0, 70.0, 75.0, 80.0, 85.0, 118.0, 122.0, 130.0, 132.0, 135.0],
            "mean_area": [350.0, 400.0, 450.0, 500.0, 550.0, 1000.0, 1100.0, 1200.0, 1300.0, 1400.0],
            "mean_smoothness": [0.09, 0.09, 0.1, 0.1, 0.11, 0.08, 0.09, 0.1, 0.11, 0.12],
            "label": [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
        })
        
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        self.mock_data.to_csv(self.temp_csv_path, index=False)
        self.clf = CancerClassifier(self.temp_csv_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_csv_path):
            os.remove(self.temp_csv_path)

    def test_load_data(self):
        self.assertEqual(len(self.clf.df), 10)
        self.assertEqual(len(self.clf.features), 5)
        self.assertNotIn("label", self.clf.features)

    def test_model_training(self):
        X_test, y_test = self.clf.train_model()
        
        self.assertTrue(self.clf.is_trained)
        self.assertEqual(len(X_test), 2)
        self.assertEqual(len(y_test), 2)

    def test_predict_patient(self):
        self.clf.train_model()
        
        # Test benign sample (small radius, texture)
        benign_sample = [11.0, 13.0, 70.0, 400.0, 0.09]
        pred, prob = self.clf.predict_patient(benign_sample)
        
        self.assertEqual(pred, 0)
        self.assertTrue(0.0 <= prob <= 1.0)
        
        # Test malignant sample (large radius, texture)
        malignant_sample = [20.0, 24.0, 130.0, 1200.0, 0.10]
        pred_m, prob_m = self.clf.predict_patient(malignant_sample)
        
        self.assertEqual(pred_m, 1)

if __name__ == "__main__":
    unittest.main()
