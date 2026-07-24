# Malaria Microscopic Cell Image Feature Classifier

A Python-based Machine Learning pipeline that processes morphological image features of red blood cells, trains a Random Forest Classifier to identify parasitized cells, and plots the Receiver Operating Characteristic (ROC) validation curves.

This demonstrates a machine learning classification workflow for digital pathology and cell microscopy analytics, utilizing numerical features derived from the NIH Malaria Dataset.

## Features
- **Pathology Feature Processing**: Processes cell features (mean red intensity, standard deviation, area, and eccentricity).
- **Label Mapping**: Maps text classification categories (`Parasitized`, `Uninfected`) to binary outcomes (`1` and `0`).
- **Ensemble Classifier Model**: Trains a Random Forest model with stratified partitioning.
- **ROC Curve Visualization**: Plots the trade-off between True Positive and False Positive rates, calculating the Area Under Curve (AUC).
- **Feature Significance Mapping**: Ranks morphological features to find the strongest indicator of cell infection.

## Project Structure
- `image_classifier.py`: Core machine learning class `CellImageClassifier` managing preprocessing, training, and plotting.
- `main.py`: Command-line interface driver executing the pipeline.
- `test_classifier.py`: Unit test suite testing splits, labels, and metrics.
- `cell_data.csv`: Sample numerical features dataset.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To run the classification pipeline:
```bash
python main.py --input cell_data.csv --output malaria_roc.png
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_classifier.py
```
