"""
Unit Tests for Wine Classifier Model
Author: Portfolio Creator
Description: Verify dataset splits, model training fits, and predicted qualities.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from wine_classifier import WineQualityClassifier

class TestWineQualityClassifier(unittest.TestCase):

    def setUp(self):
        # Create a mock wine dataset with 10 records (5 quality=1, 5 quality=0)
        self.mock_data = pd.DataFrame({
            "fixed_acidity": [7.4, 7.8, 11.2, 7.4, 7.9, 7.3, 7.8, 7.5, 6.7, 7.5],
            "volatile_acidity": [0.7, 0.88, 0.28, 0.7, 0.6, 0.65, 0.58, 0.5, 0.58, 0.5],
            "pH": [3.51, 3.2, 3.16, 3.51, 3.3, 3.39, 3.36, 3.35, 3.35, 3.35],
            "alcohol": [9.4, 9.8, 9.8, 9.4, 9.4, 12.1, 10.5, 10.5, 10.0, 10.5],
            "quality": [0, 0, 1, 0, 0, 1, 1, 1, 0, 1]
        })
        
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        self.mock_data.to_csv(self.temp_csv_path, index=False)
        self.clf = WineQualityClassifier(self.temp_csv_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_csv_path):
            os.remove(self.temp_csv_path)

    def test_load_data(self):
        self.assertEqual(len(self.clf.df), 10)
        self.assertIn("quality", self.clf.df.columns)
        self.assertNotIn("quality", self.clf.features)

    def test_model_training(self):
        # Split: 10 records, test_size=0.2 -> 8 train, 2 test
        X_test, y_test = self.clf.train_model(max_depth=2)
        
        self.assertTrue(self.clf.is_trained)
        self.assertEqual(len(X_test), 2)
        self.assertEqual(len(y_test), 2)
        
        # Test max depth matches fitted tree depth
        self.assertTrue(self.clf.model.get_depth() <= 2)

    def test_predictions(self):
        self.clf.train_model(max_depth=2)
        
        # Chemical inputs: fixed_acidity, volatile_acidity, pH, alcohol
        sample_wine = [7.3, 0.65, 3.39, 12.1]
        pred = self.clf.predict_quality(sample_wine)
        self.assertIn(pred, [0, 1])

if __name__ == "__main__":
    unittest.main()
