"""
RNA-Seq Differential Gene Expression Analyzer
Author: Portfolio Creator
Description: Norms raw sequencing counts to Counts Per Million (CPM),
             computes log2 Fold Changes, conducts independent two-sample t-tests,
             and exports a Volcano plot highlighting significant genes.
Language: English (100%)
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

class GeneExpressionAnalyzer:
    """Performs statistical differential expression analysis on RNA-Seq profiles."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None
        self.results_df = None
        self.load_data()

    def load_data(self):
        """Loads gene expression matrix."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Gene expression data not found: {self.data_path}")
        self.df = pd.read_csv(self.data_path)

    def normalize_to_cpm(self) -> pd.DataFrame:
        """
        Normalizes raw read counts to Counts Per Million (CPM) to adjust for sequencing depth.
        Formula: (count / column_sum) * 1,000,000
        
        Returns:
            pd.DataFrame: CPM normalized expression matrix.
        """
        numeric_cols = [c for c in self.df.columns if c != 'gene_id']
        cpm_df = self.df.copy()
        
        # Column sums represent library sizes
        library_sizes = self.df[numeric_cols].sum()
        
        for col in numeric_cols:
            cpm_df[col] = (self.df[col] / library_sizes[col]) * 1000000
            
        return cpm_df

    def analyze_differential_expression(self, p_threshold: float = 0.05, fc_threshold: float = 2.0) -> pd.DataFrame:
        """
        Runs differential analysis:
        - Calculates means.
        - Calculates Log2 Fold Change.
        - Runs independent t-tests for p-values.
        
        Returns:
            pd.DataFrame: Analysis summary including fold changes and statistical significance.
        """
        cpm_df = self.normalize_to_cpm()
        control_cols = [c for c in cpm_df.columns if 'control' in c]
        treated_cols = [c for c in cpm_df.columns if 'treated' in c]
        
        results = []
        for _, row in cpm_df.iterrows():
            gene_id = row['gene_id']
            ctrl_vals = row[control_cols].values.astype(float)
            trt_vals = row[treated_cols].values.astype(float)
            
            mean_ctrl = np.mean(ctrl_vals)
            mean_trt = np.mean(trt_vals)
            
            # Add a small pseudo-count (e.g., 0.1) to avoid divide-by-zero or log of zero
            fold_change = (mean_trt + 0.1) / (mean_ctrl + 0.1)
            log2_fc = np.log2(fold_change)
            
            # Perform two-sided independent t-test
            stat, p_val = ttest_ind(trt_vals, ctrl_vals, equal_var=False)
            
            # Handle edge cases (nan p-values)
            if np.isnan(p_val):
                p_val = 1.0
                
            # Classify significance
            log2_fc_cutoff = np.log2(fc_threshold)
            if p_val < p_threshold and log2_fc >= log2_fc_cutoff:
                status = "Upregulated"
            elif p_val < p_threshold and log2_fc <= -log2_fc_cutoff:
                status = "Downregulated"
            else:
                status = "Non-significant"
                
            results.append({
                "gene_id": gene_id,
                "mean_control": mean_ctrl,
                "mean_treated": mean_trt,
                "fold_change": fold_change,
                "log2_fold_change": log2_fc,
                "p_value": p_val,
                "minus_log10_pvalue": -np.log10(p_val) if p_val > 0 else 0.0,
                "regulation_status": status
            })
            
        self.results_df = pd.DataFrame(results)
        return self.results_df

    def plot_volcano(self, output_path: str, p_threshold: float = 0.05, fc_threshold: float = 2.0):
        """
        Generates and saves a publication-quality Volcano plot.
        
        Args:
            output_path (str): Save path for chart.
        """
        if self.results_df is None:
            self.analyze_differential_expression(p_threshold, fc_threshold)
            
        plt.figure(figsize=(8, 6))
        
        log2_cutoff = np.log2(fc_threshold)
        
        # Color coding
        up = self.results_df[self.results_df['regulation_status'] == 'Upregulated']
        down = self.results_df[self.results_df['regulation_status'] == 'Downregulated']
        ns = self.results_df[self.results_df['regulation_status'] == 'Non-significant']
        
        plt.scatter(ns['log2_fold_change'], ns['minus_log10_pvalue'], color='#94a3b8', alpha=0.6, label='Non-significant')
        plt.scatter(up['log2_fold_change'], up['minus_log10_pvalue'], color='#ef4444', alpha=0.8, label='Upregulated')
        plt.scatter(down['log2_fold_change'], down['minus_log10_pvalue'], color='#3b82f6', alpha=0.8, label='Downregulated')
        
        # Threshold lines
        plt.axhline(-np.log10(p_threshold), color='#64748b', linestyle='--', linewidth=1, label=f'p-value = {p_threshold}')
        plt.axvline(log2_cutoff, color='#64748b', linestyle=':', linewidth=1)
        plt.axvline(-log2_cutoff, color='#64748b', linestyle=':', linewidth=1)
        
        plt.title("Volcano Plot - RNA-Seq Differential Gene Expression", fontsize=12, fontweight='bold', pad=15)
        plt.xlabel("Log2 Fold Change (Treated vs Control)", fontsize=10)
        plt.ylabel("-Log10 p-value", fontsize=10)
        plt.legend(loc='upper right')
        plt.grid(True, linestyle=':', alpha=0.5)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
