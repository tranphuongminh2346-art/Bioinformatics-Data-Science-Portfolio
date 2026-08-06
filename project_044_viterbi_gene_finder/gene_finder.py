"""
Eukaryotic Gene Finder using Hidden Markov Models
Author: Portfolio Creator
Description: Implements the log-space Viterbi dynamic programming decoding algorithm
             to identify exons (coding regions) vs introns (non-coding).
Language: English (100%)
"""

import os
import numpy as np

class HMMGeneFinder:
    """Hidden Markov Model gene structure finder implementing the Viterbi algorithm."""
    
    def __init__(self, fasta_path: str):
        self.fasta_path = fasta_path
        self.header = ""
        self.sequence = ""
        
        # States: 0 = Non-coding (N), 1 = Exon (E)
        self.states = [0, 1]
        self.state_names = {0: 'N', 1: 'E'}
        
        # Initial state probabilities: Starts in Non-coding
        self.pi = np.array([1.0, 0.0])
        
        # Transition probabilities:
        # Rows: from N, E
        # Cols: to N, E
        self.transitions = np.array([
            [0.9, 0.1],  # N -> N, E
            [0.2, 0.8]   # E -> N, E
        ])
        
        # Emission probabilities:
        # Rows: states N, E
        # Cols: bases A, C, G, T (mapped to index 0, 1, 2, 3)
        self.emissions = np.array([
            [0.30, 0.20, 0.20, 0.30],  # Non-coding (AT-rich background)
            [0.15, 0.35, 0.35, 0.15]   # Exon (GC-rich coding region)
        ])
        
        self.base_map = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
        self.load_sequence()

    def load_sequence(self):
        """Reads DNA sequence from FASTA file."""
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

    def decode_viterbi(self, dna_seq: str) -> tuple:
        """
        Runs log-space Viterbi decoding on a DNA sequence.
        
        Returns:
            tuple: (decoded_states_string, log_probability)
        """
        n = len(dna_seq)
        if n == 0:
            return "", 0.0
            
        # Log-space conversions to prevent underflow, silencing divide by zero warnings
        with np.errstate(divide='ignore'):
            log_pi = np.log(self.pi)
            log_trans = np.log(self.transitions)
            log_emit = np.log(self.emissions)
        
        # Lattice matrix: size = number of states x sequence length
        # Pointer matrix: size = number of states x sequence length (to trace back states)
        viterbi_lattice = np.zeros((2, n))
        pointers = np.zeros((2, n), dtype=int)
        
        # Initialize first step
        first_base_idx = self.base_map.get(dna_seq[0], 0)
        viterbi_lattice[0, 0] = log_pi[0] + log_emit[0, first_base_idx]
        viterbi_lattice[1, 0] = log_pi[1] + log_emit[1, first_base_idx]
        
        # Recurrence loop
        for t in range(1, n):
            base_idx = self.base_map.get(dna_seq[t], 0)
            for s in range(2):
                # Calculate: max_prev_state ( Viterbi[prev_state, t-1] + trans[prev_state, s] )
                prev_scores = viterbi_lattice[:, t-1] + log_trans[:, s]
                best_prev = np.argmax(prev_scores)
                
                viterbi_lattice[s, t] = prev_scores[best_prev] + log_emit[s, base_idx]
                pointers[s, t] = best_prev
                
        # Find final best state
        best_final_state = np.argmax(viterbi_lattice[:, n-1])
        final_log_prob = viterbi_lattice[best_final_state, n-1]
        
        # Traceback
        decoded_path = []
        curr_state = best_final_state
        decoded_path.append(self.state_names[curr_state])
        
        for t in range(n - 1, 0, -1):
            curr_state = pointers[curr_state, t]
            decoded_path.append(self.state_names[curr_state])
            
        decoded_path.reverse()
        return "".join(decoded_path), final_log_prob

    def parse_exons(self, path_str: str) -> list:
        """
        Extracts start and end coordinates of Exon (E) runs from a decoded path string.
        
        Returns:
            list: List of tuples (start, end) representing 0-indexed intervals.
        """
        exons = []
        in_exon = False
        start = -1
        
        for i, char in enumerate(path_str):
            if char == 'E' and not in_exon:
                in_exon = True
                start = i
            elif char != 'E' and in_exon:
                in_exon = False
                exons.append((start, i))
        # Handle exon extending to the very end of sequence
        if in_exon:
            exons.append((start, len(path_str)))
            
        return exons
