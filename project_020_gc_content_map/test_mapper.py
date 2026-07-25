"""
Unit Tests for Genomic GC-Skew & Content Mapper
Author: Portfolio Creator
Description: Verify fasta loading, sliding window ranges, and GC skew mathematical outputs.
Language: English (100%)
"""

import unittest
import os
import sys
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gc_mapper import GCContentMapper

class TestGCContentMapper(unittest.TestCase):

    def setUp(self):
        # Mock sequence of 100 bp
        # 0-39: all A/T -> GC = 0
        # 40-79: all G -> GC = 1.0, Skew = 1.0
        # 80-99: all C -> GC = 1.0, Skew = -1.0
        self.mock_fasta = (
            ">test_chromosome\n"
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
            "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG\n"
            "CCCCCCCCCCCCCCCCCCCC\n"
        )
        
        self.db_fd, self.temp_fasta_path = tempfile.mkstemp(suffix=".fasta")
        with open(self.temp_fasta_path, 'w', encoding='utf-8') as f:
            f.write(self.mock_fasta)
            
        self.mapper = GCContentMapper(self.temp_fasta_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_fasta_path):
            os.remove(self.temp_fasta_path)

    def test_fasta_loader(self):
        self.assertEqual(self.mapper.header, "test_chromosome")
        self.assertEqual(len(self.mapper.sequence), 100)

    def test_gc_window_calculations(self):
        # Window size 20, Step 20
        # Window 1 (0-19): all A -> GC Content = 0.0
        # Window 3 (40-59): all G -> GC Content = 1.0, Skew = 1.0
        # Window 5 (80-99): all C -> GC Content = 1.0, Skew = -1.0
        pos, gc, skew = self.mapper.calculate_gc_stats(window_size=20, step_size=20)
        
        self.assertEqual(len(pos), 5)
        # Check positions are centered: window size 20 means first pos is index 10
        self.assertEqual(pos[0], 10)
        
        # Test values
        self.assertAlmostEqual(gc[0], 0.0)
        self.assertAlmostEqual(gc[2], 1.0)
        self.assertAlmostEqual(skew[2], 1.0)
        
        self.assertAlmostEqual(gc[4], 1.0)
        self.assertAlmostEqual(skew[4], -1.0)

if __name__ == "__main__":
    unittest.main()
