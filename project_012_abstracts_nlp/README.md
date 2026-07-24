# Clinical Text Mining & Sentiment Analysis of Abstracts

A Python text mining and Natural Language Processing (NLP) pipeline that processes PubMed publication abstracts, computes term frequency-inverse document frequency (TF-IDF) weights using scikit-learn, and applies rule-based clinical lexicons to classify publication outcomes.

This represents a text analytics workflow for scanning large sets of medical literature to filter positive drug trials, toxic side-effects, or neutral pharmacokinetics.

## Features
- **Tokenization & Stopword Removal**: Cleans abstracts by stripping punctuation, converting to lowercase, and filtering standard English stopwords without external download dependencies.
- **TF-IDF Term Weighting**: Implements scikit-learn's `TfidfVectorizer` to identify the most significant words across the literature corpus.
- **Clinical Lexicon Sentiment Classifier**: Scans tokenized abstracts for positive clinical terminology (e.g. `efficacy`, `promising`, `improved`) and negative toxicity flags (e.g. `toxicity`, `failed`, `adverse`), computing a net polarity score to predict outcomes.

## Project Structure
- `text_miner.py`: Main class `ClinicalTextMiner` handling text parsing, tf-idf, and sentiment scores.
- `main.py`: Command-line interface driver printing results.
- `test_text_miner.py`: Unit test suite verifying cleaning, lexicon matches, and scores.
- `abstracts.json`: Sample database of real PubMed abstracts.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To run the NLP pipeline:
```bash
python main.py --input abstracts.json
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_text_miner.py
```
