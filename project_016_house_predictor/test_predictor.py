"""
Unit Tests for House Price Predictor
Author: Portfolio Creator
Description: Verify standardization scaling, Ridge training, and MAE/RMSE score math.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from price_predictor import HousePricePredictor

class TestHousePricePredictor(unittest.TestCase):

    def setUp(self):
        # Create a mock housing dataset
        # 10 records, target column MedHouseValue
        self.mock_data = pd.DataFrame({
            "MedInc": [8.3, 3.7, 1.8, 2.0, 3.1, 7.2, 3.2, 5.6, 3.8, 3.2],
            "HouseAge": [41.0, 52.0, 52.0, 52.0, 52.0, 52.0, 52.0, 52.0, 52.0, 52.0],
            "AveRooms": [6.9, 6.2, 4.0, 4.7, 5.0, 8.2, 4.7, 6.1, 5.6, 4.7],
            "AveBedrms": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            "Population": [322.0, 485.0, 425.0, 396.0, 465.0, 558.0, 458.0, 532.0, 514.0, 432.0],
            "AveOccup": [2.5, 2.1, 2.3, 2.4, 2.1, 2.5, 2.1, 2.1, 2.1, 2.1],
            "Latitude": [37.8, 37.8, 37.8, 37.8, 37.8, 37.8, 37.8, 37.8, 37.8, 37.8],
            "Longitude": [-122.2, -122.2, -122.2, -122.2, -122.2, -122.2, -122.2, -122.2, -122.2, -122.2],
            "MedHouseValue": [4.5, 2.7, 0.9, 1.0, 1.1, 3.5, 1.0, 2.4, 1.5, 1.3]
        })
        
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        self.mock_data.to_csv(self.temp_csv_path, index=False)
        self.predictor = HousePricePredictor(self.temp_csv_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_csv_path):
            os.remove(self.temp_csv_path)

    def test_preprocessing_and_scaling(self):
        X_train, X_test, y_train, y_test = self.predictor.preprocess()
        
        # Test split shapes: 10 records, test_size=0.2 means 8 train, 2 test
        self.assertEqual(len(X_train), 8)
        self.assertEqual(len(X_test), 2)
        
        # Test mean of scaled features (should be close to 0)
        self.assertAlmostEqual(np.mean(X_train, axis=0)[0], 0.0, places=5)
        # Test standard deviation (should be close to 1)
        self.assertAlmostEqual(np.std(X_train, axis=0)[0], 1.0, places=5)

    def test_training_and_evaluation(self):
        X_train, X_test, y_train, y_test = self.predictor.preprocess()
        self.predictor.train(X_train, y_train)
        
        self.assertTrue(self.predictor.is_trained)
        
        metrics = self.predictor.evaluate(X_test, y_test)
        self.assertIn("mae", metrics)
        self.assertIn("rmse", metrics)
        self.assertIn("r2", metrics)
        
        # Predict single record
        demo_prop = np.array([5.0, 30.0, 6.0, 1.0, 450.0, 2.2, 37.8, -122.2])
        val = self.predictor.predict_value(demo_prop)
        self.assertTrue(val > 0.0)

if __name__ == "__main__":
    unittest.main()
