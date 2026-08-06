"""
Unit Tests for Solubility Predictor
Author: Portfolio Creator
Description: Verify dataset loading, Ridge fitting metrics, and compound solubility predictions.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from solubility_predictor import SolubilityPredictor

class TestSolubilityPredictor(unittest.TestCase):

    def setUp(self):
        # Create a mock solubility dataset of 10 records
        # Higher logp values map to lower solubility
        self.mock_data = pd.DataFrame({
            "molecular_weight": [100.0, 120.0, 140.0, 160.0, 180.0, 200.0, 220.0, 240.0, 260.0, 280.0],
            "logp": [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
            "rotatable_bonds": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            "polar_surface_area": [20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0],
            "solubility": [-0.5, -1.0, -1.5, -2.0, -2.5, -3.0, -3.5, -4.0, -4.5, -5.0]
        })
        
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        os.close(self.db_fd)
        self.mock_data.to_csv(self.temp_csv_path, index=False)
        self.predictor = SolubilityPredictor(self.temp_csv_path)

    def tearDown(self):
        if os.path.exists(self.temp_csv_path):
            try:
                os.remove(self.temp_csv_path)
            except PermissionError:
                pass

    def test_load(self):
        self.assertEqual(len(self.predictor.df), 10)
        self.assertEqual(len(self.predictor.features), 4)

    def test_model_training(self):
        X_test, y_test = self.predictor.train_model()
        self.assertTrue(self.predictor.is_trained)
        
        # Test size = 20% of 10 -> 2
        self.assertEqual(X_test.shape[0], 2)
        self.assertEqual(len(y_test), 2)
        
        metrics = self.predictor.evaluate_model(X_test, y_test)
        self.assertTrue(metrics["mse"] >= 0)
        self.assertTrue(-1.0 <= metrics["r2_score"] <= 1.0)

    def test_solubility_prediction(self):
        self.predictor.train_model()
        
        # Low logp (high solubility predicted)
        high_sol_chem = [100.0, 0.5, 0, 20.0]
        pred_high = self.predictor.predict_solubility(high_sol_chem)
        
        # High logp (low solubility predicted)
        low_sol_chem = [280.0, 5.0, 9, 65.0]
        pred_low = self.predictor.predict_solubility(low_sol_chem)
        
        self.assertTrue(pred_high > pred_low)

if __name__ == "__main__":
    unittest.main()
