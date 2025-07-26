"""
Process utilities for running external scripts.
"""

import os
import subprocess
import sys


def run_scraper():
    """Run the iceberg scraper directly (no subprocess needed)."""
    print("Collecting latest iceberg data...")
    try:
        # Import and call the iceberg collection function directly
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from iceberg import collect_iceberg_data

        success = collect_iceberg_data()

        if success:
            print("Data collection completed")
            return True
        else:
            print("Data collection failed")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def generate_api():
    """Generate API endpoints for external data access directly (no subprocess needed)."""
    print("Generating API endpoints...")
    try:
        # Import and call the API generation function directly
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from api_generator import create_api_endpoints

        create_api_endpoints()

        print("API endpoints generated successfully")
        print("\nYour data is now accessible via:")
        print(
            "• Raw JSON: https://raw.githubusercontent.com/Joel-hanson/Iceberg-locations/main/data/iceberg_location.json"
        )
        print(
            "• Latest data: https://raw.githubusercontent.com/Joel-hanson/Iceberg-locations/main/api/latest.json"
        )
        print(
            "• Summary: https://raw.githubusercontent.com/Joel-hanson/Iceberg-locations/main/api/summary.json"
        )
        print(
            "• Recent data: https://raw.githubusercontent.com/Joel-hanson/Iceberg-locations/main/api/recent.json"
        )
        print(
            "• JSONP version: https://raw.githubusercontent.com/Joel-hanson/Iceberg-locations/main/api/latest.jsonp"
        )
        return True
    except Exception as e:
        print(f"Error generating API: {e}")
        return False
