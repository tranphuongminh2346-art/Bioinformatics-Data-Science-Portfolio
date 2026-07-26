"""
Web Log Anomaly Detector
Author: Portfolio Creator
Description: Parses Apache access logs, extracts request metrics, and trains
             an Isolation Forest model to flag cyber intrusion probes and huge downloads.
Language: English (100%)
"""

import os
import re
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

# Regex for Apache common log format
# Example: 192.168.1.1 - - [16/Jul/2026:10:00:01 +0000] "GET /index.html HTTP/1.1" 200 450
LOG_PATTERN = re.compile(
    r'^(\S+) \S+ \S+ \[(.*?)\] "(\S+) (\S+) \S+" (\d+) (\d+|-)$'
)

class LogAnomalyDetector:
    """Parses server log entries and trains Isolation Forest to identify anomalous requests."""
    
    def __init__(self, log_path: str):
        self.log_path = log_path
        self.df = None
        self.features_names = ['status_code', 'response_bytes', 'url_length']
        self.model = None
        self.is_trained = False
        self.load_and_parse_logs()

    def parse_log_line(self, line: str) -> dict:
        """Parses a single log line into a feature dictionary."""
        match = LOG_PATTERN.match(line.strip())
        if not match:
            return None
            
        ip, date, method, url, status, bytes_val = match.groups()
        
        # Handle '-' symbol in bytes
        bytes_val = 0 if bytes_val == '-' else int(bytes_val)
        
        return {
            "ip": ip,
            "date": date,
            "method": method,
            "url": url,
            "status_code": int(status),
            "response_bytes": bytes_val,
            "url_length": len(url),
            "raw_line": line.strip()
        }

    def load_and_parse_logs(self):
        """Reads log lines and populates features dataframe."""
        if not os.path.exists(self.log_path):
            raise FileNotFoundError(f"Log file not found: {self.log_path}")
            
        parsed_records = []
        with open(self.log_path, 'r', encoding='utf-8') as f:
            for line in f:
                record = self.parse_log_line(line)
                if record:
                    parsed_records.append(record)
                    
        self.df = pd.DataFrame(parsed_records)

    def train_detector(self, contamination: float = 0.15) -> np.ndarray:
        """
        Fits Isolation Forest on parsed logs.
        
        Returns:
            np.ndarray: Predicted labels (1: normal, -1: anomaly).
        """
        if self.df.empty:
            raise ValueError("No logs parsed to train model.")
            
        X = self.df[self.features_names]
        
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.model.fit(X)
        self.is_trained = True
        
        # Predict: 1 = normal, -1 = anomaly
        predictions = self.model.predict(X)
        self.df['AnomalyLabel'] = predictions
        
        # Higher score means less anomalous
        self.df['AnomalyScore'] = self.model.decision_function(X)
        
        return predictions

    def get_anomalies(self) -> pd.DataFrame:
        """Returns flagged anomalous records."""
        if not self.is_trained:
            raise ValueError("Model must be trained first.")
        return self.df[self.df['AnomalyLabel'] == -1]
