"""
Genomic PCR Primer Designer
Author: Portfolio Creator
Description: Designs forward and reverse PCR primers for DNA sequences,
             evaluates melting temperatures (Tm), and filters out hairpin loops.
Language: English (100%)
"""

import os

class PrimerDesigner:
    """Designs PCR primer pairs for target DNA sequences."""
    
    def __init__(self, fasta_path: str):
        self.fasta_path = fasta_path
        self.header = ""
        self.sequence = ""
        self.load_sequence()

    def load_sequence(self):
        """Loads sequence from FASTA file."""
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

    def calculate_tm(self, primer: str) -> float:
        """
        Calculates primer melting temperature using the standard Wallace formula.
        
        Formula:
          Tm = 2 * (A + T) + 4 * (G + C)
          
        Returns:
            float: Melting temperature in °C.
        """
        a = primer.count('A')
        t = primer.count('T')
        g = primer.count('G')
        c = primer.count('C')
        return float(2 * (a + t) + 4 * (g + c))

    def calculate_gc(self, primer: str) -> float:
        """Calculates GC content ratio."""
        g = primer.count('G')
        c = primer.count('C')
        return float(g + c) / len(primer)

    def get_reverse_complement(self, seq: str) -> str:
        """Returns the reverse complement of a DNA sequence."""
        comp_map = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        comp = "".join(comp_map.get(base, 'N') for base in seq)
        return comp[::-1]

    def has_hairpin(self, primer: str, max_complementarity: int = 4) -> bool:
        """
        Checks for self-complementarity (hairpin loop risk).
        
        Checks if any k-mer of size max_complementarity in the primer
        matches the reverse complement of the primer.
        
        Returns:
            bool: True if hairpin risk exists, False otherwise.
        """
        rev_comp = self.get_reverse_complement(primer)
        k = max_complementarity
        n = len(primer)
        
        for i in range(n - k + 1):
            kmer = primer[i : i + k]
            if kmer in rev_comp:
                # Exclude self-matching at identical coordinates (which is impossible)
                # But simple match in reverse complement is a good general test
                return True
        return False

    def design_candidates(self, min_len: int = 18, max_len: int = 22,
                          min_tm: float = 52.0, max_tm: float = 65.0,
                          min_gc: float = 0.4, max_gc: float = 0.6) -> tuple:
        """
        Scans sequence to design forward and reverse primer candidate lists.
        
        Returns:
            tuple: (forward_candidates: list, reverse_candidates: list)
        """
        forward_candidates = []
        reverse_candidates = []
        
        n = len(self.sequence)
        
        # 1. Design Forward Primers (Scan first 100 bp from 5' end)
        scan_limit = min(100, n - max_len)
        for start in range(scan_limit):
            for length in range(min_len, max_len + 1):
                primer = self.sequence[start : start + length]
                tm = self.calculate_tm(primer)
                gc = self.calculate_gc(primer)
                
                if min_tm <= tm <= max_tm and min_gc <= gc <= max_gc:
                    if not self.has_hairpin(primer):
                        forward_candidates.append({
                            "type": "FORWARD",
                            "start": start,
                            "length": length,
                            "sequence": primer,
                            "tm": tm,
                            "gc": gc
                        })
                        
        # 2. Design Reverse Primers (Scan last 100 bp from 3' end)
        # Reverse primers are reverse complement of the template sequence
        reverse_limit = max(0, n - 100)
        for start in range(reverse_limit, n - min_len):
            for length in range(min_len, max_len + 1):
                if start + length > n:
                    continue
                template_segment = self.sequence[start : start + length]
                primer = self.get_reverse_complement(template_segment)
                tm = self.calculate_tm(primer)
                gc = self.calculate_gc(primer)
                
                if min_tm <= tm <= max_tm and min_gc <= gc <= max_gc:
                    if not self.has_hairpin(primer):
                        reverse_candidates.append({
                            "type": "REVERSE",
                            "start": start,
                            "length": length,
                            "sequence": primer,
                            "tm": tm,
                            "gc": gc
                        })
                        
        return forward_candidates, reverse_candidates
