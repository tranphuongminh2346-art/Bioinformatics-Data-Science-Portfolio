"""
Unit Tests for DNA ORF Finder
Author: Portfolio Creator
Description: Verify codon translations, reverse complements, and 6-frame coordinate mappings.
Language: English (100%)
"""

import unittest
import os
import sys
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orf_finder import ORFFinder

class TestORFFinder(unittest.TestCase):

    def setUp(self):
        # Create a mock FASTA sequence containing:
        # Sense: GCT + ATG + CCG + AAA + TAA + GCG (18 bp)
        # ORF: ATG CCG AAA TAA -> translates to "MPK" (9 bp sequence, 3 codons)
        self.mock_fasta = (
            ">test_orf_gene\n"
            "GCTATGCCGAAATAAGCG\n"
        )
        
        self.db_fd, self.temp_fasta_path = tempfile.mkstemp(suffix=".fasta")
        with open(self.temp_fasta_path, 'w', encoding='utf-8') as f:
            f.write(self.mock_fasta)
            
        self.finder = ORFFinder(self.temp_fasta_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_fasta_path):
            os.remove(self.temp_fasta_path)

    def test_fasta_loading(self):
        self.assertEqual(self.finder.header, "test_orf_gene")
        self.assertEqual(self.finder.sequence, "GCTATGCCGAAATAAGCG")

    def test_reverse_complement(self):
        # Complement of "GCTATGCCGAAATAAGCG" -> "CGATACGGCTTTATTCGC", reversed -> "CGACTTATTCGGCATAGC"
        rev_comp = self.finder.get_reverse_complement()
        self.assertEqual(rev_comp, "CGCTTATTTCGGCATAGC")

    def test_dna_translation(self):
        # "ATGCCGAAATAA" -> "MPK*" (* is stop codon, excluded in translation)
        translation = self.finder.translate_dna("ATGCCGAAATAA")
        self.assertEqual(translation, "MPK")

    def test_orf_scanning_forward(self):
        # Scan with min_len_bp = 10 (our mock ORF is 12 bp: ATGCCGAAATAA)
        orfs = self.finder.find_all_orfs(min_len_bp=10)
        
        self.assertEqual(len(orfs), 1)
        orf = orfs[0]
        self.assertEqual(orf["strand"], "FORWARD")
        self.assertEqual(orf["start"], 3)
        self.assertEqual(orf["end"], 15)
        self.assertEqual(orf["dna_sequence"], "ATGCCGAAATAA")
        self.assertEqual(orf["translation"], "MPK")

if __name__ == "__main__":
    unittest.main()
