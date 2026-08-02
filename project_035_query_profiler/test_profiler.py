"""
Unit Tests for Database Query Profiler
Author: Portfolio Creator
Description: Verify SQLite table creations, index existences, and record insertions.
Language: English (100%)
"""

import unittest
import os
import sys
import sqlite3
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from query_profiler import DatabaseProfiler

class TestDatabaseProfiler(unittest.TestCase):

    def setUp(self):
        # Temp database setup
        self.db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.db_fd)
        self.profiler = DatabaseProfiler(self.temp_db_path)

    def tearDown(self):
        if os.path.exists(self.temp_db_path):
            try:
                os.remove(self.temp_db_path)
            except PermissionError:
                pass

    def test_table_creation(self):
        # Check tables exist
        with sqlite3.connect(self.temp_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [t[0] for t in cursor.fetchall()]
            self.assertIn("users_unindexed", tables)
            self.assertIn("users_indexed", tables)

    def test_populate_data(self):
        # Populate 10 records
        self.profiler.populate_data(n_records=10)
        self.assertEqual(len(self.profiler.emails), 10)
        
        with sqlite3.connect(self.temp_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users_unindexed")
            self.assertEqual(cursor.fetchone()[0], 10)

    def test_index_existence(self):
        self.profiler.populate_data(n_records=10)
        self.profiler.create_index()
        
        # Verify index exists in sqlite_master
        with sqlite3.connect(self.temp_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='users_indexed'")
            indices = [idx[0] for idx in cursor.fetchall()]
            self.assertIn("idx_email", indices)

    def test_benchmarking(self):
        self.profiler.populate_data(n_records=10)
        self.profiler.create_index()
        
        unindexed, indexed = self.profiler.run_benchmark(n_lookups=5)
        self.assertEqual(len(unindexed), 5)
        self.assertEqual(len(indexed), 5)
        
        # Assert latencies are numbers
        for val in unindexed + indexed:
            self.assertTrue(val >= 0)

if __name__ == "__main__":
    unittest.main()
