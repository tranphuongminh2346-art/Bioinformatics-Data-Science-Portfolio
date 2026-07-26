"""
Web Log Anomaly Detector CLI
Author: Portfolio Creator
Description: CLI driver to execute Isolation Forest anomaly detection on server traffic.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from anomaly_detector import LogAnomalyDetector

def main():
    parser = argparse.ArgumentParser(
        description="Web Log Anomaly Detector - Flag suspicious access requests using Isolation Forest."
    )
    parser.add_argument(
        "-i", "--input",
        default="web_access.log",
        help="Path to the server access log file (default: web_access.log)."
    )
    parser.add_argument(
        "-c", "--contamination",
        type=float,
        default=0.15,
        help="Proportion of anomalies in the dataset (default: 0.15)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Web Server Access Log Anomaly Detector Pipeline")
    print("=" * 60)
    print(f"[*] Input Log:       {args.input}")
    print(f"[*] Contamination:   {args.contamination * 100:.1f}%")

    try:
        detector = LogAnomalyDetector(args.input)
        print(f"[+] Parsed {len(detector.df)} log lines successfully.")
        
        print("[*] Running Isolation Forest clustering...")
        detector.train_detector(contamination=args.contamination)
        
        anomalies = detector.get_anomalies()
        
        print("\n" + "=" * 60)
        print("Flagged Anomalous Traffic Records")
        print("=" * 60)
        print(f"Total Anomalies Flagged: {len(anomalies)} / {len(detector.df)}")
        print("-" * 60)
        
        for idx, row in anomalies.iterrows():
            print(f"[!] Anomaly #{idx+1} | Score: {row['AnomalyScore']:.4f}")
            print(f"    Line   : {row['raw_line']}")
            print(f"    Metrics: Status={row['status_code']}, Bytes={row['response_bytes']}, URL Len={row['url_length']}")
            print("-" * 60)
            
    except Exception as e:
        print(f"[-] Pipeline execution failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
