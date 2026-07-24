"""
Unit Tests for Protein Structure Coordinate Analyzer
Author: Portfolio Creator
Description: Test suite for verifying PDB file parsing and geometric distance math.
Language: English (100%)
"""

import unittest
import os
import sys
import tempfile
import numpy as np

# Add directory containing this file to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pdb_analyzer import PDBParser

class TestPDBParser(unittest.TestCase):

    def setUp(self):
        # Mock PDB coordinate content
        # Res 1 (ALA) and Res 2 (GLY)
        # Residue 1: N, CA, C, O
        # Residue 2: N, CA, C, O
        self.pdb_content = (
            "HEADER    TEST PROTEIN                            14-JUL-26   1XXX\n"
            "ATOM      1  N   ALA A   1       0.000   0.000   0.000  1.00 10.00           N\n"
            "ATOM      2  CA  ALA A   1       1.000   0.000   0.000  1.00 10.00           C\n"
            "ATOM      3  C   ALA A   1       1.000   1.000   0.000  1.00 10.00           C\n"
            "ATOM      4  O   ALA A   1       1.000   1.000   1.000  1.00 10.00           O\n"
            "ATOM      5  N   GLY A   2       2.000   2.000   0.000  1.00 10.00           N\n"
            "ATOM      6  CA  GLY A   2       2.000   2.000   2.000  1.00 10.00           C\n"
            "ATOM      7  C   GLY A   2       3.000   2.000   2.000  1.00 10.00           C\n"
            "ATOM      8  O   GLY A   2       3.000   3.000   2.000  1.00 10.00           O\n"
        )
        
        self.db_fd, self.temp_pdb_path = tempfile.mkstemp(suffix=".pdb")
        with open(self.temp_pdb_path, 'w', encoding='utf-8') as f:
            f.write(self.pdb_content)
        
        self.parser = PDBParser(self.temp_pdb_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_pdb_path):
            os.remove(self.temp_pdb_path)

    def test_parsing(self):
        # 8 ATOM records should be loaded
        self.assertEqual(len(self.parser.atoms), 8)
        
        # Test first atom properties
        first_atom = self.parser.atoms[0]
        self.assertEqual(first_atom["name"], "N")
        self.assertEqual(first_atom["res_name"], "ALA")
        self.assertEqual(first_atom["res_seq"], 1)
        self.assertAlmostEqual(first_atom["x"], 0.0)

    def test_get_ca_atoms(self):
        ca_atoms = self.parser.get_ca_atoms()
        # Should be 2 CA atoms
        self.assertEqual(len(ca_atoms), 2)
        self.assertEqual(ca_atoms[0]["res_name"], "ALA")
        self.assertEqual(ca_atoms[1]["res_name"], "GLY")

    def test_calculate_distance_matrix(self):
        matrix = self.parser.calculate_distance_matrix()
        # CA 1: (1, 0, 0)
        # CA 2: (2, 2, 2)
        # Distance = sqrt((2-1)^2 + (2-0)^2 + (2-0)^2) = sqrt(1 + 4 + 4) = sqrt(9) = 3.0
        self.assertEqual(matrix.shape, (2, 2))
        self.assertAlmostEqual(matrix[0, 1], 3.0)
        self.assertAlmostEqual(matrix[1, 0], 3.0)
        self.assertAlmostEqual(matrix[0, 0], 0.0)

    def test_find_hydrogen_bonds(self):
        # Nitrogens:
        # Atom 1: ALA 1 N at (0,0,0)
        # Atom 5: GLY 2 N at (2,2,0)
        # Oxygens:
        # Atom 4: ALA 1 O at (1,1,1)
        # Atom 8: GLY 2 O at (3,3,2)
        
        # Distance ALA 1 O <--> GLY 2 N:
        # O: (1,1,1), N: (2,2,0)
        # Dist = sqrt(1^2 + 1^2 + (-1)^2) = sqrt(3) = 1.732 Å (Too close, out of range 2.5-3.5)
        
        # Distance ALA 1 N <--> GLY 2 O:
        # N: (0,0,0), O: (3,3,2)
        # Dist = sqrt(3^2 + 3^2 + 2^2) = sqrt(9+9+4) = sqrt(22) = 4.69 Å (Too far)
        
        # Let's verify no bonds in current default setup
        h_bonds = self.parser.find_hydrogen_bonds(min_dist=1.5, max_dist=2.0)
        self.assertEqual(len(h_bonds), 1)
        self.assertEqual(h_bonds[0]["donor"], "GLY2_N")
        self.assertEqual(h_bonds[0]["acceptor"], "ALA1_O")
        self.assertAlmostEqual(h_bonds[0]["distance"], np.sqrt(3))

if __name__ == "__main__":
    unittest.main()
