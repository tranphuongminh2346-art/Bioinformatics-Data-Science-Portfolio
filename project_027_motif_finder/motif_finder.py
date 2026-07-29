"""
Gibbs DNA Motif Sampler
Author: Portfolio Creator
Description: Implements the Gibbs Sampling heuristic algorithm to identify conserved
             motifs (transcription factor binding sites) across DNA promoter sequences.
Language: English (100%)
"""

import os
import numpy as np

class GibbsMotifFinder:
    """Finds optimal transcription factor motifs in DNA sequences using Gibbs Sampling."""
    
    def __init__(self, fasta_path: str, motif_len: int = 6):
        self.fasta_path = fasta_path
        self.motif_len = motif_len
        self.sequences = []
        self.load_sequences()

    def load_sequences(self):
        """Loads sequences from FASTA file."""
        if not os.path.exists(self.fasta_path):
            raise FileNotFoundError(f"FASTA file not found: {self.fasta_path}")
            
        seqs = []
        current_seq = []
        with open(self.fasta_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith(">"):
                    if current_seq:
                        seqs.append("".join(current_seq))
                        current_seq = []
                else:
                    current_seq.append(line.upper())
            if current_seq:
                seqs.append("".join(current_seq))
                
        self.sequences = seqs

    def build_profile(self, motifs: list) -> np.ndarray:
        """
        Creates a position frequency profile matrix with Laplace pseudocounts (+1).
        
        Matrix rows: 0=A, 1=C, 2=G, 3=T
        Columns: motif length positions
        
        Returns:
            np.ndarray: 4 x L profile matrix of probabilities.
        """
        n_motifs = len(motifs)
        # 4 rows (A, C, G, T) x L columns
        counts = np.ones((4, self.motif_len))  # Initialized with pseudocounts = 1
        
        base_map = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
        
        for motif in motifs:
            for j, char in enumerate(motif):
                if char in base_map:
                    counts[base_map[char], j] += 1
                    
        # Divide by column sum (number of motifs + 4 pseudocount bases)
        profile = counts / (n_motifs + 4)
        return profile

    def score_kmer(self, kmer: str, profile: np.ndarray) -> float:
        """Calculates the probability of a kmer according to the profile matrix."""
        base_map = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
        prob = 1.0
        for j, char in enumerate(kmer):
            if char in base_map:
                prob *= profile[base_map[char], j]
            else:
                prob *= 0.01  # Small penalty for unknown bases
        return prob

    def find_motifs(self, iterations: int = 100, seed: int = 42) -> tuple:
        """
        Executes the Gibbs Sampler optimization loop.
        
        Returns:
            tuple: (best_motifs: list, consensus_motif: str)
        """
        np.random.seed(seed)
        n = len(self.sequences)
        L = self.motif_len
        
        # 1. Randomly initialize starting positions
        start_positions = []
        for seq in self.sequences:
            max_start = len(seq) - L
            start_positions.append(np.random.randint(0, max_start + 1))
            
        # 2. Optimization loop
        for _ in range(iterations):
            # Select sequence to remove
            remove_idx = np.random.randint(0, n)
            
            # Build profile of other sequences
            other_motifs = []
            for i in range(n):
                if i != remove_idx:
                    start = start_positions[i]
                    other_motifs.append(self.sequences[i][start : start + L])
                    
            profile = self.build_profile(other_motifs)
            
            # Score all kmers in the removed sequence
            seq = self.sequences[remove_idx]
            max_start = len(seq) - L
            probabilities = []
            
            for start in range(max_start + 1):
                kmer = seq[start : start + L]
                prob = self.score_kmer(kmer, profile)
                probabilities.append(prob)
                
            # Normalize probabilities
            prob_sum = sum(probabilities)
            if prob_sum == 0:
                # Uniform probability if all scores are 0
                probabilities = [1.0 / (max_start + 1)] * (max_start + 1)
            else:
                probabilities = [p / prob_sum for p in probabilities]
                
            # Sample new starting position
            new_start = np.random.choice(range(max_start + 1), p=probabilities)
            start_positions[remove_idx] = new_start
            
        # Extract best motifs
        best_motifs = []
        for i, seq in enumerate(self.sequences):
            start = start_positions[i]
            best_motifs.append(seq[start : start + L])
            
        consensus = self.get_consensus(best_motifs)
        return best_motifs, consensus

    def get_consensus(self, motifs: list) -> str:
        """Determines the consensus sequence from a list of motifs."""
        consensus_chars = []
        base_map = {0: 'A', 1: 'C', 2: 'G', 3: 'T'}
        
        for j in range(self.motif_len):
            counts = [0, 0, 0, 0]  # A, C, G, T
            for motif in motifs:
                char = motif[j]
                if char == 'A': counts[0] += 1
                elif char == 'C': counts[1] += 1
                elif char == 'G': counts[2] += 1
                elif char == 'T': counts[3] += 1
            max_idx = np.argmax(counts)
            consensus_chars.append(base_map[max_idx])
            
        return "".join(consensus_chars)
