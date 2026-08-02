"""
Database Indexing & Query Profiler
Author: Portfolio Creator
Description: Measures SQL query execution latency on SQLite databases,
             profiles B-tree index read/write benchmarks, and plots latency comparisons.
Language: English (100%)
"""

import sqlite3
import time
import random
import matplotlib.pyplot as plt

class DatabaseProfiler:
    """Profiles SQLite search queries on indexed vs unindexed table structures."""
    
    def __init__(self, db_path: str = "profiler.db"):
        self.db_path = db_path
        self.emails = []
        self.create_tables()

    def create_tables(self):
        """Initializes tables for indexing latency profiling benchmarks."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Unindexed Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users_unindexed (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    email TEXT,
                    registration_date TEXT
                )
            """)
            
            # Indexed Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users_indexed (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    email TEXT,
                    registration_date TEXT
                )
            """)
            conn.commit()

    def populate_data(self, n_records: int = 5000):
        """Generates random user records and inserts them in bulk transactions."""
        self.emails = [f"user_{i}_{random.randint(1000, 9999)}@domain.com" for i in range(n_records)]
        
        records = []
        for i in range(n_records):
            records.append((
                f"UID_{random.randint(100000, 999999)}",
                self.emails[i],
                "2026-07-16"
            ))
            
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Clear previous runs
            cursor.execute("DELETE FROM users_unindexed")
            cursor.execute("DELETE FROM users_indexed")
            
            # Insert into Unindexed Table
            cursor.executemany("""
                INSERT INTO users_unindexed (user_id, email, registration_date)
                VALUES (?, ?, ?)
            """, records)
            
            # Insert into Indexed Table
            cursor.executemany("""
                INSERT INTO users_indexed (user_id, email, registration_date)
                VALUES (?, ?, ?)
            """, records)
            conn.commit()

    def create_index(self):
        """Builds a B-tree index on the email column in the indexed table."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Drop index if exists to allow rerun
            cursor.execute("DROP INDEX IF EXISTS idx_email")
            cursor.execute("""
                CREATE INDEX idx_email ON users_indexed(email)
            """)
            conn.commit()

    def run_benchmark(self, n_lookups: int = 100) -> tuple:
        """
        Measures search times for email lookup queries on both tables.
        
        Returns:
            tuple: (unindexed_latencies: list, indexed_latencies: list)
        """
        if not self.emails:
            raise ValueError("Database must be populated before benchmarking.")
            
        unindexed_times = []
        indexed_times = []
        
        # Sample random emails to search for
        query_emails = random.sample(self.emails, min(n_lookups, len(self.emails)))
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 1. Profile Unindexed Lookups
            for email in query_emails:
                start = time.perf_counter()
                cursor.execute("SELECT * FROM users_unindexed WHERE email = ?", (email,))
                cursor.fetchall()
                duration = time.perf_counter() - start
                unindexed_times.append(duration * 1000.0)  # Convert to milliseconds
                
            # 2. Profile Indexed Lookups
            for email in query_emails:
                start = time.perf_counter()
                cursor.execute("SELECT * FROM users_indexed WHERE email = ?", (email,))
                cursor.fetchall()
                duration = time.perf_counter() - start
                indexed_times.append(duration * 1000.0)  # Convert to milliseconds
                
        return unindexed_times, indexed_times

    def plot_benchmark(self, unindexed_times: list, indexed_times: list, output_path: str):
        """Generates latency distribution boxplots comparing both databases."""
        plt.figure(figsize=(8, 6))
        
        data = [unindexed_times, indexed_times]
        labels = ['Unindexed (Full Scan)', 'Indexed (B-Tree Search)']
        
        colors = ['#ef4444', '#10b981']
        bp = plt.boxplot(data, labels=labels, patch_artist=True, widths=0.5)
        
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.6)
            
        plt.title("SQLite Query Latency Benchmark (Indexed vs Unindexed)", fontsize=12, fontweight='bold', pad=15)
        plt.ylabel("Query Latency (milliseconds)", fontsize=10)
        plt.yscale('log')  # Log scale since indexing is orders of magnitude faster
        plt.grid(True, which="both", linestyle=':', alpha=0.5)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
