"""
Climate Temperature Anomaly CLI Runner
Author: Portfolio Creator
Description: CLI driver to execute timeseries seasonal decomposition
             and estimate decadal warming index slopes.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from time_series import TemperatureAnomalyAnalyzer

def main():
    parser = argparse.ArgumentParser(
        description="Temperature Anomaly Analyzer - Perform seasonal decomposition on climate timeseries."
    )
    parser.add_argument(
        "-i", "--input",
        default="temperature_anomaly.csv",
        help="Path to input temperature anomaly CSV (default: temperature_anomaly.csv)."
    )
    parser.add_argument(
        "-o", "--output",
        default="anomaly_decomposition.png",
        help="Path to save output decomposition plot (default: anomaly_decomposition.png)."
    )
    parser.add_argument(
        "-p", "--period",
        type=int,
        default=12,
        help="Seasonal cycle period in steps/months (default: 12)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Climate Temperature Anomaly Time Series Analyzer")
    print("=" * 60)
    print(f"[*] Input Data:      {args.input}")
    print(f"[*] Output Plot:     {args.output}")
    print(f"[*] Seasonal Period: {args.period} steps")

    try:
        analyzer = TemperatureAnomalyAnalyzer(args.input)
        print(f"[+] Loaded {len(analyzer.df)} monthly anomaly logs.")
        
        # Calculate Trend
        print("[*] Computing linear regression warming trend...")
        slope = analyzer.calculate_trend_slope()
        
        # Express as decadal rate (120 months)
        decadal_rate = slope * 120
        
        # Run decomposition
        print("[*] Running additive seasonal decomposition...")
        trend, seasonal, resid = analyzer.decompose_series(period=args.period)
        
        print("\n" + "=" * 60)
        print("Time Series Trend Analysis Results")
        print("=" * 60)
        print(f"[*] Calculated slope per step  : {slope:+.6f} °C/month")
        print(f"[*] Decadal Warming Rate Index : {decadal_rate:+.4f} °C/decade")
        
        # Save plots
        print("\n[*] Exporting 4-panel decomposition dashboard...")
        analyzer.plot_analysis(args.output)
        print(f"[+] Diagnostic plots saved successfully.")
        
    except Exception as e:
        print(f"[-] Pipeline execution failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
