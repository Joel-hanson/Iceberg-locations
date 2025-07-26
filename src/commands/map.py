"""
Map generation command for the Antarctic Iceberg Tracker CLI.
"""

from utils.map_generator import generate_map


def map_command():
    """Execute the map command."""
    return 0 if generate_map() else 1
