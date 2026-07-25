"""
GC-Content Map Generator CLI
Author: Portfolio Creator
Description: CLI utility to map sliding window GC ratios, trace GC islands,
             and plot skew profiles.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gc_mapper import GCContentMapper

def main():
    parser = argparse.ArgumentParser(
        description="Genomic GC-Content & Skew Map Generator - Sliding window analysis."
    )
    parser.add_argument(
        "-i", "--input",
        default="genome.fasta",
        help="Path to input FASTA file (default: genome.fasta)."
    )
    parser.add_argument(
        "-o", "--output",
        default="gc_map.png",
        help="Path to save output chart (default: gc_map.png)."
    )
    parser.add_argument(
        "-w", "--window",
        type=int,
        default=50,
        help="Sliding window size in bp (default: 50)."
    )
    parser.add_argument(
        "-s", "--step",
        type=int,
        default=10,
        help="Sliding step size in bp (default: 10)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Genomic GC-Content & Skew Map Generator")
    print("=" * 60)
    print(f"[*] Input File:  {args.input}")
    print(f"[*] Output Plot: {args.output}")
    print(f"[*] Window Size: {args.window} bp | Step Size: {args.step} bp")

    try:
        mapper = GCContentMapper(args.input)
        print(f"[+] Loaded sequence header: '{mapper.header}'")
        print(f"[+] Total sequence length: {len(mapper.sequence)} bp")
        
        print("[*] Running sliding window calculations...")
        pos, gc, skew = mapper.calculate_gc_stats(args.window, args.step)
        
        # Calculate summary statistics
        avg_gc = sum(gc) / len(gc) if gc else 0.0
        print("\n" + "=" * 60)
        print("Sequence GC Profile Summary")
        print("=" * 60)
        print(f"[*] Total Windows Processed : {len(pos)}")
        print(f"[*] Genome-wide Average GC  : {avg_gc * 100:.2f}%")
        
        # Save visualization
        print("\n[*] Exporting chromosome landscape plots...")
        mapper.plot_map(pos, gc, skew, args.output)
        print(f"[+] Plot successfully saved to {args.output}")
        
    except Exception as e:
        print(f"[-] Pipeline failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
