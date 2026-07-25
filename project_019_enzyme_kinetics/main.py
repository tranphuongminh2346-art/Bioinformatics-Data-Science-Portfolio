"""
Enzyme Kinetics Fitter CLI Runner
Author: Portfolio Creator
Description: CLI runner to process substrate concentration datasets, fit Km/Vmax parameters,
             and save MM/Lineweaver-Burk diagnostic plots.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enzyme_fitter import EnzymeKineticsFitter

def main():
    parser = argparse.ArgumentParser(
        description="Enzyme Kinetics Parameter Fitter - Michaelis-Menten regression."
    )
    parser.add_argument(
        "-i", "--input",
        default="kinetics_data.csv",
        help="Path to the kinetics CSV data (default: kinetics_data.csv)."
    )
    parser.add_argument(
        "-o", "--output",
        default="kinetics_plot.png",
        help="Path to save the generated kinetics plot (default: kinetics_plot.png)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Enzyme Kinetics Parameter Fitter Pipeline")
    print("=" * 60)
    print(f"[*] Input Data: {args.input}")
    print(f"[*] Output Plot: {args.output}")

    try:
        fitter = EnzymeKineticsFitter(args.input)
        print("[*] Performing non-linear least squares fit...")
        vmax, km = fitter.fit_parameters()
        
        print("\n" + "=" * 60)
        print("Fitted Model Parameters")
        print("=" * 60)
        print(f"[*] Maximum Velocity (Vmax) : {vmax:.4f} µmol/min")
        print(f"[*] Michaelis Constant (Km)  : {km:.4f} mM")
        print(f"[*] Turn-over Index (1/Km)  : {1.0 / km:.4f} 1/mM")
        
        # Save plots
        print("\n[*] Saving plots...")
        fitter.plot_kinetics(args.output)
        print(f"[+] Diagnostic plots saved to {args.output}")
        
    except Exception as e:
        print(f"[-] Pipeline execution failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
