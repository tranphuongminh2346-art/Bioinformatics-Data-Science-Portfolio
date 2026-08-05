# Markov DNA Transition Sequence Simulator

A genomic simulation utility that implements first-order **Markov Chains** to generate synthetic DNA sequences.

It includes presets for uniform background distributions and CpG island hotspots (characterized by elevated $C \to G$ transition probabilities), and estimates empirical transition probability matrices from generated sequences.

## Features
- **Markov Chain Generator**: Simulates DNA sequences step-by-step using transition probability matrices:
  $$P(X_t = j \mid X_{t-1} = i)$$
- **Hotspot Modeling (CpG Islands)**: Integrates custom transition matrices modeling CpG dinucleotide frequencies.
- **Empirical Probability Analyzer**: Computes the empirical $4 \times 4$ base transition matrix.

## Project Structure
- `dna_generator.py`: Transition matrices, sequence generators, and transition analyzers.
- `main.py`: Command-line interface driver.
- `test_generator.py`: Unit test suite verifying matrix properties and sequence statistics.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To generate sequence and print transition statistics:
```bash
python main.py --length 200 --model cpg
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_generator.py
```
