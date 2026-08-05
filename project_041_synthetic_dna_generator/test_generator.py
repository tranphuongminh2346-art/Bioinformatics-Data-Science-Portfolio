"""
Unit Tests for Markov DNA Generator
Author: Portfolio Creator
Description: Verify transition probability rows, sequence lengths, and transition matrix counts.
Language: English (100%)
"""

import unittest
import os
import sys
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dna_generator import MarkovDNAGenerator

class TestMarkovDNAGenerator(unittest.TestCase):

    def setUp(self):
        self.gen = MarkovDNAGenerator(seed=42)

    def test_transition_matrix_sums(self):
        # Rows must sum to 1.0
        np.testing.assert_allclose(self.gen.uniform_transition.sum(axis=1), 1.0)
        np.testing.assert_allclose(self.gen.cpg_transition.sum(axis=1), 1.0)

    def test_sequence_length(self):
        seq_50 = self.gen.generate_sequence(50, model_type="uniform")
        self.assertEqual(len(seq_50), 50)
        
        # Test empty
        self.assertEqual(self.gen.generate_sequence(0), "")

    def test_frequency_calculation(self):
        # Generate 1000 bp CpG sequence to ensure robust statistics
        seq = self.gen.generate_sequence(1000, model_type="cpg")
        freqs = self.gen.calculate_transition_frequencies(seq)
        
        # Verify matrix row sums equal 1.0
        np.testing.assert_allclose(freqs.sum(axis=1), 1.0)
        
        # In CpG model, C to G transition is modeled high (~0.38)
        # Verify C -> G transition is higher than C -> T transition (~0.12)
        idx_c = self.gen.base_to_idx['C']
        idx_g = self.gen.base_to_idx['G']
        idx_t = self.gen.base_to_idx['T']
        
        self.assertTrue(freqs[idx_c, idx_g] > freqs[idx_c, idx_t])

if __name__ == "__main__":
    unittest.main()
