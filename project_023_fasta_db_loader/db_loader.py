"""
Protein database Loader
Author: Portfolio Creator
Description: Initializes SQLite tables, loads FASTA-derived metadata profiles,
             and queries statistical outputs.
Language: English (100%)
"""

import sqlite3

class ProteinDatabaseLoader:
    """Manages SQLite database inserts and queries for protein metadata."""
    
    def __init__(self, db_path: str = "proteins.db"):
        self.db_path = db_path
        self.create_tables()

    def create_tables(self):
        """Initializes tables for protein sequence records."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS proteins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    accession TEXT UNIQUE,
                    entry_name TEXT,
                    db_source TEXT,
                    protein_name TEXT,
                    organism TEXT,
                    tax_id INTEGER,
                    gene_name TEXT,
                    protein_existence INTEGER,
                    sequence_version INTEGER,
                    sequence TEXT,
                    sequence_length INTEGER
                )
            """)
            conn.commit()

    def load_records(self, records: list) -> int:
        """
        Inserts list of parsed records using transactional queries.
        
        Returns:
            int: Number of records successfully loaded.
        """
        inserted_count = 0
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for rec in records:
                try:
                    cursor.execute("""
                        INSERT OR REPLACE INTO proteins (
                            accession, entry_name, db_source, protein_name,
                            organism, tax_id, gene_name, protein_existence,
                            sequence_version, sequence, sequence_length
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        rec["accession"], rec["entry_name"], rec["db_source"], rec["protein_name"],
                        rec["organism"], rec["tax_id"], rec["gene_name"], rec["protein_existence"],
                        rec["sequence_version"], rec["sequence"], len(rec["sequence"])
                    ))
                    inserted_count += 1
                except sqlite3.Error:
                    continue
            conn.commit()
        return inserted_count

    def query_organism_counts(self) -> list:
        """Returns sequence counts grouped by Organism."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT organism, COUNT(*), AVG(sequence_length)
                FROM proteins
                GROUP BY organism
                ORDER BY COUNT(*) DESC
            """)
            return cursor.fetchall()

    def query_longest_proteins(self, limit: int = 5) -> list:
        """Returns the top longest sequence records."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT accession, entry_name, protein_name, sequence_length
                FROM proteins
                ORDER BY sequence_length DESC
                LIMIT ?
            """, (limit,))
            return cursor.fetchall()
