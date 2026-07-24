# Heart Disease Diagnostic Classifier

A Python-based Machine Learning pipeline that auto-downloads the famous **Cleveland Heart Disease Dataset** from the UCI Machine Learning Repository, cleans and standardizes clinical features, trains a Logistic Regression classifier, and visualizes model diagnostic performance.

It demonstrates key data science practices: handling missing clinical data, feature scaling, model training, confusion matrix reporting, Receiver Operating Characteristic (ROC) curves, and single-patient clinical risk prediction.

## Features
- **Auto-Download**: Fetches the real dataset directly from UCI-mirrored GitHub repository on first run.
- **Preprocessing**:
  - Feature selection: extracts 13 clinical attributes (age, chest pain, cholesterol, resting heart rate, ECG, etc.).
  - Split: standard stratified 80-20 train-test partition.
  - Scaling: fits standard normalizer (`StandardScaler`) to features.
- **Model Training**: Logistic Regression classifier fitted with L2 regularization.
- **Performance Evaluation**:
  - Classification report: logs precision, recall, and F1-score.
  - Plots: Confusion Matrix and ROC Curve (calculates AUC).
- **Patient Inference**: Takes clinical inputs and generates classification predictions (Heart Disease risk detected vs. normal) along with probability scores.

## Project Structure
- `model.py`: Core ML class `HeartDiseaseClassifier` containing download, preprocessing, training, and plotting functions.
- `main.py`: Command-line interface driver that trains the model and performs a sample inference.
- `test_model.py`: Unit test suite testing split distributions, standard scaling, and prediction bounds.
- `requirements.txt`: Project package dependencies.

## Installation

Ensure you have Python 3.8+ installed.

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

To run the pipeline (which automatically downloads the dataset `heart.csv` if it is not present):
```bash
python main.py --confusion confusion_matrix.png --roc roc_curve.png
```

This command will:
1. Fetch and save `heart.csv` locally.
2. Output dataset shape and split metrics.
3. Train the model and print validation accuracy, precision, and recall.
4. Save the performance charts `confusion_matrix.png` and `roc_curve.png`.
5. Run a sample diagnostic prediction for a mock patient with high-risk attributes and output the results.

## Running Unit Tests
To run the automated tests:
```bash
python -m unittest test_model.py
```
