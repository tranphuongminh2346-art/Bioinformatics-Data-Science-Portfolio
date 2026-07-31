# VCF Genotype Quality Control Filter

A genomics data engineering pipeline that parses **Variant Call Format (VCF)** sequence databases, extracts call metrics (such as Read Depth and Genotype Quality), applies QC filtration rules, and evaluates genomic mutation profiles using the **Transition/Transversion (Ti/Tv)** ratio index.

## Features
- **VCF Schema Parser**: Reads genotype call headers and formats, extracting variables (GQ, DP, REF, ALT, QUAL).
- **QC Filtration Engine**: Evaluates minimum variant call quality (QUAL), genotype quality (GQ), and read depth (DP) bounds.
- **Ti/Tv Mutation Index**: Evaluates transitions ($A \leftrightarrow G, C \leftrightarrow T$) and transversions ($A \leftrightarrow C, A \leftrightarrow T, C \leftrightarrow G, G \leftrightarrow T$) ratios to monitor variant call accuracy.

## Project Structure
- `vcf_filter.py`: VCF line mapping, parameter filters, and Ti/Tv calculators.
- `main.py`: Command-line interface driver.
- `test_filter.py`: Unit test suite verifying genotype extraction and Ti/Tv ratios.
- `raw_variants.vcf`: Sample variants dataset in VCF format.
- `requirements.txt`: Package dependencies.

## Installation
No third-party packages are required. Standard Python library packages (`re`) are sufficient.
```bash
pip install -r requirements.txt
```

## Usage
To filter variants and check ratios:
```bash
python main.py --input raw_variants.vcf --qual 30.0 --gq 20 --dp 10 --output filtered_variants.vcf
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_filter.py
```
