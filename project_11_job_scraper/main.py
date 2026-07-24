"""
Jobs Listing Scraper Pipeline CLI
Author: Portfolio Creator
Description: Command-line script to parse job board HTML, clean attributes,
             load database records, and query statistical summaries.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from job_parser import JobListingParser
from db_loader import JobDatabaseLoader

def main():
    parser = argparse.ArgumentParser(
        description="Bioinformatics Job Listings Scraper - Parse job postings and query salaries."
    )
    parser.add_argument(
        "-i", "--input",
        default="jobs.html",
        help="Path to job listings HTML page (default: jobs.html)."
    )
    parser.add_argument(
        "-d", "--db",
        default="jobs.db",
        help="Path to SQLite database file (default: jobs.db)."
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"[-] Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)

    print("=" * 60)
    print("Initializing Job Listings HTML Scraper Pipeline")
    print("=" * 60)

    # 1. Parse HTML
    print(f"[*] Parsing job cards from HTML file: {args.input}")
    try:
        parser_engine = JobListingParser(args.input)
        jobs = parser_engine.scrape_jobs()
        print(f"[+] Successfully extracted {len(jobs)} job listing(s).")
    except Exception as e:
        print(f"[-] Scrape failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. Database Load
    print(f"[*] Loading listings into SQLite database: {args.db}")
    db_loader = JobDatabaseLoader(args.db)
    try:
        db_loader.load_jobs(jobs)
        print("[+] Database loading complete.")
    except Exception as e:
        print(f"[-] Database loading failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 3. SQL Analytics
    print("\n" + "=" * 60)
    print("Location Salary Statistics (SQL Aggregated)")
    print("=" * 60)
    try:
        loc_df = db_loader.get_salary_by_location()
        for idx, row in loc_df.iterrows():
            print(f"  Location: {row['location']:<20} | Jobs: {row['job_count']:<2} | Avg Salary: ${row['average_salary']:,.2f}")
    except Exception as e:
        print(f"[-] Location stats query failed: {e}", file=sys.stderr)

    print("\n" + "=" * 60)
    print("Top 3 Highest-Paying Biotech Positions")
    print("=" * 60)
    try:
        top_df = db_loader.get_highest_paying_jobs(limit=3)
        for idx, row in top_df.iterrows():
            print(f"  Title: {row['title']:<38} | Company: {row['company']:<25} | Salary: ${row['avg_salary']:,.2f}")
    except Exception as e:
        print(f"[-] Top paying query failed: {e}", file=sys.stderr)

    print("\nPipeline execution complete.")

if __name__ == "__main__":
    main()
