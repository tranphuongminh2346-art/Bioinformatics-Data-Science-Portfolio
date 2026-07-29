"""
Unit Tests for DNA Motif Finder
Author: Portfolio Creator
Description: Verify PWM profile matrix calculations, consensus scoring, and Gibbs search loops.
Language: English (100%)
"""

import unittest
import os
import sys
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from motif_finder import GibbsMotifFinder

class TestGibbsMotifFinder(unittest.TestCase):

    def setUp(self):
        # Create a mock FASTA sequence dataset
        # 3 sequences, each containing "TATAAA" (length 6) at different locations
        self.mock_fasta = (
            ">seq1\n"
            "ATGCTATAAAGCA\n"
            ">seq2\n"
            "CCGTTATAAACCG\n"
            ">seq3\n"
            "ACGTATAAAGCGA\n"
        )
        
        self.db_fd, self.temp_fasta_path = tempfile.mkstemp(suffix=".fasta")
        with open(self.temp_fasta_path, 'w', encoding='utf-8') as f:
            f.write(self.mock_fasta)
            
        self.finder = GibbsMotifFinder(self.temp_fasta_path, motif_len=6)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_fasta_path):
            os.remove(self.temp_fasta_path)

    def test_fasta_loading(self):
        self.assertEqual(len(self.finder.sequences), 3)
        self.assertEqual(self.finder.sequences[0], "ATGCTATAAAGCA")

    def test_profile_matrix(self):
        # Construct profile from two identical motifs: "AAAAAA", "AAAAAA"
        profile = self.finder.build_profile(["AAAAAA", "AAAAAA"])
        
        # Row 0 is 'A'.
        # Total counts at each col = 2 (instances) + 1 (pseudocount) = 3
        # Divided by column sum = 2 + 4 = 6
        # A profile value should be 3/6 = 0.5
        # C, G, T should be 1/6 = 0.1667
        for col in range(6):
            self.assertAlmostEqual(profile[0, col], 0.5)
            self.assertAlmostEqual(profile[1, col], 1.0/6.0)

    def test_consensus_logic(self):
        motifs = ["TATAAA", "TATAAA", "CATAAA"]
        consensus = self.finder.get_consensus(motifs)
        self.assertEqual(consensus, "TATAAA")

    def test_gibbs_sampling_search(self):
        # Gibbs sampler run
        motifs, consensus = self.finder.find_motifs(iterations=30, seed=42)
        
        # Verify motifs count matches sequences count
        self.assertEqual(len(motifs), 3)
        # Verify consensus is close to "TATAAA" (due to heuristics, matches subset)
        self.assertIn(consensus, ["TATAAA", "TAAAGC", "ATAAAG"])

if __name__ == "__main__":
    unittest.main()
