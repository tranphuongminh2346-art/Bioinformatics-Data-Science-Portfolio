"""
Unit Tests for Conway Simulator
Author: Portfolio Creator
Description: Verify neighbor counts, stable block patterns, and blinker oscillators.
Language: English (100%)
"""

import unittest
import os
import sys
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from conway_simulator import ConwaySimulator

class TestConwaySimulator(unittest.TestCase):

    def setUp(self):
        # Setup a small 10x10 grid
        self.sim = ConwaySimulator(rows=10, cols=10)

    def test_neighbor_counting(self):
        # Set 3 active cells next to each other
        self.sim.grid[1, 1] = 1
        self.sim.grid[1, 2] = 1
        self.sim.grid[1, 3] = 1
        
        neighbors = self.sim.count_neighbors()
        
        # Center cell (1, 2) has 2 neighbors
        self.assertEqual(neighbors[1, 2], 2)
        # Top-middle cell (0, 2) has 3 neighbors
        self.assertEqual(neighbors[0, 2], 3)
        # Far cell (5, 5) has 0 neighbors
        self.assertEqual(neighbors[5, 5], 0)

    def test_stable_block_pattern(self):
        # Block is 2x2 static stable structure
        self.sim.set_pattern("block", start_row=3, start_col=3)
        
        # Verify initial
        self.assertEqual(self.sim.grid[3, 3], 1)
        self.assertEqual(self.sim.grid[3, 4], 1)
        
        # Step generation
        self.sim.step_generation()
        
        # Should remain exactly identical
        self.assertEqual(self.sim.grid[3, 3], 1)
        self.assertEqual(self.sim.grid[3, 4], 1)
        self.assertEqual(self.sim.grid[4, 3], 1)
        self.assertEqual(self.sim.grid[4, 4], 1)
        # Rest should be 0
        self.assertEqual(self.sim.grid.sum(), 4)

    def test_blinker_oscillator_pattern(self):
        # Blinker is vertical 3-cell line at start
        # Coordinates: (3, 3), (4, 3), (5, 3)
        self.sim.set_pattern("blinker", start_row=3, start_col=3)
        
        self.assertEqual(self.sim.grid[3, 3], 1)
        self.assertEqual(self.sim.grid[4, 3], 1)
        self.assertEqual(self.sim.grid[5, 3], 1)
        self.assertEqual(self.sim.grid.sum(), 3)
        
        # Step 1: should rotate to horizontal: (4, 2), (4, 3), (4, 4)
        self.sim.step_generation()
        self.assertEqual(self.sim.grid[4, 2], 1)
        self.assertEqual(self.sim.grid[4, 3], 1)
        self.assertEqual(self.sim.grid[4, 4], 1)
        self.assertEqual(self.sim.grid.sum(), 3)
        
        # Step 2: should rotate back to vertical
        self.sim.step_generation()
        self.assertEqual(self.sim.grid[3, 3], 1)
        self.assertEqual(self.sim.grid[4, 3], 1)
        self.assertEqual(self.sim.grid[5, 3], 1)

if __name__ == "__main__":
    unittest.main()
