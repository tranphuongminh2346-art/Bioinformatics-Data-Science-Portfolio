"""
Genomic Variant Consequence Predictor
Author: Portfolio Creator
Description: Parses VCF files, maps genomic mutations to coding sequence codons,
             predicts translation consequences (synonymous, missense, nonsense),
             and applies rule-based pathogenicity labels.
Language: English (100%)
"""

import os
import matplotlib.pyplot as plt

# Genetic Code for translation
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

class VariantPredictor:
    """Predicts variant consequences on protein sequences."""
    
    def __init__(self, ref_seq: str, coding_start_pos: int):
        """
        Initializes the predictor with a reference template coding sequence.
        
        Args:
            ref_seq (str): Reference DNA sequence starting at coding_start_pos.
            coding_start_pos (int): Genomic POS corresponding to the first base (index 0) of ref_seq.
        """
        self.ref_seq = ref_seq.upper()
        self.coding_start_pos = coding_start_pos

    def parse_vcf(self, vcf_path: str) -> list:
        """
        Parses variants from a VCF file.
        
        Args:
            vcf_path (str): Path to VCF file.
            
        Returns:
            list: List of variant records dicts.
        """
        if not os.path.exists(vcf_path):
            raise FileNotFoundError(f"VCF file not found: {vcf_path}")
            
        variants = []
        with open(vcf_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith("#"):
                    continue
                parts = line.strip().split("\t")
                if len(parts) < 8:
                    continue
                    
                chrom = parts[0]
                pos = int(parts[1])
                var_id = parts[2]
                ref = parts[3].upper()
                alt = parts[4].upper()
                info_str = parts[7]
                
                # Parse INFO key-values
                info = {}
                for item in info_str.split(";"):
                    if "=" in item:
                        k, v = item.split("=", 1)
                        info[k] = v
                        
                variants.append({
                    "chrom": chrom,
                    "pos": pos,
                    "id": var_id,
                    "ref": ref,
                    "alt": alt,
                    "info": info
                })
        return variants

    def predict_consequence(self, pos: int, ref: str, alt: str) -> tuple:
        """
        Predicts consequence of a single-nucleotide variant (SNV).
        
        Args:
            pos (int): Genomic position of the mutation.
            ref (str): Reference allele base.
            alt (str): Alternate allele base.
            
        Returns:
            tuple: (ref_amino_acid, alt_amino_acid, consequence_label)
        """
        # Calculate local index relative to the coding start
        offset = pos - self.coding_start_pos
        
        # Ensure mutation is within the coding range
        if offset < 0 or offset >= len(self.ref_seq):
            return "N/A", "N/A", "Non-Coding Variant"
            
        # Only support SNV (single nucleotide variants) for simplicity
        if len(ref) != 1 or len(alt) != 1:
            return "N/A", "N/A", "Indel Variant (Unclassified)"

        # Calculate codon index and position within the codon (0, 1, or 2)
        codon_idx = offset // 3
        codon_pos = offset % 3
        
        codon_start = codon_idx * 3
        ref_codon = self.ref_seq[codon_start:codon_start+3]
        
        # Verify reference base matches VCF ref base
        if ref_codon[codon_pos] != ref:
            return "N/A", "N/A", "Reference Mismatch"
            
        # Construct mutant codon
        mutant_codon = list(ref_codon)
        mutant_codon[codon_pos] = alt
        mutant_codon = "".join(mutant_codon)
        
        # Translate codons
        ref_aa = GENETIC_CODE.get(ref_codon, "X")
        alt_aa = GENETIC_CODE.get(mutant_codon, "X")
        
        if ref_aa == alt_aa:
            consequence = "Synonymous"
        elif alt_aa == "_":
            consequence = "Nonsense (Stop Gain)"
        else:
            consequence = "Missense"
            
        return ref_aa, alt_aa, consequence

    def evaluate_pathogenicity(self, consequence: str, allele_frequency: float) -> str:
        """
        Determines the clinical severity class using simple decision rules.
        
        Args:
            consequence (str): Synonymous, Missense, or Nonsense.
            allele_frequency (float): Rarity of the mutation.
            
        Returns:
            str: Pathogenicity category.
        """
        if consequence == "Nonsense (Stop Gain)":
            return "Likely Pathogenic"
        elif consequence == "Missense":
            # Rare variants are more likely to have clinical impacts (VUS)
            if allele_frequency < 0.05:
                return "Variant of Uncertain Significance (VUS)"
            else:
                return "Likely Benign"
        elif consequence == "Synonymous":
            return "Benign"
        return "Unclassified"

    def plot_variant_summary(self, variant_list: list, output_path: str):
        """
        Generates a summary bar chart of variant consequences.
        
        Args:
            variant_list (list): Evaluated variants.
            output_path (str): File path to save summary plot.
        """
        consequences = [v["consequence"] for v in variant_list]
        unique_cons = list(set(consequences))
        counts = [consequences.count(c) for c in unique_cons]

        plt.figure(figsize=(7, 5))
        colors = ['#10b981', '#f59e0b', '#ef4444', '#64748b']
        
        bars = plt.bar(unique_cons, counts, color=colors[:len(unique_cons)], edgecolor='#e2e8f0', width=0.4)
        plt.grid(axis='y', linestyle=':', alpha=0.6)
        plt.title("Genomic Variant Consequence Counts", fontsize=12, fontweight='bold', pad=15)
        plt.xlabel("Mutation Consequence Type", fontsize=10)
        plt.ylabel("Variant Count", fontsize=10)
        
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{height}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold')

        plt.ylim(0, max(counts) + 1)
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
