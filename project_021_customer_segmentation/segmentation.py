"""
Customer Segmentation Engine
Author: Portfolio Creator
Description: Fits K-Means clustering to classify consumers, standardizes features,
             and plots segment distributions and elbow curves.
Language: English (100%)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

class CustomerSegmenter:
    """Clustering framework for discovering customer purchasing archetypes."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None
        self.scaler = StandardScaler()
        self.features = ['AnnualIncome', 'SpendingScore']
        self.kmeans = None
        self.is_fit = False
        self.load_data()

    def load_data(self):
        """Loads customer profiling CSV records."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Customer data not found: {self.data_path}")
        self.df = pd.read_csv(self.data_path)

    def fit_clusters(self, n_clusters: int = 3) -> np.ndarray:
        """
        Standardizes selected numeric variables and fits the K-Means model.
        
        Returns:
            np.ndarray: Predicted cluster labels.
        """
        X = self.df[self.features]
        scaled_X = pd.DataFrame(self.scaler.fit_transform(X), columns=self.features)
        
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.kmeans.fit(scaled_X)
        self.is_fit = True
        
        self.df['Cluster'] = self.kmeans.labels_
        return self.kmeans.labels_

    def compute_elbow_curve(self, max_k: int = 5) -> list:
        """
        Computes clustering inertias across various choices of K.
        
        Returns:
            list: List of inertias.
        """
        X = self.df[self.features]
        from sklearn.exceptions import NotFittedError
        try:
            scaled_X = pd.DataFrame(self.scaler.transform(X), columns=self.features)
        except NotFittedError:
            scaled_X = pd.DataFrame(self.scaler.fit_transform(X), columns=self.features)
        
        inertias = []
        for k in range(1, max_k + 1):
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            km.fit(scaled_X)
            inertias.append(km.inertia_)
            
        return inertias

    def plot_segmentation(self, inertias: list, output_path: str):
        """Generates side-by-side plots of elbow curves and cluster groups."""
        if not self.is_fit:
            raise ValueError("KMeans must be fit before plotting.")
            
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
        
        # 1. Elbow Plot
        k_values = list(range(1, len(inertias) + 1))
        ax1.plot(k_values, inertias, marker='o', color='#0284c7', lw=2)
        ax1.set_title("Elbow Method for Optimal K", fontsize=11, fontweight='bold')
        ax1.set_xlabel("Number of Clusters K")
        ax1.set_ylabel("Inertia (Within-Cluster Distances)")
        ax1.grid(True, linestyle=':', alpha=0.5)
        
        # 2. Scatter Plot
        unique_clusters = sorted(self.df['Cluster'].unique())
        colors = ['#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899']
        
        for cluster_id in unique_clusters:
            cluster_data = self.df[self.df['Cluster'] == cluster_id]
            ax2.scatter(
                cluster_data['AnnualIncome'],
                cluster_data['SpendingScore'],
                color=colors[cluster_id % len(colors)],
                s=60,
                label=f'Cluster {cluster_id}',
                zorder=5
            )
            
        # Draw scaled centroids back in raw feature space
        centroids_scaled = self.kmeans.cluster_centers_
        centroids_raw = self.scaler.inverse_transform(centroids_scaled)
        
        ax2.scatter(
            centroids_raw[:, 0],
            centroids_raw[:, 1],
            color='black',
            marker='X',
            s=150,
            zorder=6,
            label='Centroids'
        )
        
        ax2.set_title("Customer Segments Map", fontsize=11, fontweight='bold')
        ax2.set_xlabel("Annual Income (k$)")
        ax2.set_ylabel("Spending Score (1-100)")
        ax2.grid(True, linestyle=':', alpha=0.5)
        ax2.legend(loc='upper right')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
