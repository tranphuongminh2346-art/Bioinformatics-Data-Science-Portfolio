"""
VCF Genotype QC Filter CLI
Author: Portfolio Creator
Description: CLI driver to execute quality control filters on VCF records
             and print Ti/Tv summary ratios.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vcf_filter import VCFGenotypeFilter

def main():
    parser = argparse.ArgumentParser(
        description="VCF Quality Control Filter - Filter variant calls and calculate Ti/Tv ratios."
    )
    parser.add_argument(
        "-i", "--input",
        default="raw_variants.vcf",
        help="Path to input VCF file (default: raw_variants.vcf)."
    )
    parser.add_argument(
        "-o", "--output",
        default="filtered_variants.vcf",
        help="Path to save filtered VCF output (default: filtered_variants.vcf)."
    )
    parser.add_argument(
        "-q", "--qual",
        type=float,
        default=30.0,
        help="Minimum variant call quality QUAL (default: 30.0)."
    )
    parser.add_argument(
        "-gq", "--gq",
        type=int,
        default=20,
        help="Minimum genotype quality GQ (default: 20)."
    )
    parser.add_argument(
        "-dp", "--dp",
        type=int,
        default=10,
        help="Minimum read depth DP (default: 10)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("VCF Genotype Quality Control Filter Pipeline")
    print("=" * 60)
    print(f"[*] Input VCF:     {args.input}")
    print(f"[*] Output VCF:    {args.output}")
    print(f"[*] QC Filters:    QUAL >= {args.qual} | GQ >= {args.gq} | DP >= {args.dp}")

    try:
        vcf = VCFGenotypeFilter(args.input)
        print(f"[+] Loaded {len(vcf.variants)} variants from raw VCF database.")
        
        print("[*] Running filtering criteria...")
        filtered = vcf.filter_variants(min_qual=args.qual, min_gq=args.gq, min_dp=args.dp)
        print(f"[+] Retained {len(filtered)} / {len(vcf.variants)} variants after filter.")
        
        print("[*] Calculating transition/transversion (Ti/Tv) ratios...")
        raw_titv = vcf.calculate_titv_ratio(vcf.variants)
        filtered_titv = vcf.calculate_titv_ratio(filtered)
        
        print("\n" + "=" * 60)
        print("Genotype Quality Control Metrics Summary")
        print("=" * 60)
        print(f"[*] Raw Ti/Tv Ratio      : {raw_titv:.4f}")
        print(f"[*] Filtered Ti/Tv Ratio : {filtered_titv:.4f}")
        
        # Write filtered variants to new VCF
        print(f"\n[*] Exporting filtered records to {args.output}...")
        with open(args.output, 'w', encoding='utf-8') as out_f:
            # Write headers
            for header_line in vcf.headers:
                out_f.write(header_line + "\n")
            # Write filtered records
            for var in filtered:
                out_f.write(var["raw_line"] + "\n")
                
        print(f"[+] Output VCF written successfully.")
        
    except Exception as e:
        print(f"[-] Pipeline execution failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
