# PLINK PED/MAP Pedigree Parser

A genomics quality control utility that parses genetic pedigree databases formatted in **PLINK PED/MAP** standards, computes marker call rates, and audits parent-offspring transmission lines to flag **Mendelian inheritance errors**.

## Features
- **PLINK Format Parsers**: Reads `.map` marker lists and `.ped` family genotype rows.
- **Marker Call Rate Analysis**: Evaluates data completion rates for each marker by tracking missing genotypes (`0 0`).
- **Mendelian Error Auditor**: Audits parental genotype pairs to verify that child alleles are strictly inherited from parents, flagging any inheritance mismatches.

## Project Structure
- `ped_parser.py`: MAP marker, PED column, call rate, and Mendelian checking engines.
- `main.py`: Command-line interface driver.
- `test_parser.py`: Unit test suite verifying genotype structures and Mendelian errors.
- `genotypes.ped` / `genotypes.map`: Sample PLINK pedigree files.
- `requirements.txt`: Package dependencies.

## Installation
No third-party packages are required. Standard Python library packages are sufficient.
```bash
pip install -r requirements.txt
```

## Usage
To audit pedigree data:
```bash
python main.py --ped genotypes.ped --map genotypes.map
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_parser.py
```
