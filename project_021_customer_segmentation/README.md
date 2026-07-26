# Customer Segmentation with K-Means Clustering

An unsupervised machine learning pipeline that standardizes numerical customer attributes (e.g. Annual Income and Spending Score) and applies the **K-Means Clustering** algorithm to segment customers into distinct purchasing groups.

This project implements the **Elbow Method** to select the optimal number of clusters and maps the final cluster groups and their centroids.

## Features
- **Standard Scaling Preprocessing**: Employs `StandardScaler` to prevent feature scaling bias between different units (e.g. thousands of dollars vs. scale 1-100).
- **Elbow Analysis**: Evaluates clustering inertia metrics across candidate cluster numbers ($K=1$ to $K=5$).
- **Centroid Re-Mapping**: Computes cluster centroids in scaled space and maps them back to raw values for business interpretations.

## Project Structure
- `segmentation.py`: Preprocessing, fitting, and plot functions.
- `main.py`: Command-line interface driver.
- `test_segmentation.py`: Unit test suite verifying loading and inertia properties.
- `customers.csv`: Sample customer profiling database.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To partition customers:
```bash
python main.py --input customers.csv --output segments_map.png --clusters 3
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_segmentation.py
```
