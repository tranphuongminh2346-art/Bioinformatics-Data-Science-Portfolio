# Text Summarizer (Extractive PageRank)

An extractive text summarization pipeline that parses text documents into individual sentences, computes TF-IDF vector embeddings, constructs a sentence similarity graph using cosine metrics, and runs the **PageRank** centrality algorithm to select the most representative sentences.

## Features
- **Sentence Splits & Cleaning**: Segments text using regex punctuation markers.
- **TF-IDF & Cosine Similarities**: Builds sentence vector weights using `scikit-learn` and maps similarity linkages.
- **Graph Centrality (TextRank)**: Converts similarity matrices into NetworkX graphs and evaluates node ranks using PageRank to identify structural centers.

## Project Structure
- `summarizer.py`: Text parser, similarity loaders, PageRank, and summaries.
- `main.py`: Command-line interface driver.
- `test_summarizer.py`: Unit test suite verifying sentence splits and ranks.
- `document.txt`: Sample text document about molecular biology.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To extract text summaries:
```bash
python main.py --input document.txt --limit 2
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_summarizer.py
```
