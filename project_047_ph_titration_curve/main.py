"""
Titration Curve Simulator CLI
Author: Portfolio Creator
Description: CLI driver to compute acid-base pH curves and export charts.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from titration import PHTitrator

def main():
    parser = argparse.ArgumentParser(
        description="Titration Simulator - Solve and plot weak acid/strong base pH curves."
    )
    parser.add_argument(
        "-ca", "--ca",
        type=float,
        default=0.1,
        help="Acid concentration Ca in M (default: 0.1)."
    )
    parser.add_argument(
        "-va", "--va",
        type=float,
        default=50.0,
        help="Acid volume Va in mL (default: 50.0)."
    )
    parser.add_argument(
        "-pka", "--pka",
        type=float,
        default=4.76,
        help="Acid dissociation constant pKa (default: 4.76 for Acetic Acid)."
    )
    parser.add_argument(
        "-cb", "--cb",
        type=float,
        default=0.1,
        help="Base concentration Cb in M (default: 0.1)."
    )
    parser.add_argument(
        "-o", "--output",
        default="titration_curve.png",
        help="Path to save output chart (default: titration_curve.png)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("pH Titration Curve Simulator - Chemical Equilibrium Solver")
    print("=" * 60)
    print(f"[*] Acid Parameter: Ca={args.ca} M | Va={args.va} mL | pKa={args.pka}")
    print(f"[*] Base Parameter: Cb={args.cb} M")
    print(f"[*] Saving plot to: {args.output}")

    try:
        titrator = PHTitrator(c_acid=args.ca, v_acid=args.va, pka=args.pka, c_base=args.cb)
        
        # Calculate Equivalence Point
        print(f"[+] Equivalence volume V_eq: {titrator.v_eq:.2f} mL")
        eq_ph = titrator.calculate_ph_at_volume(titrator.v_eq)
        print(f"[+] Equivalence point pH   : {eq_ph:.2f}")
        
        # Generate and save plot
        print("[*] Simulating titration steps and drawing curve...")
        titrator.plot_titration(args.output)
        print("[+] Titration curve successfully generated.")
        
    except Exception as e:
        print(f"[-] Titration failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
