"""
Unit Tests for Genomic Variant Predictor
Author: Portfolio Creator
Description: Test suite for verifying VCF parsing, translation consequences, and pathogenicity.
Language: English (100%)
"""

import unittest
import os
import sys
import tempfile

# Add directory containing this file to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from variant_predictor import VariantPredictor

class TestVariantPredictor(unittest.TestCase):

    def setUp(self):
        # Reference sequence: ATG (M), CTA (L)
        self.ref_seq = "ATGCTA"
        self.coding_start_pos = 1000
        self.predictor = VariantPredictor(self.ref_seq, self.coding_start_pos)

    def test_vcf_parsing(self):
        vcf_content = (
            "##fileformat=VCFv4.2\n"
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n"
            "chr1\t1001\trs123\tT\tG\t100\tPASS\tDP=30;AF=0.01;GENE=TEST\n"
        )
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".vcf") as temp_file:
            temp_file.write(vcf_content)
            temp_path = temp_file.name

        try:
            variants = self.predictor.parse_vcf(temp_path)
            self.assertEqual(len(variants), 1)
            self.assertEqual(variants[0]["pos"], 1001)
            self.assertEqual(variants[0]["id"], "rs123")
            self.assertEqual(variants[0]["ref"], "T")
            self.assertEqual(variants[0]["alt"], "G")
            self.assertEqual(variants[0]["info"]["GENE"], "TEST")
            self.assertEqual(variants[0]["info"]["AF"], "0.01")
        finally:
            os.remove(temp_path)

    def test_predict_consequence(self):
        # 1. Test Missense mutation
        # ATG -> AGG (M -> R) at pos 1001 (Index 1 is 'T')
        ref_aa, alt_aa, consequence = self.predictor.predict_consequence(1001, "T", "G")
        self.assertEqual(ref_aa, "M")
        self.assertEqual(alt_aa, "R")
        self.assertEqual(consequence, "Missense")

        # 2. Test Synonymous mutation
        # CTA -> CTT (L -> L) at pos 1005 (Index 5 is 'A')
        ref_aa, alt_aa, consequence = self.predictor.predict_consequence(1005, "A", "T")
        self.assertEqual(ref_aa, "L")
        self.assertEqual(alt_aa, "L")
        self.assertEqual(consequence, "Synonymous")

        # 3. Test Nonsense mutation
        # Let's mock a sequence that can mutate to stop codon
        # TAC -> TAA (Y -> Stop)
        pred_stop = VariantPredictor("TAC", 1000)
        # Pos 1002 (Index 2 is 'C') mutant to 'A'
        ref_aa, alt_aa, consequence = pred_stop.predict_consequence(1002, "C", "A")
        self.assertEqual(ref_aa, "Y")
        self.assertEqual(alt_aa, "_")
        self.assertEqual(consequence, "Nonsense (Stop Gain)")

        # 4. Test Non-Coding Out of Bounds
        ref_aa, alt_aa, consequence = self.predictor.predict_consequence(999, "A", "G")
        self.assertEqual(consequence, "Non-Coding Variant")

        # 5. Test Reference Mismatch
        # Pos 1000 is 'A', let's supply 'G' as ref
        ref_aa, alt_aa, consequence = self.predictor.predict_consequence(1000, "G", "C")
        self.assertEqual(consequence, "Reference Mismatch")

    def test_evaluate_pathogenicity(self):
        # Nonsense -> Likely Pathogenic
        self.assertEqual(
            self.predictor.evaluate_pathogenicity("Nonsense (Stop Gain)", 0.01),
            "Likely Pathogenic"
        )
        
        # Missense & Rare (AF < 0.05) -> VUS
        self.assertEqual(
            self.predictor.evaluate_pathogenicity("Missense", 0.01),
            "Variant of Uncertain Significance (VUS)"
        )
        
        # Missense & Common (AF >= 0.05) -> Likely Benign
        self.assertEqual(
            self.predictor.evaluate_pathogenicity("Missense", 0.10),
            "Likely Benign"
        )
        
        # Synonymous -> Benign
        self.assertEqual(
            self.predictor.evaluate_pathogenicity("Synonymous", 0.01),
            "Benign"
        )

if __name__ == "__main__":
    unittest.main()
