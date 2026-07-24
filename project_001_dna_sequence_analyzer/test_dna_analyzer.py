"""
Unit Tests for DNA Sequence Analyzer
Author: Portfolio Creator
Description: Test suite for verifying DNASequence methods and FASTA parsing logic.
Language: English (100%)
"""

import unittest
import os
import sys
import tempfile

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dna_analyzer import DNASequence, parse_fasta

class TestDNASequence(unittest.TestCase):
    
    def setUp(self):
        # A simple DNA sequence: length 15
        # Nucleotides: A:4, C:3, G:4, T:4
        # GC Content: (3+4)/15 = 46.667%
        self.seq_str = "ATGCTAGCGGTCATA"
        self.header = "Test Gene"
        self.dna = DNASequence(self.seq_str, self.header)

    def test_validation_and_cleaning(self):
        # Test lowercase conversion
        dna_lower = DNASequence("atgctagcggtcata")
        self.assertEqual(dna_lower.sequence, "ATGCTAGCGGTCATA")

        # Test whitespaces and newlines removal
        dna_spaces = DNASequence(" ATG\nCTA GCG\tGTC ATA ")
        self.assertEqual(dna_spaces.sequence, "ATGCTAGCGGTCATA")

        # Test validation of invalid characters
        with self.assertRaises(ValueError):
            DNASequence("ATGCTAGCGGTCATAX")  # 'X' is invalid
            
        with self.assertRaises(ValueError):
            DNASequence("ATG123")  # digits are invalid

    def test_get_length(self):
        self.assertEqual(self.dna.get_length(), 15)

    def test_nucleotide_frequencies(self):
        freqs = self.dna.nucleotide_frequencies()
        self.assertEqual(freqs['A']['count'], 4)
        self.assertEqual(freqs['C']['count'], 3)
        self.assertEqual(freqs['G']['count'], 4)
        self.assertEqual(freqs['T']['count'], 4)
        self.assertEqual(freqs['N']['count'], 0)
        
        # Check percentage
        self.assertAlmostEqual(freqs['A']['percentage'], (4/15)*100)

    def test_gc_content(self):
        # GC = 7 bases out of 15 = 46.667%
        self.assertAlmostEqual(self.dna.gc_content(), (7/15)*100)

    def test_transcribe(self):
        # DNA -> RNA
        self.assertEqual(self.dna.transcribe(), "AUGCUAGCGGUCAUA")

    def test_translate(self):
        # Codons:
        # ATG -> M
        # CTA -> L
        # GCG -> A
        # GTC -> V
        # ATA -> I
        # Total Protein: MLAVI
        self.assertEqual(self.dna.translate(), "MLAVI")

    def test_find_motifs(self):
        # Sequence: ATGCTAGCGGTCATA
        # Motifs:
        # 'CG' at index 7 (ATGCTA[CG]GTCATA)
        self.assertEqual(self.dna.find_motifs("CG"), [7])
        
        # 'TA' at index 5 (ATGCT[TA]GCGGTCATA) and 13 (ATGCTAGCGGTC[TA]A)
        # Wait: Index of 'TA' in ATGCTAGCGGTCATA
        # 0:A 1:T 2:G 3:C 4:T 5:A -> 'TA' starts at index 4 (T at 4, A at 5) - Wait!
        # Let's count indices:
        # A T G C T A G C G G T C A T A
        # 0 1 2 3 4 5 6 7 8 9 1011121314
        # 'TA' is at index 4: "TA" (T is 4, A is 5)
        # 'TA' is at index 12: "TA" (T is 13, A is 14) -> wait, index 12 is 'A', 13 is 'T', 14 is 'A'.
        # Let's check:
        # seq[4:6] = "TA"
        # seq[13:15] = "TA" (Wait, seq[12] is 'A', seq[13] is 'T', seq[14] is 'A' -> "ATA" -> "TA" starts at 13).
        # Let's check indices of 'TA':
        # indices are 4 and 13.
        self.assertEqual(self.dna.find_motifs("TA"), [4, 13])

        # Non-existent motif
        self.assertEqual(self.dna.find_motifs("GGGG"), [])

    def test_sliding_window_gc(self):
        # Test short sequence logic
        pos, gc = self.dna.sliding_window_gc(window_size=20)
        # Length is 15, so it should return midpoint and overall GC
        self.assertEqual(pos, [7])
        self.assertAlmostEqual(gc[0], (7/15)*100)

        # Test sliding window on a simple repeat
        repeat_dna = DNASequence("GCGCGCGCGC") # length 10
        pos, gc = repeat_dna.sliding_window_gc(window_size=4, step_size=2)
        # Windows:
        # 0..3: GCGC -> 100% GC
        # 2..5: GCGC -> 100% GC
        # 4..7: GCGC -> 100% GC
        # 6..9: GCGC -> 100% GC
        # Midpoints: 2, 4, 6, 8
        self.assertEqual(pos, [2, 4, 6, 8])
        self.assertEqual(gc, [100.0, 100.0, 100.0, 100.0])


class TestFASTAUtility(unittest.TestCase):
    
    def test_parse_fasta(self):
        fasta_content = (
            ">Seq1 Gene A\n"
            "ATGCTAGCGGTCATA\n"
            ">Seq2 Gene B\n"
            "GGCC\nTTAA\n"
        )
        
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file.write(fasta_content)
            temp_path = temp_file.name

        try:
            sequences = parse_fasta(temp_path)
            self.assertEqual(len(sequences), 2)
            
            self.assertEqual(sequences[0].header, "Seq1 Gene A")
            self.assertEqual(sequences[0].sequence, "ATGCTAGCGGTCATA")
            
            self.assertEqual(sequences[1].header, "Seq2 Gene B")
            self.assertEqual(sequences[1].sequence, "GGCCTTAA")
        finally:
            os.remove(temp_path)

if __name__ == "__main__":
    unittest.main()
