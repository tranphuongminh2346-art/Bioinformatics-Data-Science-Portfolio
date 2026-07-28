"""
PubMed API Literature pipeline
Author: Portfolio Creator
Description: Searches the NCBI Entrez API, extracts article titles, journals,
             and publication dates, and logs results with local offline fallbacks.
Language: English (100%)
"""

import os
import requests
import json
import pandas as pd

ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
ESUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

class PubMedFetcher:
    """Interfaces with the NCBI Entrez API to search and retrieve PubMed articles."""
    
    def __init__(self, offline_cache_path: str = "api_cache.json"):
        self.cache_path = offline_cache_path
        self.mock_records = [
            {
                "pmid": "32112345",
                "title": "Deep Learning in Bioinformatics: A Review",
                "journal": "Bioinformatics Journal",
                "pub_date": "2020 Jan 15",
                "authors": "Smith J, Doe A"
            },
            {
                "pmid": "31223456",
                "title": "ETL Pipelines for Genomic Variant Annotation",
                "journal": "Genomics Database",
                "pub_date": "2019 Jun 20",
                "authors": "Brown M, Green P"
            },
            {
                "pmid": "30123457",
                "title": "Phylogenetic UPGMA Tree Reconstruction Tools",
                "journal": "Evolutionary Science",
                "pub_date": "2018 Sep 10",
                "authors": "Wilson K, Taylor R"
            }
        ]

    def search_articles(self, term: str, retmax: int = 5) -> list:
        """
        Queries NCBI ESearch for PMIDs corresponding to a keyword.
        
        Returns:
            list: List of PMID strings.
        """
        params = {
            "db": "pubmed",
            "term": term,
            "retmax": retmax,
            "retmode": "json"
        }
        
        try:
            response = requests.get(ESEARCH_URL, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                pmids = data.get("esearchresult", {}).get("idlist", [])
                return pmids
        except requests.RequestException:
            pass
            
        # Fallback offline mock PMIDs
        print("[!] NCBI ESearch offline or timeout. Falling back to mock cache PMIDs.")
        return [rec["pmid"] for rec in self.mock_records]

    def fetch_summaries(self, pmids: list) -> list:
        """
        Queries NCBI ESummary to retrieve structured metadata for a list of PMIDs.
        
        Returns:
            list: List of parsed article dicts.
        """
        if not pmids:
            return []
            
        params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "json"
        }
        
        try:
            response = requests.get(ESUMMARY_URL, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                results = data.get("result", {})
                
                articles = []
                for pmid in pmids:
                    if pmid in results:
                        info = results[pmid]
                        # Parse authors list
                        authors_list = [auth.get("name", "") for auth in info.get("authors", [])]
                        authors_str = ", ".join(authors_list)
                        
                        articles.append({
                            "pmid": pmid,
                            "title": info.get("title", "No Title"),
                            "journal": info.get("source", "Unknown Journal"),
                            "pub_date": info.get("pubdate", "Unknown Date"),
                            "authors": authors_str
                        })
                return articles
        except requests.RequestException:
            pass
            
        # Fallback offline mock summaries
        print("[!] NCBI ESummary offline or timeout. Falling back to mock cached metadata.")
        return [rec for rec in self.mock_records if rec["pmid"] in pmids]

    def export_to_csv(self, articles: list, output_path: str):
        """Saves article records into a CSV file."""
        df = pd.DataFrame(articles)
        df.to_csv(output_path, index=False)
