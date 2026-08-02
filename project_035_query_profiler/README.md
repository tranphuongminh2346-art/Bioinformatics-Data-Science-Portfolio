# SQLite Indexing & Query Profiler

A database engineering benchmarking utility that measures SQLite query latencies, profiles the impact of B-tree indexing on read/write speeds, and generates logarithmic-scale benchmark charts.

## Features
- **Database Schema Builder**: Builds unindexed and indexed table duplicates.
- **Bulk Insert Transactions**: Inserts large datasets under active transactions using `executemany` to profile baseline population latency.
- **Query Latency Benchmarking**: Profiles search execution speeds using `time.perf_counter()` over random queries and calculates speedup ratios.
- **Benchmark Charting**: Generates log-scale boxplot dashboards comparing search latencies.

## Project Structure
- `query_profiler.py`: SQL tables setup, index builder, benchmarking, and boxplotters.
- `main.py`: Command-line interface driver.
- `test_profiler.py`: Unit test suite verifying index creations and SQL records.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To run the database profiler benchmarks:
```bash
python main.py --records 5000 --lookups 100 --output indexing_benchmark.png
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_profiler.py
```
