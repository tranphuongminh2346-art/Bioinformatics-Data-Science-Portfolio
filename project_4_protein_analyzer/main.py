"""
Protein Coordinate Analyzer CLI Runner
Author: Portfolio Creator
Description: Command-line interface to parse coordinates, calculate structural metrics,
             identify hydrogen bonds, and export distance heatmaps.
Language: English (100%)
"""

import argparse
import sys
import os
import numpy as np

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pdb_analyzer import PDBParser

def main():
    parser = argparse.ArgumentParser(
        description="Protein Coordinate Analyzer - Process 3D atomic coordinates from PDB files."
    )
    parser.add_argument(
        "-i", "--input",
        default="1crn.pdb",
        help="Path to local PDB file or 4-letter PDB ID (default: 1crn.pdb)."
    )
    parser.add_argument(
        "-o", "--output",
        default="distance_matrix.png",
        help="Path to save the generated distance matrix plot (default: distance_matrix.png)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Initializing Protein Coordinate Analyzer")
    print("=" * 60)

    try:
        parser = PDBParser(args.input)
    except Exception as e:
        print(f"[-] Parsing failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 1. Basic Stats
    total_atoms = len(parser.atoms)
    ca_atoms = parser.get_ca_atoms()
    num_residues = len(ca_atoms)
    
    print(f"[+] Successfully loaded: {parser.file_path}")
    print(f"    Total Atoms Parsed: {total_atoms}")
    print(f"    Residues (CA Atoms): {num_residues}")

    if total_atoms == 0:
        print("[-] No atoms parsed. Exiting.", file=sys.stderr)
        sys.exit(1)

    # 2. Geometric Dimensions
    coords = np.array([[a["x"], a["y"], a["z"]] for a in parser.atoms])
    min_coords = coords.min(axis=0)
    max_coords = coords.max(axis=0)
    dimensions = max_coords - min_coords
    
    print("\n" + "=" * 60)
    print("Structural Geometry Metrics")
    print("=" * 60)
    print(f"Protein Bounding Box Dimensions (Angstroms):")
    print(f"  Width (X):  {dimensions[0]:.2f} Å  (Range: {min_coords[0]:.2f} to {max_coords[0]:.2f})")
    print(f"  Height (Y): {dimensions[1]:.2f} Å  (Range: {min_coords[1]:.2f} to {max_coords[1]:.2f})")
    print(f"  Depth (Z):  {dimensions[2]:.2f} Å  (Range: {min_coords[2]:.2f} to {max_coords[2]:.2f})")

    # 3. Hydrogen Bond Detections
    print("\n" + "=" * 60)
    print("Potential Hydrogen Bonds Detected (2.5 Å - 3.5 Å)")
    print("=" * 60)
    
    h_bonds = parser.find_hydrogen_bonds()
    print(f"Total potential hydrogen bonds: {len(h_bonds)}")
    print("-" * 50)
    # Print first 10 bonds as summary
    for bond in h_bonds[:10]:
        print(f"  Donor: {bond['donor']:<10} <---> Acceptor: {bond['acceptor']:<10} | Distance: {bond['distance']:.2f} Å")
    if len(h_bonds) > 10:
        print(f"  ... and {len(h_bonds) - 10} more.")

    # 4. Distance Matrix Plot
    if num_residues > 1:
        print("\n" + "=" * 60)
        print("Generating Distance Matrix Visualization")
        print("=" * 60)
        try:
            print(f"[*] Calculating CA-CA distance matrix...")
            matrix = parser.calculate_distance_matrix()
            print(f"[*] Saving heatmap to: {args.output}")
            parser.plot_distance_matrix(matrix, args.output)
            print("[+] Matrix successfully saved.")
        except Exception as e:
            print(f"[-] Plotting failed: {e}", file=sys.stderr)
    else:
        print("\n[!] Skipping distance matrix plot (requires at least 2 residues).")

    print("\nAnalysis complete.")

if __name__ == "__main__":
    main()
