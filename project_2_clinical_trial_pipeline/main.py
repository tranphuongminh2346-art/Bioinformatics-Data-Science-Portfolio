"""
Clinical Trial ETL Pipeline Runner
Author: Portfolio Creator
Description: CLI entry point to run clinical trial ETL operations.
Language: English (100%)
"""

import argparse
import sys
import os
# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pipeline import ClinicalTrialPipeline

def main():
    parser = argparse.ArgumentParser(
        description="Clinical Trial ETL Data Pipeline - Parse, clean, load to SQLite, and analyze clinical trial records."
    )
    parser.add_argument(
        "-i", "--input",
        default="trials_data.json",
        help="Path to the input JSON file containing raw trial records (default: trials_data.json)."
    )
    parser.add_argument(
        "-d", "--db",
        default="trials.db",
        help="Path to the output SQLite database file (default: trials.db)."
    )
    parser.add_argument(
        "-o", "--output",
        default="phase_chart.png",
        help="Path to save the generated phase distribution chart (default: phase_chart.png)."
    )

    args = parser.parse_args()

    # Verify input JSON exists
    if not os.path.exists(args.input):
        print(f"Error: Input JSON file '{args.input}' does not exist.", file=sys.stderr)
        sys.exit(1)

    print("=" * 60)
    print("Initializing Clinical Trial ETL Pipeline")
    print("=" * 60)
    
    pipeline = ClinicalTrialPipeline(args.db)

    # 1. Extract
    print(f"[*] Extracting raw records from: {args.input}")
    try:
        raw_df = pipeline.extract(args.input)
        print(f"    Extracted {len(raw_df)} raw records.")
    except Exception as e:
        print(f"[-] Extraction failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. Transform
    print("[*] Transforming and cleaning records...")
    try:
        clean_df = pipeline.transform(raw_df)
        skipped = len(raw_df) - len(clean_df)
        print(f"    Cleaned {len(clean_df)} records (skipped {skipped} invalid records).")
    except Exception as e:
        print(f"[-] Transformation failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 3. Load
    print(f"[*] Loading cleaned records into SQLite DB: {args.db}")
    try:
        pipeline.load(clean_df)
        print("    Data loading successful.")
    except Exception as e:
        print(f"[-] Database loading failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 4. Analyze (SQL Queries)
    print("\n" + "=" * 60)
    print("Database SQL Aggregations & Analysis")
    print("=" * 60)

    try:
        # Phase distribution
        phase_dist = pipeline.query_phase_distribution()
        print("\nTrial Count & Enrollment by Phase (SQL):")
        print("-" * 50)
        for _, row in phase_dist.iterrows():
            print(f"  {row['phase']}: {row['trial_count']} trials (Total Enrollment: {row['total_enrollment']:,})")
            
        # Top conditions
        top_conditions = pipeline.query_top_conditions(limit=3)
        print("\nTop Conditions Studied (SQL):")
        print("-" * 50)
        for _, row in top_conditions.iterrows():
            print(f"  {row['condition']}: {row['trial_count']} trials")
            
    except Exception as e:
        print(f"[-] Database querying failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 5. Visualize
    print("\n" + "=" * 60)
    print("Generating Analytics Visualization")
    print("=" * 60)
    
    try:
        print(f"[*] Plotting phase distribution to: {args.output}")
        pipeline.plot_phase_distribution(phase_dist, args.output)
        print("    Plot successfully generated.")
    except Exception as e:
        print(f"[-] Visualization generation failed: {e}", file=sys.stderr)

    print("\nPipeline execution complete.")

if __name__ == "__main__":
    main()
