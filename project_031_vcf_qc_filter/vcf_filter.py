"""
VCF Genotype Quality Control Filter
Author: Portfolio Creator
Description: Parses genomic VCF lines, filters call variants by depth (DP)
             and genotype quality (GQ), and calculates transition/transversion (Ti/Tv) ratios.
Language: English (100%)
"""

import os

class VCFGenotypeFilter:
    """Parses and filters VCF genomic databases according to sample call qualities."""
    
    def __init__(self, vcf_path: str):
        self.vcf_path = vcf_path
        self.headers = []
        self.variants = []
        self.load_vcf()

    def load_vcf(self):
        """Reads VCF file lines and separates headers from variant rows."""
        if not os.path.exists(self.vcf_path):
            raise FileNotFoundError(f"VCF database not found: {self.fasta_path}")
            
        with open(self.vcf_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("#"):
                    self.headers.append(line)
                else:
                    self.variants.append(self.parse_variant_line(line))

    def parse_variant_line(self, line: str) -> dict:
        """Parses a single VCF variant line into a structured dictionary."""
        fields = line.split('\t')
        chrom, pos, id_val, ref, alt, qual, filt, info, format_str, sample_str = fields
        
        # Parse FORMAT and SAMPLE key-value links
        format_keys = format_str.split(':')
        sample_vals = sample_str.split(':')
        sample_data = dict(zip(format_keys, sample_vals))
        
        # Parse GQ and DP
        gq = int(sample_data.get('GQ', 0)) if sample_data.get('GQ') else 0
        dp = int(sample_data.get('DP', 0)) if sample_data.get('DP') else 0
        
        return {
            "chrom": chrom,
            "pos": int(pos),
            "id": id_val,
            "ref": ref.upper(),
            "alt": alt.upper(),
            "qual": float(qual) if qual != '.' else 0.0,
            "filter": filt,
            "gq": gq,
            "dp": dp,
            "raw_line": line
        }

    def filter_variants(self, min_qual: float = 30.0, min_gq: int = 20, min_dp: int = 10) -> list:
        """
        Filters variants based on quality threshold conditions.
        
        Returns:
            list: List of filtered variant dictionaries.
        """
        filtered = []
        for var in self.variants:
            if var["qual"] >= min_qual and var["gq"] >= min_gq and var["dp"] >= min_dp:
                filtered.append(var)
        return filtered

    def calculate_titv_ratio(self, variants: list) -> float:
        """
        Computes the transition/transversion (Ti/Tv) ratio.
        
        Transitions (Ti): A <-> G, C <-> T
        Transversions (Tv): A <-> C, A <-> T, C <-> G, G <-> T
        
        Returns:
            float: Ti/Tv ratio. Returns 0.0 if transversions = 0.
        """
        transitions = 0
        transversions = 0
        
        transition_pairs = [
            ('A', 'G'), ('G', 'A'),
            ('C', 'T'), ('T', 'C')
        ]
        
        for var in variants:
            ref = var["ref"]
            alt = var["alt"]
            
            # Simple check for single nucleotide variations (SNVs) only
            if len(ref) != 1 or len(alt) != 1:
                continue
                
            pair = (ref, alt)
            if pair in transition_pairs:
                transitions += 1
            else:
                transversions += 1
                
        if transversions == 0:
            return 0.0
            
        return transitions / transversions
