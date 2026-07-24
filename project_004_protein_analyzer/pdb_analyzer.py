"""
Protein Structure Coordinate Analyzer
Author: Portfolio Creator
Description: Core module to parse Protein Data Bank (PDB) coordinates,
             calculate CA-CA 3D Euclidean distances, identify hydrogen bonds,
             and plot distance matrices.
Language: English (100%)
"""

import os
import urllib.request
import numpy as np
import matplotlib.pyplot as plt

RCSB_DOWNLOAD_URL = "https://files.rcsb.org/download/{}.pdb"

class PDBParser:
    """Parses protein 3D structures in legacy PDB format."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.atoms = []
        self.parse()

    def parse(self):
        """Parses ATOM records from the PDB file."""
        if not os.path.exists(self.file_path):
            # Attempt to download if file_path is a PDB ID (like '1CRN')
            if len(self.file_path) == 4 and self.file_path.isalnum():
                pdb_id = self.file_path.upper()
                print(f"[*] File '{self.file_path}' not found. Attempting download for PDB: {pdb_id}")
                local_dest = f"{pdb_id.lower()}.pdb"
                urllib.request.urlretrieve(RCSB_DOWNLOAD_URL.format(pdb_id), local_dest)
                self.file_path = local_dest
            else:
                raise FileNotFoundError(f"PDB file not found: {self.file_path}")

        self.atoms = []
        with open(self.file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith("ATOM  ") or line.startswith("HETATM"):
                    # Fixed-column indexing as per PDB format specifications
                    try:
                        serial = int(line[6:11].strip())
                        name = line[12:16].strip()
                        res_name = line[17:20].strip()
                        chain = line[21].strip()
                        res_seq = int(line[22:26].strip())
                        x = float(line[30:38].strip())
                        y = float(line[38:46].strip())
                        z = float(line[46:54].strip())
                        element = line[76:78].strip()

                        self.atoms.append({
                            "serial": serial,
                            "name": name,
                            "res_name": res_name,
                            "chain": chain,
                            "res_seq": res_seq,
                            "x": x,
                            "y": y,
                            "z": z,
                            "element": element
                        })
                    except (ValueError, IndexError):
                        # Skip malformed coordinate lines
                        continue

    def get_ca_atoms(self) -> list:
        """Filters and returns all Alpha Carbon (CA) atoms."""
        return [atom for atom in self.atoms if atom["name"] == "CA"]

    def calculate_distance_matrix(self) -> np.ndarray:
        """
        Computes the CA-CA distance matrix.
        
        Returns:
            np.ndarray: 2D symmetric distance matrix.
        """
        ca_atoms = self.get_ca_atoms()
        n = len(ca_atoms)
        matrix = np.zeros((n, n))
        
        for i in range(n):
            coord_i = np.array([ca_atoms[i]["x"], ca_atoms[i]["y"], ca_atoms[i]["z"]])
            for j in range(i + 1, n):
                coord_j = np.array([ca_atoms[j]["x"], ca_atoms[j]["y"], ca_atoms[j]["z"]])
                dist = np.linalg.norm(coord_i - coord_j)
                matrix[i, j] = dist
                matrix[j, i] = dist
                
        return matrix

    def find_hydrogen_bonds(self, min_dist: float = 2.5, max_dist: float = 3.5) -> list:
        """
        Identifies potential hydrogen bonds based on distance criteria
        between donor Nitrogens (N) and acceptor Oxygens (O).
        
        Args:
            min_dist (float): Minimum distance (Å).
            max_dist (float): Maximum distance (Å).
            
        Returns:
            list: List of dictionaries detailing matching bond pairs.
        """
        nitrogens = [a for a in self.atoms if a["name"] == "N"]
        oxygens = [a for a in self.atoms if a["name"] == "O"]
        h_bonds = []
        
        for n_atom in nitrogens:
            coord_n = np.array([n_atom["x"], n_atom["y"], n_atom["z"]])
            for o_atom in oxygens:
                # Do not bond within the same residue
                if n_atom["res_seq"] == o_atom["res_seq"]:
                    continue
                coord_o = np.array([o_atom["x"], o_atom["y"], o_atom["z"]])
                dist = np.linalg.norm(coord_n - coord_o)
                if min_dist <= dist <= max_dist:
                    h_bonds.append({
                        "donor": f"{n_atom['res_name']}{n_atom['res_seq']}_N",
                        "acceptor": f"{o_atom['res_name']}{o_atom['res_seq']}_O",
                        "distance": dist
                    })
        return h_bonds

    def plot_distance_matrix(self, matrix: np.ndarray, output_path: str):
        """
        Plots a distance matrix heatmap.
        
        Args:
            matrix (np.ndarray): 2D distance matrix.
            output_path (str): Save path for heatmap image.
        """
        ca_atoms = self.get_ca_atoms()
        labels = [f"{a['res_name']}{a['res_seq']}" for a in ca_atoms]

        plt.figure(figsize=(8, 7))
        plt.imshow(matrix, cmap="viridis", origin="lower")
        
        # Grid/Labels styling
        plt.title("Protein CA-CA Distance Matrix Map", fontsize=12, fontweight='bold', pad=15)
        plt.colorbar(label="Distance (Angstroms)")
        
        plt.xticks(np.arange(len(labels)), labels, rotation=90, fontsize=8)
        plt.yticks(np.arange(len(labels)), labels, fontsize=8)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
