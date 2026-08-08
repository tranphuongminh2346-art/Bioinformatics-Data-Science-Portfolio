"""
BWT DNA Indexer CLI
Author: Portfolio Creator
Description: CLI driver to index DNA and search for query k-mers.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bwt_indexer import BWTIndexer

def main():
    parser = argparse.ArgumentParser(
        description="BWT DNA Indexer - Compress DNA and search for exact k-mer alignments."
    )
    parser.add_argument(
        "-s", "--sequence",
        default="GCATGCATGC",
        help="Input DNA sequence string (default: GCATGCATGC)."
    )
    parser.add_argument(
        "-q", "--query",
        default="ATG",
        help="Search k-mer query string (default: ATG)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Burrows-Wheeler Transform DNA Indexer & Matcher")
    print("=" * 60)
    print(f"[*] Input DNA: {args.sequence}")
    print(f"[*] Query    : {args.query}")

    try:
        indexer = BWTIndexer(args.sequence)
        print(f"[+] BWT String: {indexer.bwt_string}")
        print(f"[+] Suffix Array: {indexer.suffix_array}")
        
        # Test reconstruction
        print("[*] Reconstructing original DNA via Inverse BWT...")
        recovered = indexer.inverse_bwt()
        print(f"[+] Recovered DNA: {recovered}")
        
        # Search query
        print(f"[*] Searching for exact matches of k-mer '{args.query}'...")
        matches = indexer.search_kmer(args.query)
        print(f"[+] Found {len(matches)} match(es) at starting coordinate indexes: {matches}")
        
    except Exception as e:
        print(f"[-] BWT Indexer failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
