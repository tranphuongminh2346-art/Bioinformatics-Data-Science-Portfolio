# Stock Trading Strategy Backtester

A quantitative finance simulation pipeline that parses historical stock daily close prices, computes rolling **Simple Moving Average (SMA)** crossover indicators, and executes a transactional trading simulation backtester.

It generates buy/sell triggers, updates cash ledger accounts, and plots portfolio equity growth curves alongside drawdown profiles and Sharpe ratios.

## Features
- **SMA Crossover Strategy logic**: Generates buy triggers when short-term SMA exceeds long-term SMA (bullish crossover) and sell signals otherwise.
- **Transactional Ledger Accounting**: Simulates cash allocations where capital gains dynamically track stock growth during long position phases.
- **Backtesting Performance Metrics**:
  - Annualized Sharpe Ratio.
  - Maximum Drawdown (peak-to-trough drops).
  - Cumulative Returns.
- **Diagnostics Charting**: Generates buy/sell triggers markers and cumulative equity curves.

## Project Structure
- `backtester.py`: SMA indicators math, ledger logs, and plot builders.
- `main.py`: Command-line interface driver.
- `test_backtester.py`: Unit test suite verifying rolling averages and drawdown math.
- `stock_prices.csv`: Sample historical daily prices database.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To simulate strategy backtests:
```bash
python main.py --input stock_prices.csv --short 3 --long 5 --capital 10000.0 --output backtest_result.png
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_backtester.py
```
