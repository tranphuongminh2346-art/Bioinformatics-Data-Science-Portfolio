"""
SMS Spam Filter CLI Runner
Author: Portfolio Creator
Description: CLI driver to execute SMS text spam classifications.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from spam_filter import SMSSpamFilter

def main():
    parser = argparse.ArgumentParser(
        description="SMS Spam Filter - Fit text classification models on SMS dataset."
    )
    parser.add_argument(
        "-i", "--input",
        default="spam_sms.csv",
        help="Path to input SMS CSV data (default: spam_sms.csv)."
    )
    parser.add_argument(
        "-m", "--message",
        default="Get free cash prizes and claim rewards now!",
        help="Custom text message to test classification (default: Get free cash prizes...)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("SMS Spam Filter Pipeline - TF-IDF & Logistic Regression")
    print("=" * 60)
    print(f"[*] Input Data: {args.input}")

    try:
        filter_obj = SMSSpamFilter(args.input)
        print(f"[+] Loaded {len(filter_obj.df)} SMS messages.")
        
        # Train model
        print("[*] Processing text vectors and training model...")
        X_test, y_test = filter_obj.train_model()
        
        # Evaluate model
        print("[*] Evaluating testing metrics...")
        metrics = filter_obj.evaluate_model(X_test, y_test)
        
        print("\n" + "=" * 60)
        print("Model Accuracy Performance Scores")
        print("=" * 60)
        print(f"[*] Classification Accuracy: {metrics['accuracy'] * 100:.2f}%")
        
        print("\nConfusion Matrix:")
        print(metrics["confusion_matrix"])
        
        # Predict custom message
        print("\n" + "=" * 60)
        print("Custom Message Classification Test")
        print("=" * 60)
        print(f"[*] Text: '{args.message}'")
        label, prob = filter_obj.predict_message(args.message)
        print(f"[+] Prediction : {label.upper()} (Spam Probability: {prob * 100:.2f}%)")
        
    except Exception as e:
        print(f"[-] Pipeline execution failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
