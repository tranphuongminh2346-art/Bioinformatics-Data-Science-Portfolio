"""
Breast Cancer SVM Classifier CLI
Author: Portfolio Creator
Description: CLI driver to train Support Vector Machine models,
             evaluate metrics, and plot decision boundaries.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cancer_classifier import CancerClassifier

def main():
    parser = argparse.ArgumentParser(
        description="Breast Cancer Tumor Classifier - Support Vector Machine model pipeline."
    )
    parser.add_argument(
        "-i", "--input",
        default="cancer_data.csv",
        help="Path to input cancer diagnostic CSV (default: cancer_data.csv)."
    )
    parser.add_argument(
        "-o", "--output",
        default="decision_boundary.png",
        help="Path to save decision boundary plot (default: decision_boundary.png)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Breast Cancer Tumor Classification Pipeline - SVM (RBF)")
    print("=" * 60)
    print(f"[*] Input Data:  {args.input}")
    print(f"[*] Output Plot: {args.output}")

    try:
        classifier = CancerClassifier(args.input)
        print(f"[+] Loaded {len(classifier.df)} diagnostic records.")
        
        # Train model
        print("[*] Training SVM classifier model...")
        X_test, y_test = classifier.train_model()
        
        # Evaluate model
        print("[*] Running testing validation evaluations...")
        metrics = classifier.evaluate_model(X_test, y_test)
        
        # Output results
        print("\n" + "=" * 60)
        print("Model Accuracy Performance Scores")
        print("=" * 60)
        print(f"[*] Classification Accuracy: {metrics['accuracy'] * 100:.2f}%")
        print(f"[*] Area Under ROC (AUC)    : {metrics['auc']:.4f}")
        
        print("\nConfusion Matrix:")
        print(metrics["confusion_matrix"])
        
        # Save plots
        print("\n[*] Exporting decision boundary plot...")
        classifier.plot_decision_boundary(args.output)
        print(f"[+] Decision boundary saved to {args.output}")
        
    except Exception as e:
        print(f"[-] Pipeline execution failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
