"""
Unit Tests for Weather ETL Pipeline
Author: Portfolio Creator
Description: Verify temperature conversions, rolling average values, and database logs.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import tempfile
import json

# Add directory containing this file to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from etl import WeatherETL
from db_loader import WeatherDatabaseLoader

class TestWeatherETL(unittest.TestCase):

    def setUp(self):
        # Create temp cache file
        self.mock_payload = {
            "hourly": {
                "time": ["2026-07-13T00:00", "2026-07-13T01:00", "2026-07-13T02:00"],
                "temperature_2m": [10.0, 20.0, 30.0]
            }
        }
        
        self.db_fd, self.temp_cache_path = tempfile.mkstemp(suffix=".json")
        with open(self.temp_cache_path, 'w', encoding='utf-8') as f:
            json.dump(self.mock_payload, f)
            
        self.etl = WeatherETL(self.temp_cache_path)
        
        # Temp database path
        self.db_db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        self.db_loader = WeatherDatabaseLoader(self.temp_db_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_cache_path):
            os.remove(self.temp_cache_path)
            
        os.close(self.db_db_fd)
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

    def test_extraction_from_cache(self):
        data = self.etl.extract()
        self.assertEqual(data["hourly"]["temperature_2m"], [10.0, 20.0, 30.0])

    def test_transformation(self):
        df = self.etl.transform(self.mock_payload)
        
        # Check shapes
        self.assertEqual(len(df), 3)
        
        # 1. Check Fahrenheit conversions
        # 10.0 C -> 50.0 F
        # 20.0 C -> 68.0 F
        # 30.0 C -> 86.0 F
        self.assertAlmostEqual(df.iloc[0]["temperature_f"], 50.0)
        self.assertAlmostEqual(df.iloc[1]["temperature_f"], 68.0)
        self.assertAlmostEqual(df.iloc[2]["temperature_f"], 86.0)
        
        # 2. Check 3-hour rolling averages
        # Hour 0: [10.0] -> avg = 10.0
        # Hour 1: [10.0, 20.0] -> avg = 15.0
        # Hour 2: [10.0, 20.0, 30.0] -> avg = 20.0
        self.assertAlmostEqual(df.iloc[0]["rolling_avg_c"], 10.0)
        self.assertAlmostEqual(df.iloc[1]["rolling_avg_c"], 15.0)
        self.assertAlmostEqual(df.iloc[2]["rolling_avg_c"], 20.0)

    def test_database_loading_and_summary(self):
        df = self.etl.transform(self.mock_payload)
        self.db_loader.load(df)
        
        stats = self.db_loader.get_summary_stats()
        self.assertIn("avg_temp_c", stats)
        # Avg of (10, 20, 30) is 20.0
        self.assertAlmostEqual(stats["avg_temp_c"], 20.0)
        self.assertAlmostEqual(stats["max_temp_c"], 30.0)
        self.assertAlmostEqual(stats["min_temp_c"], 10.0)

if __name__ == "__main__":
    unittest.main()
