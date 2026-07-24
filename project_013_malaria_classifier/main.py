"""
Malaria Cell Classifier CLI Entrypoint
Author: Portfolio Creator
Description: CLI driver to execute data load, train the model, print reports,
             and save ROC plots.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from image_classifier import CellImageClassifier

def main():
    parser = argparse.ArgumentParser(
        description="Malaria Microscopy Cell Classifier - Predict parasitized cells from numeric image features."
    )
    parser.add_argument(
        "-i", "--input",
        default="cell_data.csv",
        help="Path to numerical features CSV (default: cell_data.csv)."
    )
    parser.add_argument(
        "-o", "--output",
        default="malaria_roc.png",
        help="Path to save the generated ROC curve plot (default: malaria_roc.png)."
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"[-] Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)

    print("=" * 60)
    print("Initializing Malaria Cell Feature Classifier Pipeline")
    print("=" * 60)

    classifier = CellImageClassifier(args.input)

    # 1. Preprocess
    try:
        X_train, X_test, y_train, y_test = classifier.preprocess()
        print(f"[+] Loaded cell records. Training size: {len(X_train)} | Test size: {len(X_test)}")
        print(f"    Selected Features: {', '.join(classifier.features)}")
    except Exception as e:
        print(f"[-] Preprocessing failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. Train
    print("[*] Fitting Random Forest model...")
    try:
        classifier.train(X_train, y_train)
        print("[+] Model training successful.")
    except Exception as e:
        print(f"[-] Model training failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 3. Evaluate
    print("[*] Running validation tests...")
    try:
        evals = classifier.evaluate(X_test, y_test)
        print("\n" + "=" * 60)
        print("Model Performance Classification Report")
        print("=" * 60)
        print(f"Accuracy: {evals['accuracy'] * 100:.2f}%")
        print(f"ROC Area Under Curve (AUC): {evals['auc']:.4f}")
        
        rep = evals["report"]
        print("\nClassification Report Summary:")
        print("-" * 50)
        print(f"  Uninfected Cells (Class 0):")
        print(f"    Precision: {rep['0']['precision']:.2f} | Recall: {rep['0']['recall']:.2f} | F1-score: {rep['0']['f1-score']:.2f}")
        print(f"  Parasitized Cells (Class 1):")
        print(f"    Precision: {rep['1']['precision']:.2f} | Recall: {rep['1']['recall']:.2f} | F1-score: {rep['1']['f1-score']:.2f}")
    except Exception as e:
        print(f"[-] Evaluation failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 4. Feature significance
    print("\n" + "=" * 60)
    print("Feature Significances (Feature Importances)")
    print("=" * 60)
    try:
        importances = classifier.get_feature_importances()
        for feature, weight in sorted(importances.items(), key=lambda x: x[1], reverse=True):
            print(f"  Feature: {feature:<26} | Weight: {weight:.4f}")
    except Exception as e:
        print(f"[-] Extraction failed: {e}", file=sys.stderr)

    # 5. Plot ROC
    print("\n" + "=" * 60)
    print("Generating ROC Evaluation Plot")
    print("=" * 60)
    try:
        print(f"[*] Saving ROC chart to: {args.output}")
        classifier.plot_roc_curve(evals['fpr'], evals['tpr'], evals['auc'], args.output)
        print("[+] Plot generation complete.")
    except Exception as e:
        print(f"[-] Plotting failed: {e}", file=sys.stderr)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
