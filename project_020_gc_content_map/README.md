# Genomic GC-Content & Skew Map Generator

A Python tool designed to read chromosomal genomic sequences in FASTA format and perform sliding-window profiling of GC-Content ratio and GC-skew metrics. 

This helps identify structural features of genomes such as **GC Islands** (associated with promoters and gene-dense regions) and replication origin regions (replication forks often show distinct GC skew transitions).

## Features
- **FASTA Sequence Parser**: Parses multi-line standard FASTA biological sequences.
- **Sliding Window Statistics**:
  - GC Content:
    $$\text{GC Content} = \frac{G + C}{A + T + G + C}$$
  - GC Skew:
    $$\text{GC Skew} = \frac{G - C}{G + C}$$
- **Genomic Landscape Visualization**: Generates high-fidelity line charts of GC trends and highlights GC-rich islands.

## Project Structure
- `gc_mapper.py`: Main sequence calculation logic and plot builders.
- `main.py`: Command-line interface driver.
- `test_mapper.py`: Unit test suite verifying sliding window indexes and skew calculations.
- `genome.fasta`: Sample chromosomal DNA sequence in FASTA format.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To compute chromosomal maps:
```bash
python main.py --input genome.fasta --output gc_map.png --window 50 --step 10
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_mapper.py
```
