# Bioinformatics Job Listings Scraper & Database

A Python-based Data Engineering pipeline that parses job listing details from structural HTML job cards, extracts salary numbers using regular expressions, loads the cleaned datasets into an SQLite database, and queries aggregations.

It demonstrates HTML web parsing, regex data cleaning, database schema loading, and SQL query summarizations.

## Features
- **HTML Parsing**: Uses BeautifulSoup to target classes (`job-title`, `company`, `location`, `salary`) from structural pages.
- **Salary Regex Parsing**: Extracts numerical salary bounds from string patterns (e.g. `$110,000 - $130,000 a year`, `120 - 150`), calculates midpoints, and handles scale factors (e.g., thousands).
- **SQLite Database Load**: Saves job parameters into SQLite (`jobs.db`) with automatic table creation and idempotent data cleans.
- **SQL Analytics Queries**:
  - Computes average salary by geographic location.
  - Queries top paying positions.

## Project Structure
- `job_parser.py`: HTML processing class `JobListingParser` and regex salary normalizers.
- `db_loader.py`: Class `JobDatabaseLoader` for SQLite schemas, inserts, and reports.
- `main.py`: Command-line interface driver executing the pipeline.
- `test_parser.py`: Unit test suite testing regex matching and card selections.
- `jobs.html`: Mock job postings board page.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To run the scraper and load database metrics:
```bash
python main.py --input jobs.html --db jobs.db
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_parser.py
```
