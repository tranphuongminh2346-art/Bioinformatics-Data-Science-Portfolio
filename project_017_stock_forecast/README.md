# Stock Price Forecasting with Lag Features

A time series forecasting program in Python that engineers autoregressive features (lags and shifted rolling statistics), trains a regularized **Ridge Regression** model, and performs recursive multi-step forecasting of future values.

This project demonstrates sequential data splits, avoiding target leakage in rolling window statistics, and recursive out-of-sample prediction loops.

## Features
- **Autoregressive Feature Engineering**:
  - Lags: `lag_1`, `lag_2`, `lag_3` close values.
  - Non-leaking Rolling Stats: 3-day shifted moving averages and standard deviations (volatility) calculated from prior data only.
- **Sequential Validation Split**: Splits dataset sequentially by time (first 80% train, last 20% test) to prevent time-travel leakage in models.
- **Recursive Forecasting**: Implements recursive prediction loops where forecasts at step $t+1$ use predictions from step $t$ as lag inputs.
- **Forecast Dashboard**: Plots historic stock values, test predictions, and future forecasted prices.

## Project Structure
- `forecaster.py`: Main class `StockPriceForecaster` executing features engineering, splits, training, and plotting.
- `main.py`: Command-line interface driver executing the pipeline.
- `test_forecaster.py`: Unit test suite verifying shifted lags, sequential splits, and predictions.
- `stock_history.csv`: Sample historical stock prices dataset.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To run the forecasting pipeline:
```bash
python main.py --input stock_history.csv --output stock_forecast.png --steps 5
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_forecaster.py
```
