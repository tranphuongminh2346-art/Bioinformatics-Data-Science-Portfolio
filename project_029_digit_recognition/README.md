# Handwritten Digit Recognition (Naive Bayes)

A pixel-level computer vision and classification pipeline that trains a **Gaussian Naive Bayes** classifier on downsampled handwritten digit images (represented as 8x8 grids of pixel intensities, totaling 64 features).

It classifies the digits into numerical values (0-9) and evaluates classification accuracies.

## Features
- **Naive Bayes Classification**: Employs `GaussianNB` to build probability distributions representing pixel configurations for each digit class.
- **Multiclass Validation Evaluator**: Computes multiclass metrics, confusion matrices, and precision/recall scores.

## Project Structure
- `digit_classifier.py`: Model fitting, testing, and predict functions.
- `main.py`: Command-line interface driver.
- `test_classifier.py`: Unit test suite verifying model splits and predictions.
- `digits.csv`: Sample handwritten digit pixel values database.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To evaluate digit predictions:
```bash
python main.py --input digits.csv
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_classifier.py
```
