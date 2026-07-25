"""
Needleman-Wunsch Global Sequence Alignment Algorithm
Author: Portfolio Creator
Description: Implements dynamic programming for global alignment of two sequences.
             Calculates the score matrix, tracebacks path, and formats alignments.
Language: English (100%)
"""

import numpy as np

class NeedlemanWunschAligner:
    """Computes optimal global alignments for biological sequences."""
    
    def __init__(self, match_score: int = 1, mismatch_penalty: int = -1, gap_penalty: int = -1):
        self.match_score = match_score
        self.mismatch_penalty = mismatch_penalty
        self.gap_penalty = gap_penalty
        self.score_matrix = None

    def align(self, seq1: str, seq2: str) -> tuple:
        """
        Runs the dynamic programming alignment matrix fill and backtracking traceback.
        
        Args:
            seq1 (str): First sequence.
            seq2 (str): Second sequence.
            
        Returns:
            tuple: (alignment_score: float, aligned_seq1: str, aligned_seq2: str)
        """
        m = len(seq1)
        n = len(seq2)
        
        # 1. Initialize scoring matrix
        self.score_matrix = np.zeros((m + 1, n + 1))
        
        # Base cases: gap penalties along borders
        for i in range(m + 1):
            self.score_matrix[i, 0] = i * self.gap_penalty
        for j in range(n + 1):
            self.score_matrix[0, j] = j * self.gap_penalty
            
        # 2. Fill the matrix
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # Calculate match/mismatch score
                char1 = seq1[i - 1]
                char2 = seq2[j - 1]
                score_match = self.match_score if char1 == char2 else self.mismatch_penalty
                
                # Dynamic programming recurrence relation
                diagonal = self.score_matrix[i - 1, j - 1] + score_match
                up = self.score_matrix[i - 1, j] + self.gap_penalty
                left = self.score_matrix[i, j - 1] + self.gap_penalty
                
                self.score_matrix[i, j] = max(diagonal, up, left)
                
        # 3. Traceback
        aligned1 = []
        aligned2 = []
        
        i = m
        j = n
        while i > 0 or j > 0:
            current_score = self.score_matrix[i, j]
            
            # Match/mismatch case (diagonal)
            if i > 0 and j > 0:
                char1 = seq1[i - 1]
                char2 = seq2[j - 1]
                score_match = self.match_score if char1 == char2 else self.mismatch_penalty
                if current_score == self.score_matrix[i - 1, j - 1] + score_match:
                    aligned1.append(seq1[i - 1])
                    aligned2.append(seq2[j - 1])
                    i -= 1
                    j -= 1
                    continue
                    
            # Gap in seq2 (up)
            if i > 0 and (j == 0 or current_score == self.score_matrix[i - 1, j] + self.gap_penalty):
                aligned1.append(seq1[i - 1])
                aligned2.append("-")
                i -= 1
                
            # Gap in seq1 (left)
            else:
                aligned2.append(seq2[j - 1])
                aligned1.append("-")
                j -= 1
                
        # Reverse aligned lists
        aligned_seq1 = "".join(reversed(aligned1))
        aligned_seq2 = "".join(reversed(aligned2))
        
        final_score = self.score_matrix[m, n]
        return float(final_score), aligned_seq1, aligned_seq2

    def format_alignment(self, aligned1: str, aligned2: str) -> str:
        """
        Creates a readable alignment text representation.
        
        Returns:
            str: Pretty-printed alignment.
        """
        middle = []
        for c1, c2 in zip(aligned1, aligned2):
            if c1 == c2:
                middle.append("|")  # Match
            elif c1 == "-" or c2 == "-":
                middle.append(" ")  # Gap
            else:
                middle.append(".")  # Mismatch
                
        middle_line = "".join(middle)
        return f"Seq1: {aligned1}\n      {middle_line}\nSeq2: {aligned2}"
