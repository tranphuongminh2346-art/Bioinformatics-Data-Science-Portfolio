# Acid-Base pH Titration Curve Simulator

A chemical data science utility that models the pH changes during a weak acid / strong base titration.

It solves chemical equilibrium equations across four distinct regions (pre-titration, Henderson-Hasselbalch buffer, weak base salt hydrolysis at the equivalence point, and strong base excess) and plots the corresponding sigmoidal titration curve.

## Features
- **Equilibrium Solvers**: Computes exact pH values using chemical thermodynamics:
  - Buffer region:
    $$pH = pK_a + \log_{10} \frac{[A^-]}{[HA]}$$
  - Equivalence point:
    $$pH = 14 - pOH = 14 - (-\log_{10} \sqrt{\frac{K_w}{K_a} \cdot C_{salt}})$$
- **Curve Plotter**: Visualizes pH values vs added titrant volume, highlighting the equivalence point.

## Project Structure
- `titration.py`: pH calculations, curve builders, and plotters.
- `main.py`: Command-line interface driver.
- `test_titration.py`: Unit test suite verifying pH levels across all titration phases.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To simulate pH curves:
```bash
python main.py --ca 0.1 --va 50.0 --pka 4.76 --cb 0.1 --output titration_curve.png
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_titration.py
```
