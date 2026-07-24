"""
COVID-19 Time Series Runner CLI
Author: Portfolio Creator
Description: Command-line driver to execute daily COVID-19 differential transformations
             and generate trend dashboards.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from covid_analyzer import CovidTimeSeriesAnalyzer

def main():
    parser = argparse.ArgumentParser(
        description="COVID-19 Timeseries Dashboard - Process cumulative statistics to study daily dynamics."
    )
    parser.add_argument(
        "-i", "--input",
        default="covid_data.csv",
        help="Path to cumulative cases/deaths CSV file (default: covid_data.csv)."
    )
    parser.add_argument(
        "-o", "--output",
        default="covid_trends.png",
        help="Path to save the generated trend plot (default: covid_trends.png)."
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"[-] Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)

    print("=" * 60)
    print("Initializing COVID-19 Time Series Analyzer")
    print("=" * 60)

    try:
        analyzer = CovidTimeSeriesAnalyzer(args.input)
        df = analyzer.calculate_daily_metrics()
    except Exception as e:
        print(f"[-] Data processing failed: {e}", file=sys.stderr)
        sys.exit(1)

    total_cases = df['confirmed_cases'].iloc[-1]
    total_deaths = df['confirmed_deaths'].iloc[-1]
    max_daily_new = df['new_cases'].max()
    avg_growth = df['case_growth_rate'].mean()

    print(f"[+] Loaded records from: {args.input}")
    print(f"    Observation Days: {len(df)}")
    print(f"    Cumulative Cases: {total_cases}")
    print(f"    Cumulative Deaths: {total_deaths}")
    print(f"    Peak Daily New Cases: {max_daily_new:.0f}")
    print(f"    Average Case Growth Rate: {avg_growth * 100:.2f}%")

    print("\n" + "=" * 60)
    print("Generating Analytical Visualizations")
    print("=" * 60)
    try:
        print(f"[*] Saving dual-axis trend dashboard plot to: {args.output}")
        analyzer.plot_dashboard(args.output)
        print("[+] Dashboard plot successfully saved.")
    except Exception as e:
        print(f"[-] Plotting failed: {e}", file=sys.stderr)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
