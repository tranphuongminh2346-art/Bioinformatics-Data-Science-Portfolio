# Chemical Solubility Descriptor Regressor

A cheminformatics machine learning pipeline that standardizes compound structural features (Molecular Weight, LogP, Rotatable Bonds, and Polar Surface Area) and trains a regularized **Ridge Regression** model to predict aqueous chemical solubility indices ($LogS$).

It generates correlation scatter plots comparing predicted values with actual experimental measurements.

## Features
- **Chemical Descriptor Parser**: Parses molecular features and experimental solubility coefficients from CSV datasets.
- **Ridge Regression Model**: Trains a regularized regression model to prevent overfitting on collinear molecular features.
- **LogS Fit Visualizer**: Generates scatter plots mapping target experimental LogS values against model predictions.

## Project Structure
- `solubility_predictor.py`: Standard Scalers, Ridge model training, evaluations, and scatter plotters.
- `main.py`: Command-line interface driver.
- `test_predictor.py`: Unit test suite verifying standardized scaling and solubilities predictions.
- `solubility.csv`: Sample chemical solubility database.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To evaluate chemical solubility:
```bash
python main.py --input solubility.csv --output solubility_fit.png
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_predictor.py
```
