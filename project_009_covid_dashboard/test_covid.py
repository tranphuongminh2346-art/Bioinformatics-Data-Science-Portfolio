"""
Unit Tests for COVID-19 Time Series Analyzer
Author: Portfolio Creator
Description: Verify daily new calculations, rolling averages, and growth rate computations.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from covid_analyzer import CovidTimeSeriesAnalyzer

class TestCovidTimeSeriesAnalyzer(unittest.TestCase):

    def setUp(self):
        # Create a mock cumulative sequence
        self.mock_data = (
            "date,confirmed_cases,confirmed_deaths\n"
            "2020-03-01,10,0\n"
            "2020-03-02,15,1\n"
            "2020-03-03,22,1\n"
            "2020-03-04,30,2\n"
            "2020-03-05,40,2\n"
            "2020-03-06,55,3\n"
            "2020-03-07,75,4\n"
        )
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        with open(self.temp_csv_path, 'w', encoding='utf-8') as f:
            f.write(self.mock_data)
            
        self.analyzer = CovidTimeSeriesAnalyzer(self.temp_csv_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_csv_path):
            os.remove(self.temp_csv_path)

    def test_daily_calculations(self):
        df = self.analyzer.calculate_daily_metrics()
        
        # 1. Check daily diffs
        # Index 0: 10 (fallback to cumulative)
        # Index 1: 15 - 10 = 5
        # Index 2: 22 - 15 = 7
        self.assertEqual(df.iloc[0]['new_cases'], 10)
        self.assertEqual(df.iloc[1]['new_cases'], 5)
        self.assertEqual(df.iloc[2]['new_cases'], 7)

        # 2. Check deaths diffs
        # Index 0: 0
        # Index 1: 1 - 0 = 1
        # Index 2: 1 - 1 = 0
        self.assertEqual(df.iloc[0]['new_deaths'], 0)
        self.assertEqual(df.iloc[1]['new_deaths'], 1)
        self.assertEqual(df.iloc[2]['new_deaths'], 0)

        # 3. Check growth rate (pct_change)
        # Index 1: (5 - 10)/10 = -0.5
        # Index 2: (7 - 5)/5 = 0.4
        self.assertAlmostEqual(df.iloc[1]['case_growth_rate'], -0.5)
        self.assertAlmostEqual(df.iloc[2]['case_growth_rate'], 0.4)

    def test_rolling_averages(self):
        df = self.analyzer.calculate_daily_metrics()
        
        # At Index 1 (rolling window 7, elements = [10, 5]): average = 7.5
        self.assertAlmostEqual(df.iloc[1]['new_cases_rolling'], 7.5)

if __name__ == "__main__":
    unittest.main()
