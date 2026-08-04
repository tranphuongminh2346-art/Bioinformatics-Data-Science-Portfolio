"""
Microarray Gene Expression Hierarchical Clusterer
Author: Portfolio Creator
Description: Standardizes gene expression profiles, performs average linkage
             hierarchical clustering, and plots dendrogram matrices.
Language: English (100%)
"""

import os
import pandas as pd
import numpy as np
import scipy.cluster.hierarchy as sch
import matplotlib.pyplot as plt

class MicroarrayClusterer:
    """Manages hierarchical clustering pipeline for microarray samples."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None
        self.genes = []
        self.samples = []
        self.data_matrix = None
        self.normalized_matrix = None
        self.linkage_matrix = None
        self.load_data()

    def load_data(self):
        """Loads flat microarray matrix from CSV."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Microarray file not found: {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        self.genes = self.df['gene_name'].tolist()
        self.samples = [col for col in self.df.columns if col != 'gene_name']
        self.data_matrix = self.df[self.samples].values

    def standardize_rows(self) -> np.ndarray:
        """
        Calculates row Z-scores: Z = (X - Mean) / StdDev.
        
        Returns:
            np.ndarray: Normalised expression matrix.
        """
        means = np.mean(self.data_matrix, axis=1, keepdims=True)
        stds = np.std(self.data_matrix, axis=1, keepdims=True)
        # Avoid division by zero
        stds[stds == 0] = 1.0
        self.normalized_matrix = (self.data_matrix - means) / stds
        return self.normalized_matrix

    def compute_linkage(self, method: str = 'average', metric: str = 'euclidean') -> np.ndarray:
        """Computes hierarchical clustering linkage matrix."""
        if self.normalized_matrix is None:
            self.standardize_rows()
        self.linkage_matrix = sch.linkage(self.normalized_matrix, method=method, metric=metric)
        return self.linkage_matrix

    def plot_heatmap(self, output_path: str):
        """Plots dual-panel dendrogram and gene expression heat map."""
        if self.linkage_matrix is None:
            self.compute_linkage()
            
        fig = plt.figure(figsize=(10, 8))
        
        # 1. Left Dendrogram Axes
        ax_dendro = fig.add_axes([0.05, 0.1, 0.2, 0.8])
        dendrogram = sch.dendrogram(self.linkage_matrix, orientation='left', labels=self.genes, ax=ax_dendro)
        ax_dendro.set_xticks([])
        ax_dendro.set_frame_on(False)
        
        # Reorder genes according to dendrogram leaf indexes
        reordered_idx = dendrogram['leaves']
        reordered_matrix = self.normalized_matrix[reordered_idx, :]
        reordered_genes = [self.genes[i] for i in reordered_idx]
        
        # 2. Right Heatmap Axes
        ax_matrix = fig.add_axes([0.3, 0.1, 0.6, 0.8])
        im = ax_matrix.imshow(reordered_matrix, aspect='auto', cmap='coolwarm', interpolation='nearest')
        
        ax_matrix.set_xticks(range(len(self.samples)))
        ax_matrix.set_xticklabels(self.samples, rotation=45, ha='right')
        ax_matrix.set_yticks(range(len(reordered_genes)))
        ax_matrix.set_yticklabels(reordered_genes)
        ax_matrix.yaxis.tick_right()
        
        # Colorbar
        ax_cb = fig.add_axes([0.92, 0.1, 0.02, 0.8])
        fig.colorbar(im, cax=ax_cb, label='Expression Z-Score')
        
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
