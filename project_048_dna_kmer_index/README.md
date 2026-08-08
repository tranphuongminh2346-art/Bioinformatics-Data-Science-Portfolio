# Burrows-Wheeler Transform DNA Indexer

A genomics indexing and search pipeline that compresses genomic sequences using the **Burrows-Wheeler Transform (BWT)**, generates **Suffix Arrays (SA)**, and executes exact k-mer matching lookups via **Last-to-First (LF) mapping backward searches**.

## Features
- **Burrows-Wheeler Transform (BWT)**: Permutes DNA sequences (appended with a sentinel `$`) by sorting all cyclic shifts to group redundant characters together.
- **Inverse BWT Reconstructor**: Restores the original string from the last column character vectors.
- **Backward Search Matcher**: Searches for exact query sequences in $O(M)$ time (where $M$ is the query length) using LF-mapping vectors.

## Project Structure
- `bwt_indexer.py`: BWT transforms, inverse algorithms, suffix arrays, and backward searches.
- `main.py`: Command-line interface driver.
- `test_indexer.py`: Unit test suite verifying transform values and coordinate lookups.
- `requirements.txt`: Package dependencies.

## Installation
No third-party packages are required. Standard Python library packages are sufficient.
```bash
pip install -r requirements.txt
```

## Usage
To index sequences and search:
```bash
python main.py --sequence GCATGCATGC --query ATG
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_indexer.py
```
