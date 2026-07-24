"""
Weather ETL Pipeline CLI Runner
Author: Portfolio Creator
Description: CLI wrapper executing the weather ETL sequence, querying live API (or cache),
             loading data to SQLite, and generating trend diagrams.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from etl import WeatherETL
from db_loader import WeatherDatabaseLoader

def main():
    parser = argparse.ArgumentParser(
        description="Weather ETL Pipeline - Process hourly temperature logs from Open-Meteo."
    )
    parser.add_argument(
        "--latitude",
        type=float,
        help="Optional latitude coordinate for live API call (e.g., 51.5085 for London)."
    )
    parser.add_argument(
        "--longitude",
        type=float,
        help="Optional longitude coordinate for live API call (e.g., -0.1257)."
    )
    parser.add_argument(
        "-d", "--db",
        default="weather.db",
        help="Path to output SQLite database file (default: weather.db)."
    )
    parser.add_argument(
        "-o", "--output",
        default="weather_trend.png",
        help="Path to save the generated trend plot (default: weather_trend.png)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Initializing Weather Monitoring ETL Pipeline")
    print("=" * 60)

    etl = WeatherETL()

    # 1. Extract
    try:
        raw_data = etl.extract(args.latitude, args.longitude)
    except Exception as e:
        print(f"[-] Extraction failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. Transform
    print("[*] Preprocessing and transforming temperature logs...")
    try:
        clean_df = etl.transform(raw_data)
        print(f"    Transformed {len(clean_df)} hourly temperature records.")
    except Exception as e:
        print(f"[-] Transformation failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 3. Load
    print(f"[*] Loading processed weather records into SQLite DB: {args.db}")
    db_loader = WeatherDatabaseLoader(args.db)
    try:
        db_loader.load(clean_df)
        print("    Database loading complete.")
    except Exception as e:
        print(f"[-] Database load failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 4. Analyze (SQL Queries)
    print("\n" + "=" * 60)
    print("Database SQL Analytics Summary")
    print("=" * 60)
    try:
        stats = db_loader.get_summary_stats()
        if stats:
            avg_f = stats['avg_temp_c'] * 1.8 + 32.0
            max_f = stats['max_temp_c'] * 1.8 + 32.0
            min_f = stats['min_temp_c'] * 1.8 + 32.0
            
            print(f"Hourly Records Summary (from SQL):")
            print(f"  Average Temperature: {stats['avg_temp_c']:.2f}°C ({avg_f:.2f}°F)")
            print(f"  Maximum Temperature: {stats['max_temp_c']:.2f}°C ({max_f:.2f}°F)")
            print(f"  Minimum Temperature: {stats['min_temp_c']:.2f}°C ({min_f:.2f}°F)")
        else:
            print("[-] No summary metrics could be extracted.")
    except Exception as e:
        print(f"[-] Summary aggregation failed: {e}", file=sys.stderr)

    # 5. Plot
    print("\n" + "=" * 60)
    print("Generating Climate Trend Charts")
    print("=" * 60)
    try:
        print(f"[*] Exporting line chart plot to: {args.output}")
        etl.generate_plot(clean_df, args.output)
        print("[+] Plot generation successful.")
    except Exception as e:
        print(f"[-] Chart plotting failed: {e}", file=sys.stderr)

    print("\nPipeline execution complete.")

if __name__ == "__main__":
    main()
