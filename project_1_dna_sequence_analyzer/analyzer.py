import os
import numpy as np
import matplotlib.pyplot as plt

# Genetic Code Dictionary for Translation
GENETIC_CODE = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_', 'TGA':'_' # _ represents Stop codon
}

class DNASequenceAnalyzer:
    def __init__(self, sequence: str):
        """Initialize the analyzer with a DNA sequence string."""
        self.sequence = sequence.strip().upper()
        self.validate_sequence()

    def validate_sequence(self):
        """Validate that the sequence only contains A, C, G, T."""
        valid_nucleotides = set("ACGT")
        invalid = [char for char in self.sequence if char not in valid_nucleotides]
        if invalid:
            raise ValueError(f"Invalid characters in DNA sequence: {set(invalid)}. Only A, C, G, T are allowed.")

    def get_nucleotide_frequencies(self) -> dict:
        """Calculate the frequency of each nucleotide."""
        length = len(self.sequence)
        if length == 0:
            return {"A": 0, "C": 0, "G": 0, "T": 0}
        return {nt: self.sequence.count(nt) / length for nt in "ACGT"}

    def get_gc_content(self) -> float:
        """Calculate the overall GC content of the sequence."""
        length = len(self.sequence)
        if length == 0:
            return 0.0
        gc_count = self.sequence.count('G') + self.sequence.count('C')
        return gc_count / length

    def transcribe(self) -> str:
        """Transcribe DNA sequence to RNA sequence (T -> U)."""
        return self.sequence.replace('T', 'U')

    def translate(self) -> str:
        """Translate DNA sequence to Protein sequence."""
        protein = []
        for i in range(0, len(self.sequence) - 2, 3):
            codon = self.sequence[i:i+3]
            amino_acid = GENETIC_CODE.get(codon, 'X')  # X for unknown
            if amino_acid == '_':  # Stop codon reached
                protein.append('*')
                break
            protein.append(amino_acid)
        return "".join(protein)

    def calculate_sliding_window_gc(self, window_size: int = 10, step_size: int = 5) -> tuple:
        """Calculate GC content in a sliding window along the sequence."""
        seq_len = len(self.sequence)
        if seq_len < window_size:
            # Fallback to smaller window size
            window_size = seq_len
        
        positions = []
        gc_values = []
        
        for i in range(0, seq_len - window_size + 1, step_size):
            window = self.sequence[i:i+window_size]
            gc_count = window.count('G') + window.count('C')
            gc_pct = (gc_count / window_size) * 100
            positions.append(i + window_size // 2)
            gc_values.append(gc_pct)
            
        return positions, gc_values

    def plot_gc_content(self, window_size: int = 20, step_size: int = 5, save_path: str = "gc_content_plot.png"):
        """Plot the GC content along the sequence and save as an image."""
        positions, gc_values = self.calculate_sliding_window_gc(window_size, step_size)
        
        if not positions:
            print("Sequence too short for plotting GC content.")
            return

        plt.figure(figsize=(10, 5))
        plt.plot(positions, gc_values, color='#00adb5', linewidth=2, label=f'GC Content (Window {window_size}bp)')
        
        # Add average line
        avg_gc = self.get_gc_content() * 100
        plt.axhline(y=avg_gc, color='#ff5722', linestyle='--', label=f'Average GC Content ({avg_gc:.1f}%)')
        
        plt.title('GC Content Distribution Along DNA Sequence', fontsize=14, fontweight='bold', pad=15)
        plt.xlabel('Sequence Position (bp)', fontsize=12)
        plt.ylabel('GC Percentage (%)', fontsize=12)
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.ylim(0, 100)
        plt.legend(loc='upper right')
        plt.tight_layout()
        
        plt.savefig(save_path, dpi=300)
        plt.close()
        print(f"GC content plot saved to: {save_path}")

def main():
    # Example DNA Sequence (insulin gene fragment)
    sample_dna = "AGCCCTCCAGGACAGGCTGCATCAGAAGAGGCCATCAAGCAGGTCTGTTCCAAGGGCCTTTGCGTCAGGTGGGCTCAGGATTCCAGGGTGGCTGGACCCCAGGCCCCAGCTCTGCAGCAGGGAGGACGTGGCTGGGCTCGTGAAGCATGTGGGGGTGAGCCC"
    
    print("=" * 60)
    print("           DNA SEQUENCE ANALYZER - PORTFOLIO DAY 01")
    print("=" * 60)
    print(f"Sequence Length: {len(sample_dna)} bp")
    print(f"Sequence preview (first 50 bp): {sample_dna[:50]}...")
    
    analyzer = DNASequenceAnalyzer(sample_dna)
    
    # 1. Nucleotide Frequencies
    freqs = analyzer.get_nucleotide_frequencies()
    print("\n[1] Nucleotide Frequencies:")
    for nt, freq in freqs.items():
        print(f"    - {nt}: {freq*100:.2f}% (Count: {sample_dna.count(nt)})")
        
    # 2. GC Content
    gc_pct = analyzer.get_gc_content() * 100
    print(f"\n[2] Overall GC Content: {gc_pct:.2f}%")
    
    # 3. Transcription
    rna = analyzer.transcribe()
    print(f"\n[3] Transcribed RNA preview: {rna[:50]}...")
    
    # 4. Translation
    protein = analyzer.translate()
    print(f"\n[4] Translated Protein preview: {protein[:20]}...")
    
    # 5. Sliding Window & Plotting
    output_plot = os.path.join(os.path.dirname(__file__), "gc_content_profile.png") if __file__ else "gc_content_profile.png"
    analyzer.plot_gc_content(window_size=20, step_size=5, save_path=output_plot)
    print(f"\n[5] GC Content profile plotted successfully.")
    print("=" * 60)

if __name__ == "__main__":
    main()
