"""
Clinical Trial Data ETL Pipeline
Author: Portfolio Creator
Description: Core module implementing Extract, Transform, Load (ETL) logic,
             SQLite database interactions, SQL aggregations, and plotting.
Language: English (100%)
"""

import json
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import re
from datetime import datetime

class ClinicalTrialPipeline:
    """ETL Pipeline for clinical trial records."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path

    def extract(self, json_path: str) -> pd.DataFrame:
        """
        Extracts raw data from JSON file.
        
        Args:
            json_path (str): Path to JSON file.
            
        Returns:
            pd.DataFrame: Raw DataFrame.
        """
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return pd.DataFrame(data)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms and cleans clinical trial records.
        - Validates NCT ID format (starts with NCT followed by 8 digits).
        - Filters out records with negative enrollment.
        - Standardizes phases to Phase 1/2/3/4 or Other.
        - Standardizes start dates to YYYY-MM-DD.
        
        Args:
            df (pd.DataFrame): Raw clinical trial data.
            
        Returns:
            pd.DataFrame: Cleaned data.
        """
        cleaned_records = []
        
        for _, row in df.iterrows():
            nct_id = str(row.get('nct_id', '')).strip()
            
            # 1. Validate NCT ID (e.g., NCT04368728)
            if not re.match(r"^NCT\d{8}$", nct_id):
                continue  # Skip invalid IDs
                
            # 2. Clean enrollment
            try:
                enrollment = int(row.get('enrollment', 0))
                if enrollment < 0:
                    continue  # Skip negative enrollment
            except (ValueError, TypeError):
                enrollment = 0
                
            # 3. Clean phase
            phase = str(row.get('phase', 'Other')).strip()
            valid_phases = ["Phase 1", "Phase 2", "Phase 3", "Phase 4"]
            if phase not in valid_phases:
                # Attempt to map variations
                match = re.search(r"Phase\s*([1-4])", phase, re.IGNORECASE)
                if match:
                    phase = f"Phase {match.group(1)}"
                else:
                    phase = "Other"

            # 4. Clean start date
            start_date = str(row.get('start_date', '')).strip()
            try:
                # Check if it fits YYYY-MM-DD
                parsed_date = datetime.strptime(start_date, "%Y-%m-%d")
                clean_date = parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                clean_date = None  # Handle invalid date string
                
            # 5. Clean Title, Sponsor, and Condition
            title = str(row.get('title', 'Untitled')).strip()
            sponsor = str(row.get('sponsor', 'Unknown')).strip()
            condition = str(row.get('condition', 'Unknown')).strip()
            status = str(row.get('status', 'Unknown')).strip()

            cleaned_records.append({
                "nct_id": nct_id,
                "title": title,
                "status": status,
                "phase": phase,
                "enrollment": enrollment,
                "sponsor": sponsor,
                "start_date": clean_date,
                "condition": condition
            })
            
        return pd.DataFrame(cleaned_records)

    def load(self, df: pd.DataFrame):
        """
        Loads cleaned records into SQLite database.
        
        Args:
            df (pd.DataFrame): Cleaned DataFrame.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create table schema
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
        
        # Clear existing entries for idempotent loading
        cursor.execute("DELETE FROM trials")
        
        # Insert records
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO trials (nct_id, title, status, phase, enrollment, sponsor, start_date, condition)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row['nct_id'], row['title'], row['status'], row['phase'],
                row['enrollment'], row['sponsor'], 
                None if pd.isna(row['start_date']) else row['start_date'], 
                row['condition']
            ))
            
        conn.commit()
        conn.close()

    def query_phase_distribution(self) -> pd.DataFrame:
        """
        Runs an SQL query to get count of trials per phase.
        
        Returns:
            pd.DataFrame: Aggregated data.
        """
        conn = sqlite3.connect(self.db_path)
        query = """
            SELECT phase, COUNT(*) as trial_count, SUM(enrollment) as total_enrollment
            FROM trials
            GROUP BY phase
            ORDER BY phase
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def query_top_conditions(self, limit: int = 5) -> pd.DataFrame:
        """
        Runs an SQL query to get top conditions studied.
        
        Args:
            limit (int): Max number of conditions.
            
        Returns:
            pd.DataFrame: Top conditions list.
        """
        conn = sqlite3.connect(self.db_path)
        query = f"""
            SELECT condition, COUNT(*) as trial_count
            FROM trials
            GROUP BY condition
            ORDER BY trial_count DESC
            LIMIT {limit}
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def plot_phase_distribution(self, phase_df: pd.DataFrame, output_path: str):
        """
        Generates a premium bar plot showing trial counts by phase.
        
        Args:
            phase_df (pd.DataFrame): Phase summary dataframe.
            output_path (str): File path to save plot.
        """
        plt.figure(figsize=(8, 5))
        
        # Bar plotting
        colors = ['#38bdf8', '#0284c7', '#0369a1', '#075985', '#0f172a']
        bars = plt.bar(
            phase_df['phase'], 
            phase_df['trial_count'], 
            color=colors[:len(phase_df)],
            edgecolor='#e2e8f0',
            width=0.5
        )
        
        # Grid and Labels
        plt.grid(axis='y', linestyle=':', alpha=0.6)
        plt.title("Clinical Trial Distribution by Phase", fontsize=12, fontweight='bold', pad=15)
        plt.xlabel("Development Phase", fontsize=10)
        plt.ylabel("Number of Trials", fontsize=10)
        
        # Annotate counts on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.annotate(
                f'{height}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom', fontsize=9, fontweight='bold'
            )
            
        plt.ylim(0, max(phase_df['trial_count']) + 1)
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
