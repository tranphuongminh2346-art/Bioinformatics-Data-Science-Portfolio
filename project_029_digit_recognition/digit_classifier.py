"""
Handwritten Digit Naive Bayes Classifier
Author: Portfolio Creator
Description: Fits a Gaussian Naive Bayes model to predict handwritten digits
             from 8x8 downsampled pixel grids, and evaluates performance scores.
Language: English (100%)
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

class DigitClassifier:
    """Gaussian Naive Bayes model wrapper for classified handwritten digits."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None
        self.features = []
        self.model = None
        self.is_trained = False
        self.load_data()

    def load_data(self):
        """Loads digit pixel features from CSV."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Digits data file not found: {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        self.features = [col for col in self.df.columns if col != 'label']

    def train_model(self) -> tuple:
        """
        Splits features and target, and fits the Gaussian Naive Bayes classifier.
        
        Returns:
            tuple: (X_test, y_test)
        """
        X = self.df[self.features]
        y = self.df['label']
        
        # Split (80% train, 20% test)
        # Stratification is critical for small balanced mock datasets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        self.model = GaussianNB()
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        return X_test, y_test

    def evaluate_model(self, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
        """
        Predicts classes on test data and returns performance metrics.
        
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

    def predict_digit(self, pixel_grid: list) -> int:
        """Predicts the digit class (0-9) for a single pixel grid."""
        if not self.is_trained:
            raise ValueError("Model must be trained first.")
            
        # Convert list to DataFrame wrapper to suppress sklearn feature name warnings
        sample_df = pd.DataFrame([pixel_grid], columns=self.features)
        pred = self.model.predict(sample_df)[0]
        return int(pred)
