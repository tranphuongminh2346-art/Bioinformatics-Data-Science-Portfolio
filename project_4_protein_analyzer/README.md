# Protein Structure Coordinate Analyzer

A lightweight, self-contained Python program to parse Protein Data Bank (PDB) coordinate files, calculate 3D structural metrics, identify hydrogen bonds between donor-acceptor groups, and map distance profiles in a 2D matrix heatmap.

It utilizes the real coordinates of **Crambin (1CRN)**, a small seed protein, to demonstrate coordinate math, structural geometry parsing, and spatial visualization techniques in bioinformatics.

## Features
- **PDB Parsing**: Robust fixed-column parsing of `ATOM` coordinate records without external heavy dependencies.
- **Auto-Download Support**: Automatically downloads full PDB files from the RCSB protein database if a 4-letter PDB ID is supplied.
- **Euclidean Distance Map**: Computes the 3D distances between Alpha Carbon (CA) atoms to produce a symmetric $N \times N$ matrix.
- **Hydrogen Bond Finder**: Identifies candidate hydrogen bonds between Nitrogens (donors) and Oxygens (acceptors) within a configurable spatial window ($2.5\text{ Å} - 3.5\text{ Å}$).
- **Geometry Profile**: Computes overall protein bounding box dimensions along the X, Y, and Z axes.
- **Distance Heatmap**: Visualizes structural proximity using a premium Matplotlib heatmap plot.

## Project Structure
- `pdb_analyzer.py`: Main class module implementing `PDBParser` and distance math.
- `main.py`: Command-line interface driver that prints metrics and saves plots.
- `test_pdb_analyzer.py`: Unit test suite verifying distance formulas, parsing, and H-bond filters.
- `requirements.txt`: Package dependencies.
- `1crn.pdb`: Real PDB coordinate data segment for Crambin.

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

To run the structural analysis on the provided Crambin PDB file:
```bash
python main.py --input 1crn.pdb --output distance_matrix.png
```

To fetch and analyze a different protein directly using its PDB identifier (e.g. Ubiquitin `1UBQ`):
```bash
python main.py --input 1ubq --output ubiquitin_matrix.png
```

This command will:
1. Parse the coordinate records.
2. Calculate bounding box dimensions.
3. Count and list detected candidate hydrogen bonds.
4. Calculate and export the CA-CA distance profile heat-map.

## Running Unit Tests
To run the automated tests:
```bash
python -m unittest test_pdb_analyzer.py
```
