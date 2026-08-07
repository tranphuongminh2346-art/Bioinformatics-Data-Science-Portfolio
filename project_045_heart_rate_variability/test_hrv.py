"""
Unit Tests for ECG HRV Extractor
Author: Portfolio Creator
Description: Verify SDNN, RMSSD, pNN50 time-domain stats and resampled FFT bandpowers.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from hrv_extractor import HRVExtractor

class TestHRVExtractor(unittest.TestCase):

    def setUp(self):
        # Create a mock RR interval dataset (10 records)
        # RR intervals: 900, 950, 850, 900, 950, 850, 900, 950, 850, 900 (ms)
        # Mean = 900 ms.
        # Differences: +50, -100, +50, +50, -100, +50, +50, -100, +50 (9 diffs)
        # Diff magnitudes: 50, 100, 50, 50, 100, 50, 50, 100, 50
        # NN50 (diff > 50 ms): 100, 100, 100 -> 3 NN50 out of 9 diffs -> pNN50 = 3/9 = 33.33%
        self.mock_data = pd.DataFrame({
            "rr_interval": [900.0, 950.0, 850.0, 900.0, 950.0, 850.0, 900.0, 950.0, 850.0, 900.0]
        })
        
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        os.close(self.db_fd)
        self.mock_data.to_csv(self.temp_csv_path, index=False)
        self.extractor = HRVExtractor(self.temp_csv_path)

    def tearDown(self):
        if os.path.exists(self.temp_csv_path):
            try:
                os.remove(self.temp_csv_path)
            except PermissionError:
                pass

    def test_load(self):
        self.assertEqual(len(self.extractor.rr_intervals), 10)
        self.assertEqual(self.extractor.rr_intervals[0], 900.0)

    def test_time_domain_metrics(self):
        metrics = self.extractor.calculate_time_domain()
        
        self.assertEqual(metrics["mean_rr"], 900.0)
        # HR = 60000 / 900 = 66.67 bpm
        self.assertAlmostEqual(metrics["mean_hr"], 66.6667, places=3)
        
        # Verify SDNN: standard deviation of intervals (900, 950, 850, ...)
        # ddof=1: std should be ~40.82
        self.assertAlmostEqual(metrics["sdnn"], np.std(self.extractor.rr_intervals, ddof=1), places=4)
        
        # Verify RMSSD: sqrt(mean(diffs**2))
        # diffs: 50, -100, 50, 50, -100, 50, 50, -100, 50
        # squared diffs: 2500, 10000, 2500, 2500, 10000, 2500, 2500, 10000, 2500
        # sum of squares = 45000. mean = 45000 / 9 = 5000.
        # rmssd = sqrt(5000) = 70.71
        self.assertAlmostEqual(metrics["rmssd"], np.sqrt(5000.0), places=4)
        
        # NN50 checks: diff magnitudes > 50 ms.
        # differences: 50 (no), -100 (yes), 50 (no), 50 (no), -100 (yes), 50 (no), 50 (no), -100 (yes), 50 (no)
        # nn50 = 3, total diffs = 9 -> pnn50 = 33.333%
        self.assertAlmostEqual(metrics["pnn50"], 33.3333, places=3)

    def test_frequency_domain_metrics(self):
        # resample at 4Hz and check results are dictionaries
        freq = self.extractor.calculate_frequency_domain()
        self.assertIn("lf_power", freq)
        self.assertIn("hf_power", freq)
        self.assertIn("lf_hf_ratio", freq)
        self.assertTrue(freq["lf_power"] >= 0.0)
        self.assertTrue(freq["hf_power"] >= 0.0)

if __name__ == "__main__":
    unittest.main()
