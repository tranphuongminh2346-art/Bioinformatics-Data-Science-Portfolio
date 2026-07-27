# FASTA Header Parser & SQLite Loader

A high-fidelity biological sequence database engineering pipeline that parses protein sequence databases in FASTA format using regular expressions matching **UniProt header formats**, extracts metadata schemas, and loads them into a normalized SQLite database.

## Features
- **Regex UniProt Header Parser**: Extracts database sources (`sp` for Swiss-Prot or `tr` for TrEMBL), unique accession identifiers, entry names, protein descriptions, taxonomy IDs, gene names, protein existences (PE), and sequence versions (SV).
- **SQLite Database Normalization**: Stores sequences, metadata, and sequence lengths with unique indexes on accession numbers.
- **Diagnostics Summaries**: Runs group-by queries to list sequence counts and average sequence lengths by organism.

## Project Structure
- `fasta_parser.py`: UniProt regex header matcher and record loader.
- `db_loader.py`: SQLite connection schema definitions, inserts, and queries.
- `main.py`: Command-line interface driver.
- `test_parser.py`: Unit test suite verifying header matching and database counts.
- `proteins.fasta`: Sample protein sequences.
- `requirements.txt`: Package dependencies.

## Installation
No third-party packages are required. Standard Python library packages (`sqlite3`, `re`) are sufficient.
```bash
pip install -r requirements.txt
```

## Usage
To parse and load sequences:
```bash
python main.py --input proteins.fasta --db proteins.db
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_parser.py
```
