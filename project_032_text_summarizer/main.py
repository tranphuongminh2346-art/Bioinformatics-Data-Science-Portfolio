"""
Text Summarizer CLI Runner
Author: Portfolio Creator
Description: CLI driver to execute extractive TextRank summarizations.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from summarizer import TextSummarizer

def main():
    parser = argparse.ArgumentParser(
        description="Text Summarizer - Extract key sentences using PageRank centrality."
    )
    parser.add_argument(
        "-i", "--input",
        default="document.txt",
        help="Path to input text document (default: document.txt)."
    )
    parser.add_argument(
        "-l", "--limit",
        type=int,
        default=2,
        help="Max number of sentences in summary output (default: 2)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Extractive Text Summarizer Pipeline - TextRank")
    print("=" * 60)
    print(f"[*] Input File:      {args.input}")
    print(f"[*] Summary Length:  {args.limit} sentences")

    try:
        summarizer = TextSummarizer(args.input)
        print(f"[+] Parsed {len(summarizer.sentences)} sentences from document.")
        
        print("[*] Running TF-IDF sentence cosine PageRank...")
        summary = summarizer.summarize(limit=args.limit)
        
        print("\n" + "=" * 60)
        print("Generated Extractive Summary")
        print("=" * 60)
        for sent, score in summary:
            print(f"[+] (Score: {score:.4f}) {sent}")
            print()
        print("=" * 60)
        
    except Exception as e:
        print(f"[-] Summarizer failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("Execution complete.")

if __name__ == "__main__":
    main()
