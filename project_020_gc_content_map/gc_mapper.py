"""
Genomic GC-Content & Skew Mapper
Author: Portfolio Creator
Description: Parses genomic FASTA sequences, computes GC ratios and GC skew
             in sliding windows, and generates chromosomal maps.
Language: English (100%)
"""

import os
import numpy as np
import matplotlib.pyplot as plt

class GCContentMapper:
    """Computes sliding window statistics on genomic fasta sequences."""
    
    def __init__(self, fasta_path: str):
        self.fasta_path = fasta_path
        self.header = ""
        self.sequence = ""
        self.load_fasta()

    def load_fasta(self):
        """Reads a single FASTA sequence entry from disk."""
        if not os.path.exists(self.fasta_path):
            raise FileNotFoundError(f"FASTA file not found: {self.fasta_path}")
            
        lines = []
        with open(self.fasta_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith(">"):
                    self.header = line[1:]
                else:
                    lines.append(line.upper())
                    
        self.sequence = "".join(lines)

    def calculate_gc_stats(self, window_size: int = 50, step_size: int = 10) -> tuple:
        """
        Computes GC Content and GC Skew in sliding windows.
        
        Formula:
          GC Content = (G + C) / (A + T + G + C)
          GC Skew = (G - C) / (G + C)
          
        Returns:
          tuple: (positions: list, gc_content: list, gc_skew: list)
        """
        positions = []
        gc_content = []
        gc_skew = []
        
        n = len(self.sequence)
        
        for i in range(0, n - window_size + 1, step_size):
            window = self.sequence[i : i + window_size]
            
            # Count bases
            g_count = window.count('G')
            c_count = window.count('C')
            a_count = window.count('A')
            t_count = window.count('T')
            
            total_bases = a_count + t_count + g_count + c_count
            
            if total_bases == 0:
                gc_ratio = 0.0
            else:
                gc_ratio = (g_count + c_count) / total_bases
                
            if g_count + c_count == 0:
                skew = 0.0
            else:
                skew = (g_count - c_count) / (g_count + c_count)
                
            positions.append(i + window_size // 2)
            gc_content.append(gc_ratio)
            gc_skew.append(skew)
            
        return positions, gc_content, gc_skew

    def plot_map(self, positions: list, gc_content: list, gc_skew: list, output_path: str):
        """Generates line charts showing GC profiles along coordinates."""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
        
        # 1. GC Content Plot
        ax1.plot(positions, gc_content, color='#0284c7', lw=1.8, label='GC Content')
        # Draw threshold marker for typical genome GC (~50%)
        ax1.axhline(0.5, color='#475569', linestyle=':', alpha=0.8, label='50% Threshold')
        ax1.set_ylabel("GC Ratio", fontsize=10)
        ax1.set_title(f"Genomic Landscape Map - Sequence: {self.header}", fontsize=12, fontweight='bold')
        ax1.grid(True, linestyle=':', alpha=0.5)
        ax1.legend(loc='upper right')
        
        # Highlight regions of GC island
        ax1.fill_between(positions, 0.5, gc_content, where=(np.array(gc_content) >= 0.5),
                         color='#10b981', alpha=0.3, label='GC Rich Islands')
        
        # 2. GC Skew Plot
        ax2.plot(positions, gc_skew, color='#f97316', lw=1.8, label='GC Skew')
        ax2.axhline(0.0, color='#475569', linestyle=':', alpha=0.8)
        ax2.set_xlabel("Genomic Position (bp)", fontsize=10)
        ax2.set_ylabel("GC Skew (G-C)/(G+C)", fontsize=10)
        ax2.grid(True, linestyle=':', alpha=0.5)
        ax2.legend(loc='upper right')
        
        # Color coding positive vs negative skew
        ax2.fill_between(positions, 0, gc_skew, where=(np.array(gc_skew) >= 0),
                         color='#10b981', alpha=0.2)
        ax2.fill_between(positions, 0, gc_skew, where=(np.array(gc_skew) < 0),
                         color='#ef4444', alpha=0.2)
                         
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
