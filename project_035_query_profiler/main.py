"""
Database Query Profiler CLI
Author: Portfolio Creator
Description: CLI driver to populate mock SQLite records, construct indexes,
             and print benchmarking latency statistics.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from query_profiler import DatabaseProfiler

def main():
    parser = argparse.ArgumentParser(
        description="Database Indexing & Query Profiler - Profile SQL query speeds."
    )
    parser.add_argument(
        "-d", "--db",
        default="profiler.db",
        help="Path to temporary SQLite database (default: profiler.db)."
    )
    parser.add_argument(
        "-o", "--output",
        default="indexing_benchmark.png",
        help="Path to save latency comparison plot (default: indexing_benchmark.png)."
    )
    parser.add_argument(
        "-n", "--records",
        type=int,
        default=5000,
        help="Number of records to insert (default: 5000)."
    )
    parser.add_argument(
        "-l", "--lookups",
        type=int,
        default=100,
        help="Number of search lookup benchmarks to run (default: 100)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("SQLite Indexing & Query Profiling Benchmark")
    print("=" * 60)
    print(f"[*] Database file : {args.db}")
    print(f"[*] Target Records: {args.records}")
    print(f"[*] Lookups Run   : {args.lookups}")
    print(f"[*] Saving plot to: {args.output}")

    try:
        profiler = DatabaseProfiler(args.db)
        
        print(f"[*] Populating {args.records} user records...")
        profiler.populate_data(n_records=args.records)
        
        print("[*] Creating B-tree index on email column...")
        profiler.create_index()
        
        print("[*] Running query search lookups benchmarks...")
        unindexed, indexed = profiler.run_benchmark(n_lookups=args.lookups)
        
        # Calculate stats
        avg_unindexed = sum(unindexed) / len(unindexed)
        avg_indexed = sum(indexed) / len(indexed)
        speedup = avg_unindexed / avg_indexed if avg_indexed > 0 else 1.0
        
        print("\n" + "=" * 60)
        print("Performance Benchmark Results Summary")
        print("=" * 60)
        print(f"[*] Avg Unindexed Latency (Full Scan) : {avg_unindexed:8.4f} ms")
        print(f"[*] Avg Indexed Latency (B-Tree Search): {avg_indexed:8.4f} ms")
        print(f"[*] Speedup Multiplier Factor          : {speedup:8.1f}x faster")
        
        print("\n[*] Saving latency boxplots...")
        profiler.plot_benchmark(unindexed, indexed, args.output)
        print("[+] Output chart saved successfully.")
        
    except Exception as e:
        print(f"[-] Profiler failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
