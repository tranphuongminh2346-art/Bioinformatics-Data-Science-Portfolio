# Clinical Trials Metadata REST API

A Flask-based REST API that exposes clinical trial metadata records stored in an SQLite database. It reads the database generated during the Day 2 clinical trial pipeline, providing endpoints to filter, query, and aggregate clinical research datasets.

This project demonstrates RESTful web service design, JSON API payloads, and query-parameter database mapping.

## Features
- **Flexible SQL Filters**: Supports querying trials dynamically with parameters:
  - `phase` (e.g. `Phase 3`)
  - `status` (e.g. `RECRUITING`)
  - `sponsor` (e.g. `Mayo Clinic`)
- **Metadata Retreival**: Accesses full clinical parameters for a specific study key using `/api/trials/<nct_id>`.
- **Statistical Aggregations**: Exposes cumulative counts, total/average enrollments, and phase ratios in JSON format.

## API Endpoint Documentation

| Endpoint | Method | Params | Description |
| :--- | :--- | :--- | :--- |
| `/` | GET | None | Index page showing details of available routes. |
| `/api/trials` | GET | `phase`, `status`, `sponsor` | Retrieve all trials matching optional filters. |
| `/api/trials/<nct_id>` | GET | None | Retrieve specific clinical record details. |
| `/api/statistics` | GET | None | Return summary stats and study distributions. |

## Project Structure
- `app.py`: Main Flask application file containing SQLite connectivity and routes.
- `test_api.py`: Integration test suite using the Flask test client and a mock DB.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To start the REST API web server locally:
```bash
python app.py
```
By default, the server runs on `http://127.0.0.1:5000/`.

You can query endpoints using your web browser or `curl`:
```bash
curl http://127.0.0.1:5000/api/trials?phase=Phase%203
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_api.py
```
