"""
DNA ORF Finder CLI Runner
Author: Portfolio Creator
Description: CLI driver to execute 6-frame ORF scanning on FASTA sequences.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orf_finder import ORFFinder

def main():
    parser = argparse.ArgumentParser(
        description="DNA Translation ORF Finder - Discover coding regions in DNA sequences."
    )
    parser.add_argument(
        "-i", "--input",
        default="sequence_with_orfs.fasta",
        help="Path to input FASTA file (default: sequence_with_orfs.fasta)."
    )
    parser.add_argument(
        "-l", "--min-len",
        type=int,
        default=30,
        help="Minimum ORF length threshold in bp (default: 30)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("DNA Translation Open Reading Frame (ORF) Finder Pipeline")
    print("=" * 60)
    print(f"[*] Input File:      {args.input}")
    print(f"[*] Min ORF Length:  {args.min_len} bp")

    try:
        finder = ORFFinder(args.input)
        print(f"[+] Loaded DNA sequence: '{finder.header}' ({len(finder.sequence)} bp)")
        
        print("[*] Scanning all 6 reading frames for start/stop codons...")
        orfs = finder.find_all_orfs(min_len_bp=args.min_len)
        
        print("\n" + "=" * 60)
        print("Discovered Open Reading Frames (ORFs) Summary")
        print("=" * 60)
        print(f"Total ORFs Found: {len(orfs)}")
        print("-" * 60)
        
        for idx, orf in enumerate(orfs):
            print(f"[{idx+1}] Strand: {orf['strand']:7} | Frame: {orf['frame']} | Range: {orf['start']}-{orf['end']} bp | Len: {orf['length']} bp")
            print(f"    DNA  : {orf['dna_sequence']}")
            print(f"    Trans: {orf['translation']}")
            print("-" * 60)
            
    except Exception as e:
        print(f"[-] ORF finder pipeline failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
