"""
UniProt FASTA Parser
Author: Portfolio Creator
Description: Parses UniProt header metadata schemas (accession, name, species, gene)
             and sequence bodies from biological FASTA files.
Language: English (100%)
"""

import os
import re

# Regex matching UniProt FASTA headers
# Schema: >db|Accession|EntryName ProteinName OS=OrganismName OX=OrganismIdentifier [GN=GeneName ]PE=ProteinExistence SV=SequenceVersion
UNIPROT_PATTERN = re.compile(
    r'^>(sp|tr)\|(\S+)\|(\S+)\s+(.+?)\s+OS=(.+?)\s+OX=(\d+)(?:\s+GN=(\S+))?\s+PE=(\d+)\s+SV=(\d+)$'
)

def parse_uniprot_header(header: str) -> dict:
    """
    Parses UniProt metadata fields from a header line.
    
    Args:
        header (str): Raw FASTA header line.
        
    Returns:
        dict: Parsed metadata fields, or None if match fails.
    """
    match = UNIPROT_PATTERN.match(header.strip())
    if not match:
        return None
        
    db_source, accession, entry_name, protein_name, organism, tax_id, gene_name, pe, sv = match.groups()
    
    return {
        "db_source": db_source,
        "accession": accession,
        "entry_name": entry_name,
        "protein_name": protein_name,
        "organism": organism,
        "tax_id": int(tax_id),
        "gene_name": gene_name if gene_name else None,
        "protein_existence": int(pe),
        "sequence_version": int(sv)
    }

def read_fasta_records(fasta_path: str) -> list:
    """
    Reads a FASTA file and returns a list of dictionaries with metadata and sequences.
    
    Returns:
        list: List of parsed protein record dicts.
    """
    if not os.path.exists(fasta_path):
        raise FileNotFoundError(f"FASTA file not found: {fasta_path}")
        
    records = []
    current_meta = None
    current_seq_lines = []
    
    with open(fasta_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith(">"):
                # Save previous record
                if current_meta:
                    current_meta["sequence"] = "".join(current_seq_lines)
                    records.append(current_meta)
                    
                # Start new record
                current_meta = parse_uniprot_header(line)
                # If header is not in standard UniProt format, create fallback dict
                if not current_meta:
                    current_meta = {
                        "db_source": "unknown",
                        "accession": line[1:].split()[0] if line[1:].split() else "unknown",
                        "entry_name": "unknown",
                        "protein_name": line[1:],
                        "organism": "unknown",
                        "tax_id": 0,
                        "gene_name": None,
                        "protein_existence": 0,
                        "sequence_version": 0
                    }
                current_seq_lines = []
            else:
                current_seq_lines.append(line.upper())
                
        # Save last record
        if current_meta:
            current_meta["sequence"] = "".join(current_seq_lines)
            records.append(current_meta)
            
    return records
