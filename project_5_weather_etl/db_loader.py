"""
Weather Database Loader Utility
Author: Portfolio Creator
Description: Handles SQLite schema creation, data insertion, and analytics queries.
Language: English (100%)
"""

import sqlite3
import pandas as pd

class WeatherDatabaseLoader:
    """Manages SQLite database storage and summarizations for weather logs."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path

    def load(self, df: pd.DataFrame):
        """
        Creates the weather table and inserts DataFrame records.
        
        Args:
            df (pd.DataFrame): Cleaned weather data.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table schema setup
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_log (
                timestamp TEXT PRIMARY KEY,
                temperature_c REAL,
                temperature_f REAL,
                rolling_avg_c REAL
            )
        """)
        
        # Idempotent write: clean old records
        cursor.execute("DELETE FROM weather_log")
        
        # Insert
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO weather_log (timestamp, temperature_c, temperature_f, rolling_avg_c)
                VALUES (?, ?, ?, ?)
            """, (
                row['timestamp'], row['temperature_c'], row['temperature_f'], row['rolling_avg_c']
            ))
            
        conn.commit()
        conn.close()

    def get_summary_stats(self) -> dict:
        """
        Executes SQL queries to retrieve day stats (avg temp, max temp, min temp).
        
        Returns:
            dict: Summary metrics.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                AVG(temperature_c), 
                MAX(temperature_c), 
                MIN(temperature_c) 
            FROM weather_log
        """)
        row = cursor.fetchone()
        conn.close()
        
        if row and row[0] is not None:
            return {
                "avg_temp_c": float(row[0]),
                "max_temp_c": float(row[1]),
                "min_temp_c": float(row[2])
            }
        return {}
