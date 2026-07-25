# Enzyme Kinetics Parameter Fitter

A Python-based biophysical calculator that fits substrate velocity datasets to the non-linear **Michaelis-Menten** kinetics model to estimate maximum reaction velocity ($V_{max}$) and the Michaelis constant ($K_m$).

It also calculates the **Lineweaver-Burk** double reciprocal values and outputs diagnostic plots showing the hyperbolic fit and double reciprocal linear fit.

## Features
- **Non-Linear Least Squares Regression**: Employs `scipy.optimize.curve_fit` to estimate kinetics parameters directly from hyperbolic curves.
- **Double Reciprocal Transformations**: Computes Lineweaver-Burk reciprocal factors:
  $$\frac{1}{V} = \frac{K_m}{V_{max}} \cdot \frac{1}{[S]} + \frac{1}{V_{max}}$$
- **Diagnostic Plot Export**: Generates side-by-side plots highlighting asymptotes, Km thresholds, and axes intercepts.

## Project Structure
- `enzyme_fitter.py`: Core fitting engine and graphing functions.
- `main.py`: Command-line interface driver.
- `test_fitter.py`: Unit test suite verifying mathematical functions and fits.
- `kinetics_data.csv`: Sample substrate-velocity kinetics database.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To run the parameter fitting pipeline:
```bash
python main.py --input kinetics_data.csv --output kinetics_plot.png
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_fitter.py
```
