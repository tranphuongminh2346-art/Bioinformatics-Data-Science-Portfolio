# PubMed Literature Search API Pipeline

A biological data engineering pipeline that interfaces with the **NCBI Entrez e-Utilities REST API** (`ESearch` and `ESummary`) to search scientific literature, retrieve metadata abstracts summaries, and log them into structured CSV files.

Includes automatic network exception-handling wrappers that fall back to a localized mock database when executing in network-restricted environments.

## Features
- **NCBI Entrez API Interface**: Sends requests to ESearch and ESummary endpoints to obtain PMIDs and structured XML/JSON article profiles.
- **Robust Exception Handling**: Integrates timeouts and connection status checks to ensure graceful fallbacks when offline.
- **CSV Data Exporter**: Saves structured article database tables (PMID, title, source journal, publication date, authors list).

## Project Structure
- `pubmed_fetcher.py`: Entrez API requests calls, parser, and offline fallbacks.
- `main.py`: Command-line interface driver.
- `test_fetcher.py`: Unit test suite verifying offline fallbacks and output files.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To search and download articles:
```bash
python main.py --query bioinformatics --limit 3 --output pubmed_articles.csv
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_fetcher.py
```
