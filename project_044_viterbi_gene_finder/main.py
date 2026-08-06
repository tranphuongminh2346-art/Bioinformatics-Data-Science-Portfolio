"""
HMM Viterbi Gene Finder CLI
Author: Portfolio Creator
Description: CLI driver to run Viterbi decoding and identify genomic coding exons.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gene_finder import HMMGeneFinder

def main():
    parser = argparse.ArgumentParser(
        description="HMM Gene Finder - Predict exon/intron regions using Viterbi decoding."
    )
    parser.add_argument(
        "-i", "--input",
        default="eukaryote.fasta",
        help="Path to input DNA sequence FASTA (default: eukaryote.fasta)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Hidden Markov Model (HMM) Viterbi Eukaryotic Gene Finder")
    print("=" * 60)
    print(f"[*] Input DNA: {args.input}")

    try:
        finder = HMMGeneFinder(args.input)
        print(f"[+] Loaded DNA sequence: '{finder.header}' ({len(finder.sequence)} bp)")
        
        print("[*] Decoding hidden state sequence using Viterbi lattice path...")
        path, log_prob = finder.decode_viterbi(finder.sequence)
        
        print(f"[+] Decoded state sequence log probability: {log_prob:.4f}")
        
        print("\nExon Coordinates Parse Results:")
        exons = finder.parse_exons(path)
        print(f"Total Exons Found: {len(exons)}")
        print("-" * 60)
        
        for idx, (start, end) in enumerate(exons):
            segment = finder.sequence[start:end]
            # Calculate GC content
            gc_count = segment.count('G') + segment.count('C')
            gc_percent = (gc_count / len(segment)) * 100 if len(segment) > 0 else 0
            
            print(f"[{idx+1}] Exon Range: {start}-{end} bp | Length: {end - start} bp | GC: {gc_percent:.1f}%")
            print(f"    Sequence  : {segment[:50]}...")
            print("-" * 60)
            
    except Exception as e:
        print(f"[-] Gene finder failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
