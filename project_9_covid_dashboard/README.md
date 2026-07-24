# COVID-19 Daily Report Dashboard

A lightweight, self-contained Python program to transform cumulative epidemic timeseries statistics, calculate daily new metrics (cases, deaths), compute moving window averages, and plot trend curves using dual y-axes.

It implements basic mathematical operations for timeseries preprocessing, including differencing (`diff()`), percentage change (`pct_change()`), and rolling window means.

## Features
- **Timeseries Transformation**: Converts cumulative counts of cases and deaths into daily increments.
- **Trend Smoothing**: Computes 7-day rolling averages of daily cases and deaths to reduce weekday reporting noise.
- **Growth Analysis**: Evaluates case growth rates over time using percentage change metrics.
- **Dual Y-Axis Dashboard**: Plots new cases (bar chart and smoothed trendline) on the left y-axis, and new deaths (smoothed trendline) on the right y-axis.

## Project Structure
- `covid_analyzer.py`: Main class `CovidTimeSeriesAnalyzer` performing calculations and plotting.
- `main.py`: Command-line driver printing stats and saving plots.
- `test_covid.py`: Automated unit tests verifying differencing and moving averages.
- `covid_data.csv`: Sample historical cumulative COVID-19 dataset.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To run the analysis:
```bash
python main.py --input covid_data.csv --output covid_trends.png
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_covid.py
```
