"""
Handwritten Digit Classifier CLI
Author: Portfolio Creator
Description: CLI driver to train Naive Bayes digit recognition models.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from digit_classifier import DigitClassifier

def main():
    parser = argparse.ArgumentParser(
        description="Handwritten Digit Naive Bayes Classifier - Predict digits from pixel arrays."
    )
    parser.add_argument(
        "-i", "--input",
        default="digits.csv",
        help="Path to input digits CSV data (default: digits.csv)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Handwritten Digit Classifier Pipeline - Gaussian Naive Bayes")
    print("=" * 60)
    print(f"[*] Input Data: {args.input}")

    try:
        classifier = DigitClassifier(args.input)
        print(f"[+] Loaded {len(classifier.df)} digit images ({len(classifier.features)} features).")
        
        # Train model
        print("[*] Training Gaussian Naive Bayes model...")
        X_test, y_test = classifier.train_model()
        
        # Evaluate model
        print("[*] Running testing validation evaluations...")
        metrics = classifier.evaluate_model(X_test, y_test)
        
        # Output results
        print("\n" + "=" * 60)
        print("Model Accuracy Performance Scores")
        print("=" * 60)
        print(f"[*] Classification Accuracy: {metrics['accuracy'] * 100:.2f}%")
        
        print("\nConfusion Matrix:")
        print(metrics["confusion_matrix"])
        
    except Exception as e:
        print(f"[-] Pipeline execution failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
