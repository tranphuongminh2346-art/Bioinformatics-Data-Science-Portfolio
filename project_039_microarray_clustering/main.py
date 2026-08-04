"""
Microarray Clustering CLI
Author: Portfolio Creator
Description: CLI driver to execute hierarchical clustering on gene matrices.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clustering import MicroarrayClusterer

def main():
    parser = argparse.ArgumentParser(
        description="Microarray Clusterer - Run hierarchical clustering on gene expression profiles."
    )
    parser.add_argument(
        "-i", "--input",
        default="microarray.csv",
        help="Path to input microarray CSV (default: microarray.csv)."
    )
    parser.add_argument(
        "-o", "--output",
        default="clustered_heatmap.png",
        help="Path to save output heatmap plot (default: clustered_heatmap.png)."
    )
    parser.add_argument(
        "-m", "--method",
        default="average",
        choices=["average", "single", "complete", "ward"],
        help="Linkage clustering method (default: average)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Microarray Gene Expression Hierarchical Clustering")
    print("=" * 60)
    print(f"[*] Input File : {args.input}")
    print(f"[*] Method     : {args.method}")
    print(f"[*] Output Plot: {args.output}")

    try:
        clusterer = MicroarrayClusterer(args.input)
        print(f"[+] Loaded expression levels for {len(clusterer.genes)} genes across {len(clusterer.samples)} samples.")
        
        print("[*] Normalizing expressions via Z-Score row calculations...")
        clusterer.standardize_rows()
        
        print(f"[*] Computing linkage tree using '{args.method}' method...")
        clusterer.compute_linkage(method=args.method)
        
        print("[*] Generating dendrogram heat map diagram...")
        clusterer.plot_heatmap(args.output)
        print(f"[+] Heatmap successfully exported to {args.output}")
        
    except Exception as e:
        print(f"[-] Clustering failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
