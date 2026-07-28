"""
Movie Recommendation System CLI
Author: Portfolio Creator
Description: CLI driver to execute item-item collaborative filtering recommendations.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from recommender import MovieRecommender

def main():
    parser = argparse.ArgumentParser(
        description="Movie Recommender System - Item-based collaborative filtering."
    )
    parser.add_argument(
        "-i", "--input",
        default="ratings.csv",
        help="Path to ratings CSV file (default: ratings.csv)."
    )
    parser.add_argument(
        "-m", "--movie",
        default="Toy Story",
        help="Target movie title to get recommendations for (default: Toy Story)."
    )
    parser.add_argument(
        "-l", "--limit",
        type=int,
        default=3,
        help="Max number of recommendations to show (default: 3)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Item-Based Collaborative Filtering Movie Recommender")
    print("=" * 60)
    print(f"[*] Ratings Database: {args.input}")
    print(f"[*] Target Movie:     {args.movie}")
    print(f"[*] Max Suggestions:  {args.limit}")

    try:
        recommender = MovieRecommender(args.input)
        print(f"[+] Loaded {len(recommender.df)} ratings across {len(recommender.df['user_id'].unique())} users.")
        
        print("[*] Generating item-item cosine similarity matrices...")
        recommender.build_similarity_matrix()
        
        # Check target existence
        if args.movie not in recommender.similarity_df.index:
            print(f"[-] Error: '{args.movie}' not in movie indices.", file=sys.stderr)
            print("[*] Available movies in database:")
            for title in sorted(recommender.similarity_df.index):
                print(f"    - {title}")
            sys.exit(1)
            
        print(f"[*] Finding top-{args.limit} recommendations for '{args.movie}'...")
        recommendations = recommender.get_similar_movies(args.movie, limit=args.limit)
        
        print("\n" + "=" * 60)
        print(f"Recommendations for: {args.movie}")
        print("=" * 60)
        for idx, (title, score) in enumerate(recommendations):
            print(f"[{idx+1}] Movie: {title:25} | Cosine Similarity: {score:.4f}")
            
    except Exception as e:
        print(f"[-] Recommendation pipeline failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
