"""
DNA Motif Gibbs Sampler Finder CLI
Author: Portfolio Creator
Description: CLI driver to execute Gibbs Sampling motif finding on DNA sequences.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from motif_finder import GibbsMotifFinder

def main():
    parser = argparse.ArgumentParser(
        description="DNA Motif Finder - Discover conserved regions using Gibbs Sampling."
    )
    parser.add_argument(
        "-i", "--input",
        default="promoters.fasta",
        help="Path to input FASTA file (default: promoters.fasta)."
    )
    parser.add_argument(
        "-l", "--length",
        type=int,
        default=6,
        help="Target motif length L (default: 6)."
    )
    parser.add_argument(
        "-t", "--iterations",
        type=int,
        default=100,
        help="Number of sampler iterations (default: 100)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("DNA Promoter Motif Search - Gibbs Sampler Engine")
    print("=" * 60)
    print(f"[*] Input Sequences: {args.input}")
    print(f"[*] Motif Length L:  {args.length} bp")
    print(f"[*] Iterations:      {args.iterations}")

    try:
        finder = GibbsMotifFinder(args.input, motif_len=args.length)
        print(f"[+] Loaded {len(finder.sequences)} DNA sequences.")
        
        print("[*] Launching Gibbs Sampler optimization loop...")
        motifs, consensus = finder.find_motifs(iterations=args.iterations)
        
        print("\n" + "=" * 60)
        print("Discovered Sequence Motifs")
        print("=" * 60)
        for i, motif in enumerate(motifs):
            print(f"[*] Sequence {i+1} Motif : {motif}")
            
        print("-" * 60)
        print(f"[+] Consensus Motif : {consensus}")
        print("=" * 60)
        
    except Exception as e:
        print(f"[-] Motif finder execution failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
