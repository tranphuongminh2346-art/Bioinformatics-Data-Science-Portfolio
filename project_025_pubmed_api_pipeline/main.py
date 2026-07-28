"""
PubMed API Pipeline CLI
Author: Portfolio Creator
Description: CLI driver to query PubMed API literature databases,
             parse metadata formats, and write CSV logs.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pubmed_fetcher import PubMedFetcher

def main():
    parser = argparse.ArgumentParser(
        description="PubMed API Search Pipeline - Fetch and log scientific papers."
    )
    parser.add_argument(
        "-q", "--query",
        default="bioinformatics",
        help="Search query keyword for PubMed search (default: bioinformatics)."
    )
    parser.add_argument(
        "-o", "--output",
        default="pubmed_articles.csv",
        help="Path to save output CSV (default: pubmed_articles.csv)."
    )
    parser.add_argument(
        "-l", "--limit",
        type=int,
        default=3,
        help="Max number of articles to retrieve (default: 3)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("NCBI PubMed Literature Search API Pipeline")
    print("=" * 60)
    print(f"[*] Query Term:      {args.query}")
    print(f"[*] Max Records:     {args.limit}")
    print(f"[*] Output CSV:      {args.output}")

    try:
        fetcher = PubMedFetcher()
        
        print(f"[*] Searching PubMed for '{args.query}'...")
        pmids = fetcher.search_articles(args.query, retmax=args.limit)
        print(f"[+] Found PMIDs: {', '.join(pmids)}")
        
        print("[*] Retrieving article summaries...")
        articles = fetcher.fetch_summaries(pmids)
        
        print("\n" + "=" * 60)
        print("Retrieved Article Metadata")
        print("=" * 60)
        for idx, art in enumerate(articles):
            print(f"[{idx+1}] PMID   : {art['pmid']}")
            print(f"    Title  : {art['title']}")
            print(f"    Journal: {art['journal']} ({art['pub_date']})")
            print(f"    Authors: {art['authors']}")
            print("-" * 60)
            
        print(f"[*] Exporting metadata to {args.output}...")
        fetcher.export_to_csv(articles, args.output)
        print(f"[+] Successfully exported {len(articles)} rows.")
        
    except Exception as e:
        print(f"[-] Pipeline failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
