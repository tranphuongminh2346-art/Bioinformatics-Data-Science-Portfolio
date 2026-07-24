"""
Unit Tests for Clinical Trial ETL Pipeline
Author: Portfolio Creator
Description: Test suite for verifying pipeline extraction, cleaning, and database loading.
Language: English (100%)
"""

import unittest
import os
import sqlite3
import pandas as pd
import sys
import tempfile

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pipeline import ClinicalTrialPipeline

class TestClinicalTrialPipeline(unittest.TestCase):

    def setUp(self):
        # Create a temp database file
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        self.pipeline = ClinicalTrialPipeline(self.db_path)

        # Mock raw data
        self.raw_data = pd.DataFrame([
            {
                "nct_id": "NCT12345678",
                "title": "Trial 1",
                "status": "Completed",
                "phase": "Phase 3",
                "enrollment": 100,
                "sponsor": "Sponsor A",
                "start_date": "2021-01-01",
                "condition": "Diabetes"
            },
            {
                "nct_id": "INVALID_ID",  # Invalid NCT ID format
                "title": "Trial 2",
                "status": "Recruiting",
                "phase": "Phase 2",
                "enrollment": 50,
                "sponsor": "Sponsor B",
                "start_date": "2021-02-02",
                "condition": "Oncology"
            },
            {
                "nct_id": "NCT87654321",
                "title": "Trial 3",
                "status": "Completed",
                "phase": "Phase 1/2",  # Will map to Phase 1
                "enrollment": -10,      # Invalid negative enrollment
                "sponsor": "Sponsor C",
                "start_date": "2021-03-03",
                "condition": "Cardiology"
            },
            {
                "nct_id": "NCT00001111",
                "title": "Trial 4",
                "status": "Completed",
                "phase": "Early Phase 1",  # Will map to Phase 1
                "enrollment": 25,
                "sponsor": "Sponsor D",
                "start_date": "invalid-date",  # Invalid date format, sets to None
                "condition": "Diabetes"
            }
        ])

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_transformation(self):
        cleaned_df = self.pipeline.transform(self.raw_data)
        
        # Valid records should be 2: Trial 1 and Trial 4
        # Trial 2 is excluded (invalid ID)
        # Trial 3 is excluded (negative enrollment)
        self.assertEqual(len(cleaned_df), 2)
        
        # Verify specific values for Trial 1
        trial_1 = cleaned_df[cleaned_df['nct_id'] == 'NCT12345678'].iloc[0]
        self.assertEqual(trial_1['phase'], 'Phase 3')
        self.assertEqual(trial_1['enrollment'], 100)
        self.assertEqual(trial_1['start_date'], '2021-01-01')

        # Verify mapping for Trial 4
        trial_4 = cleaned_df[cleaned_df['nct_id'] == 'NCT00001111'].iloc[0]
        self.assertEqual(trial_4['phase'], 'Phase 1')
        self.assertTrue(pd.isna(trial_4['start_date']))

    def test_load_and_queries(self):
        cleaned_df = self.pipeline.transform(self.raw_data)
        self.pipeline.load(cleaned_df)

        # Check raw DB contents
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM trials")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 2)
        conn.close()

        # Query phase distribution
        phase_df = self.pipeline.query_phase_distribution()
        self.assertEqual(len(phase_df), 2)  # Phase 1 and Phase 3
        
        # Check counts
        phase_3_row = phase_df[phase_df['phase'] == 'Phase 3'].iloc[0]
        self.assertEqual(phase_3_row['trial_count'], 1)
        self.assertEqual(phase_3_row['total_enrollment'], 100)

        # Query top conditions
        condition_df = self.pipeline.query_top_conditions(limit=5)
        # Diabetes should have 2 trials
        diabetes_row = condition_df[condition_df['condition'] == 'Diabetes'].iloc[0]
        self.assertEqual(diabetes_row['trial_count'], 2)

if __name__ == "__main__":
    unittest.main()
