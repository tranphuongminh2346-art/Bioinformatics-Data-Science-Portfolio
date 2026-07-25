# Needleman-Wunsch Global Sequence Alignment

A Python implementation of the classic **Needleman-Wunsch** dynamic programming algorithm for optimal global pairwise alignment of biological sequences (DNA, RNA, or proteins).

It computes the full scoring grid, traces back the optimal path, and prints the pretty-formatted sequence alignment showing matches, mismatches, and gaps.

## Features
- **Dynamic Programming Scoring Matrix**: Calculates optimal alignment scores for every substring pair.
- **Traceback Backtracking**: Backtracks from the bottom-right of the score matrix to the top-left to recover the optimal path.
- **Customizable Scoring Scheme**: Adjustable scores for matches, mismatch penalties, and gap insertion penalties.
- **Formatted Alignment Visualizations**: Prints alignments with matching connectors (`|`), mismatch indicators (`.`), and empty spaces for gap insertions.

## Project Structure
- `needleman_wunsch.py`: Main class `NeedlemanWunschAligner` performing alignments and formatting.
- `main.py`: Command-line driver printing grid tables and alignment outputs.
- `test_alignment.py`: Unit test suite verifying dynamic programming values, paths, and borders.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To align two custom sequences with custom scoring parameters:
```bash
python main.py --seq1 HEAGAWGHEE --seq2 PAWHEAE --match 2 --mismatch -1 --gap -2
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_alignment.py
```
