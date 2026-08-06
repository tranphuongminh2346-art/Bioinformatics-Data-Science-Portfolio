"""
Chemical Solubility Predictor
Author: Portfolio Creator
Description: Standardizes molecular descriptors and fits a Ridge regression model
             to predict compound solubility (LogS), exporting correlation plots.
Language: English (100%)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score

class SolubilityPredictor:
    """Predicts compound solubility (LogS) using molecular descriptors."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None
        self.features = ['molecular_weight', 'logp', 'rotatable_bonds', 'polar_surface_area']
        self.scaler = StandardScaler()
        self.model = None
        self.is_trained = False
        self.load_data()

    def load_data(self):
        """Loads chemical descriptors CSV database."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Solubility file not found: {self.data_path}")
        self.df = pd.read_csv(self.data_path)

    def train_model(self) -> tuple:
        """
        Standardizes features and fits a Ridge regression model.
        
        Returns:
            tuple: (X_test_scaled, y_test)
        """
        X = self.df[self.features]
        y = self.df['solubility']
        
        # Split (80% train, 20% test)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        X_train_scaled = pd.DataFrame(self.scaler.fit_transform(X_train), columns=self.features)
        X_test_scaled = pd.DataFrame(self.scaler.transform(X_test), columns=self.features)
        
        # Fit Ridge regression
        self.model = Ridge(alpha=1.0)
        self.model.fit(X_train_scaled, y_train)
        self.is_trained = True
        
        return X_test_scaled, y_test

    def evaluate_model(self, X_test_scaled: pd.DataFrame, y_test: pd.Series) -> dict:
        """Computes evaluation metrics (R2 score and MSE)."""
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation.")
            
        y_pred = self.model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        return {
            "mse": mse,
            "r2_score": r2,
            "predictions": y_pred
        }

    def predict_solubility(self, descriptor_list: list) -> float:
        """Predicts solubility (LogS) for a single compound input descriptors vector."""
        if not self.is_trained:
            raise ValueError("Model must be trained first.")
            
        sample_df = pd.DataFrame([descriptor_list], columns=self.features)
        scaled_sample = pd.DataFrame(self.scaler.transform(sample_df), columns=self.features)
        
        pred = self.model.predict(scaled_sample)[0]
        return float(pred)

    def plot_fit(self, X_test_scaled: pd.DataFrame, y_test: pd.Series, output_path: str):
        """Plots a correlation scatter plot of actual vs predicted solubilities."""
        if not self.is_trained:
            raise ValueError("Model must be trained first.")
            
        y_pred = self.model.predict(X_test_scaled)
        
        plt.figure(figsize=(7, 6))
        plt.scatter(y_test, y_pred, color='#0284c7', edgecolors='k', s=50, alpha=0.8, label='Test Compounds')
        
        # Identity line
        min_val = min(y_test.min(), y_pred.min()) - 0.5
        max_val = max(y_test.max(), y_pred.max()) + 0.5
        plt.plot([min_val, max_val], [min_val, max_val], color='#ef4444', linestyle='--', label='Ideal Fit')
        
        plt.title("Chemical Solubility Predictor (Actual vs Predicted LogS)", fontsize=11, fontweight='bold')
        plt.xlabel("Actual Solubility (LogS)")
        plt.ylabel("Predicted Solubility (LogS)")
        plt.grid(True, linestyle=':', alpha=0.5)
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
