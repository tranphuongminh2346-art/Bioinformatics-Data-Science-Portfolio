"""
Unit Tests for PubMed Citation Graph Analyzer
Author: Portfolio Creator
Description: Verify graph construction, in-degree citation count ranking,
             PageRank centrality values, and shortest citation pathways.
Language: English (100%)
"""

import unittest
import os
import sys
import tempfile
import json
import networkx as nx

# Add directory containing this file to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from citation_network import CitationNetwork

class TestCitationNetwork(unittest.TestCase):

    def setUp(self):
        # Create a mock citation network JSON
        # Paper A (cites B)
        # Paper B (cites C)
        # Paper C (cites none)
        self.mock_citations = [
            {
                "pmid": "1",
                "title": "Paper A",
                "authors": "Author A",
                "year": 2020,
                "citations": ["2"]
            },
            {
                "pmid": "2",
                "title": "Paper B",
                "authors": "Author B",
                "year": 2018,
                "citations": ["3"]
            },
            {
                "pmid": "3",
                "title": "Paper C",
                "authors": "Author C",
                "year": 2015,
                "citations": []
            }
        ]

        self.db_fd, self.temp_json_path = tempfile.mkstemp(suffix=".json")
        with open(self.temp_json_path, 'w', encoding='utf-8') as f:
            json.dump(self.mock_citations, f)
            
        self.net = CitationNetwork(self.temp_json_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.temp_json_path):
            os.remove(self.temp_json_path)

    def test_graph_construction(self):
        self.assertEqual(self.net.graph.number_of_nodes(), 3)
        self.assertEqual(self.net.graph.number_of_edges(), 2)
        
        # Verify directed edges: 1 -> 2 and 2 -> 3
        self.assertTrue(self.net.graph.has_edge("1", "2"))
        self.assertTrue(self.net.graph.has_edge("2", "3"))
        self.assertFalse(self.net.graph.has_edge("1", "3"))

    def test_get_citation_counts(self):
        in_degrees = self.net.get_citation_counts()
        
        # Paper 3 has 1 citation (from 2)
        # Paper 2 has 1 citation (from 1)
        # Paper 1 has 0 citations
        self.assertEqual(in_degrees["3"], 1)
        self.assertEqual(in_degrees["2"], 1)
        self.assertEqual(in_degrees["1"], 0)

    def test_calculate_pagerank(self):
        pr = self.net.calculate_pagerank()
        
        # Total sum of PageRank must be approximately 1.0
        self.assertAlmostEqual(sum(pr.values()), 1.0)
        
        # Node 3 is cited by 2 which is cited by 1, so 3 should have highest PageRank
        self.assertTrue(pr["3"] > pr["2"])
        self.assertTrue(pr["2"] > pr["1"])

    def test_shortest_citation_path(self):
        # Path from 1 to 3 should be 1 -> 2 -> 3
        path = self.net.find_shortest_citation_path("1", "3")
        self.assertEqual(path, ["1", "2", "3"])
        
        # Path from 3 to 1 should be empty (since it's a directed graph and 3 doesn't cite 1)
        path_reverse = self.net.find_shortest_citation_path("3", "1")
        self.assertEqual(path_reverse, [])

if __name__ == "__main__":
    unittest.main()
