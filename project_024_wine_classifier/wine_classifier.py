"""
Wine Quality Decision Tree Classifier
Author: Portfolio Creator
Description: Trains a Decision Tree model to classify wine quality,
             evaluates performance metrics, and plots the decision logic path.
Language: English (100%)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

class WineQualityClassifier:
    """Decision Tree Classifier framework for predictive wine grading."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None
        self.features = []
        self.model = None
        self.is_trained = False
        self.load_data()

    def load_data(self):
        """Loads wine chemical variables from CSV."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Wine data CSV not found: {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        self.features = [col for col in self.df.columns if col != 'quality']

    def train_model(self, max_depth: int = 3) -> tuple:
        """
        Splits features and target, fits the decision tree classifier.
        
        Returns:
            tuple: (X_test, y_test)
        """
        X = self.df[self.features]
        y = self.df['quality']
        
        # Split (80% train, 20% test)
        # Note: Stratified split ensures class balances in small samples
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        self.model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        return X_test, y_test

    def evaluate_model(self, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
        """
        Runs predictions on a test set and calculates metrics.
        
        Returns:
            dict: Accuracy score, classification report, and confusion matrix.
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
            "confusion_matrix": cm,
            "predictions": y_pred
        }

    def predict_quality(self, chemical_features: list) -> int:
        """Predicts the quality of a single sample using column name wrappers."""
        if not self.is_trained:
            raise ValueError("Model must be trained.")
            
        # Convert to DataFrame with matching column names to suppress user warnings
        sample_df = pd.DataFrame([chemical_features], columns=self.features)
        pred = self.model.predict(sample_df)[0]
        return int(pred)

    def plot_decision_tree(self, output_path: str):
        """Plots the tree splits structures and saves to disk."""
        if not self.is_trained:
            raise ValueError("Model must be trained before plotting.")
            
        plt.figure(figsize=(12, 8))
        plot_tree(
            self.model,
            feature_names=self.features,
            class_names=['Low Quality', 'High Quality'],
            filled=True,
            rounded=True,
            fontsize=10
        )
        plt.title("Wine Quality Decision Tree Splits", fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
