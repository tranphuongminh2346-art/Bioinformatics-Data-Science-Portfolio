# Genomic PCR Primer Designer

A bioinformatics DNA analysis utility that parses target genomic sequences in FASTA format and designs candidate forward and reverse PCR primers.

It calculates melting temperatures ($T_m$), GC content fractions, and screens candidates to filter out self-complementary sequences (which are at risk of forming **hairpin loops**).

## Features
- **Fasta sequence parsing**: Parses template sequences from standard FASTA files.
- **Melting Temperature ($T_m$) Calculators**: Computes primer melting temperatures using the **Wallace formula**:
  $$T_m = 2 \cdot (A + T) + 4 \cdot (G + C)$$
- **Hairpin Loop Filters**: Evaluates candidate sequences to filter out those containing self-complementary patterns (matching reverse complement sub-sequences of size $\ge 4$ bp).

## Project Structure
- `primer_designer.py`: Main design coordinates loops, Tm, and self-complementarity checks.
- `main.py`: Command-line interface driver.
- `test_designer.py`: Unit test suite verifying Tm formulas and reverse complements.
- `target_gene.fasta`: Sample template sequence.
- `requirements.txt`: Package dependencies.

## Installation
No third-party packages are required. Standard Python library packages are sufficient.
```bash
pip install -r requirements.txt
```

## Usage
To search PCR primers:
```bash
python main.py --input target_gene.fasta --min-len 18 --max-len 22
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_designer.py
```
