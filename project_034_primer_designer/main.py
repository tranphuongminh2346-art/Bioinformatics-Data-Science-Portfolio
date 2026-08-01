"""
PCR Primer Designer CLI
Author: Portfolio Creator
Description: CLI driver to design forward and reverse primers for target DNA sequences.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from primer_designer import PrimerDesigner

def main():
    parser = argparse.ArgumentParser(
        description="PCR Genomic Primer Designer - Search candidate primer pairs."
    )
    parser.add_argument(
        "-i", "--input",
        default="target_gene.fasta",
        help="Path to input FASTA sequence (default: target_gene.fasta)."
    )
    parser.add_argument(
        "-min", "--min-len",
        type=int,
        default=18,
        help="Minimum primer length in bp (default: 18)."
    )
    parser.add_argument(
        "-max", "--max-len",
        type=int,
        default=22,
        help="Maximum primer length in bp (default: 22)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Genomic PCR Primer Designer Pipeline")
    print("=" * 60)
    print(f"[*] Input sequence: {args.input}")
    print(f"[*] Length constraints: {args.min_len} to {args.max_len} bp")

    try:
        designer = PrimerDesigner(args.input)
        print(f"[+] Loaded template: '{designer.header}' ({len(designer.sequence)} bp)")
        
        print("[*] Running candidate scans and filters...")
        fw_list, rv_list = designer.design_candidates(min_len=args.min_len, max_len=args.max_len)
        
        # Display top candidates
        print("\n" + "=" * 60)
        print("Designed Forward Primer Candidates (Top 3)")
        print("=" * 60)
        for idx, p in enumerate(fw_list[:3]):
            print(f"[{idx+1}] Seq: {p['sequence']:22} | Start: {p['start']:4d} | Tm: {p['tm']:.1f}°C | GC: {p['gc']*100:.1f}%")
            
        print("\n" + "=" * 60)
        print("Designed Reverse Primer Candidates (Top 3)")
        print("=" * 60)
        for idx, p in enumerate(rv_list[:3]):
            print(f"[{idx+1}] Seq: {p['sequence']:22} | Start: {p['start']:4d} | Tm: {p['tm']:.1f}°C | GC: {p['gc']*100:.1f}%")
            
        print("\n" + "=" * 60)
        print("Summary of Candidates")
        print("=" * 60)
        print(f"[*] Total Forward candidates: {len(fw_list)}")
        print(f"[*] Total Reverse candidates: {len(rv_list)}")
        
    except Exception as e:
        print(f"[-] Designer failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
