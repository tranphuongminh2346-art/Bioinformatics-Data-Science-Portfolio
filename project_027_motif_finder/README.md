# DNA Motif Finder (Gibbs Sampling)

A bioinformatics algorithm pipeline that implements the **Gibbs Sampling** heuristic to discover conserved DNA promoter motifs (such as transcription factor binding sites) across multiple unaligned genomic promoter sequences.

## Features
- **FASTA DNA Sequence Parser**: Parses genomic sequences from standard FASTA files.
- **Position Weight Profile Matrix**: Computes nucleotide frequency matrices (PWM) using **Laplace smoothing (add-one pseudocounts)** to prevent zero-probability traps.
- **Gibbs Sampler Optimization**: Iteratively updates motif selections by sampling positions proportionally to alignment profiles.
- **Consensus Sequence Generator**: Determines the highest-frequency nucleotide string from final aligned motifs.

## Project Structure
- `motif_finder.py`: Main Gibbs sampler loops, PWM builders, and consensus tools.
- `main.py`: Command-line interface driver.
- `test_motif.py`: Unit test suite verifying Laplace profile math and consensus alignments.
- `promoters.fasta`: Sample promoter database containing hidden motifs.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To search DNA motifs:
```bash
python main.py --input promoters.fasta --length 6 --iterations 100
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_motif.py
```
