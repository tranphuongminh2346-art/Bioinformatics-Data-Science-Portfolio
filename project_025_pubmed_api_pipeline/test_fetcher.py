"""
Unit Tests for PubMed Fetcher Pipeline
Author: Portfolio Creator
Description: Verify Entrez API queries parsing and offline mock fallbacks.
Language: English (100%)
"""

import unittest
import os
import sys
import tempfile
from unittest.mock import patch
import requests

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pubmed_fetcher import PubMedFetcher

class TestPubMedFetcher(unittest.TestCase):

    def setUp(self):
        self.fetcher = PubMedFetcher()

    @patch('requests.get')
    def test_mock_fallback_search(self, mock_get):
        # Force requests to raise exception to trigger offline mock fallback
        mock_get.side_effect = requests.RequestException("Simulated Offline")
        pmids = self.fetcher.search_articles("bioinformatics", retmax=3)
        
        self.assertEqual(len(pmids), 3)
        self.assertIn("32112345", pmids)

    @patch('requests.get')
    def test_mock_fallback_summaries(self, mock_get):
        # Force requests to raise exception to trigger offline mock fallback
        mock_get.side_effect = requests.RequestException("Simulated Offline")
        pmids = ["32112345", "31223456"]
        summaries = self.fetcher.fetch_summaries(pmids)
        
        self.assertEqual(len(summaries), 2)
        self.assertEqual(summaries[0]["pmid"], "32112345")
        self.assertEqual(summaries[0]["journal"], "Bioinformatics Journal")
        self.assertIn("Smith J", summaries[0]["authors"])

    def test_export_csv(self):
        mock_articles = [
            {
                "pmid": "123",
                "title": "A Test Paper",
                "journal": "Science",
                "pub_date": "2026",
                "authors": "Author A"
            }
        ]
        
        # Test writing to temp CSV
        db_fd, temp_csv_path = tempfile.mkstemp(suffix=".csv")
        try:
            self.fetcher.export_to_csv(mock_articles, temp_csv_path)
            self.assertTrue(os.path.exists(temp_csv_path))
            
            # Read back
            df = pd_read = pd = import_pandas = pandas_check = None
            import pandas as pd
            df = pd.read_csv(temp_csv_path)
            self.assertEqual(len(df), 1)
            self.assertEqual(df["pmid"].iloc[0], 123)
        finally:
            os.close(db_fd)
            if os.path.exists(temp_csv_path):
                os.remove(temp_csv_path)

if __name__ == "__main__":
    unittest.main()
