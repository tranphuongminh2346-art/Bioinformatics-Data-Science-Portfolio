"""
PLINK PED/MAP pedigree Parser & QC checks
Author: Portfolio Creator
Description: Parses PLINK pedigree files, detects Mendelian inheritance errors,
             and computes genetic marker call rates.
Language: English (100%)
"""

import os

class PLINKParser:
    """Parses PLINK genetic datasets (.ped / .map) and runs inheritance validation checks."""
    
    def __init__(self, ped_path: str, map_path: str):
        self.ped_path = ped_path
        self.map_path = map_path
        self.markers = []
        self.individuals = {}
        self.load_map()
        self.load_ped()

    def load_map(self):
        """Reads genomic marker details from MAP file."""
        if not os.path.exists(self.map_path):
            raise FileNotFoundError(f"MAP file not found: {self.map_path}")
            
        with open(self.map_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    self.markers.append(parts[1])  # Marker ID

    def load_ped(self):
        """Reads pedigree lines and genotypes from PED file."""
        if not os.path.exists(self.ped_path):
            raise FileNotFoundError(f"PED file not found: {self.ped_path}")
            
        with open(self.ped_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) < 6:
                    continue
                    
                fid = parts[0]
                iid = parts[1]
                pat = parts[2]
                mat = parts[3]
                sex = parts[4]
                pheno = parts[5]
                
                # Genotypes: pairs of alleles
                genotype_tokens = parts[6:]
                genotypes = []
                for i in range(0, len(genotype_tokens), 2):
                    if i + 1 < len(genotype_tokens):
                        genotypes.append((genotype_tokens[i], genotype_tokens[i+1]))
                        
                self.individuals[iid] = {
                    "fid": fid,
                    "iid": iid,
                    "pat": pat,
                    "mat": mat,
                    "sex": sex,
                    "pheno": pheno,
                    "genotypes": genotypes
                }

    def check_mendelian_errors(self) -> list:
        """
        Scans offspring to find Mendelian inheritance mismatches.
        
        Returns:
            list: List of dicts representing Mendelian errors (offspring, marker, father, mother, genotypes).
        """
        errors = []
        
        for iid, ind in self.individuals.items():
            pat = ind["pat"]
            mat = ind["mat"]
            
            # Check if parents exist in our database
            if pat in self.individuals and mat in self.individuals:
                father = self.individuals[pat]
                mother = self.individuals[mat]
                
                child_genotypes = ind["genotypes"]
                father_genotypes = father["genotypes"]
                mother_genotypes = mother["genotypes"]
                
                # Check each marker
                for m_idx, marker_id in enumerate(self.markers):
                    if m_idx >= len(child_genotypes) or m_idx >= len(father_genotypes) or m_idx >= len(mother_genotypes):
                        continue
                        
                    c_g = child_genotypes[m_idx]
                    f_g = father_genotypes[m_idx]
                    m_g = mother_genotypes[m_idx]
                    
                    # If any allele is missing ('0'), skip check
                    if '0' in c_g or '0' in f_g or '0' in m_g:
                        continue
                        
                    c1, c2 = c_g
                    f1, f2 = f_g
                    m1, m2 = m_g
                    
                    # Offspring must inherit one allele from father and one from mother
                    # Condition: (c1 in father and c2 in mother) or (c2 in father and c1 in mother)
                    valid = ((c1 == f1 or c1 == f2) and (c2 == m1 or c2 == m2)) or \
                            ((c2 == f1 or c2 == f2) and (c1 == m1 or c1 == m2))
                            
                    if not valid:
                        errors.append({
                            "child_id": iid,
                            "father_id": pat,
                            "mother_id": mat,
                            "marker": marker_id,
                            "child_gt": f"{c1}/{c2}",
                            "father_gt": f"{f1}/{f2}",
                            "mother_gt": f"{m1}/{m2}"
                        })
                        
        return errors

    def calculate_call_rates(self) -> dict:
        """
        Calculates call rates for each marker.
        
        Returns:
            dict: Marker ID mapped to call rate percentage.
        """
        call_rates = {}
        total_ind = len(self.individuals)
        if total_ind == 0:
            return {}
            
        for m_idx, marker_id in enumerate(self.markers):
            called_count = 0
            for iid, ind in self.individuals.items():
                if m_idx < len(ind["genotypes"]):
                    g = ind["genotypes"][m_idx]
                    if '0' not in g:
                        called_count += 1
            call_rates[marker_id] = float(called_count) / total_ind
            
        return call_rates
