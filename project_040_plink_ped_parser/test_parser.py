"""
Unit Tests for PLINK Pedigree Parser
Author: Portfolio Creator
Description: Verify MAP markers, individual PED parsing, call rates, and Mendelian errors.
Language: English (100%)
"""

import unittest
import os
import sys
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ped_parser import PLINKParser

class TestPLINKParser(unittest.TestCase):

    def setUp(self):
        # Create a mock map file
        self.mock_map = (
            "1\tmarker1\t0.0\t100\n"
            "1\tmarker2\t0.0\t200\n"
        )
        
        # Create a mock ped file:
        # F: A A, C C
        # M: A T, C G
        # C_valid: A A, C C (valid)
        # C_error: T T, C C (Mendelian error at marker1! Father has A A)
        # C_missing: 0 0, C G (should be excluded from Mendelian checks at marker1)
        self.mock_ped = (
            "FAM1\tF1\t0\t0\t1\t1\tA\tA\tC\tC\n"
            "FAM1\tM1\t0\t0\t2\t1\tA\tT\tC\tG\n"
            "FAM1\tC1\tF1\tM1\t1\t2\tA\tA\tC\tC\n"
            "FAM1\tC2\tF1\tM1\t2\t2\tT\tT\tC\tC\n"
            "FAM1\tC3\tF1\tM1\t1\t1\t0\t0\tC\tG\n"
        )
        
        self.map_fd, self.temp_map_path = tempfile.mkstemp(suffix=".map")
        os.close(self.map_fd)
        with open(self.temp_map_path, 'w', encoding='utf-8') as f:
            f.write(self.mock_map)
            
        self.ped_fd, self.temp_ped_path = tempfile.mkstemp(suffix=".ped")
        os.close(self.ped_fd)
        with open(self.temp_ped_path, 'w', encoding='utf-8') as f:
            f.write(self.mock_ped)
            
        self.parser = PLINKParser(self.temp_ped_path, self.temp_map_path)

    def tearDown(self):
        if os.path.exists(self.temp_map_path):
            try:
                os.remove(self.temp_map_path)
            except PermissionError:
                pass
        if os.path.exists(self.temp_ped_path):
            try:
                os.remove(self.temp_ped_path)
            except PermissionError:
                pass

    def test_map_load(self):
        self.assertEqual(len(self.parser.markers), 2)
        self.assertEqual(self.parser.markers[0], "marker1")

    def test_ped_load(self):
        self.assertEqual(len(self.parser.individuals), 5)
        self.assertIn("C1", self.parser.individuals)
        self.assertEqual(self.parser.individuals["C1"]["pat"], "F1")

    def test_call_rates(self):
        rates = self.parser.calculate_call_rates()
        # For marker1, C3 is missing '0 0' -> 4 out of 5 call rate = 80% = 0.8
        self.assertAlmostEqual(rates["marker1"], 0.8)
        # For marker2, no missing values -> 5 out of 5 call rate = 100% = 1.0
        self.assertAlmostEqual(rates["marker2"], 1.0)

    def test_mendelian_errors(self):
        errors = self.parser.check_mendelian_errors()
        
        # Only C2 at marker1 has Mendelian error (T T when parents have A A and A T)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["child_id"], "C2")
        self.assertEqual(errors[0]["marker"], "marker1")
        self.assertEqual(errors[0]["child_gt"], "T/T")

if __name__ == "__main__":
    unittest.main()
