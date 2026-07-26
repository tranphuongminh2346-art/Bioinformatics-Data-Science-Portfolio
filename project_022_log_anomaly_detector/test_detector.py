"""
Unit Tests for Web Log Anomaly Detector
Author: Portfolio Creator
Description: Verify regex log parsing patterns and Isolation Forest anomaly boundaries.
Language: English (100%)
"""

import unittest
import os
import sys
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from anomaly_detector import LogAnomalyDetector

class TestLogAnomalyDetector(unittest.TestCase):

    def setUp(self):
        # Create a mock web access log with normal entries and 1 anomaly (huge payload/status)
        self.mock_log = (
            '192.168.1.1 - - [16/Jul/2026:10:00:01 +0000] "GET /index.html HTTP/1.1" 200 450\n'
            '192.168.1.2 - - [16/Jul/2026:10:00:02 +0000] "GET /about.html HTTP/1.1" 200 450\n'
            '192.168.1.3 - - [16/Jul/2026:10:00:03 +0000] "GET /contact.html HTTP/1.1" 200 450\n'
            '192.168.1.4 - - [16/Jul/2026:10:00:04 +0000] "GET /index.html HTTP/1.1" 200 450\n'
            '192.168.1.5 - - [16/Jul/2026:10:00:05 +0000] "GET /index.html HTTP/1.1" 200 450\n'
            '10.0.0.99 - - [16/Jul/2026:10:00:06 +0000] "GET /admin?search=SELECT*FROM*users HTTP/1.1" 403 99999999\n'
        )
        
        self.db_fd, self.temp_log_path = tempfile.mkstemp(suffix=".log")
        with open(self.temp_log_path, 'w', encoding='utf-8') as f:
            f.write(self.mock_log)
            
        self.detector = LogAnomalyDetector(self.temp_log_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_log_path):
            os.remove(self.temp_log_path)

    def test_log_line_parsing(self):
        line = '192.168.1.1 - - [16/Jul/2026:10:00:01 +0000] "GET /index.html HTTP/1.1" 200 450'
        parsed = self.detector.parse_log_line(line)
        
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed['ip'], "192.168.1.1")
        self.assertEqual(parsed['method'], "GET")
        self.assertEqual(parsed['url'], "/index.html")
        self.assertEqual(parsed['status_code'], 200)
        self.assertEqual(parsed['response_bytes'], 450)
        self.assertEqual(parsed['url_length'], 11)

    def test_detector_training(self):
        # Fit model with 1 anomaly out of 6 items (~16%)
        predictions = self.detector.train_detector(contamination=0.17)
        
        self.assertEqual(len(predictions), 6)
        
        anomalies = self.detector.get_anomalies()
        self.assertEqual(len(anomalies), 1)
        
        # Verify the flagged row is the mock anomaly (10.0.0.99)
        self.assertEqual(anomalies['ip'].iloc[0], "10.0.0.99")
        self.assertEqual(anomalies['status_code'].iloc[0], 403)

if __name__ == "__main__":
    unittest.main()
