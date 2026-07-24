# UPGMA Phylogenetic Tree Reconstructor

A bioinformatics tool that parses aligned DNA or protein FASTA sequences, calculates pairwise Hamming distance matrices, and reconstructs evolutionary lineage relationships using the **Unweighted Pair Group Method with Arithmetic Mean (UPGMA)** hierarchical clustering algorithm.

This project demonstrates sequence processing, custom binary trees, recursive string conversions, and ASCII layouts.

## Features
- **Hamming Distance Matrix**: Calculates alignment mismatch proportions between sequence pairs.
- **UPGMA Hierarchical Clustering**: Implements iterative clustering to merge the closest nodes, calculating branch lengths based on cluster node distances.
- **Standard Newick Export**: Outputs trees in Newick format suitable for loading in phylogenetic viewers (such as FigTree or iTOL).
- **Interactive ASCII Layout**: Prints a hierarchical text diagram of the evolutionary tree.

## Project Structure
- `upgma.py`: Class `PhylogeneticNode` and core algorithm class `UPGMATreeReconstructor`.
- `main.py`: Command-line driver printing tables and trees.
- `test_upgma.py`: Unit test suite verifying distance calculations and cluster merges.
- `sequences.fasta`: Aligned homologous test sequences.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To run the reconstructor pipeline:
```bash
python main.py --input sequences.fasta
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_upgma.py
```
