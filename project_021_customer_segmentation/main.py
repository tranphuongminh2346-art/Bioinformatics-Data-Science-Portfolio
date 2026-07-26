"""
Customer Segmentation CLI Runner
Author: Portfolio Creator
Description: CLI driver to fit KMeans clusters, compute elbow metrics,
             and output client groups.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from segmentation import CustomerSegmenter

def main():
    parser = argparse.ArgumentParser(
        description="Customer Segmentation Tool - Unsupervised K-Means clustering."
    )
    parser.add_argument(
        "-i", "--input",
        default="customers.csv",
        help="Path to input customer CSV data (default: customers.csv)."
    )
    parser.add_argument(
        "-o", "--output",
        default="segments_map.png",
        help="Path to save generated plots (default: segments_map.png)."
    )
    parser.add_argument(
        "-k", "--clusters",
        type=int,
        default=3,
        help="Number of clusters K (default: 3)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Customer Segmentation Pipeline - KMeans Analysis")
    print("=" * 60)
    print(f"[*] Input File:  {args.input}")
    print(f"[*] Output Plot: {args.output}")
    print(f"[*] Target K:    {args.clusters}")

    try:
        segmenter = CustomerSegmenter(args.input)
        print(f"[+] Loaded {len(segmenter.df)} customer logs successfully.")
        
        # Fit K-Means
        print(f"[*] Fitting KMeans clustering with K={args.clusters}...")
        labels = segmenter.fit_clusters(args.clusters)
        
        # Evaluate elbow curve
        print("[*] Computing elbow inertias for K=1 to K=5...")
        inertias = segmenter.compute_elbow_curve(max_k=5)
        
        # Save plots
        print("[*] Exporting diagnostic plots...")
        segmenter.plot_segmentation(inertias, args.output)
        
        # Print cluster summaries
        print("\n" + "=" * 60)
        print("Cluster Characteristics Summary")
        print("=" * 60)
        
        # Calculate centroids and statistics
        means = segmenter.df.groupby('Cluster')[segmenter.features].mean()
        counts = segmenter.df.groupby('Cluster').size()
        
        for cluster_id in means.index:
            m_income = means.loc[cluster_id, 'AnnualIncome']
            m_score = means.loc[cluster_id, 'SpendingScore']
            size = counts.loc[cluster_id]
            print(f"[*] Cluster {cluster_id:2d} (Size: {size:3d}) | Mean Income: {m_income:6.2f}k$ | Mean Score: {m_score:6.2f}")
            
        print(f"\n[+] Diagnostic map saved to {args.output}")
        
    except Exception as e:
        print(f"[-] Segmentation failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
