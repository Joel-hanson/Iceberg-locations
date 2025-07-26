#!/usr/bin/env python3
"""
Modular CLI for the Antarctic Iceberg Tracker.

This is a simplified, maintainable version that delegates to specific command modules.
"""

import argparse
import sys
import os

# Add the src directory to the Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from commands.scrape import scrape_command
from commands.info import info_command
from commands.map import map_command
from commands.animations import animations_command
from commands.api import api_command


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Antarctic Iceberg Tracker CLI",
        epilog="""
Examples:
  python main.py scrape      # Collect latest iceberg data
  python main.py info        # Show data summary  
  python main.py map         # Generate interactive map
  python main.py animations  # Show iceberg movement animation URLs
  python main.py api         # Generate API endpoints for external access
        """.strip(),
    )

    parser.add_argument(
        "command",
        choices=["scrape", "info", "map", "animations", "api"],
        help="Command to execute",
    )

    args = parser.parse_args()

    # Command routing - each command is handled by its own module
    command_map = {
        "scrape": scrape_command,
        "info": info_command,
        "map": map_command,
        "animations": animations_command,
        "api": api_command,
    }

    try:
        command_func = command_map[args.command]
        return command_func()
    except KeyError:
        print(f"Unknown command: {args.command}")
        return 1
    except Exception as e:
        print(f"Error executing command '{args.command}': {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
