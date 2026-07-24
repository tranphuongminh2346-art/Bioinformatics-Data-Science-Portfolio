"""
Clinical Text Miner & Sentiment Analyzer
Author: Portfolio Creator
Description: Tokenizes medical abstracts, computes TF-IDF term weights,
             applies rule-based clinical lexicons, and classifies sentiment.
Language: English (100%)
"""

import os
import json
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Basic stopword list to avoid external download dependencies (NLTK)
STOPWORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'aren', 'as', 'at',
    'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by',
    'can', 'could', 'did', 'do', 'does', 'doing', 'down', 'during',
    'each', 'few', 'for', 'from', 'further',
    'had', 'has', 'have', 'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how',
    'i', 'if', 'in', 'into', 'is', 'it', 'its', 'itself',
    'just', 'me', 'more', 'most', 'my', 'myself',
    'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own',
    'same', 'she', 'should', 'so', 'some', 'such',
    't', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these', 'they',
    'this', 'those', 'through', 'to', 'too',
    'under', 'until', 'up', 'very',
    'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'with', 'would',
    'you', 'your', 'yours', 'yourself', 'yourselves'
}

# Clinical Lexicon lists
CLINICAL_POSITIVE = {
    'improved', 'reduced', 'significantly', 'efficacy', 'promising', 'positive', 
    'robust', 'benefits', 'activated', 'success', 'effective', 'safe'
}

CLINICAL_NEGATIVE = {
    'toxicity', 'failed', 'harmful', 'unsafe', 'mortality', 'regrettably', 
    'poor', 'ineffective', 'adverse', 'severe', 'negative', 'side-effects', 'death'
}

class ClinicalTextMiner:
    """Mines terminology and predicts sentiment classes of medical abstracts."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.records = []
        self.load_data()

    def load_data(self):
        """Loads PubMed abstract list from JSON."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Abstracts JSON file not found: {self.data_path}")
        with open(self.data_path, 'r', encoding='utf-8') as f:
            self.records = json.load(f)

    def clean_text(self, text: str) -> list:
        """
        Cleans text: lowercase conversion, punctuation strip, and stopword filter.
        
        Args:
            text (str): Input abstract.
            
        Returns:
            list: List of cleaned word tokens.
        """
        # Convert to lowercase and strip non-alphanumeric chars
        cleaned = re.sub(r'[^a-zA-Z\s\-]', '', text.lower())
        tokens = cleaned.split()
        
        # Remove stopwords
        filtered_tokens = [w for w in tokens if w not in STOPWORDS]
        return filtered_tokens

    def calculate_tfidf(self) -> pd.DataFrame:
        """
        Calculates TF-IDF term weights across all abstracts in the collection.
        
        Returns:
            pd.DataFrame: Top terms sorted by average TF-IDF weights.
        """
        corpus = [r['abstract'] for r in self.records]
        
        # Custom stopword list passed to TfidfVectorizer
        vectorizer = TfidfVectorizer(stop_words=list(STOPWORDS))
        tfidf_matrix = vectorizer.fit_transform(corpus)
        
        # Get term names
        feature_names = vectorizer.get_feature_names_out()
        
        # Calculate mean TF-IDF score for each term across all docs
        mean_scores = tfidf_matrix.mean(axis=0).A1
        
        term_df = pd.DataFrame({
            "term": feature_names,
            "mean_tfidf": mean_scores
        }).sort_values(by="mean_tfidf", ascending=False).reset_index(drop=True)
        
        return term_df

    def analyze_sentiment(self) -> list:
        """
        Computes sentiment polarity scores based on clinical lexicon matches.
        
        Returns:
            list: Evaluated abstracts.
        """
        evaluated_records = []
        
        for r in self.records:
            abstract_text = r['abstract']
            tokens = self.clean_text(abstract_text)
            
            pos_hits = [w for w in tokens if w in CLINICAL_POSITIVE]
            neg_hits = [w for w in tokens if w in CLINICAL_NEGATIVE]
            
            pos_count = len(pos_hits)
            neg_count = len(neg_hits)
            
            # Polarity score = (positive - negative)
            polarity_score = pos_count - neg_count
            
            if polarity_score > 0:
                sentiment = "Positive Clinical Outcome"
            elif polarity_score < 0:
                sentiment = "Negative Clinical Outcome"
            else:
                sentiment = "Neutral / Unclear"
                
            evaluated_records.append({
                "pmid": r["pmid"],
                "title": r["title"],
                "polarity_score": polarity_score,
                "sentiment_class": sentiment,
                "positive_matches": pos_hits,
                "negative_matches": neg_hits
            })
            
        return evaluated_records
