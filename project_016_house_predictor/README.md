# California Real Estate House Price Predictor

A machine learning pipeline that preprocesses real estate features, scales them using standardization (`StandardScaler`), trains a regularized **Ridge Regression** model to predict house valuations, and plots the actual vs. predicted values.

This project demonstrates preprocessing scaling pipelines, linear/ridge regression weight analysis, and standard regression evaluation metrics (MAE, RMSE, $R^2$).

## Features
- **Feature Scaling**: Implements standard scaling to normalize differing numerical features (such as income, house age, population, coordinates).
- **Ridge Regression Model**: Trains an L2 regularized Ridge model to predict median house values.
- **Evaluation Coefficients**: Calculates Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and Coefficient of Determination ($R^2$ score).
- **Diagnostics Chart**: Plots a scatter graph showing actual prices vs. model predictions along with a perfect fit line.
- **Weight Analysis**: Extracts and ranks regression coefficients to explain the positive/negative impact of features on property values.

## Project Structure
- `price_predictor.py`: Main class `HousePricePredictor` managing scaling, Ridge fitting, metrics, and plotting.
- `main.py`: Command-line interface driver executing the pipeline.
- `test_predictor.py`: Unit test suite testing standardizations, training, and scores.
- `housing.csv`: Sample real estate data subset.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To train the model and plot evaluations:
```bash
python main.py --input housing.csv --output price_fit.png
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_predictor.py
```
