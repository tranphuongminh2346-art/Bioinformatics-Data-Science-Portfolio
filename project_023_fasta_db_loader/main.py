"""
FASTA Header Parser & Database Loader CLI
Author: Portfolio Creator
Description: CLI driver to parse protein FASTA files, populate SQLite tables,
             and print statistics queries.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fasta_parser import read_fasta_records
from db_loader import ProteinDatabaseLoader

def main():
    parser = argparse.ArgumentParser(
        description="FASTA Header Parser & SQLite Loader - Parse genomic FASTA metadata into database tables."
    )
    parser.add_argument(
        "-i", "--input",
        default="proteins.fasta",
        help="Path to input FASTA file (default: proteins.fasta)."
    )
    parser.add_argument(
        "-d", "--db",
        default="proteins.db",
        help="Path to output SQLite database file (default: proteins.db)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("UniProt FASTA Metadata SQL Database Loader")
    print("=" * 60)
    print(f"[*] FASTA Source: {args.input}")
    print(f"[*] SQL Database: {args.db}")

    try:
        print("[*] Parsing FASTA protein sequences...")
        records = read_fasta_records(args.input)
        print(f"[+] Successfully parsed {len(records)} sequences from FASTA.")
        
        print("[*] Initializing SQLite tables...")
        loader = ProteinDatabaseLoader(args.db)
        
        print("[*] Loading records into SQL tables...")
        loaded = loader.load_records(records)
        print(f"[+] Loaded {loaded} records into SQLite.")
        
        # Query results
        print("\n" + "=" * 60)
        print("Sequence Summary Statistics by Organism")
        print("=" * 60)
        counts = loader.query_organism_counts()
        for org, count, avg_len in counts:
            print(f"[*] Organism: {org:30} | Sequences: {count:3d} | Avg Length: {avg_len:6.1f} aa")
            
        print("\n" + "=" * 60)
        print("Top Longest Protein Sequences")
        print("=" * 60)
        longest = loader.query_longest_proteins(limit=3)
        for acc, entry, name, seq_len in longest:
            print(f"[*] Accession: {acc:10} | Entry: {entry:15} | Length: {seq_len:4d} aa | Name: {name}")
            
    except Exception as e:
        print(f"[-] Pipeline execution failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
