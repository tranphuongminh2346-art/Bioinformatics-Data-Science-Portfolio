# Bioinformatics, Data Science, and Machine Learning Portfolio

Welcome to my portfolio! This repository contains a curated collection of small, self-contained, and professional projects focusing on **Bioinformatics**, **Data Science**, **Data Engineering**, and **Machine Learning/Deep Learning (ML/DL)**.

Each project is located in its own subfolder and is fully documented, tested, and ready to run.

## Project Directory

| Project | Domain (Tags) | Tech Stack | Description |
| :--- | :--- | :--- | :--- |
| [Project 1: DNA Sequence Analyzer](./project_001_dna_sequence_analyzer/) | ![Bioinformatics](https://img.shields.io/badge/Bioinformatics-blue?style=flat-square) ![Data Science](https://img.shields.io/badge/Data%20Science-lightblue?style=flat-square) | Python, Matplotlib | DNA sequence statistics, transcription, translation, and GC-content sliding window visualization. |
| [Project 2: Clinical Trial Pipeline](./project_002_clinical_trial_pipeline/) | ![Data Engineering](https://img.shields.io/badge/Data%20Engineering-orange?style=flat-square) ![Data Science](https://img.shields.io/badge/Data%20Science-lightblue?style=flat-square) | Python, Pandas, SQLite, Matplotlib | ETL pipeline extracting clinical records, transforming structures, loading into SQLite, and querying summaries. |
| [Project 3: Heart Disease Classifier](./project_003_heart_disease_classifier/) | ![Machine Learning](https://img.shields.io/badge/Machine%20Learning-green?style=flat-square) ![Data Science](https://img.shields.io/badge/Data%20Science-lightblue?style=flat-square) | Python, Scikit-Learn, Pandas, Matplotlib | Classifier predicting heart disease risk from the Cleveland dataset. Includes scaling, evaluation, and ROC plotting. |
| [Project 4: Protein Analyzer](./project_004_protein_analyzer/) | ![Bioinformatics](https://img.shields.io/badge/Bioinformatics-blue?style=flat-square) ![Data Science](https://img.shields.io/badge/Data%20Science-lightblue?style=flat-square) | Python, NumPy, Matplotlib | Spatial parser for 3D atomic coordinates. Computes Euclidean distances, hydrogen bonds, and exports matrix maps. |
| [Project 5: Weather ETL Pipeline](./project_005_weather_etl/) | ![Data Engineering](https://img.shields.io/badge/Data%20Engineering-orange?style=flat-square) ![Data Science](https://img.shields.io/badge/Data%20Science-lightblue?style=flat-square) | Python, Requests, Pandas, SQLite | Live ETL weather monitoring. Fetches observations, transforms Celsius/Fahrenheit, aggregates rolling metrics in DB. |
| [Project 6: Genomic Variant Predictor](./project_006_variant_predictor/) | ![Bioinformatics](https://img.shields.io/badge/Bioinformatics-blue?style=flat-square) ![Machine Learning](https://img.shields.io/badge/Machine%20Learning-green?style=flat-square) | Python, Matplotlib | Genomic variant predictor parsing VCF lines. Matches codon mutations and predicts clinical consequence severity. |
| [Project 7: Customer Churn Predictor](./project_007_churn_predictor/) | ![Machine Learning](https://img.shields.io/badge/Machine%20Learning-green?style=flat-square) ![Data Science](https://img.shields.io/badge/Data%20Science-lightblue?style=flat-square) | Python, Scikit-Learn, Random Forest | Customer churn predictive pipeline. One-hot encodes variables, evaluates precision/recall, and plots feature weights. |
| [Project 8: Citation Network Graph](./project_008_citation_network/) | ![Data Engineering](https://img.shields.io/badge/Data%20Engineering-orange?style=flat-square) | Python, NetworkX, Matplotlib | Directed citation graph analysis of PubMed literature. Computes PageRank authority and traces citation pathways. |
| [Project 9: COVID-19 Trend Dashboard](./project_009_covid_dashboard/) | ![Data Science](https://img.shields.io/badge/Data%20Science-lightblue?style=flat-square) | Python, Pandas, Matplotlib | COVID-19 daily trend dashboard. Computes daily cases diffs, rolling averages, and saves dual y-axis plots. |
| [Project 10: RNA-Seq DE Analyzer](./project_010_rna_seq_analyzer/) | ![Bioinformatics](https://img.shields.io/badge/Bioinformatics-blue?style=flat-square) ![Data Science](https://img.shields.io/badge/Data%20Science-lightblue?style=flat-square) | Python, Scipy, Pandas, Matplotlib | RNA-Seq differential expression analysis. Normalizes counts (CPM), runs t-tests, and saves Volcano plots. |
| [Project 11: Web Job Scraper](./project_011_job_scraper/) | ![Data Engineering](https://img.shields.io/badge/Data%20Engineering-orange?style=flat-square) | Python, BeautifulSoup, SQLite | HTML job listings scraper. Extracts salaries using regular expressions, loads SQLite, and aggregates metrics. |
| [Project 12: Medical Abstracts NLP Miner](./project_012_abstracts_nlp/) | ![AI & NLP](https://img.shields.io/badge/AI%20%26%20NLP-red?style=flat-square) ![Data Science](https://img.shields.io/badge/Data%20Science-lightblue?style=flat-square) | Python, Scikit-Learn (TF-IDF), Pandas | Text miner analyzing clinical outcome sentiment in PubMed abstracts using custom lexicon dictionaries. |
| [Project 13: Malaria Cell Image Classifier](./project_013_malaria_classifier/) | ![Machine Learning](https://img.shields.io/badge/Machine%20Learning-green?style=flat-square) | Python, Scikit-Learn, Pandas | Microscopy cell image classifier. Extracts intensity and morphology features, trains Random Forest, and plots ROC. |
| [Project 14: Clinical Trials REST API](./project_014_clinical_api/) | ![Software Engineering](https://img.shields.io/badge/Software%20Engineering-purple?style=flat-square) | Python, Flask, SQLite | REST API server for clinical trials database. Exposes query parameters filters and summary statistics. |
| [Project 15: Phylogenetic Tree Reconstructor](./project_015_phylogenetic_tree/) | ![Bioinformatics](https://img.shields.io/badge/Bioinformatics-blue?style=flat-square) | Python, NumPy | Phylogenetic tree reconstructor implementing UPGMA clustering. Outputs Newick strings and ASCII tree layouts. |
| [Project 16: House Price Predictor](./project_016_house_predictor/) | ![Machine Learning](https://img.shields.io/badge/Machine%20Learning-green?style=flat-square) ![Data Science](https://img.shields.io/badge/Data%20Science-lightblue?style=flat-square) | Python, Scikit-Learn, Ridge | Real estate house price predictor. Implements scaled Ridge regression, prints coefficients, and plots fit scatter. |

---

## Career Interests
- **Bioinformatics**: Sequence analysis, structural biology, gene expression analysis.
- **Data Science & Engineering**: Data analysis, pipeline construction, ETL, databases.
- **AI/ML/DL**: Predictive modeling, computer vision, natural language processing, deep learning architectures.

## Repository Setup
To run the projects, it is recommended to set up a virtual environment:
```bash
# Clone the repository
git clone https://github.com/your-username/portfolio.git
cd portfolio

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Navigate to any project folder and follow its README instructions
```

---
*Created and maintained with professional software engineering practices.*
