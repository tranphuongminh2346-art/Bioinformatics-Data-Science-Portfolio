# Clinical Trial Data ETL Pipeline

A professional Python-based ETL (Extract, Transform, Load) data engineering pipeline that processes clinical trial records, cleans and validates the attributes, stores them in an SQLite database, and generates analytical insights and visualizations.

The data is derived from the **ClinicalTrials.gov JSON API** and contains real clinical metadata for diabetes, oncology, and vaccine studies.

## Features
- **Extraction**: Reads raw trial records from JSON files.
- **Transformation**:
  - Validates NCT ID identifier patterns.
  - Excludes negative enrollment counts.
  - Standardizes development phases (e.g. mapping "Early Phase 1" or "Phase 1/2" to unified standards).
  - Formats date strings to `YYYY-MM-DD` and sets invalid entries to `None`.
- **Loading**: Idempotently inserts records into an SQLite database (`trials.db`).
- **SQL Analysis**: Executes SQL queries to compute phase distributions, enrollment metrics, and top conditions studied.
- **Data Visualization**: Generates a bar chart plot of trial counts across phases.

## Project Structure
- `pipeline.py`: Main module implementing the `ClinicalTrialPipeline` class for ETL operations.
- `main.py`: Command-line interface driver.
- `test_pipeline.py`: Automated unit tests verifying cleaning rules and DB interactions.
- `requirements.txt`: Package dependencies.
- `trials_data.json`: Real trial records subset in JSON format.

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface
Run the main program to execute the ETL pipeline:
```bash
python main.py --input trials_data.json --db trials.db --output phase_chart.png
```

This command will:
1. Parse the JSON trial data.
2. Filter out malformed entries and output counts.
3. Establish the SQLite database schema and load clean records.
4. Execute SQL queries and display summaries (Phase statistics, top disease conditions) directly in the console.
5. Save a bar chart visualization of the trial distribution to `phase_chart.png`.

## Running Unit Tests
To run the automated tests:
```bash
python -m unittest test_pipeline.py
```
