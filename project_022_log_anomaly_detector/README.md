# Web Log Anomaly Detector

A security analytics pipeline that parses Apache-style server access logs, extracts features, and trains an **Isolation Forest** unsupervised classifier to detect anomalous requests (such as SQL injection attempts, high URL length buffers, and huge downloads).

## Features
- **Regex Log Parser**: Extracts structured IP, method, date, URL, status code, and response size fields from Apache Common logs.
- **Unsupervised Anomaly Modeling**: Uses `IsolationForest` to calculate outlier scores without requiring pre-labeled training data.
- **Diagnostics Reporting**: Logs anomaly score rankings and prints the raw anomalous logs.

## Project Structure
- `anomaly_detector.py`: Log file parsed extractor and classifier classes.
- `main.py`: Command-line interface driver.
- `test_detector.py`: Unit test suite verifying log regex matching and contamination bounds.
- `web_access.log`: Sample server access log database.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To evaluate server traffic anomalies:
```bash
python main.py --input web_access.log --contamination 0.15
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_detector.py
```
