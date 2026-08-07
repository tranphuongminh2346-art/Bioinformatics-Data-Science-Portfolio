"""
ECG HRV Extractor CLI
Author: Portfolio Creator
Description: CLI driver to evaluate RR interval timeseries and log time/frequency HRV report.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from hrv_extractor import HRVExtractor

def main():
    parser = argparse.ArgumentParser(
        description="ECG HRV Extractor - Evaluate time-domain and frequency-domain heart rate variability."
    )
    parser.add_argument(
        "-i", "--input",
        default="ecg_rr_intervals.csv",
        help="Path to input RR intervals CSV (default: ecg_rr_intervals.csv)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("ECG Heart Rate Variability (HRV) Analysis Pipeline")
    print("=" * 60)
    print(f"[*] Input Data: {args.input}")

    try:
        extractor = HRVExtractor(args.input)
        print(f"[+] Loaded {len(extractor.rr_intervals)} RR intervals.")
        
        # Time Domain
        print("[*] Calculating time-domain metrics...")
        time_metrics = extractor.calculate_time_domain()
        
        # Frequency Domain
        print("[*] Calculating frequency-domain metrics (FFT PSD)...")
        freq_metrics = extractor.calculate_frequency_domain()
        
        print("\n" + "=" * 60)
        print("HRV Metrics Diagnostic Report")
        print("=" * 60)
        print("Time-Domain Metrics:")
        print(f"    - Mean RR Interval: {time_metrics['mean_rr']:.2f} ms")
        print(f"    - Mean Heart Rate  : {time_metrics['mean_hr']:.2f} bpm")
        print(f"    - SDNN             : {time_metrics['sdnn']:.2f} ms")
        print(f"    - RMSSD            : {time_metrics['rmssd']:.2f} ms")
        print(f"    - pNN50            : {time_metrics['pnn50']:.2f}%")
        print("-" * 60)
        print("Frequency-Domain Spectral Powers:")
        print(f"    - LF Power (0.04-0.15 Hz): {freq_metrics['lf_power']:.4f} ms²")
        print(f"    - HF Power (0.15-0.40 Hz): {freq_metrics['hf_power']:.4f} ms²")
        print(f"    - LF/HF Ratio            : {freq_metrics['lf_hf_ratio']:.4f}")
        
    except Exception as e:
        print(f"[-] HRV extraction failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
