"""
Customer Churn CLI Runner
Author: Portfolio Creator
Description: CLI driver to preprocess churn log records, train a Random Forest model,
             export feature significance charts, and predict customer churn risk.
Language: English (100%)
"""

import argparse
import sys
import os
import pandas as pd

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from churn_model import CustomerChurnPredictor

def main():
    parser = argparse.ArgumentParser(
        description="Customer Churn Prediction Pipeline - Train Random Forest model and analyze feature significance."
    )
    parser.add_argument(
        "-i", "--input",
        default="churn_data.csv",
        help="Path to the input customer CSV file (default: churn_data.csv)."
    )
    parser.add_argument(
        "-o", "--output",
        default="feature_importances.png",
        help="Path to save the generated feature importances plot (default: feature_importances.png)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Initializing Customer Churn Prediction Pipeline")
    print("=" * 60)

    predictor = CustomerChurnPredictor(args.input)

    # 1. Preprocess
    try:
        X_train, X_test, y_train, y_test = predictor.load_and_preprocess()
        print(f"[*] Data preprocessing completed:")
        print(f"    Training samples: {len(X_train)}")
        print(f"    Testing samples: {len(X_test)}")
        print(f"    Encoded Features: {', '.join(predictor.feature_names)}")
    except Exception as e:
        print(f"[-] Preprocessing failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. Train Model
    print("[*] Training Random Forest Classifier (100 estimators)...")
    try:
        predictor.train(X_train, y_train)
        print("[+] Model training completed.")
    except Exception as e:
        print(f"[-] Training failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 3. Evaluate
    print("[*] Evaluating model performance...")
    try:
        metrics = predictor.evaluate(X_test, y_test)
        print("\n" + "=" * 60)
        print("Model Performance Metrics")
        print("=" * 60)
        print(f"Test Accuracy: {metrics['accuracy'] * 100:.2f}%")
        
        rep = metrics["report"]
        print("\nClassification Report Summary:")
        print("-" * 50)
        print(f"  Class 0 (No Churn):")
        print(f"    Precision: {rep['0']['precision']:.2f} | Recall: {rep['0']['recall']:.2f} | F1-score: {rep['0']['f1-score']:.2f}")
        print(f"  Class 1 (Churned):")
        print(f"    Precision: {rep['1']['precision']:.2f} | Recall: {rep['1']['recall']:.2f} | F1-score: {rep['1']['f1-score']:.2f}")
    except Exception as e:
        print(f"[-] Evaluation failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 4. Feature importances plot
    print("\n" + "=" * 60)
    print("Generating Analytical Visualizations")
    print("=" * 60)
    try:
        print(f"[*] Exporting horizontal feature importance chart to: {args.output}")
        predictor.plot_feature_importances(args.output)
        print("[+] Plot generation successful.")
    except Exception as e:
        print(f"[-] Plotting failed: {e}", file=sys.stderr)

    # 5. Example Prediction Inference
    print("\n" + "=" * 60)
    print("Customer Churn Risk Prediction Demo")
    print("=" * 60)
    
    # Mock a high-risk customer profile:
    # tenure: 3, MonthlyCharges: 95.0, TotalCharges: 285.0
    # Contract_One year: 0, Contract_Two year: 0 (represents Month-to-month)
    # InternetService_Fiber optic: 1, InternetService_No: 0
    mock_customer = pd.DataFrame([{
        "tenure": 3,
        "MonthlyCharges": 95.0,
        "TotalCharges": 285.0,
        "Contract_One year": 0,
        "Contract_Two year": 0,
        "InternetService_Fiber optic": 1,
        "InternetService_No": 0
    }])
    
    # Re-order columns to match the trained features sequence
    mock_customer = mock_customer[predictor.feature_names]

    try:
        pred, prob = predictor.predict_churn(mock_customer)
        print("Customer Profile:")
        print("  Tenure: 3 months | Monthly Charges: $95.00 | Contract: Month-to-month")
        print("  Internet Service: Fiber optic")
        print("-" * 50)
        risk_label = "HIGH RISK (Potential Churn Detected)" if pred == 1 else "LOW RISK (Customer likely to stay)"
        print(f"Diagnostic Prediction: {risk_label}")
        print(f"Model Probability: {prob * 100:.2f}% churn risk")
    except Exception as e:
        print(f"[-] Inference failed: {e}", file=sys.stderr)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
