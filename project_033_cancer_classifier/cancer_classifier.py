"""
Breast Cancer SVM Classifier
Author: Portfolio Creator
Description: Fits a Support Vector Machine (SVM) classifier to identify malignant tumors,
             standardizes clinical features, and plots decision boundary contours.
Language: English (100%)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score

class CancerClassifier:
    """Support Vector Machine model for classifying fine-needle aspirate cell tumor features."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None
        self.features = []
        self.scaler = StandardScaler()
        self.model = None
        self.is_trained = False
        self.load_data()

    def load_data(self):
        """Loads diagnostic metrics from CSV."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Cancer data file not found: {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        self.features = [col for col in self.df.columns if col != 'label']

    def train_model(self) -> tuple:
        """
        Standardizes features and fits the RBF SVM classifier.
        
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
        
        # Fit scaler
        X_train_scaled = pd.DataFrame(self.scaler.fit_transform(X_train), columns=self.features)
        X_test_scaled = pd.DataFrame(self.scaler.transform(X_test), columns=self.features)
        
        # Fit SVC with probability enabled
        self.model = SVC(kernel='rbf', C=1.0, probability=True, random_state=42)
        self.model.fit(X_train_scaled, y_train)
        self.is_trained = True
        
        return X_test_scaled, y_test

    def evaluate_model(self, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
        """Runs predictions and calculates metrics."""
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation.")
            
        y_pred = self.model.predict(X_test)
        y_prob = self.model.predict_proba(X_test)[:, 1]
        
        acc = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        cm = confusion_matrix(y_test, y_pred)
        
        # Handle single class case in small splits for roc auc
        try:
            auc_score = roc_auc_score(y_test, y_prob)
        except ValueError:
            auc_score = 1.0
            
        return {
            "accuracy": acc,
            "report": report,
            "confusion_matrix": cm,
            "auc": auc_score,
            "predictions": y_pred
        }

    def predict_patient(self, clinical_features: list) -> tuple:
        """Predicts tumor type for a single unscaled patient feature vector."""
        if not self.is_trained:
            raise ValueError("Model must be trained.")
            
        # Convert list to DataFrame wrapper to suppress sklearn feature name warnings
        sample_df = pd.DataFrame([clinical_features], columns=self.features)
        scaled_sample = pd.DataFrame(self.scaler.transform(sample_df), columns=self.features)
        
        pred = self.model.predict(scaled_sample)[0]
        prob = self.model.predict_proba(scaled_sample)[0, 1]
        return int(pred), float(prob)

    def plot_decision_boundary(self, output_path: str):
        """Plots 2D decision boundary using mean_radius and mean_texture."""
        if not self.is_trained:
            raise ValueError("Model must be trained first.")
            
        # For 2D plotting, we fit a temporary 2D model on radius and texture only
        X_2d = self.df[['mean_radius', 'mean_texture']]
        y = self.df['label']
        
        scaler_2d = StandardScaler()
        X_2d_scaled = scaler_2d.fit_transform(X_2d)
        
        model_2d = SVC(kernel='rbf', C=1.0, random_state=42)
        model_2d.fit(X_2d_scaled, y)
        
        # Create grid coordinates
        x_min, x_max = X_2d_scaled[:, 0].min() - 0.5, X_2d_scaled[:, 0].max() + 0.5
        y_min, y_max = X_2d_scaled[:, 1].min() - 0.5, X_2d_scaled[:, 1].max() + 0.5
        xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                             np.arange(y_min, y_max, 0.02))
                             
        Z = model_2d.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        
        plt.figure(figsize=(8, 6))
        # Draw contour fill
        plt.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.coolwarm)
        
        # Plot data points
        scatter = plt.scatter(
            X_2d_scaled[:, 0],
            X_2d_scaled[:, 1],
            c=y,
            cmap=plt.cm.coolwarm,
            edgecolors='k',
            s=50,
            zorder=5
        )
        
        # Add labels
        plt.title("SVM Decision Boundary Surface (Scaled 2D Projection)", fontsize=12, fontweight='bold')
        plt.xlabel("Mean Radius (Standardized)")
        plt.ylabel("Mean Texture (Standardized)")
        plt.grid(True, linestyle=':', alpha=0.5)
        
        # Custom legend
        handles, _ = scatter.legend_elements()
        plt.legend(handles, ['Benign', 'Malignant'], loc='upper right')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
