"""
Unit Tests for Customer Churn Predictor
Author: Portfolio Creator
Description: Test suite for verifying preprocessing, training sequences, and prediction boundaries.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np
import tempfile

# Add directory containing this file to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from churn_model import CustomerChurnPredictor

class TestCustomerChurnPredictor(unittest.TestCase):

    def setUp(self):
        # Create a mock dataset with 10 records (5 Churn=Yes, 5 Churn=No)
        self.mock_data = pd.DataFrame({
            "customerID": [f"ID{i}" for i in range(10)],
            "tenure": [2, 50, 5, 60, 3, 40, 15, 68, 8, 4],
            "MonthlyCharges": [70.5, 20.0, 55.1, 115.8, 80.8, 45.3, 95.0, 60.2, 75.0, 85.5],
            "TotalCharges": [141.0, 1000.0, 275.5, 6948.0, 242.4, 1812.0, 1425.0, 4093.6, 600.0, 342.0],
            "Contract": ["Month-to-month", "Two year", "Month-to-month", "Two year", 
                         "Month-to-month", "One year", "Month-to-month", "Two year", 
                         "One year", "Month-to-month"],
            "InternetService": ["Fiber optic", "No", "DSL", "Fiber optic", 
                               "Fiber optic", "DSL", "Fiber optic", "DSL", 
                               "Fiber optic", "Fiber optic"],
            "Churn": ["Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No", "No", "Yes"]
        })
        
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        self.mock_data.to_csv(self.temp_csv_path, index=False)
        self.predictor = CustomerChurnPredictor(self.temp_csv_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_csv_path):
            os.remove(self.temp_csv_path)

    def test_preprocessing(self):
        X_train, X_test, y_train, y_test = self.predictor.load_and_preprocess()
        
        # Test split shapes (10 records, test_size=0.2 means 8 train, 2 test)
        self.assertEqual(len(X_train), 8)
        self.assertEqual(len(X_test), 2)
        
        # Test target conversion mapping
        # 5 Churns should correspond to 1, others to 0
        self.assertEqual(sum(y_train == 1), 4)
        self.assertEqual(sum(y_train == 0), 4)

        # Check encoded columns
        self.assertIn("Contract_One year", X_train.columns)
        self.assertIn("InternetService_Fiber optic", X_train.columns)

    def test_training_and_inference(self):
        X_train, X_test, y_train, y_test = self.predictor.load_and_preprocess()
        self.predictor.train(X_train, y_train)
        
        self.assertTrue(self.predictor.is_trained)
        
        # Evaluate
        metrics = self.predictor.evaluate(X_test, y_test)
        self.assertIn("accuracy", metrics)
        self.assertIn("confusion_matrix", metrics)

        # Single customer inference
        single_customer = pd.DataFrame([{
            "tenure": 12,
            "MonthlyCharges": 45.0,
            "TotalCharges": 540.0,
            "Contract_One year": 1,
            "Contract_Two year": 0,
            "InternetService_Fiber optic": 0,
            "InternetService_No": 0
        }])
        # Re-align columns
        single_customer = single_customer[self.predictor.feature_names]
        
        pred, prob = self.predictor.predict_churn(single_customer)
        self.assertIn(pred, [0, 1])
        self.assertTrue(0.0 <= prob <= 1.0)

if __name__ == "__main__":
    unittest.main()
