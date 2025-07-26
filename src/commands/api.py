"""
API generation command for the Antarctic Iceberg Tracker CLI.
"""

from utils.process_runner import generate_api


def api_command():
    """Execute the API generation command."""
    return 0 if generate_api() else 1
