# Microarray Hierarchical Clustering

A bioinformatics expression analysis pipeline that parses microarray gene expression levels, standardizes expression profiles per gene using row-wise Z-score normalization, and clusters similar gene patterns using **Average Linkage Hierarchical Clustering**.

It exports a dual-panel plot featuring a left-side dendrogram linked to a reordered expression heatmap.

## Features
- **Microarray CSV Parser**: Loads high-dimensional gene expression matrices.
- **Row Z-Score Normalization**: Standardizes variables per gene across samples:
  $$Z = \frac{X - \mu}{\sigma}$$
- **Scipy Linkage Clustering**: Computes hierarchical trees using Euclidean metrics.
- **Heatmap Dendrogram Plotter**: Visualizes reordered patterns matching linkage structures.

## Project Structure
- `clustering.py`: Row standardization, linkage calculations, and heatmap plots.
- `main.py`: Command-line interface driver.
- `test_clustering.py`: Unit test suite verifying Z-score stats and linkage dims.
- `microarray.csv`: Sample microarray gene matrix database.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To fit clusters and draw heatmaps:
```bash
python main.py --input microarray.csv --output clustered_heatmap.png
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_clustering.py
```
