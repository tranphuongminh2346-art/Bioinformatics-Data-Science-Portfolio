"""
Malaria Microscopic Cell Image Classifier
Author: Portfolio Creator
Description: Preprocesses morphological cell features, trains a Random Forest model,
             plots ROC curves, and extracts feature significance.
Language: English (100%)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_curve, auc

class CellImageClassifier:
    """Classifies microscopy red blood cell features into Parasitized vs Uninfected."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.features = []
        self.is_trained = False

    def preprocess(self) -> tuple:
        """
        Loads and preprocesses cell image features.
        
        Returns:
            tuple: (X_train, X_test, y_train, y_test)
        """
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Cell dataset not found: {self.data_path}")
            
        df = pd.read_csv(self.data_path)
        
        # 1. Map target label (Parasitized=1, Uninfected=0)
        df['label'] = df['label'].map({'Parasitized': 1, 'Uninfected': 0})
        
        # 2. Separate features and target
        X = df.drop(columns=['cell_id', 'label'])
        y = df['label']
        
        self.features = X.columns.tolist()
        
        # Split (80% train, 20% test)
        # Using stratify to keep class distribution balanced
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        return X_train, X_test, y_train, y_test

    def train(self, X_train, y_train):
        """Fits the Random Forest model."""
        self.model.fit(X_train, y_train)
        self.is_trained = True

    def evaluate(self, X_test, y_test) -> dict:
        """
        Evaluates classifier performance on hold-out testing set.
        
        Returns:
            dict: Evaluation results.
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation.")
            
        y_pred = self.model.predict(X_test)
        y_prob = self.model.predict_proba(X_test)[:, 1]
        
        acc = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        
        # Calculate ROC & AUC
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)
        
        return {
            "accuracy": acc,
            "report": report,
            "fpr": fpr,
            "tpr": tpr,
            "auc": roc_auc,
            "y_prob": y_prob
        }

    def get_feature_importances(self) -> dict:
        """Returns feature importance mapping."""
        if not self.is_trained:
            raise ValueError("Model must be trained to extract feature weights.")
        return dict(zip(self.features, self.model.feature_importances_))

    def plot_roc_curve(self, fpr, tpr, roc_auc, output_path: str):
        """
        Plots and saves the ROC evaluation curve.
        
        Args:
            output_path (str): File path to save graph image.
        """
        plt.figure(figsize=(7, 6))
        plt.plot(fpr, tpr, color='#0284c7', label=f'ROC Curve (AUC = {roc_auc:.2f})', linewidth=2.5)
        plt.plot([0, 1], [0, 1], color='#64748b', linestyle='--', linewidth=1)
        
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.title('Receiver Operating Characteristic (Malaria Cell Detection)', fontsize=12, fontweight='bold', pad=15)
        plt.xlabel('False Positive Rate', fontsize=10)
        plt.ylabel('True Positive Rate', fontsize=10)
        plt.legend(loc="lower right")
        plt.grid(True, linestyle=':', alpha=0.5)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
