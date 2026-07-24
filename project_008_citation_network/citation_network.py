"""
PubMed Citation Network Graph Analyzer
Author: Portfolio Creator
Description: Core module to read PubMed paper records, construct directed citation graphs,
             compute PageRank metrics, and generate network layout plots.
Language: English (100%)
"""

import os
import json
import networkx as nx
import matplotlib.pyplot as plt

class CitationNetwork:
    """Directed graph representing paper citations and authority metrics."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.graph = nx.DiGraph()
        self.metadata = {}
        self.load_graph()

    def load_graph(self):
        """Loads citation records from JSON file and builds the networkx DiGraph."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Citation dataset not found at: {self.data_path}")
            
        with open(self.data_path, 'r', encoding='utf-8') as f:
            records = json.load(f)
            
        # 1. Add nodes and store metadata
        for record in records:
            pmid = record["pmid"]
            self.metadata[pmid] = {
                "title": record.get("title", "Unknown"),
                "authors": record.get("authors", "Unknown"),
                "year": record.get("year", 0)
            }
            self.graph.add_node(pmid)
            
        # 2. Add directed edges (citation links)
        # Note: A citations list represents out-edges (this paper cites other papers)
        for record in records:
            pmid = record["pmid"]
            for cited_pmid in record.get("citations", []):
                # Only add edges to nodes present in our dataset
                if cited_pmid in self.metadata:
                    self.graph.add_edge(pmid, cited_pmid)

    def get_citation_counts(self) -> dict:
        """
        Calculates total inbound citations (in-degree) for each node.
        
        Returns:
            dict: PMID mapped to citation counts.
        """
        return dict(self.graph.in_degree())

    def calculate_pagerank(self) -> dict:
        """
        Computes PageRank metrics of authority on the network.
        
        Returns:
            dict: PMID mapped to PageRank float weights.
        """
        # alpha=0.85 is standard damping factor
        return nx.pagerank(self.graph, alpha=0.85)

    def find_shortest_citation_path(self, start_pmid: str, target_pmid: str) -> list:
        """
        Finds the shortest directed path representing citation link chains.
        
        Args:
            start_pmid (str): Citing paper.
            target_pmid (str): Target cited paper.
            
        Returns:
            list: List of PMIDs in the path.
        """
        try:
            return nx.shortest_path(self.graph, source=start_pmid, target=target_pmid)
        except nx.NetworkXNoPath:
            return []

    def plot_network(self, output_path: str):
        """
        Generates and saves a directed network graph visualization.
        Node sizes reflect PageRank authority scores.
        
        Args:
            output_path (str): File path to save graph image.
        """
        plt.figure(figsize=(10, 8))
        
        # Calculate layouts and sizes
        pos = nx.spring_layout(self.graph, k=1.5, seed=42)
        pr = self.calculate_pagerank()
        
        # Base node size on PageRank
        node_sizes = [v * 5000 for v in pr.values()]
        
        # Draw edges
        nx.draw_networkx_edges(
            self.graph, pos, 
            arrowstyle="->", arrowsize=15, 
            edge_color="#cbd5e1", width=1.5
        )
        
        # Draw nodes
        nx.draw_networkx_nodes(
            self.graph, pos, 
            node_size=node_sizes, 
            node_color="#0284c7", 
            edgecolors="#0369a1", linewidths=1.5
        )
        
        # Draw labels (use author year format)
        labels = {}
        for pmid, meta in self.metadata.items():
            first_author = meta["authors"].split(",")[0]
            labels[pmid] = f"{first_author}\n({meta['year']})"
            
        nx.draw_networkx_labels(
            self.graph, pos, 
            labels=labels, 
            font_size=9, font_weight="bold", font_color="#1e293b"
        )
        
        plt.title("Bioinformatics Citation Authority Graph (PageRank Layout)", fontsize=12, fontweight='bold', pad=15)
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
