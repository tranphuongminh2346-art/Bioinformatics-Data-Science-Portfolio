"""
Unit Tests for Titration Simulator
Author: Portfolio Creator
Description: Verify equivalence points, buffer region pH, and excess base pH equations.
Language: English (100%)
"""

import unittest
import os
import sys
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from titration import PHTitrator

class TestPHTitrator(unittest.TestCase):

    def setUp(self):
        # Weak acid Ca = 0.1 M, Va = 50 mL, pKa = 4.76 (Acetic acid)
        # Strong base Cb = 0.1 M
        # Equivalence volume V_eq = (0.1 * 50) / 0.1 = 50.0 mL
        self.titrator = PHTitrator(c_acid=0.1, v_acid=50.0, pka=4.76, c_base=0.1)

    def test_equivalence_volume(self):
        self.assertEqual(self.titrator.v_eq, 50.0)

    def test_initial_ph(self):
        # [H+] = sqrt(Ka * Ca) = sqrt(10^-4.76 * 10^-1) = sqrt(10^-5.76) = 10^-2.88
        # pH = 2.88
        ph = self.titrator.calculate_ph_at_volume(0.0)
        self.assertAlmostEqual(ph, 2.88, places=2)

    def test_buffer_region_ph(self):
        # Half equivalence point: V_b = 25 mL
        # Henderson-Hasselbalch: pH = pKa + log10([A-] / [HA])
        # [A-] = [HA] -> ratio = 1.0 -> log10(1) = 0.0 -> pH = pKa = 4.76
        ph_half = self.titrator.calculate_ph_at_volume(25.0)
        self.assertAlmostEqual(ph_half, 4.76, places=2)

    def test_equivalence_point_ph(self):
        # pH at equivalence should be basic (> 7.0) due to weak acid salt conjugate base hydrolysis
        ph_eq = self.titrator.calculate_ph_at_volume(50.0)
        self.assertTrue(ph_eq > 7.0)
        # For acetic acid 0.1M titrated with NaOH 0.1M, V_eq = 50mL.
        # C_salt = (0.1 * 50) / 100 = 0.05 M.
        # Kb = 1e-14 / 1.738e-5 = 5.75e-10.
        # [OH-] = sqrt(5.75e-10 * 0.05) = sqrt(2.87e-11) = 5.36e-6.
        # poh = -log10(5.36e-6) = 5.27 -> pH = 14 - 5.27 = 8.73.
        self.assertAlmostEqual(ph_eq, 8.73, places=2)

    def test_excess_base_ph(self):
        # V_added = 100 mL (excess base)
        # Excess moles base = 0.1 * (100 - 50) = 5.0 mmol
        # Total volume = 50 (acid) + 100 (added base) = 150 mL
        # [OH-] = 5.0 / 150 = 0.0333 M
        # poh = -log10(0.0333) = 1.48 -> pH = 14 - 1.48 = 12.52
        ph_excess = self.titrator.calculate_ph_at_volume(100.0)
        self.assertAlmostEqual(ph_excess, 12.52, places=2)

if __name__ == "__main__":
    unittest.main()
