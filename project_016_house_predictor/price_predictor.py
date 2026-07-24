"""
California Housing Ridge Regression Predictor
Author: Portfolio Creator
Description: Fits a Ridge regression model to predict housing prices,
             standardizes features, and plots predicted vs actual values.
Language: English (100%)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

class HousePricePredictor:
    """Ridge regression pipeline for numerical property evaluations."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.model = Ridge(alpha=1.0)
        self.scaler = StandardScaler()
        self.features = []
        self.is_trained = False

    def preprocess(self) -> tuple:
        """
        Loads dataset, splits features, standardizes column vectors, and splits data.
        
        Returns:
            tuple: (X_train_scaled, X_test_scaled, y_train, y_test)
        """
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Housing CSV file not found: {self.data_path}")
            
        df = pd.read_csv(self.data_path)
        
        # Target: MedHouseValue
        X = df.drop(columns=['MedHouseValue'])
        y = df['MedHouseValue']
        
        self.features = X.columns.tolist()
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Fit scaler on train features and transform both
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled, y_train, y_test

    def train(self, X_train, y_train):
        """Fits the Ridge regression model."""
        self.model.fit(X_train, y_train)
        self.is_trained = True

    def evaluate(self, X_test, y_test) -> dict:
        """
        Evaluates the model performance metrics.
        
        Returns:
            dict: Evaluation coefficients (MAE, RMSE, R2).
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation.")
            
        y_pred = self.model.predict(X_test)
        
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        return {
            "mae": mae,
            "rmse": rmse,
            "r2": r2,
            "predictions": y_pred
        }

    def predict_value(self, single_record: np.ndarray) -> float:
        """Predicts the house value for a single unscaled feature vector."""
        if not self.is_trained:
            raise ValueError("Model must be trained.")
        record_df = pd.DataFrame(single_record.reshape(1, -1), columns=self.features)
        scaled_record = self.scaler.transform(record_df)
        return float(self.model.predict(scaled_record)[0])

    def plot_predictions(self, y_test, y_pred, output_path: str):
        """
        Plots a scatter chart comparing actual vs predicted prices.
        
        Args:
            output_path (str): File path to save chart.
        """
        plt.figure(figsize=(7, 6))
        plt.scatter(y_test, y_pred, color='#0284c7', alpha=0.8, edgecolor='#0369a1', label='Predictions')
        
        # Ideal line
        min_val = min(y_test.min(), y_pred.min())
        max_val = max(y_test.max(), y_pred.max())
        plt.plot([min_val, max_val], [min_val, max_val], color='#ef4444', linestyle='--', linewidth=2, label='Perfect Fit')
        
        plt.title('Actual vs Predicted Median House Values', fontsize=12, fontweight='bold', pad=15)
        plt.xlabel('Actual Price ($100k)', fontsize=10)
        plt.ylabel('Predicted Price ($100k)', fontsize=10)
        plt.legend(loc='upper left')
        plt.grid(True, linestyle=':', alpha=0.5)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
