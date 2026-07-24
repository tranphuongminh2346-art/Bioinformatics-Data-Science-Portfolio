# PubMed Citation Graph Analyzer

A graph data engineering and analysis project that reads academic literature citations, constructs a directed citation network DiGraph, calculates citation counts (in-degree centrality) and structural authority (PageRank), and maps out citation chains and pathways.

It uses a **real scientific citation network of seminal bioinformatics publications** (including the original papers for BLAST, CLUSTAL W, MUSCLE, Bowtie, and the Human Genome projects) to evaluate research impact.

## Features
- **Graph Construction**: Parses PubMed citation logs and maps nodes (PMID papers) and directed links (citing $\rightarrow$ cited relations) using NetworkX.
- **In-degree Centrality**: Computes raw citation counts to find the most directly-cited papers.
- **PageRank Authority**: Applies Google's PageRank algorithm to identify papers with high network authority (highly cited by other highly cited papers).
- **Pathway Traversal**: Finds the shortest citation chain between any two papers (e.g. tracing newer tools like Bowtie 2 back to foundational algorithms like BLAST).
- **Network Plotting**: Saves a spring-layout network diagram using Matplotlib, where node size is dynamically scaled relative to its PageRank score.

## Project Structure
- `citation_network.py`: Core graph processing class `CitationNetwork` implementing NetworkX functions.
- `main.py`: Command-line driver executing centralities, paths, and graph plotting.
- `test_network.py`: Unit test suite verifying directed paths, degree math, and PageRank weights.
- `citations.json`: Real PubMed citation metadata database subset.
- `requirements.txt`: Package dependencies.

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

To execute the network analysis and plot the citation graph:
```bash
python main.py --input citations.json --output citation_graph.png
```

This command will:
1. Load the bibliography JSON.
2. Build the directed graph and calculate node/edge counts.
3. Print a ranked list of papers based on raw citations and PageRank influence.
4. Output the exact citation path tracing Bowtie 2 back to BLAST.
5. Save the network diagram to `citation_graph.png`.

## Running Unit Tests
To run the automated tests:
```bash
python -m unittest test_network.py
```
