"""
Unit Tests for VCF QC Filter
Author: Portfolio Creator
Description: Verify VCF parsed values, quality filter parameters, and Ti/Tv ratios.
Language: English (100%)
"""

import unittest
import os
import sys
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vcf_filter import VCFGenotypeFilter

class TestVCFGenotypeFilter(unittest.TestCase):

    def setUp(self):
        # Create a mock VCF with headers and 4 variants
        # Var 1: Transition (A->G), PASS QUAL=50, GQ=30, DP=15
        # Var 2: Transversion (T->G), PASS QUAL=40, GQ=25, DP=22
        # Var 3: Transition (C->T), PASS QUAL=55, GQ=28, DP=12
        # Var 4: Low depth filter candidate, QUAL=10, GQ=8, DP=4
        self.mock_vcf = (
            "##fileformat=VCFv4.2\n"
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n"
            "chr1\t1001\trs1\tA\tG\t50.0\tPASS\tDP=15\tGT:GQ:DP\t0/1:30:15\n"
            "chr1\t1002\trs2\tT\tG\t40.0\tPASS\tDP=22\tGT:GQ:DP\t0/1:25:22\n"
            "chr1\t1003\trs3\tC\tT\t55.0\tPASS\tDP=12\tGT:GQ:DP\t0/1:28:12\n"
            "chr1\t1004\trs4\tG\tA\t10.0\tPASS\tDP=4\tGT:GQ:DP\t0/1:8:4\n"
        )
        
        self.db_fd, self.temp_vcf_path = tempfile.mkstemp(suffix=".vcf")
        with open(self.temp_vcf_path, 'w', encoding='utf-8') as f:
            f.write(self.mock_vcf)
            
        self.filter = VCFGenotypeFilter(self.temp_vcf_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_vcf_path):
            os.remove(self.temp_vcf_path)

    def test_vcf_parsing(self):
        self.assertEqual(len(self.filter.variants), 4)
        
        # Verify first variant parsed fields
        v1 = self.filter.variants[0]
        self.assertEqual(v1["ref"], "A")
        self.assertEqual(v1["alt"], "G")
        self.assertEqual(v1["qual"], 50.0)
        self.assertEqual(v1["gq"], 30)
        self.assertEqual(v1["dp"], 15)

    def test_variant_filtering(self):
        # Filter with min_qual=30, min_gq=20, min_dp=10
        # Var 1, 2, 3 should pass. Var 4 should fail (GQ=8, DP=4)
        filtered = self.filter.filter_variants(min_qual=30, min_gq=20, min_dp=10)
        self.assertEqual(len(filtered), 3)

    def test_titv_ratio(self):
        # Filter first, get Var 1, 2, 3
        # Var 1: A->G (Transition)
        # Var 2: T->G (Transversion)
        # Var 3: C->T (Transition)
        # Transitions = 2, Transversions = 1 -> Ti/Tv = 2.0
        filtered = self.filter.filter_variants(min_qual=30, min_gq=20, min_dp=10)
        ratio = self.filter.calculate_titv_ratio(filtered)
        self.assertAlmostEqual(ratio, 2.0)

if __name__ == "__main__":
    unittest.main()
