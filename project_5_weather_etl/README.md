# Weather Monitoring ETL Pipeline

A professional Python-based ETL (Extract, Transform, Load) data engineering pipeline that processes hourly weather temperature records. The pipeline can fetch live weather parameters from the **real Open-Meteo Weather API** based on spatial coordinates or process cached regional weather histories.

It transforms temperature units (Celsius to Fahrenheit), computes rolling averages, writes datasets into SQLite, and plots temperature variations along with moving trendlines.

## Features
- **Data Extraction**:
  - Live query: connects to the Open-Meteo REST API given latitude and longitude.
  - Offline fallback: loads a cached regional weather history JSON file.
- **Data Transformation**:
  - Converts Celsius temperature observations to Fahrenheit.
  - Calculates a 3-hour rolling average using Pandas window operators.
  - Normalizes timezone timestamps.
- **Data Loading**: Performs bulk loading of data into SQLite (`weather.db`).
- **SQL Aggregations**: Executes SQL aggregation queries to summarize maximum, minimum, and average temperatures for a given record batch.
- **Trend Plotting**: Saves a line chart comparing raw hourly temperatures against rolling averages.

## Project Structure
- `etl.py`: Core ETL engine class `WeatherETL` performing extraction, transformations, and plotting.
- `db_loader.py`: Class `WeatherDatabaseLoader` handling SQLite tables, inserts, and summary queries.
- `main.py`: Command-line driver tool.
- `test_etl.py`: Automated unit tests verifying conversions, rolling formulas, and DB operations.
- `weather_cache.json`: Real hourly temperature cache payload for London.
- `requirements.txt`: Package dependencies.

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

To run the pipeline using the local weather cache data:
```bash
python main.py --db weather.db --output weather_trend.png
```

To run the pipeline and query live weather observations for a specific coordinate (e.g. London: lat `51.5085`, lon `-0.1257`):
```bash
python main.py --latitude 51.5085 --longitude -0.1257 --db weather.db --output london_weather.png
```

This command will:
1. Fetch hourly temperatures from the live Open-Meteo API.
2. Clean, transform, and compute rolling averages.
3. Establish database records.
4. Execute SQL aggregations and print average, max, and min temperatures to the console.
5. Export a trendline diagram.

## Running Unit Tests
To run the automated tests:
```bash
python -m unittest test_etl.py
```
