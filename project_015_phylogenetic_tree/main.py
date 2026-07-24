"""
UPGMA Phylogenetic Tree Runner CLI
Author: Portfolio Creator
Description: CLI entrypoint to read homologous sequences, compute Hamming distances,
             run UPGMA tree reconstruction, and print Newick paths.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from upgma import UPGMATreeReconstructor

def print_text_tree(node, indent=""):
    """Recursively draws a text-based ASCII tree for CLI visualization."""
    if node.is_leaf():
        print(f"{indent}└── {node.name} (Leaf)")
    else:
        print(f"{indent}├── {node.name} (Height: {node.distance:.4f})")
        print_text_tree(node.left, indent + "│   ")
        print_text_tree(node.right, indent + "│   ")

def main():
    parser = argparse.ArgumentParser(
        description="Phylogenetic Tree Reconstructor - Build evolutionary trees using UPGMA."
    )
    parser.add_argument(
        "-i", "--input",
        default="sequences.fasta",
        help="Path to input FASTA file containing aligned sequences (default: sequences.fasta)."
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"[-] Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)

    print("=" * 60)
    print("Initializing UPGMA Phylogenetic Tree Reconstructor")
    print("=" * 60)

    try:
        reconstructor = UPGMATreeReconstructor(args.input)
        print(f"[+] Loaded {len(reconstructor.names)} sequences from: {args.input}")
    except Exception as e:
        print(f"[-] Failed to load FASTA: {e}", file=sys.stderr)
        sys.exit(1)

    # 1. Print Distance Matrix
    print("\n" + "=" * 60)
    print("Calculated Pairwise Hamming Distance Matrix")
    print("=" * 60)
    try:
        matrix = reconstructor.calculate_distance_matrix()
        # Header
        print(f"{'':<14}", end="")
        for name in reconstructor.names:
            print(f"{name[:8]:^10}", end="")
        print()
        
        for idx, name in enumerate(reconstructor.names):
            print(f"{name[:12]:<14}", end="")
            for j in range(len(reconstructor.names)):
                print(f"{matrix[idx, j]:^10.4f}", end="")
            print()
    except Exception as e:
        print(f"[-] Matrix calculation failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. Reconstruct Tree
    print("\n" + "=" * 60)
    print("Reconstructing Phylogenetic Tree (UPGMA)")
    print("=" * 60)
    try:
        root = reconstructor.reconstruct()
        print("[+] Tree reconstruction complete.")
        
        print("\nNewick Format String:")
        print("-" * 50)
        # Append ending semicolon as required by Newick standard
        print(f"{root.to_newick()};")
        
        print("\nASCII Evolutionary Tree Layout:")
        print("-" * 50)
        print_text_tree(root)
    except Exception as e:
        print(f"[-] Reconstruction failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
