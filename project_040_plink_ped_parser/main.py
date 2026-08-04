"""
PLINK Pedigree Parser CLI
Author: Portfolio Creator
Description: CLI driver to parse pedigree data, check Mendelian errors, and print stats.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ped_parser import PLINKParser

def main():
    parser = argparse.ArgumentParser(
        description="PLINK PED/MAP Parser - Detect Mendelian inheritance discrepancies."
    )
    parser.add_argument(
        "-p", "--ped",
        default="genotypes.ped",
        help="Path to genotypes PED file (default: genotypes.ped)."
    )
    parser.add_argument(
        "-m", "--map",
        default="genotypes.map",
        help="Path to genotypes MAP file (default: genotypes.map)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("PLINK Pedigree Parser & Genotype QC Engine")
    print("=" * 60)
    print(f"[*] PED File: {args.ped}")
    print(f"[*] MAP File: {args.map}")

    try:
        parser_obj = PLINKParser(args.ped, args.map)
        print(f"[+] Loaded {len(parser_obj.markers)} genetic markers.")
        print(f"[+] Loaded {len(parser_obj.individuals)} individual genotypes.")
        
        # Check call rates
        print("[*] Computing marker call rates...")
        call_rates = parser_obj.calculate_call_rates()
        for marker, rate in call_rates.items():
            print(f"    - Marker: {marker:10} | Call Rate: {rate * 100:.2f}%")
            
        # Check Mendelian errors
        print("[*] Auditing pedigree inheritance links for Mendelian errors...")
        errors = parser_obj.check_mendelian_errors()
        
        print("\n" + "=" * 60)
        print("Mendelian Inheritance Audit Summary")
        print("=" * 60)
        print(f"[*] Total Errors Found: {len(errors)}")
        print("-" * 60)
        for idx, err in enumerate(errors):
            print(f"[{idx+1}] Locus: {err['marker']} | Offspring: {err['child_id']}")
            print(f"    - Child Genotype  : {err['child_gt']}")
            print(f"    - Father Genotype : {err['father_gt']} ({err['father_id']})")
            print(f"    - Mother Genotype : {err['mother_gt']} ({err['mother_id']})")
            print("-" * 60)
            
    except Exception as e:
        print(f"[-] Pedigree parser failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
