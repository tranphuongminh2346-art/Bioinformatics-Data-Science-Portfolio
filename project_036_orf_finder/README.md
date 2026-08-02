# DNA Translation Open Reading Frame (ORF) Finder

A bioinformatics algorithm pipeline that scans genomic DNA sequences in all **6 reading frames** (3 forward frames and 3 reverse complement frames) to identify **Open Reading Frames (ORFs)** beginning with `ATG` start codons and terminating at `TAA`, `TAG`, or `TGA` stop codons, and translates them into amino acid sequences.

## Features
- **6-Frame Coordinate Scanners**: Searches for codings regions on both sense and antisense strands (using reverse complement coordinates).
- **Genetic Codon Translation**: Translates DNA sequences into amino acids using the standard genetic code codon mapping.
- **QC Coordinate Filters**: Filters out short sequence anomalies based on length constraints.

## Project Structure
- `orf_finder.py`: Main 6-frame scan loops, reverse complements, and codon translations.
- `main.py`: Command-line interface driver.
- `test_finder.py`: Unit test suite verifying frame offsets and reverse complements.
- `sequence_with_orfs.fasta`: Sample DNA sequence containing genes.
- `requirements.txt`: Package dependencies.

## Installation
No third-party packages are required. Standard Python library packages are sufficient.
```bash
pip install -r requirements.txt
```

## Usage
To search coding regions:
```bash
python main.py --input sequence_with_orfs.fasta --min-len 30
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_finder.py
```
