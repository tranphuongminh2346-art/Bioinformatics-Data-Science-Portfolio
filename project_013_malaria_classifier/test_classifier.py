"""
Unit Tests for Malaria Microscopy Cell Classifier
Author: Portfolio Creator
Description: Verify model features extraction, binary labels mapping,
             model training triggers, and ROC/AUC validation coordinates.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from image_classifier import CellImageClassifier

class TestCellImageClassifier(unittest.TestCase):

    def setUp(self):
        # Create a mock dataset with 10 records (5 Parasitized, 5 Uninfected)
        self.mock_data = pd.DataFrame({
            "cell_id": [f"CELL_{i}" for i in range(10)],
            "mean_red_intensity": [140.0, 110.0, 145.0, 105.0, 138.0, 112.0, 142.0, 108.0, 139.0, 111.0],
            "std_deviation_intensity": [50.0, 15.0, 52.0, 14.0, 48.0, 16.0, 51.0, 13.0, 47.0, 15.0],
            "cell_area": [5000, 4800, 5100, 4900, 5050, 4780, 5120, 4920, 5090, 4810],
            "eccentricity": [0.12, 0.08, 0.15, 0.09, 0.11, 0.07, 0.14, 0.10, 0.12, 0.09],
            "label": ["Parasitized", "Uninfected", "Parasitized", "Uninfected", "Parasitized",
                      "Uninfected", "Parasitized", "Uninfected", "Parasitized", "Uninfected"]
        })
        
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        self.mock_data.to_csv(self.temp_csv_path, index=False)
        self.classifier = CellImageClassifier(self.temp_csv_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_csv_path):
            os.remove(self.temp_csv_path)

    def test_preprocessing(self):
        X_train, X_test, y_train, y_test = self.classifier.preprocess()
        
        # Test shapes: 10 records, test_size=0.2 means 8 train, 2 test
        self.assertEqual(len(X_train), 8)
        self.assertEqual(len(X_test), 2)
        
        # Check label mapping: Parasitized is mapped to 1, Uninfected to 0
        self.assertEqual(sum(y_train == 1), 4)
        self.assertEqual(sum(y_train == 0), 4)

    def test_training_and_metrics(self):
        X_train, X_test, y_train, y_test = self.classifier.preprocess()
        self.classifier.train(X_train, y_train)
        
        self.assertTrue(self.classifier.is_trained)
        
        evals = self.classifier.evaluate(X_test, y_test)
        self.assertIn("accuracy", evals)
        self.assertIn("auc", evals)
        self.assertEqual(len(evals["fpr"]), len(evals["tpr"]))

if __name__ == "__main__":
    unittest.main()
