# Customer Churn Predictor

A Python-based Machine Learning pipeline that processes customer subscription records, performs one-hot encoding for categorical variables, trains a Random Forest Classifier to identify churn risk, and visualizes feature importances.

The project demonstrates practical data science techniques: processing demographic/contract features, training ensemble decision classifiers, calculating feature importances, and evaluating classification boundaries.

## Features
- **Data Preprocessing**:
  - Automatically parses numeric columns and handles missing variables.
  - One-hot encodes categorical customer features (Contract type, Internet Service type).
  - Encapsulates target categorical label ('Churn') into binary indicators (`1` for Yes, `0` for No).
- **Model Training**: Random Forest classification model with L2 regularization properties.
- **Model Diagnostics**:
  - Computes standard test accuracy, precision, and recall scores.
  - Calculates feature importances weights to understand key indicators behind customer churn.
- **Diagnostics Plot**: Generates a horizontal bar chart displaying feature significance metrics.
- **Inference Pipeline**: Classifies new customer logs to predict their likelihood to churn.

## Project Structure
- `churn_model.py`: Core machine learning class implementing the Random Forest training, evaluation, and plotting.
- `main.py`: Command-line interface driver that trains the model and performs a sample inference.
- `test_churn.py`: Unit test suite testing preprocessing pipelines, shapes, and inference boundaries.
- `churn_data.csv`: Clean sample customer database log.
- `requirements.txt`: Package dependencies.

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

To run the machine learning pipeline and train the churn classifier:
```bash
python main.py --input churn_data.csv --output feature_importances.png
```

This command will:
1. Load and encode customer metrics.
2. Partition the data and train the Random Forest model.
3. Print classification precision, recall, and F1 summaries.
4. Export the feature importance chart to `feature_importances.png`.
5. Run a diagnostic prediction on a sample customer with high-risk attributes (short tenure, fiber optic, month-to-month) and print results.

## Running Unit Tests
To run the automated tests:
```bash
python -m unittest test_churn.py
```
