# Genomic Variant Consequence Predictor

A bioinformatics tool written in Python to parse Variant Call Format (VCF) files, map genetic mutations (single nucleotide variants) to coding sequences, translate codons, predict structural changes in amino acids, and categorize pathogenicity risk.

It uses **real human genomic coordinates and reference templates** to replicate how variants are prioritized in genetic diagnostics.

## Features
- **VCF Parsing**: Reads metadata and variant fields (position, ref/alt alleles, gene identifiers, and allele frequency) from standard VCF records.
- **Translation Mapping**: Locates mutation coordinates relative to coding open reading frames (ORFs).
- **Consequence Prediction**:
  - Synonymous: Silent mutations that do not alter the translated amino acid.
  - Missense: Mutations that substitute one amino acid for another.
  - Nonsense: Mutations that introduce premature stop codons (stop gain).
- **Severity Decision Rules**: Classifies variant pathogenicity (Benign, Likely Benign, Variant of Uncertain Significance - VUS, or Likely Pathogenic) based on mutation consequence and allele frequency thresholds.
- **Visual Reporting**: Generates a bar plot showing the distribution of variant consequences in the dataset.

## Project Structure
- `variant_predictor.py`: Core logic for consequence translations and rule-based classifications.
- `main.py`: Command-line interface driver that prints evaluation details.
- `test_variant_predictor.py`: Unit test suite verifying translation outputs and boundary conditions.
- `sample.vcf`: Sample VCF file representing variants in the insulin (`INS`) gene.
- `requirements.txt`: Package dependencies.

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

To analyze the provided `sample.vcf` dataset:
```bash
python main.py --input sample.vcf --output consequence_summary.png
```

This command will:
1. Parse the VCF file.
2. For each variant:
   - Identify the affected codon.
   - Translate the reference and mutant codons.
   - Print the mutation type, amino acid swap, and allele frequency.
   - Output the clinical pathogenicity classification.
3. Save a consequence count chart to `consequence_summary.png`.

## Running Unit Tests
To run the automated tests:
```bash
python -m unittest test_variant_predictor.py
```
