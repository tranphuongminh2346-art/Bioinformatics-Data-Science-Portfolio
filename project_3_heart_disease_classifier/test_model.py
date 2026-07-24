"""
Unit Tests for Heart Disease Classifier Model
Author: Portfolio Creator
Description: Verify dataset processing, training methods, and inference predictions.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np
import tempfile
from sklearn.exceptions import NotFittedError

# Add directory containing this file to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model import HeartDiseaseClassifier

class TestHeartDiseaseClassifier(unittest.TestCase):

    def setUp(self):
        # Create mock dataset
        self.mock_data = pd.DataFrame({
            "age": [50, 60, 45, 55, 65, 40, 52, 58, 48, 62],
            "sex": [1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
            "cp": [0, 2, 1, 3, 0, 2, 1, 0, 2, 3],
            "trestbps": [130, 140, 120, 150, 135, 115, 125, 145, 128, 138],
            "chol": [250, 290, 230, 280, 310, 210, 240, 270, 260, 300],
            "fbs": [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
            "restecg": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            "thalach": [150, 130, 165, 140, 125, 170, 155, 135, 148, 142],
            "exang": [0, 1, 0, 1, 1, 0, 0, 1, 0, 1],
            "oldpeak": [1.5, 2.5, 0.5, 1.8, 3.0, 0.0, 1.0, 2.0, 0.8, 2.2],
            "slope": [1, 2, 1, 2, 2, 0, 1, 2, 1, 2],
            "ca": [0, 1, 0, 2, 3, 0, 1, 2, 0, 1],
            "thal": [2, 3, 2, 3, 3, 2, 2, 3, 2, 3],
            "target": [0, 1, 0, 1, 1, 0, 0, 1, 0, 1]  # 5 class 0, 5 class 1
        })
        
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        self.mock_data.to_csv(self.temp_csv_path, index=False)
        self.clf = HeartDiseaseClassifier(self.temp_csv_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_csv_path):
            os.remove(self.temp_csv_path)

    def test_preprocessing(self):
        X_train, X_test, y_train, y_test = self.clf.load_and_preprocess()
        
        # Test split sizes (10 records, test_size=0.2 means 8 train, 2 test)
        self.assertEqual(len(X_train), 8)
        self.assertEqual(len(X_test), 2)
        
        # Verify stratified balance in y
        self.assertEqual(sum(y_train == 1), 4)
        self.assertEqual(sum(y_train == 0), 4)
        
        # Verify scaling features are zero-mean and unit variance
        self.assertAlmostEqual(X_train.mean(), 0.0, places=5)

    def test_training_and_evaluation(self):
        # Assert not trained before preprocess
        with self.assertRaises(ValueError):
            self.clf.evaluate(np.zeros((2, 13)), [0, 1])

        X_train, X_test, y_train, y_test = self.clf.load_and_preprocess()
        self.clf.train(X_train, y_train)
        
        self.assertTrue(self.clf.is_trained)
        
        # Evaluate model
        metrics = self.clf.evaluate(X_test, y_test)
        self.assertIn("accuracy", metrics)
        self.assertIn("confusion_matrix", metrics)
        self.assertIn("roc", metrics)

    def test_inference(self):
        X_train, X_test, y_train, y_test = self.clf.load_and_preprocess()
        self.clf.train(X_train, y_train)
        
        # 13 mock patient clinical attributes
        sample_patient = [50, 1, 0, 130, 250, 0, 1, 150, 0, 1.5, 1, 0, 2]
        pred, prob = self.clf.predict_risk(sample_patient)
        
        self.assertIn(pred, [0, 1])
        self.assertTrue(0.0 <= prob <= 1.0)

if __name__ == "__main__":
    unittest.main()
