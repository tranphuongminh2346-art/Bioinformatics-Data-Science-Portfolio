# HMM Viterbi Eukaryotic Gene Finder

A bioinformatics sequence parsing utility that implements a **Hidden Markov Model (HMM)** to identify gene coding exons vs introns and intergenic regions from genomic DNA.

It decodes the most probable sequence of hidden states (Non-coding `N` and Exon `E`) using the **Viterbi dynamic programming algorithm** calculated in log-space.

## Features
- **HMM Architecture**: Modeled with two states (Non-coding background vs GC-rich Exon coding regions) and emission probabilities representing AT-rich vs GC-rich segments.
- **Log-Space Viterbi Decoders**: Implements log-transformed dynamic programming lattices to prevent double underflow:
  $$V_{t}(j) = \max_i [V_{t-1}(i) + \log a_{ij}] + \log b_{j}(O_t)$$
- **Exon Coordinate Parser**: Resolves continuous coding segments and calculates GC percentages.

## Project Structure
- `gene_finder.py`: HMM class configuration, Viterbi log-lattice builder, and exon parsers.
- `main.py`: Command-line interface driver.
- `test_finder.py`: Unit test suite verifying Viterbi traceback paths and coordinates.
- `eukaryote.fasta`: Sample DNA sequence containing genes.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To decode DNA regions:
```bash
python main.py --input eukaryote.fasta
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_finder.py
```
