"""
DNA Sequence Analyzer & Visualizer
Author: Portfolio Creator
Description: A module to parse, analyze, and visualize DNA sequences.
             Includes transcription, translation, GC-content sliding window calculations,
             motif searching, and plotting capabilities.
Language: English (100%)
"""

import os
import matplotlib.pyplot as plt
import numpy as np

# Standard Genetic Code Dictionary (DNA Codon -> Amino Acid)
# '_' represents stop codons
GENETIC_CODE = {
    'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
    'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
    'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
    'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
    'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'TAT': 'Y', 'TAC': 'Y', 'TAA': '_', 'TAG': '_',
    'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
    'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'TGT': 'C', 'TGC': 'C', 'TGA': '_', 'TGG': 'W',
    'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
}

class DNASequence:
    """Represents a DNA sequence and provides analysis tools."""
    
    def __init__(self, sequence: str, header: str = "Unknown Sequence"):
        """
        Initializes the DNASequence object.
        
        Args:
            sequence (str): Raw DNA nucleotide sequence.
            header (str): Header metadata (e.g. from FASTA file).
        """
        self.header = header.strip()
        # Clean sequence: uppercase and remove whitespaces/newlines/digits
        self.sequence = "".join(sequence.upper().split())
        self.validate()

    def validate(self):
        """Validates that the sequence contains only standard nucleotides (A, C, G, T)."""
        valid_nucleotides = set("ACGTN")
        invalid = [char for char in self.sequence if char not in valid_nucleotides]
        if invalid:
            invalid_sample = "".join(list(set(invalid))[:5])
            raise ValueError(f"Invalid characters found in DNA sequence: {invalid_sample}")

    def get_length(self) -> int:
        """Returns the length of the sequence."""
        return len(self.sequence)

    def nucleotide_frequencies(self) -> dict:
        """Calculates the count and percentage of each nucleotide."""
        length = self.get_length()
        if length == 0:
            return {}
            
        freqs = {}
        for base in ['A', 'C', 'G', 'T', 'N']:
            count = self.sequence.count(base)
            freqs[base] = {
                "count": count,
                "percentage": (count / length) * 100
            }
        return freqs

    def gc_content(self) -> float:
        """Calculates the overall GC content percentage of the sequence."""
        length = self.get_length()
        if length == 0:
            return 0.0
        g_count = self.sequence.count('G')
        c_count = self.sequence.count('C')
        return ((g_count + c_count) / length) * 100

    def transcribe(self) -> str:
        """Transcribes DNA to RNA (replacing T with U)."""
        return self.sequence.replace('T', 'U')

    def translate(self) -> str:
        """Translates the DNA sequence to protein sequence starting from the first codon."""
        protein = []
        for i in range(0, self.get_length() - 2, 3):
            codon = self.sequence[i:i+3]
            amino_acid = GENETIC_CODE.get(codon, 'X')  # 'X' for unknown codons
            protein.append(amino_acid)
        return "".join(protein)

    def find_motifs(self, motif: str) -> list:
        """
        Finds all start index positions of a specific motif in the DNA sequence.
        
        Args:
            motif (str): Motif sequence to search (e.g. 'ATG', 'AAGCTT').
            
        Returns:
            list: List of 0-based start indices.
        """
        motif = motif.upper()
        positions = []
        start = 0
        while True:
            pos = self.sequence.find(motif, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1
        return positions

    def sliding_window_gc(self, window_size: int = 50, step_size: int = 10) -> tuple:
        """
        Calculates GC content in a sliding window along the sequence.
        
        Args:
            window_size (int): Size of the sliding window.
            step_size (int): Step size to move the window.
            
        Returns:
            tuple: (positions, gc_values) where positions are window midpoints.
        """
        seq_len = self.get_length()
        if seq_len < window_size:
            return [seq_len // 2], [self.gc_content()]
            
        positions = []
        gc_values = []
        
        for i in range(0, seq_len - window_size + 1, step_size):
            window = self.sequence[i:i+window_size]
            g_count = window.count('G')
            c_count = window.count('C')
            gc_pct = ((g_count + c_count) / window_size) * 100
            
            positions.append(i + window_size // 2)
            gc_values.append(gc_pct)
            
        return positions, gc_values

    def plot_gc_content(self, output_path: str, window_size: int = 50, step_size: int = 10):
        """
        Generates and saves a line plot of the sliding window GC content.
        
        Args:
            output_path (str): File path to save the generated plot.
            window_size (int): Sliding window size.
            step_size (int): Sliding window step size.
        """
        positions, gc_values = self.sliding_window_gc(window_size, step_size)
        overall_gc = self.gc_content()

        plt.figure(figsize=(10, 5))
        plt.plot(positions, gc_values, color='#0284c7', linewidth=1.5, label=f'Window GC% (size={window_size})')
        plt.axhline(y=overall_gc, color='#ef4444', linestyle='--', linewidth=1.2, label=f'Average GC% ({overall_gc:.2f}%)')
        
        # Premium styling
        plt.title(f"GC Content Profile\n{self.header[:50]}...", fontsize=12, fontweight='bold', pad=10)
        plt.xlabel("Sequence Position (bp)", fontsize=10)
        plt.ylabel("GC Content (%)", fontsize=10)
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.legend(loc='upper right', frameon=True, facecolor='#ffffff', edgecolor='#e2e8f0')
        plt.ylim(0, 100)
        plt.tight_layout()
        
        # Save the plot
        plt.savefig(output_path, dpi=150)
        plt.close()


def parse_fasta(file_path: str) -> list:
    """
    Parses a FASTA file and returns a list of DNASequence instances.
    
    Args:
        file_path (str): Path to the FASTA file.
        
    Returns:
        list: List of DNASequence objects.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    sequences = []
    current_header = ""
    current_seq_parts = []
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                if current_seq_parts:
                    sequences.append(DNASequence("".join(current_seq_parts), current_header))
                    current_seq_parts = []
                current_header = line[1:]
            else:
                current_seq_parts.append(line)
                
        if current_seq_parts:
            sequences.append(DNASequence("".join(current_seq_parts), current_header))
            
    return sequences
