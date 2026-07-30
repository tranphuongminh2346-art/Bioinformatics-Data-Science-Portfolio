"""
Unit Tests for Digit Classifier Model
Author: Portfolio Creator
Description: Verify dataset splits, Gaussian Naive Bayes fits, and classification accuracies.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from digit_classifier import DigitClassifier

class TestDigitClassifier(unittest.TestCase):

    def setUp(self):
        # Create a mock digits dataset of 10 records with 64 features and target label
        # 5 labels = 0, 5 labels = 1
        data_dict = {f"pixel_{i}": [0]*10 for i in range(64)}
        
        # Add distinguishing values for digit 1 (middle column pixel 4 has high intensity)
        for i in range(5, 10):
            data_dict["pixel_4"][i] = 16
            data_dict["pixel_12"][i] = 16
            data_dict["pixel_20"][i] = 16
            
        data_dict["label"] = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
        
        self.mock_data = pd.DataFrame(data_dict)
        
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        self.mock_data.to_csv(self.temp_csv_path, index=False)
        self.clf = DigitClassifier(self.temp_csv_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_csv_path):
            os.remove(self.temp_csv_path)

    def test_load_data(self):
        self.assertEqual(len(self.clf.df), 10)
        self.assertEqual(len(self.clf.features), 64)
        self.assertNotIn("label", self.clf.features)

    def test_training(self):
        # Split: 10 records, test_size=0.2 -> 8 train, 2 test
        X_test, y_test = self.clf.train_model()
        
        self.assertTrue(self.clf.is_trained)
        self.assertEqual(len(X_test), 2)
        self.assertEqual(len(y_test), 2)

    def test_predict_single_digit(self):
        self.clf.train_model()
        
        # Test digit 0 vector (all 0s)
        sample_digit_0 = [0] * 64
        pred_0 = self.clf.predict_digit(sample_digit_0)
        self.assertEqual(pred_0, 0)
        
        # Test digit 1 vector (high values in col 4)
        sample_digit_1 = [0] * 64
        sample_digit_1[4] = 16
        sample_digit_1[12] = 16
        sample_digit_1[20] = 16
        pred_1 = self.clf.predict_digit(sample_digit_1)
        self.assertEqual(pred_1, 1)

if __name__ == "__main__":
    unittest.main()
