# ECG Heart Rate Variability Extractor

An ECG signal processing and data engineering pipeline that loads timeseries records of heartbeat R-R intervals (in milliseconds), calculates statistical **Time-Domain** indices (SDNN, RMSSD, pNN50), and computes **Frequency-Domain** spectral powers (LF, HF, LF/HF ratio) using Fast Fourier Transforms (FFT) on resampled grids.

## Features
- **Time-Domain HRV Metrics**:
  - SDNN: Standard Deviation of normal-to-normal intervals (overall autonomic activity).
  - RMSSD: Root Mean Square of Successive Differences (parasympathetic activity).
  - pNN50: Percentage of successive intervals differing by $>50$ ms.
- **Frequency-Domain HRV Metrics**: Resamples the irregular heartbeat timeseries onto a regular grid (at 4 Hz) using linear interpolation, detrends variables, and applies Fast Fourier Transforms (FFT) to extract LF (0.04-0.15 Hz) and HF (0.15-0.40 Hz) powers.

## Project Structure
- `hrv_extractor.py`: RR resamplers, time domain calculators, and FFT bandpower estimators.
- `main.py`: Command-line interface driver.
- `test_hrv.py`: Unit test suite verifying RMSSD, SDNN, and pNN50 math.
- `ecg_rr_intervals.csv`: Sample ECG heartbeat intervals database.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To generate HRV reports:
```bash
python main.py --input ecg_rr_intervals.csv
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_hrv.py
```
