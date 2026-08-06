"""
Chemical Solubility Predictor CLI
Author: Portfolio Creator
Description: CLI driver to fit solubility regressions and predict LogS parameters.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from solubility_predictor import SolubilityPredictor

def main():
    parser = argparse.ArgumentParser(
        description="Chemical Solubility Predictor - Fit Ridge model on molecular descriptors."
    )
    parser.add_argument(
        "-i", "--input",
        default="solubility.csv",
        help="Path to solubility CSV database (default: solubility.csv)."
    )
    parser.add_argument(
        "-o", "--output",
        default="solubility_fit.png",
        help="Path to save fit plot (default: solubility_fit.png)."
    )
    parser.add_argument(
        "-mw", "--weight",
        type=float,
        default=180.16,
        help="Molecular Weight (MW) of compound (default: 180.16)."
    )
    parser.add_argument(
        "-lp", "--logp",
        type=float,
        default=1.2,
        help="Octanol-water partition coefficient LogP (default: 1.2)."
    )
    parser.add_argument(
        "-rb", "--rotbonds",
        type=int,
        default=3,
        help="Rotatable Bonds count (default: 3)."
    )
    parser.add_argument(
        "-psa", "--psa",
        type=float,
        default=63.60,
        help="Polar Surface Area (PSA) in Å² (default: 63.60)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Chemical Solubility (LogS) Prediction Pipeline")
    print("=" * 60)
    print(f"[*] Input Data: {args.input}")
    print(f"[*] Output Plot: {args.output}")

    try:
        predictor = SolubilityPredictor(args.input)
        print(f"[+] Loaded {len(predictor.df)} chemical compounds.")
        
        # Train
        print("[*] Training Ridge regression model...")
        X_test, y_test = predictor.train_model()
        
        # Evaluate
        print("[*] Calculating R2 score and MSE validation metrics...")
        metrics = predictor.evaluate_model(X_test, y_test)
        
        print("\nModel Evaluation Summary:")
        print(f"    - Mean Squared Error (MSE): {metrics['mse']:.4f}")
        print(f"    - R2 Score (coefficient)  : {metrics['r2_score']:.4f}")
        
        print("\nModel Coefficients:")
        for feat, coef in zip(predictor.features, predictor.model.coef_):
            print(f"    - {feat:20}: {coef:+.4f}")
        print(f"    - Intercept           : {predictor.model.intercept_:+.4f}")
        
        # Predict target compound
        print("\n" + "=" * 60)
        print("Target Compound Solubility Prediction")
        print("=" * 60)
        descriptors = [args.weight, args.logp, args.rotbonds, args.psa]
        print(f"[*] Input: MW={args.weight:.2f} | LogP={args.logp:.2f} | RotBonds={args.rotbonds} | PSA={args.psa:.2f}")
        pred_logs = predictor.predict_solubility(descriptors)
        print(f"[+] Predicted Solubility (LogS): {pred_logs:+.4f}")
        
        # Plot
        print("\n[*] Exporting actual vs predicted fit plot...")
        predictor.plot_fit(X_test, y_test, args.output)
        print("[+] Fit scatter plot successfully exported.")
        
    except Exception as e:
        print(f"[-] Solubility predictor failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
