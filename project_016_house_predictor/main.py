"""
California Housing Predictor CLI Entrypoint
Author: Portfolio Creator
Description: CLI driver to preprocess real estate logs, train the Ridge regression model,
             evaluate scores, print weights, and save predictions plot.
Language: English (100%)
"""

import argparse
import sys
import os
import numpy as np

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from price_predictor import HousePricePredictor

def main():
    parser = argparse.ArgumentParser(
        description="California Housing price predictor - Train Ridge regression and evaluate scores."
    )
    parser.add_argument(
        "-i", "--input",
        default="housing.csv",
        help="Path to real estate CSV file (default: housing.csv)."
    )
    parser.add_argument(
        "-o", "--output",
        default="price_fit.png",
        help="Path to save actual vs predicted plot image (default: price_fit.png)."
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"[-] Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)

    print("=" * 60)
    print("Initializing Real Estate Price Prediction Pipeline")
    print("=" * 60)

    predictor = HousePricePredictor(args.input)

    # 1. Preprocess
    try:
        X_train, X_test, y_train, y_test = predictor.preprocess()
        print(f"[+] Loaded records. Training samples: {len(X_train)} | Test samples: {len(X_test)}")
        print(f"    Features list: {', '.join(predictor.features)}")
    except Exception as e:
        print(f"[-] Preprocessing failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. Train
    print("[*] Training Ridge Regression model (alpha=1.0)...")
    try:
        predictor.train(X_train, y_train)
        print("[+] Model training successful.")
    except Exception as e:
        print(f"[-] Model training failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 3. Evaluate
    print("[*] Evaluating prediction metrics...")
    try:
        metrics = predictor.evaluate(X_test, y_test)
        print("\n" + "=" * 60)
        print("Model Regression Performance Scores")
        print("=" * 60)
        print(f"Mean Absolute Error (MAE): ${metrics['mae'] * 100000:.2f}  ({metrics['mae']:.4f} index)")
        print(f"Root Mean Squared Error (RMSE): ${metrics['rmse'] * 100000:.2f}  ({metrics['rmse']:.4f} index)")
        print(f"Coefficient of Determination (R2 Score): {metrics['r2']:.4f}")
    except Exception as e:
        print(f"[-] Evaluation failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 4. Coefficients Weights
    print("\n" + "=" * 60)
    print("Ridge Regression Weights (Feature Coefficients)")
    print("=" * 60)
    weights = dict(zip(predictor.features, predictor.model.coef_))
    for feat, coef in sorted(weights.items(), key=lambda x: abs(x[1]), reverse=True):
        print(f"  Feature: {feat:<18} | Coefficient: {coef:+.4f}")

    # 5. Plot
    print("\n" + "=" * 60)
    print("Generating Prediction Scatter Plot")
    print("=" * 60)
    try:
        print(f"[*] Saving price fit plot to: {args.output}")
        predictor.plot_predictions(y_test, metrics['predictions'], args.output)
        print("[+] Plot generation successful.")
    except Exception as e:
        print(f"[-] Plotting failed: {e}", file=sys.stderr)

    # 6. Single Prediction Demo
    print("\n" + "=" * 60)
    print("Single Property Valuation Demo")
    print("=" * 60)
    # Mock property: MedInc=5.0, HouseAge=30, AveRooms=6.0, AveBedrms=1.0, Population=450, AveOccup=2.2, Lat=37.8, Lon=-122.2
    demo_prop = np.array([5.0, 30.0, 6.0, 1.0, 450.0, 2.2, 37.8, -122.2])
    try:
        predicted_val = predictor.predict_value(demo_prop)
        print("Property Details:")
        print("  Median Income: $50,000 | House Age: 30 years | Avg Rooms: 6")
        print("  Population: 450 | Latitude: 37.8 | Longitude: -122.2")
        print("-" * 50)
        print(f"Predicted Median Value: ${predicted_val * 100000:,.2f}  ({predicted_val:.4f} index)")
    except Exception as e:
        print(f"[-] Inference failed: {e}", file=sys.stderr)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
