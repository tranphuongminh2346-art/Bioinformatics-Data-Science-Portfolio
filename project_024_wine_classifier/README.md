# Wine Quality Classification using Decision Trees

A predictive machine learning pipeline that classifies wine quality categories (e.g. poor vs high quality) using chemical components (such as fixed/volatile acidity, pH levels, and alcohol volume percentage) and trains a **Decision Tree Classifier**.

The project visualizes the resulting decision tree structure to trace classification rules and split boundaries.

## Features
- **Rule-based Classification**: Trains a `DecisionTreeClassifier` with regularized depth parameters to prevent overfitting.
- **Tree visualization**: Exports graphical decision flow diagrams illustrating nodes, thresholds, entropy/gini reductions, and sample distributions.
- **Diagnostics Reporting**: Evaluates classification reports, confusion matrices, and precision/recall scores.

## Project Structure
- `wine_classifier.py`: Model fitting, testing, and diagram generator.
- `main.py`: Command-line interface driver.
- `test_classifier.py`: Unit test suite verifying tree depths and split records.
- `wine_quality.csv`: Sample wine chemical attributes database.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To fit models and plot tree splits:
```bash
python main.py --input wine_quality.csv --output wine_tree.png --depth 3
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_classifier.py
```
