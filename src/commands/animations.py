"""
Animations command for the Antarctic Iceberg Tracker CLI.
"""

from utils.animations import show_animations


def animations_command():
    """Execute the animations command."""
    return 0 if show_animations() else 1
