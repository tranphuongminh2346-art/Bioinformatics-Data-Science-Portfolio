"""
Job Listing Scraper & Parser
Author: Portfolio Creator
Description: Uses BeautifulSoup to parse local mock HTML job listings,
             uses regular expressions to parse salary ranges, and cleans records.
Language: English (100%)
"""

import os
import re
from bs4 import BeautifulSoup

class JobListingParser:
    """Parses structural job metrics from HTML pages."""
    
    def __init__(self, html_path: str):
        self.html_path = html_path

    def parse_salary(self, salary_text: str) -> tuple:
        """
        Extracts minimum, maximum, and average annual salaries from string text.
        e.g., "$125,000 - $145,000 a year" -> (125000.0, 145000.0, 135000.0)
        
        Args:
            salary_text (str): Raw text.
            
        Returns:
            tuple: (min_salary, max_salary, avg_salary)
        """
        # Clean text
        text = salary_text.replace(',', '').strip()
        
        # Look for digit patterns
        matches = re.findall(r'\$?(\d+)', text)
        
        if len(matches) >= 2:
            val_1 = float(matches[0])
            val_2 = float(matches[1])
            min_val = min(val_1, val_2)
            max_val = max(val_1, val_2)
            
            # Simple check to scale up if salaries are written in thousands (e.g. 120 - 150)
            if max_val < 1000:
                min_val *= 1000
                max_val *= 1000
                
            avg_val = (min_val + max_val) / 2.0
            return min_val, max_val, avg_val
        elif len(matches) == 1:
            val = float(matches[0])
            if val < 1000:
                val *= 1000
            return val, val, val
            
        return None, None, None

    def scrape_jobs(self) -> list:
        """
        Parses all job cards inside the HTML file.
        
        Returns:
            list: List of parsed job dictionaries.
        """
        if not os.path.exists(self.html_path):
            raise FileNotFoundError(f"HTML source file not found: {self.html_path}")
            
        with open(self.html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        cards = soup.find_all('div', class_='job-card')
        jobs = []
        
        for card in cards:
            title_node = card.find('h2', class_='job-title')
            comp_node = card.find('span', class_='company')
            loc_node = card.find('span', class_='location')
            sal_node = card.find('span', class_='salary')
            
            title = title_node.text.strip() if title_node else "N/A"
            company = comp_node.text.strip() if comp_node else "N/A"
            location = loc_node.text.strip() if loc_node else "N/A"
            salary_raw = sal_node.text.strip() if sal_node else "N/A"
            
            min_sal, max_sal, avg_sal = self.parse_salary(salary_raw)
            
            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "salary_text": salary_raw,
                "min_salary": min_sal,
                "max_salary": max_sal,
                "avg_salary": avg_sal
            })
            
        return jobs
