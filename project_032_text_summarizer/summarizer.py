"""
Text Summarizer (Extractive PageRank)
Author: Portfolio Creator
Description: Implements TextRank sentence summarization. Splits document strings,
             builds TF-IDF cosine similarity matrices, runs PageRank centrality,
             and returns top N sentences.
Language: English (100%)
"""

import os
import re
import numpy as np
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TextSummarizer:
    """Performs extractive text summarization using PageRank centrality on sentence graphs."""
    
    def __init__(self, document_path: str):
        self.document_path = document_path
        self.text = ""
        self.sentences = []
        self.load_document()

    def load_document(self):
        """Loads raw text content from file."""
        if not os.path.exists(self.document_path):
            raise FileNotFoundError(f"Document file not found: {self.document_path}")
            
        with open(self.document_path, 'r', encoding='utf-8') as f:
            self.text = f.read().strip()
            
        # Split text into sentences using simple regex
        # Splits on '.', '!', or '?' followed by whitespace
        self.sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', self.text) if s.strip()]

    def summarize(self, limit: int = 2) -> list:
        """
        Runs TextRank algorithm to extract top sentences.
        
        Returns:
            list: List of tuples (sentence: str, pagerank_score: float).
        """
        if len(self.sentences) <= limit:
            return [(s, 1.0) for s in self.sentences]
            
        # 1. Compute TF-IDF matrix
        # Remove common english words to improve similarity alignment
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(self.sentences)
        
        # 2. Compute Cosine Similarity matrix between sentences
        sim_matrix = cosine_similarity(tfidf_matrix)
        
        # 3. Create NetworkX graph
        # Nodes represent sentences, edges represent similarity weights
        graph = nx.Graph()
        n = len(self.sentences)
        
        for i in range(n):
            for j in range(i + 1, n):
                weight = sim_matrix[i, j]
                # Only add edges with significant similarity to keep graph sparse
                if weight > 0.01:
                    graph.add_edge(i, j, weight=weight)
                    
        # If graph is empty (no overlapping words), add uniform edges
        if graph.number_of_nodes() == 0:
            for i in range(n):
                for j in range(i + 1, n):
                    graph.add_edge(i, j, weight=1.0)
                    
        # 4. Compute PageRank centrality
        scores = nx.pagerank(graph, weight='weight')
        
        # 5. Extract top N sentences sorted by PageRank score
        ranked_indices = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        
        # Preserve original document order of sentences for final summary readability
        sorted_by_original_order = sorted(ranked_indices, key=lambda x: x[0])
        
        summary = []
        for idx, score in sorted_by_original_order:
            summary.append((self.sentences[idx], score))
            
        return summary
