"""
Unit Tests for Redis Cache Simulator
Author: Portfolio Creator
Description: Verify key-value setters, LRU evictions, AOF log re-creation, and states recovery.
Language: English (100%)
"""

import unittest
import os
import sys
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from redis_simulator import RedisCacheSimulator

class TestRedisCacheSimulator(unittest.TestCase):

    def setUp(self):
        # Create a temp AOF file path
        self.db_fd, self.temp_aof_path = tempfile.mkstemp(suffix=".aof")
        os.close(self.db_fd)
        
        # Ensure file starts empty
        if os.path.exists(self.temp_aof_path):
            os.remove(self.temp_aof_path)
            
        self.db = RedisCacheSimulator(capacity=3, aof_path=self.temp_aof_path)

    def tearDown(self):
        if os.path.exists(self.temp_aof_path):
            try:
                os.remove(self.temp_aof_path)
            except PermissionError:
                pass

    def test_set_and_get(self):
        self.db.set("k1", "v1")
        self.assertEqual(self.db.get("k1"), "v1")
        self.assertIsNone(self.db.get("k2"))

    def test_lru_eviction(self):
        # Capacity = 3
        self.db.set("k1", "v1")
        self.db.set("k2", "v2")
        self.db.set("k3", "v3")
        
        # Access k1: makes it most recently used (order: k2, k3, k1)
        self.db.get("k1")
        
        # Set k4: triggers eviction of least recently used (k2)
        self.db.set("k4", "v4")
        
        self.assertIsNone(self.db.get("k2"))
        self.assertEqual(self.db.get("k1"), "v1")
        self.assertEqual(self.db.get("k3"), "v3")
        self.assertEqual(self.db.get("k4"), "v4")

    def test_aof_persistence_and_recovery(self):
        self.db.set("k1", "v1")
        self.db.set("k2", "v2")
        self.db.delete("k1")
        
        # Verify log lines are written
        self.assertTrue(os.path.exists(self.temp_aof_path))
        with open(self.temp_aof_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
            
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0], "SET k1 v1")
        self.assertEqual(lines[1], "SET k2 v2")
        self.assertEqual(lines[2], "DEL k1")
        
        # Re-instantiate a new database pointing to the same AOF
        # Should replay commands and recover state: k2 exists, k1 deleted
        db2 = RedisCacheSimulator(capacity=3, aof_path=self.temp_aof_path)
        self.assertIsNone(db2.get("k1"))
        self.assertEqual(db2.get("k2"), "v2")

if __name__ == "__main__":
    unittest.main()
