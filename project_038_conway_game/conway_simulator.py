"""
Conway's Game of Life Cellular Automaton
Author: Portfolio Creator
Description: Implements Conway's Game of Life cellular automaton rules,
             simulates grid generations, and saves grid state diagrams.
Language: English (100%)
"""

import numpy as np
import matplotlib.pyplot as plt

class ConwaySimulator:
    """Simulates cellular automata grid cycles based on Conway's rules."""
    
    def __init__(self, rows: int = 30, cols: int = 30):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)

    def set_pattern(self, name: str, start_row: int = 10, start_col: int = 10):
        """Initializes preset structures into the grid."""
        name = name.lower()
        if name == "block":
            # 2x2 static block
            self.grid[start_row:start_row+2, start_col:start_col+2] = 1
        elif name == "beehive":
            # Stable beehive
            self.grid[start_row, start_col+1:start_col+3] = 1
            self.grid[start_row+1, start_col] = 1
            self.grid[start_row+1, start_col+3] = 1
            self.grid[start_row+2, start_col+1:start_col+3] = 1
        elif name == "blinker":
            # 3-cell vertical/horizontal oscillator
            self.grid[start_row:start_row+3, start_col] = 1
        elif name == "glider":
            # Moving glider pattern
            self.grid[start_row, start_col+1] = 1
            self.grid[start_row+1, start_col+2] = 1
            self.grid[start_row+2, start_col:start_col+3] = 1
        else:
            # Default to random grid population
            self.grid = np.random.choice([0, 1], size=(self.rows, self.cols), p=[0.8, 0.2])

    def count_neighbors(self) -> np.ndarray:
        """
        Calculates the sum of active neighbors for each cell in the grid.
        Uses periodic boundary conditions (toroidal wrapping).
        
        Returns:
            np.ndarray: Matrix of active neighbor counts.
        """
        neighbors = np.zeros(self.grid.shape, dtype=int)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                # Shift coordinates wrapping around borders
                shifted = np.roll(np.roll(self.grid, dr, axis=0), dc, axis=1)
                neighbors += shifted
        return neighbors

    def step_generation(self):
        """Applies Conway's Game of Life rules to update grid to next generation."""
        neighbors = self.count_neighbors()
        
        # Conway's Rules:
        # 1. Survival: Cell lives if it has 2 or 3 neighbors
        # 2. Reproduction: Dead cell becomes alive if it has exactly 3 neighbors
        # 3. Underpopulation/Overpopulation: Otherwise, cell dies
        birth = (self.grid == 0) & (neighbors == 3)
        survive = (self.grid == 1) & ((neighbors == 2) | (neighbors == 3))
        
        # Clear grid and apply rules
        self.grid[:] = 0
        self.grid[birth | survive] = 1

    def plot_grid(self, output_path: str, generation: int = 0):
        """Plots the current grid state using binary grid cells."""
        plt.figure(figsize=(7, 7))
        plt.imshow(self.grid, cmap='binary', interpolation='nearest')
        plt.title(f"Conway's Game of Life - Generation {generation}", fontsize=12, fontweight='bold', pad=15)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
