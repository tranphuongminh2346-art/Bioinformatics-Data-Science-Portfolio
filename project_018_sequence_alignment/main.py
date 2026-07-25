"""
Needleman-Wunsch Alignment CLI Runner
Author: Portfolio Creator
Description: CLI driver to execute global sequence alignments, customize scoring parameters,
             and print DP grids and traceback paths.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from needleman_wunsch import NeedlemanWunschAligner

def main():
    parser = argparse.ArgumentParser(
        description="Needleman-Wunsch Aligner - Compute global sequence alignment scoring matrices."
    )
    parser.add_argument(
        "-s1", "--seq1",
        default="HEAGAWGHEE",
        help="First sequence string (default: HEAGAWGHEE)."
    )
    parser.add_argument(
        "-s2", "--seq2",
        default="PAWHEAE",
        help="Second sequence string (default: PAWHEAE)."
    )
    parser.add_argument(
        "-m", "--match",
        type=int,
        default=2,
        help="Score for matching characters (default: 2)."
    )
    parser.add_argument(
        "-mis", "--mismatch",
        type=int,
        default=-1,
        help="Penalty for mismatching characters (default: -1)."
    )
    parser.add_argument(
        "-g", "--gap",
        type=int,
        default=-2,
        help="Penalty for gap insertions (default: -2)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Initializing Needleman-Wunsch Global Aligner")
    print("=" * 60)
    print(f"[*] Sequence 1: {args.seq1} (Length: {len(args.seq1)})")
    print(f"[*] Sequence 2: {args.seq2} (Length: {len(args.seq2)})")
    print(f"[*] Scoring Scheme: Match: +{args.match} | Mismatch: {args.mismatch} | Gap: {args.gap}")

    aligner = NeedlemanWunschAligner(
        match_score=args.match,
        mismatch_penalty=args.mismatch,
        gap_penalty=args.gap
    )

    try:
        score, al1, al2 = aligner.align(args.seq1, args.seq2)
        print("\n" + "=" * 60)
        print("Dynamic Programming Scoring Grid")
        print("=" * 60)
        
        # Draw columns headers
        print("      -  ", end="")
        for char in args.seq2:
            print(f"{char:^4}", end="")
        print()
        
        # Row-by-row matrix print
        for i in range(len(args.seq1) + 1):
            row_char = "-" if i == 0 else args.seq1[i - 1]
            print(f" {row_char:^3} ", end="")
            for j in range(len(args.seq2) + 1):
                val = aligner.score_matrix[i, j]
                print(f"{int(val):^4}", end="")
            print()
            
        print("\n" + "=" * 60)
        print("Optimal Global Alignment Results")
        print("=" * 60)
        print(f"Alignment Score: {score:.1f}")
        print("-" * 50)
        print(aligner.format_alignment(al1, al2))
    except Exception as e:
        print(f"[-] Alignment computation failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
