"""
Unit Tests for Jobs Board Scraper & Parser
Author: Portfolio Creator
Description: Verify regex salary string extracts and HTML node parsing accuracy.
Language: English (100%)
"""

import unittest
import os
import sys
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from job_parser import JobListingParser

class TestJobListingParser(unittest.TestCase):

    def setUp(self):
        self.parser = JobListingParser("dummy.html")

    def test_parse_salary_range(self):
        # 1. Standard range
        min_s, max_s, avg_s = self.parser.parse_salary("$100,000 - $120,000 a year")
        self.assertAlmostEqual(min_s, 100000.0)
        self.assertAlmostEqual(max_s, 120000.0)
        self.assertAlmostEqual(avg_s, 110000.0)

        # 2. Simple numeric values without dollar signs or commas
        min_s, max_s, avg_s = self.parser.parse_salary("80000 to 90000 per year")
        self.assertAlmostEqual(min_s, 80000.0)
        self.assertAlmostEqual(max_s, 90000.0)
        self.assertAlmostEqual(avg_s, 85000.0)

        # 3. Single value
        min_s, max_s, avg_s = self.parser.parse_salary("$95,000 a year")
        self.assertAlmostEqual(min_s, 95000.0)
        self.assertAlmostEqual(max_s, 95000.0)
        self.assertAlmostEqual(avg_s, 95000.0)

        # 4. Under-thousand scales (e.g., "$120 - $140k")
        min_s, max_s, avg_s = self.parser.parse_salary("120 - 140")
        self.assertAlmostEqual(min_s, 120000.0)
        self.assertAlmostEqual(max_s, 140000.0)
        self.assertAlmostEqual(avg_s, 130000.0)

        # 5. Invalid / No salary
        min_s, max_s, avg_s = self.parser.parse_salary("Competitive salary")
        self.assertIsNone(min_s)
        self.assertIsNone(max_s)
        self.assertIsNone(avg_s)

    def test_html_scraping(self):
        # Create a tiny mock HTML file
        mock_html = (
            "<div class='job-card'>\n"
            "  <h2 class='job-title'>Bioinformatics Engineer</h2>\n"
            "  <span class='company'>Biotech Corp</span>\n"
            "  <span class='location'>Boston, MA</span>\n"
            "  <span class='salary'>$120,000 a year</span>\n"
            "</div>"
        )
        db_fd, temp_html_path = tempfile.mkstemp(suffix=".html")
        with open(temp_html_path, 'w', encoding='utf-8') as f:
            f.write(mock_html)

        try:
            local_parser = JobListingParser(temp_html_path)
            jobs = local_parser.scrape_jobs()
            self.assertEqual(len(jobs), 1)
            self.assertEqual(jobs[0]["title"], "Bioinformatics Engineer")
            self.assertEqual(jobs[0]["company"], "Biotech Corp")
            self.assertEqual(jobs[0]["location"], "Boston, MA")
            self.assertAlmostEqual(jobs[0]["avg_salary"], 120000.0)
        finally:
            os.close(db_fd)
            if os.path.exists(temp_html_path):
                os.remove(temp_html_path)

if __name__ == "__main__":
    unittest.main()
