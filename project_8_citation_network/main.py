"""
PubMed Citation Network CLI Runner
Author: Portfolio Creator
Description: CLI driver to parse PubMed citation records, compute graph centrality and PageRank,
             find shortest citation paths, and export graph visualizations.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from citation_network import CitationNetwork

def main():
    parser = argparse.ArgumentParser(
        description="PubMed Citation Network Analyzer - Build DiGraphs and evaluate PageRank citation impact."
    )
    parser.add_argument(
        "-i", "--input",
        default="citations.json",
        help="Path to input citations JSON file (default: citations.json)."
    )
    parser.add_argument(
        "-o", "--output",
        default="citation_graph.png",
        help="Path to save the generated graph plot (default: citation_graph.png)."
    )

    args = parser.parse_args()

    # Check input json
    if not os.path.exists(args.input):
        print(f"Error: Input JSON file '{args.input}' does not exist.", file=sys.stderr)
        sys.exit(1)

    print("=" * 60)
    print("Initializing PubMed Citation Network Analyzer")
    print("=" * 60)

    try:
        net = CitationNetwork(args.input)
    except Exception as e:
        print(f"[-] Loading network failed: {e}", file=sys.stderr)
        sys.exit(1)

    num_nodes = net.graph.number_of_nodes()
    num_edges = net.graph.number_of_edges()
    print(f"[+] Directed graph constructed successfully:")
    print(f"    Total Nodes (Papers): {num_nodes}")
    print(f"    Total Edges (Citations): {num_edges}")

    if num_nodes == 0:
        print("[-] Graph contains no nodes. Exiting.", file=sys.stderr)
        sys.exit(1)

    # 1. In-degree Citation Counts
    print("\n" + "=" * 60)
    print("Citation Count Ranking (In-Degree Centrality)")
    print("=" * 60)
    
    in_degrees = net.get_citation_counts()
    sorted_deg = sorted(in_degrees.items(), key=lambda x: x[1], reverse=True)
    
    for rank, (pmid, count) in enumerate(sorted_deg, 1):
        meta = net.metadata[pmid]
        print(f"  {rank}. PMID: {pmid:<10} | Citations: {count:<2} | Title: {meta['title'][:50]}...")

    # 2. PageRank Calculations
    print("\n" + "=" * 60)
    print("PageRank Authority Influence Ranking")
    print("=" * 60)
    
    pr = net.calculate_pagerank()
    sorted_pr = sorted(pr.items(), key=lambda x: x[1], reverse=True)
    
    for rank, (pmid, score) in enumerate(sorted_pr, 1):
        meta = net.metadata[pmid]
        print(f"  {rank}. PMID: {pmid:<10} | PageRank: {score:.4f} | Title: {meta['title'][:50]}...")

    # 3. Path Search Demo
    print("\n" + "=" * 60)
    print("Citation Pathway Analysis (Shortest Directed Path)")
    print("=" * 60)
    
    # Trace Bowtie 2 (22247279) back to BLAST (2231712)
    source_pmid = "22247279"
    target_pmid = "2231712"
    
    if source_pmid in net.metadata and target_pmid in net.metadata:
        path = net.find_shortest_citation_path(source_pmid, target_pmid)
        if path:
            path_titles = [f"{net.metadata[p]['authors'].split(',')[0]} ({net.metadata[p]['year']})" for p in path]
            print(f"Citation Chain: Bowtie 2 -> BLAST")
            print("  " + "  ===>  ".join(path_titles))
        else:
            print(f"[-] No citation path exists between PMID {source_pmid} and {target_pmid}.")
    else:
        print("[!] Nodes not found in current dataset segment.")

    # 4. Save visualization
    print("\n" + "=" * 60)
    print("Generating Citation Graph Plot")
    print("=" * 60)
    try:
        print(f"[*] Exporting springs network layout to: {args.output}")
        net.plot_network(args.output)
        print("[+] Network graph plot successfully saved.")
    except Exception as e:
        print(f"[-] Graph plotting failed: {e}", file=sys.stderr)

    print("\nAnalysis complete.")

if __name__ == "__main__":
    main()
