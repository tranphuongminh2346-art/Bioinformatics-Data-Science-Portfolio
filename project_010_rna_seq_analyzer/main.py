"""
RNA-Seq Analyzer CLI Entrypoint
Author: Portfolio Creator
Description: CLI driver executing normalization, fold change analysis, t-tests,
             and saving differential expression Volcano plots.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from expression_analyzer import GeneExpressionAnalyzer

def main():
    parser = argparse.ArgumentParser(
        description="RNA-Seq Expression Analyzer - Run statistical tests and select biomarkers."
    )
    parser.add_argument(
        "-i", "--input",
        default="gene_counts.csv",
        help="Path to gene counts CSV file (default: gene_counts.csv)."
    )
    parser.add_argument(
        "-o", "--output",
        default="volcano_plot.png",
        help="Path to save the Volcano plot image (default: volcano_plot.png)."
    )
    parser.add_argument(
        "-p", "--pvalue",
        type=float,
        default=0.05,
        help="Alpha significance threshold (default: 0.05)."
    )
    parser.add_argument(
        "-f", "--foldchange",
        type=float,
        default=2.0,
        help="Linear Fold Change threshold (default: 2.0)."
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"[-] Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)

    print("=" * 60)
    print("Initializing RNA-Seq Differential Gene Expression Analyzer")
    print("=" * 60)

    try:
        analyzer = GeneExpressionAnalyzer(args.input)
        results = analyzer.analyze_differential_expression(
            p_threshold=args.pvalue,
            fc_threshold=args.foldchange
        )
    except Exception as e:
        print(f"[-] Pipeline failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Summarize stats
    total_genes = len(results)
    upregulated = results[results['regulation_status'] == 'Upregulated']
    downregulated = results[results['regulation_status'] == 'Downregulated']
    non_sig = results[results['regulation_status'] == 'Non-significant']

    print(f"[+] Loaded counts matrix: {args.input}")
    print(f"    Total Genes Analyzed: {total_genes}")
    print(f"    Significantly Upregulated (FC >= {args.foldchange}, p < {args.pvalue}): {len(upregulated)}")
    print(f"    Significantly Downregulated (FC <= 1/{args.foldchange}, p < {args.pvalue}): {len(downregulated)}")
    print(f"    Non-significant genes: {len(non_sig)}")

    # Print Top 5 Upregulated Genes
    print("\n" + "=" * 60)
    print("Top 5 Significantly Upregulated Genes")
    print("=" * 60)
    top_up = upregulated.sort_values(by='log2_fold_change', ascending=False).head(5)
    for index, row in top_up.iterrows():
        print(f"  Gene: {row['gene_id']:<10} | Log2FC: {row['log2_fold_change']:>6.2f} | p-value: {row['p_value']:.4e}")

    # Print Top 5 Downregulated Genes
    print("\n" + "=" * 60)
    print("Top 5 Significantly Downregulated Genes")
    print("=" * 60)
    top_down = downregulated.sort_values(by='log2_fold_change', ascending=True).head(5)
    for index, row in top_down.iterrows():
        print(f"  Gene: {row['gene_id']:<10} | Log2FC: {row['log2_fold_change']:>6.2f} | p-value: {row['p_value']:.4e}")

    # Plot
    print("\n" + "=" * 60)
    print("Generating Differential Volcano Plot")
    print("=" * 60)
    try:
        print(f"[*] Saving Volcano plot to: {args.output}")
        analyzer.plot_volcano(args.output, p_threshold=args.pvalue, fc_threshold=args.foldchange)
        print("[+] Plot generation complete.")
    except Exception as e:
        print(f"[-] Plotting failed: {e}", file=sys.stderr)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
