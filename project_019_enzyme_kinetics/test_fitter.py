"""
Unit Tests for Enzyme Kinetics Fitter
Author: Portfolio Creator
Description: Verify parameter fits, Michaelis-Menten functions, and double reciprocals.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enzyme_fitter import EnzymeKineticsFitter, michaelis_menten

class TestEnzymeKineticsFitter(unittest.TestCase):

    def setUp(self):
        # Create a mock kinetics dataset with exact MM relation (Vmax = 10, Km = 2)
        # S: 1, 2, 4, 8
        # V: 10*1/3 = 3.333, 10*2/4 = 5.0, 10*4/6 = 6.667, 10*8/10 = 8.0
        self.mock_data = pd.DataFrame({
            "substrate_concentration": [1.0, 2.0, 4.0, 8.0],
            "velocity": [3.3333, 5.0, 6.6667, 8.0]
        })
        
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        self.mock_data.to_csv(self.temp_csv_path, index=False)
        self.fitter = EnzymeKineticsFitter(self.temp_csv_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_csv_path):
            os.remove(self.temp_csv_path)

    def test_michaelis_menten_math(self):
        # Test function directly
        v = michaelis_menten(2.0, 10.0, 2.0)
        self.assertAlmostEqual(v, 5.0)

    def test_parameter_fitting(self):
        vmax, km = self.fitter.fit_parameters()
        
        # Check fitted values are close to our target parameters (Vmax = 10, Km = 2)
        self.assertAlmostEqual(vmax, 10.0, places=3)
        self.assertAlmostEqual(km, 2.0, places=3)

    def test_reciprocal_transformations(self):
        lb = self.fitter.get_lineweaver_burk()
        
        # S = 1 -> 1/S = 1.0
        # S = 2 -> 1/S = 0.5
        # v = 5.0 -> 1/v = 0.2
        self.assertAlmostEqual(lb['reciprocal_s'].iloc[0], 1.0)
        self.assertAlmostEqual(lb['reciprocal_s'].iloc[1], 0.5)
        self.assertAlmostEqual(lb['reciprocal_v'].iloc[1], 0.2)

if __name__ == "__main__":
    unittest.main()
