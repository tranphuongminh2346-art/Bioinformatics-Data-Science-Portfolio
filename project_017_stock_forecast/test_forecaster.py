"""
Unit Tests for Stock Price Forecaster
Author: Portfolio Creator
Description: Verify lag values alignment, sequential split boundaries,
             and multi-step recursive forecasting predictions.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from forecaster import StockPriceForecaster

class TestStockPriceForecaster(unittest.TestCase):

    def setUp(self):
        # Create a mock stock history of 10 days
        self.mock_data = pd.DataFrame({
            "date": [f"2026-06-{i:02d}" for i in range(1, 11)],
            "close_price": [10.0, 12.0, 15.0, 11.0, 13.0, 16.0, 18.0, 17.0, 19.0, 21.0]
        })
        
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        self.mock_data.to_csv(self.temp_csv_path, index=False)
        self.forecaster = StockPriceForecaster(self.temp_csv_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_csv_path):
            os.remove(self.temp_csv_path)

    def test_feature_engineering(self):
        clean_df = self.forecaster.engineer_features()
        
        # Test shapes: 10 rows. Since we shift 3 lags and window 3, first 3 rows are dropped -> 7 rows remain
        self.assertEqual(len(clean_df), 7)
        
        # Check first clean row (originally day 4 index 3)
        # Day 4 price = 11.0
        # Lags: lag_1 = Day 3 (15.0), lag_2 = Day 2 (12.0), lag_3 = Day 1 (10.0)
        # rolling_mean_3 (shifting 1) = Mean of [10.0, 12.0, 15.0] = 12.3333
        first_row = clean_df.iloc[0]
        self.assertEqual(first_row['close_price'], 11.0)
        self.assertEqual(first_row['lag_1'], 15.0)
        self.assertEqual(first_row['lag_2'], 12.0)
        self.assertEqual(first_row['lag_3'], 10.0)
        self.assertAlmostEqual(first_row['rolling_mean_3'], 12.3333, places=4)

    def test_sequential_split(self):
        clean_df = self.forecaster.engineer_features()
        X_train, X_test, y_train, y_test, train_df, test_df = self.forecaster.train_test_split_sequential(clean_df, train_ratio=0.8)
        
        # 7 rows. Train = 80% of 7 = 5 rows. Test = 2 rows
        self.assertEqual(len(train_df), 5)
        self.assertEqual(len(test_df), 2)
        
        # Check that test set dates strictly follow train set dates (sequential)
        self.assertTrue(test_df['date'].iloc[0] > train_df['date'].iloc[-1])

    def test_multistep_forecast(self):
        clean_df = self.forecaster.engineer_features()
        X_train, X_test, y_train, y_test, train_df, test_df = self.forecaster.train_test_split_sequential(clean_df)
        self.forecaster.train(X_train, y_train)
        
        # Test 3 steps forecast
        last_row = clean_df.iloc[-1]
        forecasts = self.forecaster.forecast_multistep(last_row, steps=3)
        self.assertEqual(len(forecasts), 3)
        
        # Assert values are numbers
        for val in forecasts:
            self.assertTrue(isinstance(val, float))

    def test_evaluate(self):
        clean_df = self.forecaster.engineer_features()
        X_train, X_test, y_train, y_test, train_df, test_df = self.forecaster.train_test_split_sequential(clean_df)
        self.forecaster.train(X_train, y_train)
        
        metrics = self.forecaster.evaluate(X_test, y_test)
        self.assertIn("mae", metrics)
        self.assertIn("rmse", metrics)
        self.assertIn("predictions", metrics)
        self.assertEqual(len(metrics["predictions"]), len(y_test))

if __name__ == "__main__":
    unittest.main()
