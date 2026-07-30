"""
Unit Tests for Temperature Anomaly Analyzer
Author: Portfolio Creator
Description: Verify DatetimeIndex formats, linear polyfit slopes, and decomposition outputs.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from time_series import TemperatureAnomalyAnalyzer

class TestTemperatureAnomalyAnalyzer(unittest.TestCase):

    def setUp(self):
        # Create a mock seasonal dataset of 24 months (2 periods of 12)
        # Trend: rising by 0.05 per month
        # Seasonal cycle: sine wave with period 12
        dates = pd.date_range(start="2024-01-01", periods=24, freq='MS')
        trend = np.arange(24) * 0.05
        seasonal = np.sin(np.arange(24) * (2 * np.pi / 12))
        anomaly = trend + seasonal
        
        self.mock_data = pd.DataFrame({
            "date": dates,
            "anomaly": anomaly
        })
        
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        os.close(self.db_fd)
        self.mock_data.to_csv(self.temp_csv_path, index=False)
        self.analyzer = TemperatureAnomalyAnalyzer(self.temp_csv_path)

    def tearDown(self):
        if os.path.exists(self.temp_csv_path):
            os.remove(self.temp_csv_path)

    def test_data_loading(self):
        # Check index type
        self.assertTrue(isinstance(self.analyzer.df.index, pd.DatetimeIndex))
        self.assertEqual(len(self.analyzer.df), 24)

    def test_trend_slope(self):
        slope = self.analyzer.calculate_trend_slope()
        
        # The exact slope is 0.05 - 0.039 = 0.011 due to sine-weighted covariances.
        self.assertAlmostEqual(slope, 0.011, places=3)

    def test_seasonal_decomposition(self):
        trend, seasonal, resid = self.analyzer.decompose_series(period=12)
        
        # Decomposed shapes should be equal to index length
        self.assertEqual(len(trend), 24)
        self.assertEqual(len(seasonal), 24)
        self.assertEqual(len(resid), 24)
        
        # Period 12 additive seasonal factors should repeat: seasonal[0] == seasonal[12]
        self.assertAlmostEqual(seasonal.iloc[0], seasonal.iloc[12])
        self.assertAlmostEqual(seasonal.iloc[5], seasonal.iloc[17])

if __name__ == "__main__":
    unittest.main()
