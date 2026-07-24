"""
Phylogenetic Tree Reconstructor (UPGMA)
Author: Portfolio Creator
Description: Parses aligned FASTA sequences, computes Hamming distance matrices,
             reconstructs phylogenetic trees via the UPGMA clustering algorithm,
             and returns Newick strings.
Language: English (100%)
"""

import os
import numpy as np

class PhylogeneticNode:
    """Represents a node in the phylogenetic tree."""
    def __init__(self, name: str, left=None, right=None, distance: float = 0.0, leaf_count: int = 1):
        self.name = name
        self.left = left
        self.right = right
        self.distance = distance  # Height of the node from its children
        self.leaf_count = leaf_count

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

    def to_newick(self) -> str:
        """Converts the node structure to Newick tree format recursively."""
        if self.is_leaf():
            return self.name
        
        # Calculate branch lengths
        left_len = self.distance - (self.left.distance if self.left else 0.0)
        right_len = self.distance - (self.right.distance if self.right else 0.0)
        
        return f"({self.left.to_newick()}:{left_len:.4f},{self.right.to_newick()}:{right_len:.4f})"

class UPGMATreeReconstructor:
    """Executes the Unweighted Pair Group Method with Arithmetic Mean (UPGMA) algorithm."""
    
    def __init__(self, fasta_path: str):
        self.fasta_path = fasta_path
        self.names = []
        self.sequences = []
        self.load_fasta()

    def load_fasta(self):
        """Parses headers and sequences from a FASTA file."""
        if not os.path.exists(self.fasta_path):
            raise FileNotFoundError(f"FASTA file not found: {self.fasta_path}")
            
        self.names = []
        self.sequences = []
        
        current_seq = []
        with open(self.fasta_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith(">"):
                    if current_seq:
                        self.sequences.append("".join(current_seq))
                        current_seq = []
                    self.names.append(line[1:])
                elif line:
                    current_seq.append(line)
            if current_seq:
                self.sequences.append("".join(current_seq))

        # Check alignment length
        if len(self.sequences) > 0:
            seq_len = len(self.sequences[0])
            if not all(len(s) == seq_len for s in self.sequences):
                raise ValueError("Input FASTA sequences must be aligned (same length).")

    def calculate_distance_matrix(self) -> np.ndarray:
        """
        Calculates pairwise Hamming distance matrix.
        Formula: count of mismatches / total sequence length
        
        Returns:
            np.ndarray: N x N distance matrix.
        """
        n = len(self.sequences)
        matrix = np.zeros((n, n))
        seq_len = len(self.sequences[0])
        
        for i in range(n):
            for j in range(i + 1, n):
                mismatches = sum(c1 != c2 for c1, c2 in zip(self.sequences[i], self.sequences[j]))
                dist = mismatches / seq_len
                matrix[i, j] = dist
                matrix[j, i] = dist
                
        return matrix

    def reconstruct(self) -> PhylogeneticNode:
        """
        Reconstructs the phylogenetic tree using the UPGMA algorithm.
        
        Returns:
            PhylogeneticNode: Root node of the reconstructed tree.
        """
        n = len(self.sequences)
        if n == 0:
            raise ValueError("No sequences found for tree reconstruction.")
            
        # 1. Initialize clusters
        nodes = [PhylogeneticNode(self.names[i]) for i in range(n)]
        
        # 2. Initialize distance matrix
        dist_matrix = self.calculate_distance_matrix()
        
        # Keep track of active indices
        active_indices = list(range(n))
        
        # Map cluster index to nodes
        cluster_map = {i: nodes[i] for i in range(n)}
        
        # Distance matrix tracking (expanding index during merges)
        current_matrix = dist_matrix.copy()
        
        # Merge loop
        next_cluster_id = n
        while len(active_indices) > 1:
            # Find min distance in current_matrix among active indices
            min_dist = float('inf')
            u, v = -1, -1
            
            # Search active pairs
            for idx_i in range(len(active_indices)):
                i = active_indices[idx_i]
                for idx_j in range(idx_i + 1, len(active_indices)):
                    j = active_indices[idx_j]
                    if current_matrix[i, j] < min_dist:
                        min_dist = current_matrix[i, j]
                        u, v = i, j
                        
            # Merge clusters u and v into a new parent node
            node_u = cluster_map[u]
            node_v = cluster_map[v]
            
            parent_height = min_dist / 2.0
            parent_node = PhylogeneticNode(
                name=f"Node_{next_cluster_id}",
                left=node_u,
                right=node_v,
                distance=parent_height,
                leaf_count=node_u.leaf_count + node_v.leaf_count
            )
            
            # Remove u and v from active list, add new cluster ID
            active_indices.remove(u)
            active_indices.remove(v)
            new_id = next_cluster_id
            
            # Calculate distance from new cluster to all other active clusters
            # Resize matrix to include new_id
            m_size = new_id + 1
            new_matrix = np.zeros((m_size, m_size))
            new_matrix[:new_id, :new_id] = current_matrix
            
            for w in active_indices:
                node_w = cluster_map[w]
                # UPGMA average distance formula
                dist_uw = current_matrix[u, w]
                dist_vw = current_matrix[v, w]
                
                weight_u = node_u.leaf_count
                weight_v = node_v.leaf_count
                
                avg_dist = (weight_u * dist_uw + weight_v * dist_vw) / (weight_u + weight_v)
                new_matrix[new_id, w] = avg_dist
                new_matrix[w, new_id] = avg_dist
                
            current_matrix = new_matrix
            cluster_map[new_id] = parent_node
            active_indices.append(new_id)
            next_cluster_id += 1
            
        # The last active index is the root of the tree
        root_id = active_indices[0]
        return cluster_map[root_id]
