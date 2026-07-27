"""
Unit Tests for FASTA Parser & DB Loader
Author: Portfolio Creator
Description: Verify header regex metadata extraction and database query counts.
Language: English (100%)
"""

import unittest
import os
import sys
import tempfile
import sqlite3

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fasta_parser import parse_uniprot_header, read_fasta_records
from db_loader import ProteinDatabaseLoader

class TestProteinLoader(unittest.TestCase):

    def setUp(self):
        # Sample headers
        self.header_sp = ">sp|P62258|1433E_HUMAN 14-3-3 protein epsilon OS=Homo sapiens OX=9606 GN=YWHAE PE=1 SV=1"
        self.header_tr_no_gn = ">tr|Q9H4P4|Q9H4P4_HUMAN Zinc finger protein 396 OS=Homo sapiens OX=9606 PE=1 SV=1"
        self.header_invalid = ">invalid_header"
        
        # Temp database setup
        self.db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.db_fd)
        self.loader = ProteinDatabaseLoader(self.temp_db_path)

    def tearDown(self):
        if os.path.exists(self.temp_db_path):
            try:
                os.remove(self.temp_db_path)
            except PermissionError:
                pass

    def test_parse_header_sp(self):
        meta = parse_uniprot_header(self.header_sp)
        self.assertIsNotNone(meta)
        self.assertEqual(meta["db_source"], "sp")
        self.assertEqual(meta["accession"], "P62258")
        self.assertEqual(meta["entry_name"], "1433E_HUMAN")
        self.assertEqual(meta["protein_name"], "14-3-3 protein epsilon")
        self.assertEqual(meta["organism"], "Homo sapiens")
        self.assertEqual(meta["tax_id"], 9606)
        self.assertEqual(meta["gene_name"], "YWHAE")
        self.assertEqual(meta["protein_existence"], 1)
        self.assertEqual(meta["sequence_version"], 1)

    def test_parse_header_tr_no_gn(self):
        meta = parse_uniprot_header(self.header_tr_no_gn)
        self.assertIsNotNone(meta)
        self.assertEqual(meta["db_source"], "tr")
        self.assertEqual(meta["accession"], "Q9H4P4")
        self.assertEqual(meta["gene_name"], None)

    def test_parse_header_invalid(self):
        meta = parse_uniprot_header(self.header_invalid)
        self.assertIsNone(meta)

    def test_database_inserts_and_queries(self):
        mock_records = [
            {
                "db_source": "sp",
                "accession": "P62258",
                "entry_name": "1433E_HUMAN",
                "protein_name": "14-3-3 protein epsilon",
                "organism": "Homo sapiens",
                "tax_id": 9606,
                "gene_name": "YWHAE",
                "protein_existence": 1,
                "sequence_version": 1,
                "sequence": "MDDREDLVYQ"
            },
            {
                "db_source": "tr",
                "accession": "Q9H4P4",
                "entry_name": "Q9H4P4_HUMAN",
                "protein_name": "Zinc finger protein 396",
                "organism": "Homo sapiens",
                "tax_id": 9606,
                "gene_name": None,
                "protein_existence": 1,
                "sequence_version": 1,
                "sequence": "MALSFLVDVSQG"
            }
        ]
        
        inserted = self.loader.load_records(mock_records)
        self.assertEqual(inserted, 2)
        
        # Check organism queries
        counts = self.loader.query_organism_counts()
        self.assertEqual(len(counts), 1)
        self.assertEqual(counts[0][0], "Homo sapiens")
        self.assertEqual(counts[0][1], 2)
        # Average length: (10 + 12)/2 = 11.0
        self.assertAlmostEqual(counts[0][2], 11.0)
        
        # Check longest queries
        longest = self.loader.query_longest_proteins(limit=1)
        self.assertEqual(longest[0][0], "Q9H4P4")
        self.assertEqual(longest[0][3], 12)

if __name__ == "__main__":
    unittest.main()
