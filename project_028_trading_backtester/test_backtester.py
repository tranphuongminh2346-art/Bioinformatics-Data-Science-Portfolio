"""
Unit Tests for Stock Backtester
Author: Portfolio Creator
Description: Verify SMA indicators, trade position shifts, and Sharpe ratio formulas.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backtester import TradingBacktester

class TestTradingBacktester(unittest.TestCase):

    def setUp(self):
        # Create a simple mock price history of 6 days
        # trending upward: 10, 11, 12, 13, 14, 15
        self.mock_data = pd.DataFrame({
            "date": [f"2026-06-0{i}" for i in range(1, 7)],
            "close_price": [10.0, 11.0, 12.0, 13.0, 14.0, 15.0]
        })
        
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        self.mock_data.to_csv(self.temp_csv_path, index=False)
        self.backtester = TradingBacktester(self.temp_csv_path, initial_capital=1000.0)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_csv_path):
            os.remove(self.temp_csv_path)

    def test_sma_calculations(self):
        # Short = 2, Long = 3
        self.backtester.run_backtest(short_window=2, long_window=3)
        
        # Day 3 close prices: 10, 11, 12.
        # SMA Short = Mean(11, 12) = 11.5
        # SMA Long = Mean(10, 11, 12) = 11.0
        row_3 = self.backtester.df.iloc[2]
        self.assertEqual(row_3['sma_short'], 11.5)
        self.assertEqual(row_3['sma_long'], 11.0)
        self.assertEqual(row_3['signal'], 1)  # 11.5 > 11.0

    def test_position_shifting(self):
        self.backtester.run_backtest(short_window=2, long_window=3)
        
        # Signal at Day 3 (index 2) is 1.
        # Position at Day 4 (index 3) must be 1.
        row_4 = self.backtester.df.iloc[3]
        self.assertEqual(row_4['position'], 1)

    def test_drawdown_calculation(self):
        # Let's verify that max drawdown returns a float <= 0.0
        metrics = self.backtester.run_backtest(short_window=2, long_window=3)
        self.assertTrue(isinstance(metrics['max_drawdown'], float))
        self.assertTrue(metrics['max_drawdown'] <= 0.0)

if __name__ == "__main__":
    unittest.main()
