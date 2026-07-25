"""
Unit Tests for Needleman-Wunsch Aligner
Author: Portfolio Creator
Description: Verify scoring matrix values, global traceback alignments, and formatted prints.
Language: English (100%)
"""

import unittest
import os
import sys
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from needleman_wunsch import NeedlemanWunschAligner

class TestNeedlemanWunschAligner(unittest.TestCase):

    def setUp(self):
        # Match = 1, Mismatch = -1, Gap = -1
        self.aligner = NeedlemanWunschAligner(match_score=1, mismatch_penalty=-1, gap_penalty=-1)

    def test_simple_match(self):
        # Alignment of AAAA to AAAA should match perfectly
        score, al1, al2 = self.aligner.align("AAAA", "AAAA")
        
        self.assertEqual(score, 4.0)
        self.assertEqual(al1, "AAAA")
        self.assertEqual(al2, "AAAA")

    def test_alignment_with_gaps(self):
        # Align ATGC with AG
        # ATGC
        # A-G- or A--G or similar
        # Best alignment:
        # A T G C
        # A - G - (Match A, Gap T, Match G, Gap C -> 1 - 1 + 1 - 1 = 0)
        score, al1, al2 = self.aligner.align("ATGC", "AG")
        
        self.assertEqual(score, 0.0)
        self.assertEqual(len(al1), len(al2))

    def test_scoring_matrix_boundaries(self):
        self.aligner.align("A", "A")
        matrix = self.aligner.score_matrix
        
        # Row 0: 0, -1
        self.assertEqual(matrix[0, 0], 0.0)
        self.assertEqual(matrix[0, 1], -1.0)
        # Col 0: 0, -1
        self.assertEqual(matrix[1, 0], -1.0)

    def test_format_alignment(self):
        al1 = "A-T"
        al2 = "ACT"
        # Match A, Gap, Match T -> should print middle line: "| |"
        res = self.aligner.format_alignment(al1, al2)
        self.assertIn("|", res)
        self.assertIn("Seq1: A-T", res)

if __name__ == "__main__":
    unittest.main()
