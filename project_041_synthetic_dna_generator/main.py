"""
Markov DNA Simulator CLI
Author: Portfolio Creator
Description: CLI driver to generate synthetic sequences and analyze transition counts.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dna_generator import MarkovDNAGenerator

def main():
    parser = argparse.ArgumentParser(
        description="Markov DNA Sequence Generator - Generate genomic sequences from transition matrices."
    )
    parser.add_argument(
        "-l", "--length",
        type=int,
        default=200,
        help="Target sequence length in base pairs (default: 200)."
    )
    parser.add_argument(
        "-m", "--model",
        default="cpg",
        choices=["uniform", "cpg"],
        help="Markov model type: uniform or cpg (default: cpg)."
    )
    parser.add_argument(
        "-s", "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility (default: 42)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Markov Chain Synthetic DNA Generator")
    print("=" * 60)
    print(f"[*] Model Choice: {args.model.upper()}")
    print(f"[*] Seq Length  : {args.length} bp")
    print(f"[*] Random Seed : {args.seed}")

    try:
        generator = MarkovDNAGenerator(seed=args.seed)
        
        print("[*] Simulating DNA sequence...")
        sequence = generator.generate_sequence(args.length, model_type=args.model)
        
        print("\nGenerated Sequence (truncated at 100 bp):")
        print(sequence[:100] + ("..." if len(sequence) > 100 else ""))
        
        print("\n[*] Analyzing empirical transition frequencies matrix...")
        empirical = generator.calculate_transition_frequencies(sequence)
        
        # Display table
        bases = ['A', 'C', 'G', 'T']
        print("    " + "   ".join(bases))
        for idx, base in enumerate(bases):
            row_str = " ".join(f"{val:.3f}" for val in empirical[idx])
            print(f"{base} | {row_str}")
            
    except Exception as e:
        print(f"[-] Generation failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
