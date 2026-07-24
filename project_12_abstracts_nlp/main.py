"""
Clinical Text Miner CLI Runner
Author: Portfolio Creator
Description: Command-line script to load PubMed abstracts, run TF-IDF calculations,
             evaluate clinical sentiment, and print reports.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from text_miner import ClinicalTextMiner

def main():
    parser = argparse.ArgumentParser(
        description="Clinical Text Miner - Term weight analysis and outcomes sentiment classification."
    )
    parser.add_argument(
        "-i", "--input",
        default="abstracts.json",
        help="Path to abstracts JSON database (default: abstracts.json)."
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"[-] Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)

    print("=" * 60)
    print("Initializing Clinical Text Mining & NLP Pipeline")
    print("=" * 60)

    try:
        miner = ClinicalTextMiner(args.input)
    except Exception as e:
        print(f"[-] Loading failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 1. Term Weights (TF-IDF)
    print(f"[*] Calculating term TF-IDF weights over {len(miner.records)} abstracts...")
    try:
        term_df = miner.calculate_tfidf()
        print("\nTop 10 Significant Terms in Corpus (TF-IDF):")
        print("-" * 50)
        for idx, row in term_df.head(10).iterrows():
            print(f"  Rank #{idx+1:<2} | Term: {row['term']:<18} | Mean TF-IDF: {row['mean_tfidf']:.4f}")
    except Exception as e:
        print(f"[-] TF-IDF calculation failed: {e}", file=sys.stderr)

    # 2. Sentiment Classification
    print("\n" + "=" * 60)
    print("Clinical Outcomes Sentiment Analysis")
    print("=" * 60)
    try:
        evaluations = miner.analyze_sentiment()
        for idx, ev in enumerate(evaluations, 1):
            print(f"Abstract #{idx}: PMID: {ev['pmid']} | {ev['title']}")
            print(f"  Sentiment: {ev['sentiment_class']} (Score: {ev['polarity_score']})")
            if ev['positive_matches']:
                print(f"    Positive terms matched: {', '.join(set(ev['positive_matches']))}")
            if ev['negative_matches']:
                print(f"    Negative terms matched: {', '.join(set(ev['negative_matches']))}")
            print("-" * 50)
    except Exception as e:
        print(f"[-] Sentiment analysis failed: {e}", file=sys.stderr)

    print("\nNLP Analysis complete.")

if __name__ == "__main__":
    main()
