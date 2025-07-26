"""
Info command for the Antarctic Iceberg Tracker CLI.
"""

from utils.info_display import show_info


def info_command():
    """Execute the info command."""
    return 0 if show_info() else 1
