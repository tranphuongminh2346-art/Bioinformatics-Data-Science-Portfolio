# RNA-Seq Differential Gene Expression Analyzer

A Python bioinformatics tool that normalizes raw sequencing read counts using the **Counts Per Million (CPM)** method, computes statistical log2 Fold Changes, conducts independent two-sample t-tests to evaluate differential significance, and creates Volcano plots.

This represents a standard workflow in computational biology to identify candidate biomarkers or differentially expressed genes (DEGs) in disease vs. control cohorts.

## Features
- **Sequencing Normalization**: Converts raw transcript counts into CPM to adjust for sample-to-sample differences in sequencing depth.
- **Expression Log-Scaling**: Calculates Fold Changes (FC) and Log2 Fold Changes ($\log_2\text{FC}$) with pseudo-counts to avoid division-by-zero.
- **Hypothesis Testing**: Runs two-sided independent Student's t-tests to compute p-values for expression shifts.
- **Volcano Visualization**: Generates a scatter plot mapping $\log_2\text{FC}$ against $-\log_{10}\text{p-value}$, highlighting significantly upregulated (red) and downregulated (blue) genes.

## Project Structure
- `expression_analyzer.py`: Main class `GeneExpressionAnalyzer` executing library scaling, t-tests, and plotting.
- `main.py`: Command-line interface driver printing results.
- `test_expression.py`: Unit test suite verifying CPM sums, fold change math, and logs.
- `gene_counts.csv`: Synthetic gene expression read counts matrix.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To run the analysis:
```bash
python main.py --input gene_counts.csv --output volcano_plot.png
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_expression.py
```
