"""
Data handling utilities for the Antarctic Iceberg Tracker.
"""

import json
import os
from datetime import datetime


def get_data_file_path():
    """Get the path to the main data file."""
    project_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    return os.path.join(project_root, "data", "iceberg_location.json")


def load_iceberg_data():
    """Load and return the iceberg data from the data file."""
    data_file = get_data_file_path()

    if not os.path.exists(data_file):
        return None, "No data file found. Run 'python main.py scrape' first."

    try:
        with open(data_file, "r") as f:
            data = json.load(f)
        return data, None
    except Exception as e:
        return None, f"Error reading data: {e}"


def get_latest_date(data):
    """Get the latest date from the data, properly sorted chronologically."""
    if not data:
        return "Unknown"

    dates = sorted(data.keys()) if data else []
    try:
        dates_with_dt = [(d, datetime.strptime(d, "%m/%d/%y")) for d in dates]
        dates_with_dt.sort(key=lambda x: x[1])  # Sort by datetime
        return dates_with_dt[-1][0] if dates_with_dt else "Unknown"
    except:
        # Fallback to string sorting if date parsing fails
        return dates[-1] if dates else "Unknown"


def get_unique_icebergs(data):
    """Get a set of unique iceberg names from the data."""
    unique_icebergs = set()
    for icebergs in data.values():
        for iceberg in icebergs:
            if iceberg.get("iceberg"):
                unique_icebergs.add(iceberg["iceberg"])
    return unique_icebergs


def get_data_freshness(date_str):
    """Get the freshness status of data based on the date."""
    try:
        latest_dt = datetime.strptime(date_str, "%m/%d/%y")
        today = datetime.now()
        days_old = (today - latest_dt).days

        if days_old == 0:
            return "Fresh (updated today)"
        elif days_old <= 7:
            return f"Recent (updated {days_old} days ago)"
        else:
            return f"Outdated (updated {days_old} days ago)"
    except:
        return "Update time unknown"
