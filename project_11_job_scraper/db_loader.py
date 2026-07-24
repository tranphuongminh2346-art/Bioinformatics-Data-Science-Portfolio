"""
Jobs Database Loader & Analyzer
Author: Portfolio Creator
Description: Standardizes SQLite operations for loading job listings,
             cleaning database records, and executing analytics queries.
Language: English (100%)
"""

import sqlite3
import pandas as pd

class JobDatabaseLoader:
    """Manages SQLite storage and aggregated queries for job listings."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path

    def load_jobs(self, jobs: list):
        """
        Creates job_listings table and bulk inserts parsed dictionary items.
        
        Args:
            jobs (list): List of job dicts.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                company TEXT,
                location TEXT,
                salary_text TEXT,
                min_salary REAL,
                max_salary REAL,
                avg_salary REAL
            )
        """)
        
        # Idempotent write
        cursor.execute("DELETE FROM job_listings")
        
        for job in jobs:
            cursor.execute("""
                INSERT INTO job_listings (title, company, location, salary_text, min_salary, max_salary, avg_salary)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                job['title'], job['company'], job['location'], job['salary_text'],
                job['min_salary'], job['max_salary'], job['avg_salary']
            ))
            
        conn.commit()
        conn.close()

    def get_salary_by_location(self) -> pd.DataFrame:
        """
        Calculates average salary grouped by location from SQLite.
        
        Returns:
            pd.DataFrame: SQL results.
        """
        conn = sqlite3.connect(self.db_path)
        query = """
            SELECT location, 
                   COUNT(*) as job_count, 
                   ROUND(AVG(avg_salary), 2) as average_salary
            FROM job_listings
            WHERE avg_salary IS NOT NULL
            GROUP BY location
            ORDER BY average_salary DESC
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def get_highest_paying_jobs(self, limit: int = 3) -> pd.DataFrame:
        """
        Selects the top N highest-paying job listings.
        
        Returns:
            pd.DataFrame: Top listings.
        """
        conn = sqlite3.connect(self.db_path)
        query = f"""
            SELECT title, company, location, avg_salary
            FROM job_listings
            WHERE avg_salary IS NOT NULL
            ORDER BY avg_salary DESC
            LIMIT {limit}
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
