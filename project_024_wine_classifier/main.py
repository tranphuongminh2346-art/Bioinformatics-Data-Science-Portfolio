"""
Wine Quality Decision Tree CLI Runner
Author: Portfolio Creator
Description: CLI driver to fit decision trees, print classification reports,
             and save tree split diagrams.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from wine_classifier import WineQualityClassifier

def main():
    parser = argparse.ArgumentParser(
        description="Wine Quality Classifier - Predict wine quality grades using Decision Trees."
    )
    parser.add_argument(
        "-i", "--input",
        default="wine_quality.csv",
        help="Path to input wine chemical CSV data (default: wine_quality.csv)."
    )
    parser.add_argument(
        "-o", "--output",
        default="wine_tree.png",
        help="Path to save decision tree visualization (default: wine_tree.png)."
    )
    parser.add_argument(
        "-d", "--depth",
        type=int,
        default=3,
        help="Max depth of the decision tree (default: 3)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Wine Quality Decision Tree Classification Pipeline")
    print("=" * 60)
    print(f"[*] Input File:  {args.input}")
    print(f"[*] Output Plot: {args.output}")
    print(f"[*] Max Depth:   {args.depth}")

    try:
        classifier = WineQualityClassifier(args.input)
        print(f"[+] Loaded {len(classifier.df)} wine samples.")
        
        # Train model
        print("[*] Training Decision Tree Classifier...")
        X_test, y_test = classifier.train_model(max_depth=args.depth)
        
        # Evaluate model
        print("[*] Evaluating classifier metrics...")
        metrics = classifier.evaluate_model(X_test, y_test)
        
        # Output results
        print("\n" + "=" * 60)
        print("Model Classification Scores")
        print("=" * 60)
        print(f"[*] Accuracy Score: {metrics['accuracy'] * 100:.2f}%")
        
        print("\nConfusion Matrix:")
        print(metrics["confusion_matrix"])
        
        # Save plots
        print("\n[*] Exporting Decision Tree splits diagram...")
        classifier.plot_decision_tree(args.output)
        print(f"[+] Splits diagram saved to {args.output}")
        
    except Exception as e:
        print(f"[-] Pipeline execution failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
