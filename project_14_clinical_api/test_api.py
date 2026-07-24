"""
Integration Tests for Clinical Trials REST API
Author: Portfolio Creator
Description: Uses Flask test client to verify routes, parameters filters, and statistics.
Language: English (100%)
"""

import unittest
import os
import sys
import tempfile
import sqlite3
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, DEFAULT_DB_PATH
import app as api_module

class TestClinicalTrialsAPI(unittest.TestCase):

    def setUp(self):
        # Configure app for testing
        app.config['TESTING'] = True
        self.client = app.test_client()

        # Create temporary database
        self.db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        
        # Override the database path in the api module
        self.original_db_path_getter = api_module.get_db_path
        api_module.get_db_path = lambda: self.temp_db_path

        # Populate temporary database with mock trial records
        conn = sqlite3.connect(self.temp_db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE trials (
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
        cursor.execute("""
            INSERT INTO trials (nct_id, title, status, phase, enrollment, sponsor, start_date, condition)
            VALUES 
            ('NCT123', 'Trial Alpha', 'RECRUITING', 'Phase 3', 100, 'Sponsor A', '2021-01-01', 'Diabetes'),
            ('NCT456', 'Trial Beta', 'COMPLETED', 'Phase 2', 50, 'Sponsor B', '2020-05-12', 'Oncology')
        """)
        conn.commit()
        conn.close()

    def tearDown(self):
        # Restore original database getter
        api_module.get_db_path = self.original_db_path_getter
        
        os.close(self.db_fd)
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("service", data)
        self.assertIn("endpoints", data["documentation"])

    def test_get_all_trials(self):
        response = self.client.get('/api/trials')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["count"], 2)
        self.assertEqual(data["trials"][0]["nct_id"], "NCT123")

    def test_get_trials_filtered(self):
        # Filter by phase
        response = self.client.get('/api/trials?phase=Phase 3')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["trials"][0]["nct_id"], "NCT123")

        # Filter by status
        response = self.client.get('/api/trials?status=COMPLETED')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["trials"][0]["nct_id"], "NCT456")

    def test_get_trial_by_id(self):
        # Valid ID
        response = self.client.get('/api/trials/NCT123')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["title"], "Trial Alpha")

        # Invalid ID
        response = self.client.get('/api/trials/NCT000')
        self.assertEqual(response.status_code, 404)

    def test_statistics(self):
        response = self.client.get('/api/statistics')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["summary"]["total_trials"], 2)
        # Average of 100 and 50 is 75
        self.assertAlmostEqual(data["summary"]["average_enrollment"], 75.0)
        self.assertEqual(data["phase_distribution"]["Phase 3"], 1)

if __name__ == "__main__":
    unittest.main()
