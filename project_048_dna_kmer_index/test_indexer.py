"""
Unit Tests for BWT DNA Indexer
Author: Portfolio Creator
Description: Verify BWT strings, Inverse reconstructions, and backward search lookups.
Language: English (100%)
"""

import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bwt_indexer import BWTIndexer

class TestBWTIndexer(unittest.TestCase):

    def setUp(self):
        # Sequence: "GCATGCATGC$"
        self.seq = "GCATGCATGC"
        self.indexer = BWTIndexer(self.seq)

    def test_bwt_generation(self):
        # Check BWT string length (should be length + 1 due to sentinel)
        self.assertEqual(len(self.indexer.bwt_string), 11)
        
        # Verify first column is sorted alphabetically: '$', 'A', 'A', 'C', 'C', 'C', 'G', 'G', 'G', 'T', 'T'
        self.assertEqual(self.indexer.first_col, sorted(list(self.seq + '$')))

    def test_inverse_bwt(self):
        # Inverse BWT must exactly recover the original sequence (without sentinel)
        recovered = self.indexer.inverse_bwt()
        self.assertEqual(recovered, self.seq)

    def test_backward_search(self):
        # "GCATGCATGC" contains "ATG" starting at index 2 (GC ATG CATGC) and index 6 (GCATG ATG C)
        matches = self.indexer.search_kmer("ATG")
        self.assertEqual(matches, [2, 6])
        
        # Query "GC"
        # "GCATGCATGC" contains "GC" starting at:
        # index 0 (GC ATGCATGC)
        # index 4 (GCAT GC ATGC)
        # index 8 (GCATGCAT GC)
        matches_gc = self.indexer.search_kmer("GC")
        self.assertEqual(matches_gc, [0, 4, 8])
        
        # Non-existing query
        self.assertEqual(self.indexer.search_kmer("TTT"), [])

if __name__ == "__main__":
    unittest.main()
