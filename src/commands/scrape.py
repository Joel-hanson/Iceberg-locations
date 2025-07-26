"""
Scraping command for the Antarctic Iceberg Tracker CLI.
"""

from utils.process_runner import run_scraper


def scrape_command():
    """Execute the scrape command."""
    return 0 if run_scraper() else 1
