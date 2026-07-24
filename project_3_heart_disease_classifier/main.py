"""
Heart Disease Predictor CLI Runner
Author: Portfolio Creator
Description: CLI driver to download dataset, train the classifier,
             generate diagnostic metric plots, and predict sample patient risk.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model import HeartDiseaseClassifier

def main():
    parser = argparse.ArgumentParser(
        description="Heart Disease Diagnostic Classifier - Download data, train Logistic Regression model, and evaluate."
    )
    parser.add_argument(
        "-d", "--data",
        default="heart.csv",
        help="Local file path for the heart disease dataset (default: heart.csv)."
    )
    parser.add_argument(
        "-c", "--confusion",
        default="confusion_matrix.png",
        help="Output path for the confusion matrix plot (default: confusion_matrix.png)."
    )
    parser.add_argument(
        "-r", "--roc",
        default="roc_curve.png",
        help="Output path for the ROC curve plot (default: roc_curve.png)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Initializing Heart Disease Diagnostic Classifier")
    print("=" * 60)

    clf = HeartDiseaseClassifier(args.data)

    # 1. Download & Preprocess
    try:
        X_train, X_test, y_train, y_test = clf.load_and_preprocess()
        print(f"[*] Preprocessing complete:")
        print(f"    Training samples: {len(X_train)}")
        print(f"    Testing samples: {len(X_test)}")
    except Exception as e:
        print(f"[-] Preprocessing failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. Train Model
    print("[*] Training Logistic Regression classifier...")
    clf.train(X_train, y_train)
    print("[+] Model training completed.")

    # 3. Evaluate Model
    print("[*] Evaluating model performance...")
    try:
        metrics = clf.evaluate(X_test, y_test)
        print("\n" + "=" * 60)
        print("Model Performance Metrics")
        print("=" * 60)
        print(f"Test Accuracy: {metrics['accuracy'] * 100:.2f}%")
        
        # Classification report summary
        rep = metrics["report"]
        print("\nClassification Report Summary:")
        print("-" * 50)
        print(f"  Class 0 (No Disease):")
        print(f"    Precision: {rep['0']['precision']:.3f} | Recall: {rep['0']['recall']:.3f} | F1-score: {rep['0']['f1-score']:.3f}")
        print(f"  Class 1 (Heart Disease):")
        print(f"    Precision: {rep['1']['precision']:.3f} | Recall: {rep['1']['recall']:.3f} | F1-score: {rep['1']['f1-score']:.3f}")
        
    except Exception as e:
        print(f"[-] Evaluation failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 4. Generate plots
    print("\n" + "=" * 60)
    print("Generating Diagnostics Visualizations")
    print("=" * 60)
    try:
        print(f"[*] Plotting Confusion Matrix to: {args.confusion}")
        print(f"[*] Plotting ROC Curve to: {args.roc}")
        clf.plot_evaluation(metrics, args.confusion, args.roc)
        print("[+] Plot generation successful.")
    except Exception as e:
        print(f"[-] Plotting failed: {e}", file=sys.stderr)

    # 5. Example Prediction Inference
    print("\n" + "=" * 60)
    print("Sample Patient Inference Demo")
    print("=" * 60)
    
    # Mock clinical features for a patient:
    # 1. age = 54
    # 2. sex = 1 (male)
    # 3. cp = 0 (typical angina)
    # 4. trestbps = 140 (mmHg rest BP)
    # 5. chol = 239 (mg/dl cholesterol)
    # 6. fbs = 0 (fasting blood sugar < 120)
    # 7. restecg = 1 (resting ecg showing hypertrophy)
    # 8. thalach = 160 (max heart rate)
    # 9. exang = 0 (no exercise induced angina)
    # 10. oldpeak = 1.2 (ST depression)
    # 11. slope = 2 (slope of peak exercise ST segment)
    # 12. ca = 0 (number of major vessels colored by fluoroscopy)
    # 13. thal = 2 (thalassemia: normal)
    sample_features = [54, 1, 0, 140, 239, 0, 1, 160, 0, 1.2, 2, 0, 2]
    
    try:
        pred, prob = clf.predict_risk(sample_features)
        print("Patient Clinical Profile:")
        print(f"  Age: {sample_features[0]} | Sex: {'Male' if sample_features[1] == 1 else 'Female'}")
        print(f"  Cholesterol: {sample_features[4]} mg/dL | Max Heart Rate: {sample_features[7]} bpm")
        print(f"  ST Depression: {sample_features[9]}")
        print("-" * 50)
        risk_label = "HIGH RISK (Heart Disease Detected)" if pred == 1 else "LOW RISK (No Heart Disease Detected)"
        print(f"Diagnostic Prediction: {risk_label}")
        print(f"Model Probability: {prob * 100:.2f}% risk")
    except Exception as e:
        print(f"[-] Inference failed: {e}", file=sys.stderr)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
