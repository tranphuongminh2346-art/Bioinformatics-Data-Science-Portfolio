"""
Unit Tests for SMS Spam Filter
Author: Portfolio Creator
Description: Verify text preprocessing strings, TF-IDF dimensions, and model spam classifications.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from spam_filter import SMSSpamFilter

class TestSMSSpamFilter(unittest.TestCase):

    def setUp(self):
        # Create a mock dataset with 10 records (5 spam, 5 ham)
        self.mock_data = pd.DataFrame({
            "label": ["spam", "spam", "spam", "spam", "spam", "ham", "ham", "ham", "ham", "ham"],
            "text": [
                "Win free cash prize claim reward",
                "Claim free cash prize now",
                "Winner cash prizes free reward",
                "URGENT free cash prize claim",
                "Congratulations win free cash prize",
                "Hey meeting for lunch today",
                "Are we meeting for lunch",
                "Let us have lunch together today",
                "Meet for lunch at noon",
                "Hello what time is lunch meeting"
            ]
        })
        
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        self.mock_data.to_csv(self.temp_csv_path, index=False)
        self.filter = SMSSpamFilter(self.temp_csv_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_csv_path):
            os.remove(self.temp_csv_path)

    def test_text_cleaning(self):
        raw = "Hello, World! URGENT: 123?"
        clean = self.filter.clean_text(raw)
        # Should be lowercased, punctuation stripped: "hello world urgent 123"
        self.assertEqual(clean, "hello world urgent 123")

    def test_model_training(self):
        # Split: 10 records, test_size=0.2 -> 8 train, 2 test
        X_test, y_test = self.filter.train_model()
        
        self.assertTrue(self.filter.is_trained)
        self.assertEqual(X_test.shape[0], 2)
        self.assertEqual(len(y_test), 2)

    def test_predict_message(self):
        self.filter.train_model()
        
        # Test spam prediction
        label_spam, prob_spam = self.filter.predict_message("Win free cash prize and claim reward!")
        self.assertEqual(label_spam, "spam")
        
        # Test ham prediction
        label_ham, prob_ham = self.filter.predict_message("Let's meet for lunch at noon.")
        self.assertEqual(label_ham, "ham")

if __name__ == "__main__":
    unittest.main()
