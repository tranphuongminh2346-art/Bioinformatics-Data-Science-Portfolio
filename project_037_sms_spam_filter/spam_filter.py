"""
SMS Spam Filter
Author: Portfolio Creator
Description: Fits a Logistic Regression model on TF-IDF word vectors to classify
             SMS messages into Spam vs Ham, and evaluates classification scores.
Language: English (100%)
"""

import os
import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

class SMSSpamFilter:
    """TF-IDF and Logistic Regression framework for text spam filtering classification."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.model = None
        self.is_trained = False
        self.load_data()

    def load_data(self):
        """Loads SMS messages from CSV."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Spam SMS data file not found: {self.data_path}")
        self.df = pd.read_csv(self.data_path)

    def clean_text(self, text: str) -> str:
        """Preprocesses message text strings by lowercasing and stripping punctuation."""
        text = text.lower()
        # Keep only alphanumeric characters and spaces
        text = re.sub(r'[^a-z0-9\s]', '', text)
        return text

    def train_model(self) -> tuple:
        """
        Cleans text data, builds TF-IDF matrix, and fits Logistic Regression model.
        
        Returns:
            tuple: (X_test, y_test)
        """
        # Clean text
        self.df['clean_text'] = self.df['text'].apply(self.clean_text)
        
        X = self.df['clean_text']
        # Map label: spam = 1, ham = 0
        y = self.df['label'].map({'spam': 1, 'ham': 0})
        
        # Split (80% train, 20% test)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Fit TF-IDF on training strings
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        X_test_tfidf = self.vectorizer.transform(X_test)
        
        # Fit model
        self.model = LogisticRegression(random_state=42)
        self.model.fit(X_train_tfidf, y_train)
        self.is_trained = True
        
        return X_test_tfidf, y_test

    def evaluate_model(self, X_test_tfidf, y_test: pd.Series) -> dict:
        """Runs predictions and calculates metrics."""
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation.")
            
        y_pred = self.model.predict(X_test_tfidf)
        
        acc = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        cm = confusion_matrix(y_test, y_pred)
        
        return {
            "accuracy": acc,
            "report": report,
            "confusion_matrix": cm,
            "predictions": y_pred
        }

    def predict_message(self, text: str) -> tuple:
        """Predicts spam vs ham classification and probability for a raw text string."""
        if not self.is_trained:
            raise ValueError("Model must be trained first.")
            
        cleaned = self.clean_text(text)
        tfidf_vec = self.vectorizer.transform([cleaned])
        
        pred = self.model.predict(tfidf_vec)[0]
        prob = self.model.predict_proba(tfidf_vec)[0, 1]
        
        label = "spam" if pred == 1 else "ham"
        return label, float(prob)
