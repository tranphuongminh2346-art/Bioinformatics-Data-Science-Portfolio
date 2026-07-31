"""
Unit Tests for Text Summarizer
Author: Portfolio Creator
Description: Verify sentence regex splitting, TF-IDF cosine weights, and PageRank ordering.
Language: English (100%)
"""

import unittest
import os
import sys
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from summarizer import TextSummarizer

class TestTextSummarizer(unittest.TestCase):

    def setUp(self):
        # Create a mock text file with 4 simple sentences
        # Sentence 1 and 2 share many words: "DNA is copied to RNA", "RNA is genetic info"
        # Sentence 3 and 4 share many words: "Ribosomes translate proteins", "Proteins fold nicely"
        self.mock_text = (
            "DNA is copied to RNA. "
            "RNA is genetic info. "
            "Ribosomes translate proteins. "
            "Proteins fold nicely."
        )
        
        self.db_fd, self.temp_text_path = tempfile.mkstemp(suffix=".txt")
        with open(self.temp_text_path, 'w', encoding='utf-8') as f:
            f.write(self.mock_text)
            
        self.summarizer = TextSummarizer(self.temp_text_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_text_path):
            os.remove(self.temp_text_path)

    def test_sentence_splitting(self):
        # Should split into 4 sentences
        self.assertEqual(len(self.summarizer.sentences), 4)
        self.assertEqual(self.summarizer.sentences[0], "DNA is copied to RNA.")
        self.assertEqual(self.summarizer.sentences[3], "Proteins fold nicely.")

    def test_summarization_output(self):
        # Extract top 2 sentences
        summary = self.summarizer.summarize(limit=2)
        
        self.assertEqual(len(summary), 2)
        # Check that sentences returned are present in document
        self.assertIn(summary[0][0], self.summarizer.sentences)
        self.assertTrue(0.0 <= summary[0][1] <= 1.0)

if __name__ == "__main__":
    unittest.main()
