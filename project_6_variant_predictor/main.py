"""
Genomic Variant Predictor CLI Runner
Author: Portfolio Creator
Description: CLI driver that executes VCF parsing, maps mutations to coding sequences,
             runs consequence translation, prints reports, and exports summaries.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from variant_predictor import VariantPredictor

# Reference coding sequence representing a small segment of the Insulin (INS) gene
# Starting at genomic POS: 220000
REF_SEQ = "ATGCTAGCGGTCATA"
CODING_START_POS = 220000

def main():
    parser = argparse.ArgumentParser(
        description="Genomic Variant Consequence Predictor - Map genetic mutations to protein changes."
    )
    parser.add_argument(
        "-i", "--input",
        default="sample.vcf",
        help="Path to the input VCF file (default: sample.vcf)."
    )
    parser.add_argument(
        "-o", "--output",
        default="consequence_summary.png",
        help="Path to save the consequence summary bar chart (default: consequence_summary.png)."
    )

    args = parser.parse_args()

    # Check input VCF
    if not os.path.exists(args.input):
        print(f"Error: Input VCF file '{args.input}' does not exist.", file=sys.stderr)
        sys.exit(1)

    print("=" * 60)
    print("Initializing Genomic Variant Consequence Predictor")
    print("=" * 60)
    print(f"[*] Coding Reference sequence: {REF_SEQ} (Length: {len(REF_SEQ)} bp)")
    print(f"[*] Coding Genomic start pos: {CODING_START_POS}")
    print(f"[*] Parsing variants from VCF: {args.input}")

    predictor = VariantPredictor(REF_SEQ, CODING_START_POS)

    try:
        raw_variants = predictor.parse_vcf(args.input)
        print(f"[+] Loaded {len(raw_variants)} variant record(s) from VCF.")
    except Exception as e:
        print(f"[-] Parsing failed: {e}", file=sys.stderr)
        sys.exit(1)

    if not raw_variants:
        print("[-] No variants found in the file.", file=sys.stderr)
        sys.exit(1)

    # Process variants
    evaluated_list = []
    print("\n" + "=" * 60)
    print("Genetic Mutation Consequences & Clinical Severity Reports")
    print("=" * 60)

    for idx, var in enumerate(raw_variants, 1):
        pos = var["pos"]
        ref = var["ref"]
        alt = var["alt"]
        var_id = var["id"]
        
        # Get allele frequency (default to 0.0 if missing)
        af = float(var["info"].get("AF", 0.0))
        gene = var["info"].get("GENE", "Unknown")

        # Predict Translation Consequence
        ref_aa, alt_aa, consequence = predictor.predict_consequence(pos, ref, alt)
        
        # Evaluate Clinical Severity Pathogenicity
        pathogenicity = predictor.evaluate_pathogenicity(consequence, af)

        evaluated_list.append({
            "pos": pos,
            "id": var_id,
            "ref": ref,
            "alt": alt,
            "consequence": consequence,
            "pathogenicity": pathogenicity
        })

        print(f"Variant #{idx}: ID: {var_id} | Position: {pos} | Gene: {gene}")
        print(f"  Mutation: {ref} ---> {alt}")
        print(f"  Consequence: {consequence} (Amino Acid: {ref_aa} ---> {alt_aa})")
        print(f"  Allele Frequency: {af:.3f}")
        print(f"  Pathogenicity Class: {pathogenicity}")
        print("-" * 50)

    # Plot summary
    print("\n" + "=" * 60)
    print("Generating Graphical Variant Summary")
    print("=" * 60)
    try:
        print(f"[*] Exporting consequence bar chart to: {args.output}")
        predictor.plot_variant_summary(evaluated_list, args.output)
        print("[+] Summary plot successfully saved.")
    except Exception as e:
        print(f"[-] Summary plotting failed: {e}", file=sys.stderr)

    print("\nAnalysis complete.")

if __name__ == "__main__":
    main()
