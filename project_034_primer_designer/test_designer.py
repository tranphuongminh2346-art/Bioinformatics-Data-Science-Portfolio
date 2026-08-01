"""
Unit Tests for PCR Primer Designer
Author: Portfolio Creator
Description: Verify Wallace Tm calculations, reverse complements, and hairpin checks.
Language: English (100%)
"""

import unittest
import os
import sys
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from primer_designer import PrimerDesigner

class TestPrimerDesigner(unittest.TestCase):

    def setUp(self):
        # Create a mock FASTA template of 120 bp
        self.mock_fasta = (
            ">test_template\n"
            "ATGCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATC\n"
            "GCATGCATGCATGCATGCATGCATGCATGCATGCATGCAT\n"
        )
        
        self.db_fd, self.temp_fasta_path = tempfile.mkstemp(suffix=".fasta")
        with open(self.temp_fasta_path, 'w', encoding='utf-8') as f:
            f.write(self.mock_fasta)
            
        self.designer = PrimerDesigner(self.temp_fasta_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_fasta_path):
            os.remove(self.temp_fasta_path)

    def test_fasta_load(self):
        self.assertEqual(self.designer.header, "test_template")
        self.assertEqual(len(self.designer.sequence), 112)

    def test_reverse_complement(self):
        seq = "ATGC"
        rev_comp = self.designer.get_reverse_complement(seq)
        # Complement of A, T, G, C -> T, A, C, G. Reversed -> G C A T
        self.assertEqual(rev_comp, "GCAT")

    def test_wallace_tm_calculation(self):
        # Primer = "AAAAAAGGGGGG" (6 A, 6 G)
        # Tm = 2 * (6 + 0) + 4 * (0 + 6) = 12 + 24 = 36.0
        primer = "AAAAAAGGGGGG"
        tm = self.designer.calculate_tm(primer)
        self.assertEqual(tm, 36.0)

    def test_gc_content(self):
        primer = "ATGCATGC"
        gc = self.designer.calculate_gc(primer)
        # 4 out of 8 bases are G/C -> 50% = 0.5
        self.assertEqual(gc, 0.5)

    def test_hairpin_detection(self):
        # Primer with no self-complementarity
        safe_primer = "AAAAAAAAAAGGGGGGGGGG"
        self.assertFalse(self.designer.has_hairpin(safe_primer, max_complementarity=10))
        
        # Primer with direct self-complementarity at ends: e.g. "ATGC...GCAT"
        # Reverse complement of ATGCGCAT is ATGCGCAT itself!
        hairpin_primer = "ATGCGCAT"
        self.assertTrue(self.designer.has_hairpin(hairpin_primer, max_complementarity=4))

if __name__ == "__main__":
    unittest.main()
