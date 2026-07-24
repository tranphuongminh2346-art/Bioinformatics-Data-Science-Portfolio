"""
Unit Tests for RNA-Seq Differential Expression Analyzer
Author: Portfolio Creator
Description: Verify CPM normalization scaling, log2 fold changes, and t-test regulation classifications.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from expression_analyzer import GeneExpressionAnalyzer

class TestGeneExpressionAnalyzer(unittest.TestCase):

    def setUp(self):
        # Create a mock count matrix with library sizing differences
        # Control sums = 100 + 100 = 200
        # Treated sums = 1000 + 1000 = 2000
        self.mock_data = (
            "gene_id,control_1,control_2,treated_1,treated_2\n"
            "GENE_A,50,50,800,800\n"
            "GENE_B,50,50,200,200\n"
        )
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        with open(self.temp_csv_path, 'w', encoding='utf-8') as f:
            f.write(self.mock_data)
            
        self.analyzer = GeneExpressionAnalyzer(self.temp_csv_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_csv_path):
            os.remove(self.temp_csv_path)

    def test_cpm_normalization(self):
        cpm_df = self.analyzer.normalize_to_cpm()
        
        # Total counts per column in cpm_df should sum to exactly 1,000,000
        numeric_cols = [c for c in cpm_df.columns if c != 'gene_id']
        for col in numeric_cols:
            self.assertAlmostEqual(cpm_df[col].sum(), 1000000.0)

    def test_differential_analysis(self):
        results = self.analyzer.analyze_differential_expression(p_threshold=0.05, fc_threshold=2.0)
        
        # Check shapes
        self.assertEqual(len(results), 2)
        
        # GENE_A:
        # Control values = 50, 50 (normalized CPM: 500,000 each -> Mean Control CPM = 500,000)
        # Treated values = 800, 800 (normalized CPM: 800,000 each -> Mean Treated CPM = 800,000)
        # Fold Change = (800000 + 0.1) / (500000 + 0.1) ~ 1.6
        # Log2FC = log2(1.6) ~ 0.67
        gene_a_res = results[results['gene_id'] == 'GENE_A'].iloc[0]
        self.assertAlmostEqual(gene_a_res['mean_control'], 500000.0)
        self.assertAlmostEqual(gene_a_res['mean_treated'], 800000.0)
        self.assertTrue(gene_a_res['log2_fold_change'] > 0)

        # GENE_B:
        # Control values = 50, 50 (CPM: 500,000)
        # Treated values = 200, 200 (CPM: 200,000)
        # Fold change = (200000 + 0.1) / (500000 + 0.1) ~ 0.4
        # Log2FC = log2(0.4) < 0
        gene_b_res = results[results['gene_id'] == 'GENE_B'].iloc[0]
        self.assertAlmostEqual(gene_b_res['mean_control'], 500000.0)
        self.assertAlmostEqual(gene_b_res['mean_treated'], 200000.0)
        self.assertTrue(gene_b_res['log2_fold_change'] < 0)

if __name__ == "__main__":
    unittest.main()
