"""
Heart Disease Risk Predictor - ML Model
Author: Portfolio Creator
Description: Auto-downloads the real Cleveland Heart Disease dataset,
             trains a Logistic Regression classifier, evaluates the model,
             plots confusion matrix/ROC curves, and performs inference.
Language: English (100%)
"""

import os
import urllib.request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_curve, auc

DATA_URL = "https://raw.githubusercontent.com/sharmaroshan/Heart-UCI-Dataset/master/heart.csv"

class HeartDiseaseClassifier:
    """Logistic Regression Model for predicting heart disease risk."""
    
    def __init__(self, data_path: str = "heart.csv"):
        self.data_path = data_path
        self.model = LogisticRegression(max_iter=1000, random_state=42)
        self.scaler = StandardScaler()
        self.features = []
        self.is_trained = False

    def download_dataset(self):
        """Downloads the Cleveland Heart Disease dataset if not present locally."""
        if not os.path.exists(self.data_path):
            print(f"[*] Local dataset '{self.data_path}' not found.")
            print(f"[*] Downloading from: {DATA_URL}")
            try:
                urllib.request.urlretrieve(DATA_URL, self.data_path)
                print(f"[+] Download complete: saved to {self.data_path}")
            except Exception as e:
                raise IOError(f"Failed to download Cleveland dataset: {e}")
        else:
            print(f"[+] Dataset '{self.data_path}' found locally.")

    def load_and_preprocess(self) -> tuple:
        """
        Loads the dataset and prepares features X and target y.
        Standardizes features and performs train-test split.
        
        Returns:
            tuple: (X_train, X_test, y_train, y_test)
        """
        self.download_dataset()
        
        # Load CSV
        df = pd.read_csv(self.data_path)
        
        # Cleveland Columns:
        # age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target
        if 'target' not in df.columns:
            raise KeyError("The dataset is missing the 'target' label column.")
            
        X = df.drop(columns=['target'])
        self.features = X.columns.tolist()
        y = df['target']
        
        # Split (80% train, 20% test)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Fit scaler on train data
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled, y_train, y_test

    def train(self, X_train, y_train):
        """Trains the Logistic Regression model."""
        self.model.fit(X_train, y_train)
        self.is_trained = True

    def evaluate(self, X_test, y_test) -> dict:
        """
        Evaluates the model on test data.
        
        Returns:
            dict: Evaluation metrics (accuracy, precision, recall, f1, confusion, roc_data)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation.")
            
        y_pred = self.model.predict(X_test)
        y_prob = self.model.predict_proba(X_test)[:, 1]
        
        acc = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        cm = confusion_matrix(y_test, y_pred)
        
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)
        
        return {
            "accuracy": acc,
            "report": report,
            "confusion_matrix": cm,
            "roc": (fpr, tpr, roc_auc),
            "y_prob": y_prob
        }

    def predict_risk(self, patient_features: list) -> tuple:
        """
        Predicts heart disease risk for a single patient.
        
        Args:
            patient_features (list): 13 clinical features.
            
        Returns:
            tuple: (prediction: int, probability: float)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before inference.")
            
        # Convert to DataFrame with feature names to suppress warnings
        features_df = pd.DataFrame([patient_features], columns=self.features)
        scaled_features = self.scaler.transform(features_df)
        
        pred = self.model.predict(scaled_features)[0]
        prob = self.model.predict_proba(scaled_features)[0, 1]
        
        return int(pred), float(prob)

    def plot_evaluation(self, metrics: dict, cm_path: str, roc_path: str):
        """
        Generates and saves model evaluation plots.
        
        Args:
            metrics (dict): Metrics dictionary returned by evaluate().
            cm_path (str): Output path for Confusion Matrix.
            roc_path (str): Output path for ROC Curve.
        """
        # 1. Plot Confusion Matrix
        cm = metrics["confusion_matrix"]
        plt.figure(figsize=(6, 5))
        plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title('Confusion Matrix', fontsize=12, fontweight='bold', pad=15)
        plt.colorbar()
        tick_marks = np.arange(2)
        plt.xticks(tick_marks, ['No Disease', 'Disease'], rotation=45)
        plt.yticks(tick_marks, ['No Disease', 'Disease'])
        
        # Annotate numbers
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                plt.text(j, i, format(cm[i, j], 'd'),
                         ha="center", va="center",
                         color="white" if cm[i, j] > thresh else "black",
                         fontweight='bold')
                         
        plt.ylabel('True Class')
        plt.xlabel('Predicted Class')
        plt.tight_layout()
        plt.savefig(cm_path, dpi=150)
        plt.close()

        # 2. Plot ROC Curve
        fpr, tpr, roc_auc = metrics["roc"]
        plt.figure(figsize=(7, 5))
        plt.plot(fpr, tpr, color='#0284c7', lw=2, label=f'ROC curve (AUC = {roc_auc:.3f})')
        plt.plot([0, 1], [0, 1], color='#ef4444', lw=1.5, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate (1 - Specificity)')
        plt.ylabel('True Positive Rate (Sensitivity)')
        plt.title('Receiver Operating Characteristic (ROC) Curve', fontsize=12, fontweight='bold', pad=15)
        plt.legend(loc="lower right")
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.tight_layout()
        plt.savefig(roc_path, dpi=150)
        plt.close()
