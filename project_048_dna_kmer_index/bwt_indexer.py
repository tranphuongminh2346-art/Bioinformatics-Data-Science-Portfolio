"""
Burrows-Wheeler Transform (BWT) DNA Indexer
Author: Portfolio Creator
Description: Implements BWT conversions, Inverse BWT reconstructions,
             and LF-mapping backward search queries on genomic sequences.
Language: English (100%)
"""

import os

class BWTIndexer:
    """Genomic indexer implementing BWT and suffix arrays for exact k-mer matching."""
    
    def __init__(self, sequence: str):
        # Enforce uppercase and append sentinel '$' if not present
        self.sequence = sequence.upper()
        if not self.sequence.endswith('$'):
            self.sequence += '$'
            
        self.bwt_string = ""
        self.suffix_array = []
        self.first_col = []
        self.lf_map = []
        
        self.build_index()

    def build_index(self):
        """Generates sorted suffix arrays and the BWT string."""
        n = len(self.sequence)
        
        # Sort suffix indexes alphabetically using cyclic shifts
        # Suffix Array (SA) stores starting indexes of sorted cyclic shifts
        self.suffix_array = sorted(range(n), key=lambda i: self.sequence[i:] + self.sequence[:i])
        
        # BWT string is the last column of the Burrows-Wheeler Matrix
        # For a cyclic shift starting at index i, the last character is at index (i - 1) % n
        self.bwt_string = "".join(self.sequence[(idx - 1) % n] for idx in self.suffix_array)
        
        # First column is simply the sorted characters
        self.first_col = sorted(list(self.sequence))
        
        # Build rank arrays for LF-mapping
        # lf_map[i] stores the index in the first column corresponding to BWT[i]
        # We need counts of occurrences to distinguish duplicate characters (rank)
        bwt_occurrences = []
        counts = {}
        for char in self.bwt_string:
            counts[char] = counts.get(char, 0) + 1
            bwt_occurrences.append((char, counts[char]))
            
        first_col_occurrences = []
        first_counts = {}
        for char in self.first_col:
            first_counts[char] = first_counts.get(char, 0) + 1
            first_col_occurrences.append((char, first_counts[char]))
            
        # Create map from BWT index to First Column index
        # Map matches identical (character, rank) pairs
        first_occurrence_map = {item: idx for idx, item in enumerate(first_col_occurrences)}
        self.lf_map = [first_occurrence_map[item] for item in bwt_occurrences]

    def inverse_bwt(self) -> str:
        """
        Reconstructs the original sequence from the BWT string.
        
        Returns:
            str: Reconstructed sequence.
        """
        n = len(self.bwt_string)
        reconstructed = []
        
        # Start at the sentinel character '$' (which is always at index 0 of the first column)
        curr_idx = 0
        for _ in range(n):
            char = self.bwt_string[curr_idx]
            reconstructed.append(char)
            curr_idx = self.lf_map[curr_idx]
            
        # Since we trace backwards, reverse and drop the sentinel '$'
        return "".join(reconstructed[::-1])[1:]

    def search_kmer(self, query: str) -> list:
        """
        Searches for exact query matches using backward search.
        
        Returns:
            list: List of matching 0-indexed starting coordinates in the original DNA sequence.
        """
        query = query.upper()
        if not query:
            return []
            
        # Initialize search range in BWT matrix rows
        # Start with full range [top, bottom]
        top = 0
        bottom = len(self.bwt_string) - 1
        
        # Backward search from right to left in query
        for char in reversed(query):
            # Check if character exists in BWT within range [top, bottom]
            # Find sub-range in first column
            if char not in self.bwt_string[top:bottom+1]:
                return []  # No match
                
            # Filter range boundaries
            top_rank = -1
            bottom_rank = -1
            
            # Find first and last occurrences of the character in BWT[top:bottom+1]
            first_col_idx_top = -1
            first_col_idx_bottom = -1
            
            # Count ranks to locate first column indices
            # Find top index
            for idx in range(top, bottom + 1):
                if self.bwt_string[idx] == char:
                    first_col_idx_top = self.lf_map[idx]
                    break
                    
            # Find bottom index
            for idx in range(bottom, top - 1, -1):
                if self.bwt_string[idx] == char:
                    first_col_idx_bottom = self.lf_map[idx]
                    break
                    
            if first_col_idx_top == -1 or first_col_idx_bottom == -1:
                return []
                
            top = first_col_idx_top
            bottom = first_col_idx_bottom
            
        # Map the remaining rows in BWT back to original coordinates using Suffix Array (SA)
        matches = [self.suffix_array[idx] for idx in range(top, bottom + 1)]
        return sorted(matches)
