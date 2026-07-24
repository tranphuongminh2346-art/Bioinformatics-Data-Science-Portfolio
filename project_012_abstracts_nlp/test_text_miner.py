"""
Unit Tests for Clinical Text Miner
Author: Portfolio Creator
Description: Verify token cleaning filters, TF-IDF weight shapes, and lexicon sentiment scores.
Language: English (100%)
"""

import unittest
import os
import sys
import tempfile
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from text_miner import ClinicalTextMiner

class TestClinicalTextMiner(unittest.TestCase):

    def setUp(self):
        # Create a mock abstracts dataset
        self.mock_data = [
            {
                "pmid": "1",
                "title": "Positive outcome",
                "abstract": "The treatment significantly improved patient survival and efficacy was robust."
            },
            {
                "pmid": "2",
                "title": "Negative outcome",
                "abstract": "Severe toxicity was observed. Treatment failed to provide benefits."
            }
        ]
        self.db_fd, self.temp_json_path = tempfile.mkstemp(suffix=".json")
        with open(self.temp_json_path, 'w', encoding='utf-8') as f:
            json.dump(self.mock_data, f)
            
        self.miner = ClinicalTextMiner(self.temp_json_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_json_path):
            os.remove(self.temp_json_path)

    def test_clean_text(self):
        tokens = self.miner.clean_text("The drug showed promising outcomes, but severe toxicity was noted!")
        
        # 'the', 'but', 'was' are stopwords, should be removed
        # Punctuation should be stripped
        self.assertNotIn("the", tokens)
        self.assertNotIn("but", tokens)
        self.assertIn("promising", tokens)
        self.assertIn("toxicity", tokens)

    def test_calculate_tfidf(self):
        term_df = self.miner.calculate_tfidf()
        
        # Check that we got non-empty terms list
        self.assertTrue(len(term_df) > 0)
        self.assertIn("treatment", term_df["term"].values)

    def test_analyze_sentiment(self):
        evaluations = self.miner.analyze_sentiment()
        
        self.assertEqual(len(evaluations), 2)
        
        # Doc 1 has positive words: 'significantly', 'improved', 'efficacy', 'robust' (score > 0)
        doc1 = evaluations[0]
        self.assertEqual(doc1["sentiment_class"], "Positive Clinical Outcome")
        self.assertTrue(doc1["polarity_score"] > 0)

        # Doc 2 has negative words: 'severe', 'toxicity', 'failed' (score < 0)
        doc2 = evaluations[1]
        self.assertEqual(doc2["sentiment_class"], "Negative Clinical Outcome")
        self.assertTrue(doc2["polarity_score"] < 0)

if __name__ == "__main__":
    unittest.main()
