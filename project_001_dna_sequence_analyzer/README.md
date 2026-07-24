# Day 01: DNA Sequence Analyzer

A professional Python tool for bioinformatics sequence analysis. It calculates basic nucleotide statistics, performs transcription and translation, and visualizes the GC content using a sliding window algorithm.

## Features
- **Nucleotide Frequency Analysis**: Computes percentage composition of Adenine (A), Cytosine (C), Guanine (G), and Thymine (T).
- **GC Content Calculation**: Computes overall GC-percentage, which is crucial for PCR primer design and understanding genomic stability.
- **Transcription**: Converts DNA to RNA (replacing Thymine with Uracil).
- **Translation**: Simulates codon-by-codon translation into amino acid sequences using standard genetic code tables, terminating at Stop codons (`*`).
- **GC Content Sliding Window Visualizer**: Evaluates regional GC content variation along the sequence length and saves a high-quality visualization plot.

## Project Structure
- [`analyzer.py`](./analyzer.py): Main script containing the `DNASequenceAnalyzer` class and execution flow.
- [`requirements.txt`](./requirements.txt): List of dependencies (`matplotlib`, `numpy`).
- `gc_content_profile.png`: The generated plot of the sliding window GC content analysis.

## Setup & Execution
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the analyzer script:
   ```bash
   python analyzer.py
   ```

## Example Visualizer Output
The tool generates a visual plot showing the local GC percentage vs. the genomic coordinates, along with the average GC content reference line.
