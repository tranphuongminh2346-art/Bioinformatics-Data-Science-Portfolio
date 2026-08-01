# Breast Cancer Wisconsin diagnostic SVM Classifier

A medical diagnostic machine learning pipeline that standardizes cell nuclear characteristics (such as mean radius, mean texture, perimeter, area, and smoothness) and trains a **Support Vector Machine (SVM) classifier with a Radial Basis Function (RBF) kernel** to classify tumors as benign or malignant.

It visualizes the decision boundary and classification margins in a standardized 2D feature projection.

## Features
- **Standardized Feature Scaling**: Employs `StandardScaler` to normalize feature vectors and prevent numerical scale dominance.
- **RBF Support Vector Machine**: Fits a non-linear `SVC` model to capture complex, non-linear classification margins.
- **2D Boundary Visualizer**: Creates contour grids maps of decision boundaries projected across mean radius and mean texture coordinates.

## Project Structure
- `cancer_classifier.py`: Preprocessing, model training, evaluation, and boundary plotters.
- `main.py`: Command-line interface driver.
- `test_classifier.py`: Unit test suite verifying loading and RBF prediction coordinates.
- `cancer_data.csv`: Sample tumor attributes database.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To partition and map diagnostics:
```bash
python main.py --input cancer_data.csv --output decision_boundary.png
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_classifier.py
```
