"""
Unit Tests for HMM Viterbi Gene Finder
Author: Portfolio Creator
Description: Verify log-space Viterbi lattices, exon boundary coordinate splits, and traceback paths.
Language: English (100%)
"""

import unittest
import os
import sys
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gene_finder import HMMGeneFinder

class TestHMMGeneFinder(unittest.TestCase):

    def setUp(self):
        # Create a mock FASTA file containing:
        # AT-rich flanking regions and a central GC-rich region:
        # ATAT (intron) + GCGGCG (exon) + ATAT (intron)
        self.mock_fasta = (
            ">test_hmm_gene\n"
            "ATATGCGGCGGCGGCGATAT\n"
        )
        
        self.db_fd, self.temp_fasta_path = tempfile.mkstemp(suffix=".fasta")
        os.close(self.db_fd)
        with open(self.temp_fasta_path, 'w', encoding='utf-8') as f:
            f.write(self.mock_fasta)
            
        self.finder = HMMGeneFinder(self.temp_fasta_path)

    def tearDown(self):
        if os.path.exists(self.temp_fasta_path):
            try:
                os.remove(self.temp_fasta_path)
            except PermissionError:
                pass

    def test_fasta_load(self):
        self.assertEqual(self.finder.header, "test_hmm_gene")
        self.assertEqual(self.finder.sequence, "ATATGCGGCGGCGGCGATAT")

    def test_viterbi_decoding(self):
        # Decodes the sequence: expect 'N' for AT-rich, 'E' for GC-rich
        path, log_prob = self.finder.decode_viterbi(self.finder.sequence)
        
        self.assertEqual(len(path), 20)
        # Exon (E) should be decoded in the middle
        self.assertEqual(path[4:16], "EEEEEEEEEEEE")
        self.assertEqual(path[0:4], "NNNN")
        self.assertEqual(path[16:20], "NNNN")
        self.assertTrue(log_prob < 0.0)  # Log probabilities of sequences are negative

    def test_exon_parsing(self):
        # Decoded path containing exons: "NNNNNNNEEEENNNNNNEEEEE"
        path = "NNNNNNNEEEENNNNNNEEEEE"
        exons = self.finder.parse_exons(path)
        
        self.assertEqual(len(exons), 2)
        # Exon 1: index 7 to 11
        self.assertEqual(exons[0], (7, 11))
        # Exon 2: index 17 to 22 (runs to end)
        self.assertEqual(exons[1], (17, 22))

if __name__ == "__main__":
    unittest.main()
