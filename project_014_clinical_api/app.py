"""
Clinical Trials REST API Web Server
Author: Portfolio Creator
Description: Flask server exposing SQL database logs of clinical trials via JSON APIs.
             Includes filters for condition, phase, and status.
Language: English (100%)
"""

import os
import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

# Locate Day 2 database or fall back to local folder
DEFAULT_DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "day02_clinical_trial_pipeline",
    "trials.db"
)
LOCAL_DB_PATH = "trials.db"

def get_db_path() -> str:
    """Returns the path to the SQLite database."""
    if os.path.exists(DEFAULT_DB_PATH):
        return DEFAULT_DB_PATH
    return LOCAL_DB_PATH

def query_db(query: str, args: tuple = (), one: bool = False):
    """Utility to query SQLite and return dictionary structures."""
    db_path = get_db_path()
    if not os.path.exists(db_path):
        # Create a mock database with empty table if not found to prevent crashes
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trials (
                nct_id TEXT PRIMARY KEY,
                title TEXT,
                status TEXT,
                phase TEXT,
                enrollment INTEGER,
                sponsor TEXT,
                start_date TEXT,
                condition TEXT
            )
        """)
        conn.commit()
        conn.close()

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, args)
    rv = cursor.fetchall()
    conn.close()
    
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
    """Service Index Page returning API listings."""
    return jsonify({
        "service": "Clinical Trials Metadata REST API",
        "documentation": {
            "endpoints": [
                {
                    "path": "/api/trials",
                    "method": "GET",
                    "description": "Retrieve list of all clinical trials. Supports query filters: status, phase, sponsor.",
                    "parameters": "?phase=Phase%203&status=RECRUITING&sponsor=Pfizer"
                },
                {
                    "path": "/api/trials/<nct_id>",
                    "method": "GET",
                    "description": "Retrieve metadata details for a specific clinical trial (NCT ID)."
                },
                {
                    "path": "/api/statistics",
                    "method": "GET",
                    "description": "Retrieve database statistical aggregations (enrollment metrics, phase counts)."
                }
            ]
        }
    })

@app.route('/api/trials', methods=['GET'])
def get_trials():
    """Queries and returns list of trials, applying URL parameters filters."""
    phase = request.args.get('phase')
    status = request.args.get('status')
    sponsor = request.args.get('sponsor')
    
    query = "SELECT * FROM trials WHERE 1=1"
    params = []
    
    if phase:
        query += " AND phase = ?"
        params.append(phase)
    if status:
        query += " AND status = ?"
        params.append(status)
    if sponsor:
        query += " AND sponsor LIKE ?"
        params.append(f"%{sponsor}%")
        
    rows = query_db(query, tuple(params))
    trials_list = [dict(row) for row in rows]
    return jsonify({"count": len(trials_list), "trials": trials_list})

@app.route('/api/trials/<nct_id>', methods=['GET'])
def get_trial_by_id(nct_id):
    """Retrieves a single trial profile by its NCT ID key."""
    row = query_db("SELECT * FROM trials WHERE nct_id = ?", (nct_id,), one=True)
    if row:
        return jsonify(dict(row))
    return jsonify({"error": f"Clinical trial with NCT ID '{nct_id}' not found."}), 404

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Aggregates metrics directly via SQL."""
    stats_row = query_db("""
        SELECT COUNT(*) as total_trials, 
               SUM(enrollment) as cumulative_enrollment,
               AVG(enrollment) as average_enrollment
        FROM trials
    """, one=True)
    
    phase_rows = query_db("SELECT phase, COUNT(*) as count FROM trials GROUP BY phase")
    
    if stats_row and stats_row["total_trials"] > 0:
        return jsonify({
            "summary": {
                "total_trials": stats_row["total_trials"],
                "cumulative_enrollment": stats_row["cumulative_enrollment"],
                "average_enrollment": round(stats_row["average_enrollment"], 2)
            },
            "phase_distribution": {row["phase"]: row["count"] for row in phase_rows if row["phase"]}
        })
        
    return jsonify({"message": "Database is empty. No statistics available."}), 200

if __name__ == '__main__':
    # Get port from environment or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
