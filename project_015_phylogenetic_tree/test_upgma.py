"""
Unit Tests for UPGMA Phylogenetic Reconstructor
Author: Portfolio Creator
Description: Verify distance matrix, node height math, and Newick string construction.
Language: English (100%)
"""

import unittest
import os
import sys
import tempfile
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from upgma import UPGMATreeReconstructor

class TestUPGMAReconstructor(unittest.TestCase):

    def setUp(self):
        # Create a mock aligned FASTA
        # Seq A: AAAA (0 mismatches to A)
        # Seq B: AAAT (1 mismatch to A -> dist = 0.25)
        # Seq C: GGTT (4 mismatches to A -> dist = 1.0)
        self.mock_fasta = (
            ">SeqA\n"
            "AAAA\n"
            ">SeqB\n"
            "AAAT\n"
            ">SeqC\n"
            "GGTT\n"
        )
        self.db_fd, self.temp_fasta_path = tempfile.mkstemp(suffix=".fasta")
        with open(self.temp_fasta_path, 'w', encoding='utf-8') as f:
            f.write(self.mock_fasta)
            
        self.reconstructor = UPGMATreeReconstructor(self.temp_fasta_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_fasta_path):
            os.remove(self.temp_fasta_path)

    def test_fasta_parsing(self):
        self.assertEqual(len(self.reconstructor.names), 3)
        self.assertEqual(self.reconstructor.sequences[0], "AAAA")
        self.assertEqual(self.reconstructor.sequences[1], "AAAT")

    def test_hamming_distance(self):
        matrix = self.reconstructor.calculate_distance_matrix()
        
        # A vs B has 1 mismatch in 4 bases -> 0.25
        self.assertAlmostEqual(matrix[0, 1], 0.25)
        # A vs C has 4 mismatches in 4 bases -> 1.0
        self.assertAlmostEqual(matrix[0, 2], 1.0)
        # B vs C has 3 mismatches in 4 bases (A->G, A->G, T->T is match) -> 0.75
        self.assertAlmostEqual(matrix[1, 2], 0.75)

    def test_upgma_reconstruction(self):
        root = self.reconstructor.reconstruct()
        
        # Root node should not be a leaf
        self.assertFalse(root.is_leaf())
        
        # Newick formatting check
        newick_str = root.to_newick()
        # SeqA and SeqB should merge first (dist 0.25 -> height 0.125)
        self.assertIn("SeqA:0.1250", newick_str)
        self.assertIn("SeqB:0.1250", newick_str)
        self.assertIn("SeqC", newick_str)

if __name__ == "__main__":
    unittest.main()
