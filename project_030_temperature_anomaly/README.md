# Climate Temperature Anomaly Time Series Analyzer

A climatological data science pipeline that parses monthly global temperature anomaly logs, fits linear regression trends to calculate decadal warming indexes, and performs **Seasonal Decomposition** to separate global warming trends from seasonal cycles.

## Features
- **Seasonal Decomposition of Timeseries**: Uses `statsmodels.tsa.seasonal.seasonal_decompose` to break down time series records into Trend, Seasonal, and Residual components:
  $$Y(t) = T(t) + S(t) + E(t)$$
- **Decadal Warming Index Estimation**: Calculates regression slope coefficients over time coordinates to output decadal warming rates.
- **4-Panel Diagnostic dashboards**: Exports observed lines, trend directions, seasonal patterns, and residuals scatter plots.

## Project Structure
- `time_series.py`: Timeseries loaders, trend fits, and seasonal decompose engines.
- `main.py`: Command-line interface driver.
- `test_series.py`: Unit test suite verifying index formatting and regression slopes.
- `temperature_anomaly.csv`: Sample temperature anomaly database.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To run the decomposition pipeline:
```bash
python main.py --input temperature_anomaly.csv --period 12 --output anomaly_decomposition.png
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_series.py
```
