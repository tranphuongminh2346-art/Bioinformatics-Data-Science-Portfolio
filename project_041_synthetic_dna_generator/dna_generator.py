"""
Markov Chain DNA Sequence Generator
Author: Portfolio Creator
Description: Simulates synthetic DNA sequences matching a transition probability matrix,
             modeling background genomes and CpG island hotspots.
Language: English (100%)
"""

import numpy as np

class MarkovDNAGenerator:
    """Generates synthetic DNA sequences using first-order Markov chain transitions."""
    
    def __init__(self, seed: int = 42):
        self.bases = ['A', 'C', 'G', 'T']
        self.base_to_idx = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
        np.random.seed(seed)
        
        # 1. Uniform background model transition probabilities
        self.uniform_transition = np.array([
            [0.25, 0.25, 0.25, 0.25],  # A -> A, C, G, T
            [0.25, 0.25, 0.25, 0.25],  # C ->
            [0.25, 0.25, 0.25, 0.25],  # G ->
            [0.25, 0.25, 0.25, 0.25]   # T ->
        ])
        
        # 2. CpG Island model transition probabilities (elevated C -> G transition)
        self.cpg_transition = np.array([
            [0.18, 0.27, 0.37, 0.18],  # A -> A, C, G, T
            [0.16, 0.34, 0.38, 0.12],  # C -> (High C -> G: 0.38)
            [0.15, 0.35, 0.35, 0.15],  # G ->
            [0.09, 0.38, 0.38, 0.15]   # T ->
        ])

    def generate_sequence(self, length: int, model_type: str = "uniform") -> str:
        """
        Generates a synthetic DNA sequence of target length.
        
        Returns:
            str: DNA sequence string.
        """
        if length <= 0:
            return ""
            
        trans_matrix = self.cpg_transition if model_type == "cpg" else self.uniform_transition
        
        # Choose first base uniformly
        seq = [np.random.choice(self.bases)]
        
        for _ in range(length - 1):
            curr_base = seq[-1]
            curr_idx = self.base_to_idx[curr_base]
            # Transition distribution
            probs = trans_matrix[curr_idx]
            next_base = np.random.choice(self.bases, p=probs)
            seq.append(next_base)
            
        return "".join(seq)

    def calculate_transition_frequencies(self, seq: str) -> np.ndarray:
        """
        Analyzes a DNA sequence and calculates the empirical transition frequency matrix.
        
        Returns:
            np.ndarray: 4 x 4 matrix of transition frequencies.
        """
        freqs = np.zeros((4, 4))
        for i in range(len(seq) - 1):
            b1 = seq[i]
            b2 = seq[i+1]
            if b1 in self.base_to_idx and b2 in self.base_to_idx:
                freqs[self.base_to_idx[b1], self.base_to_idx[b2]] += 1
                
        # Normalize rows to sum to 1.0 (if row sum > 0)
        row_sums = freqs.sum(axis=1, keepdims=True)
        # Avoid division by zero
        row_sums[row_sums == 0] = 1.0
        normalized = freqs / row_sums
        return normalized
