"""
DNA Translation Open Reading Frame (ORF) Finder
Author: Portfolio Creator
Description: Scans genomic DNA sequences in all 6 reading frames to identify
             Open Reading Frames (ORFs) and translates them into protein sequences.
Language: English (100%)
"""

import os

GENETIC_CODE = {
    'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
    'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
    'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
    'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
    'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*', 'TGA': '*',
    'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
    'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W',
    'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
}

class ORFFinder:
    """Finds and translates Open Reading Frames in double-stranded DNA."""
    
    def __init__(self, fasta_path: str):
        self.fasta_path = fasta_path
        self.header = ""
        self.sequence = ""
        self.load_fasta()

    def load_fasta(self):
        """Reads DNA sequence from FASTA file."""
        if not os.path.exists(self.fasta_path):
            raise FileNotFoundError(f"FASTA sequence not found: {self.fasta_path}")
            
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

    def get_reverse_complement(self) -> str:
        """Returns the reverse complement of the target sequence."""
        comp_map = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        comp = "".join(comp_map.get(base, 'N') for base in self.sequence)
        return comp[::-1]

    def translate_dna(self, dna_seq: str) -> str:
        """Translates a DNA sequence into a protein amino acid sequence."""
        protein = []
        for i in range(0, len(dna_seq) - 2, 3):
            codon = dna_seq[i : i + 3]
            amino_acid = GENETIC_CODE.get(codon, 'X')
            if amino_acid == '*':
                break
            protein.append(amino_acid)
        return "".join(protein)

    def scan_frames(self, sequence: str, is_reverse: bool = False) -> list:
        """Scans 3 reading frames on the supplied sequence coordinate strand."""
        orfs = []
        n = len(sequence)
        
        # Scan reading frames 0, 1, 2
        for frame in range(3):
            i = frame
            while i < n - 2:
                codon = sequence[i : i + 3]
                if codon == "ATG":
                    # Found start codon. Scan for stop codon.
                    start_pos = i
                    stop_pos = -1
                    for j in range(start_pos, n - 2, 3):
                        stop_codon = sequence[j : j + 3]
                        if stop_codon in ["TAA", "TAG", "TGA"]:
                            stop_pos = j
                            break
                            
                    if stop_pos != -1:
                        orf_seq = sequence[start_pos : stop_pos + 3]
                        
                        # Store coordinates relative to original sequence
                        if is_reverse:
                            # Map coordinates back to original template strand
                            # Start and end positions are mapped backwards
                            orig_start = n - (stop_pos + 3)
                            orig_end = n - start_pos
                        else:
                            orig_start = start_pos
                            orig_end = stop_pos + 3
                            
                        orfs.append({
                            "strand": "REVERSE" if is_reverse else "FORWARD",
                            "frame": frame + 1,
                            "start": orig_start,
                            "end": orig_end,
                            "length": len(orf_seq),
                            "dna_sequence": orf_seq,
                            "translation": self.translate_dna(orf_seq)
                        })
                        
                        # Advance iterator past stop codon
                        i = stop_pos + 3
                        continue
                i += 3
        return orfs

    def find_all_orfs(self, min_len_bp: int = 30) -> list:
        """
        Scans both forward and reverse strands in all 6 reading frames.
        
        Returns:
            list: List of filtered ORF dictionaries.
        """
        # 1. Scan forward strand (3 frames)
        forward_orfs = self.scan_frames(self.sequence, is_reverse=False)
        
        # 2. Scan reverse strand (3 frames)
        rev_seq = self.get_reverse_complement()
        reverse_orfs = self.scan_frames(rev_seq, is_reverse=True)
        
        all_orfs = forward_orfs + reverse_orfs
        
        # Filter by minimum length
        filtered_orfs = [orf for orf in all_orfs if orf["length"] >= min_len_bp]
        
        # Sort by start coordinates
        filtered_orfs.sort(key=lambda x: x["start"])
        return filtered_orfs
