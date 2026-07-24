"""
Customer Churn Predictor - ML Model
Author: Portfolio Creator
Description: Preprocesses telecom customer logs, trains a Random Forest model,
             evaluates model metrics, and plots feature importances.
Language: English (100%)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

class CustomerChurnPredictor:
    """Random Forest Classifier for predicting customer churn risk."""
    
    def __init__(self, data_path: str = "churn_data.csv"):
        self.data_path = data_path
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.feature_names = []
        self.is_trained = False

    def load_and_preprocess(self) -> tuple:
        """
        Loads the dataset and performs preprocessing:
        - Maps target label ('Churn') to binary (Yes=1, No=0).
        - One-hot encodes categorical values ('Contract', 'InternetService').
        - Performs train-test splitting.
        
        Returns:
            tuple: (X_train, X_test, y_train, y_test)
        """
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Dataset not found at: {self.data_path}")
            
        df = pd.read_csv(self.data_path)
        
        # 1. Clean missing/invalid values
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        df['TotalCharges'] = df['TotalCharges'].fillna(df['tenure'] * df['MonthlyCharges'])
        
        # 2. Map Target label
        df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
        
        # 3. Features selection and One-Hot encoding
        # Exclude customerID and target
        X = df.drop(columns=['customerID', 'Churn'])
        y = df['Churn']
        
        X_encoded = pd.get_dummies(X, columns=['Contract', 'InternetService'], drop_first=True)
        self.feature_names = X_encoded.columns.tolist()
        
        # Split (80% train, 20% test)
        # Given small size of dataset (20 rows), stratify is crucial
        X_train, X_test, y_train, y_test = train_test_split(
            X_encoded, y, test_size=0.2, random_state=42, stratify=y
        )
        
        return X_train, X_test, y_train, y_test

    def train(self, X_train, y_train):
        """Trains the Random Forest model."""
        self.model.fit(X_train, y_train)
        self.is_trained = True

    def evaluate(self, X_test, y_test) -> dict:
        """
        Evaluates the model on test data.
        
        Returns:
            dict: Model metrics.
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation.")
            
        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        cm = confusion_matrix(y_test, y_pred)
        
        return {
            "accuracy": acc,
            "report": report,
            "confusion_matrix": cm
        }

    def predict_churn(self, customer_df: pd.DataFrame) -> tuple:
        """
        Predicts churn probability for an encoded customer record.
        
        Args:
            customer_df (pd.DataFrame): Encoded customer features.
            
        Returns:
            tuple: (prediction: int, probability: float)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction.")
            
        pred = self.model.predict(customer_df)[0]
        prob = self.model.predict_proba(customer_df)[0, 1]
        return int(pred), float(prob)

    def plot_feature_importances(self, output_path: str):
        """
        Plots a bar chart showing feature importances.
        
        Args:
            output_path (str): Save path for chart image.
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before plotting feature importances.")
            
        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        sorted_features = [self.feature_names[i] for i in indices]
        sorted_importances = importances[indices]

        plt.figure(figsize=(9, 5))
        plt.barh(sorted_features[::-1], sorted_importances[::-1], color='#0284c7', edgecolor='#e2e8f0')
        plt.grid(axis='x', linestyle=':', alpha=0.6)
        plt.title("Random Forest Feature Importances", fontsize=12, fontweight='bold', pad=15)
        plt.xlabel("Importance Weight", fontsize=10)
        plt.ylabel("Feature", fontsize=10)
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
