#!/usr/bin/env python3
"""
Setup script for the Iceberg Location Tracker.
"""

from pathlib import Path

from src.config import create_directories, get_config


def setup_project():
    """Set up project directories and initial configuration."""
    print("Setting up Iceberg Location Tracker...")

    # Load and create directories
    config = get_config()
    create_directories(config)

    # Create initial data file if it doesn't exist
    output_file = Path(config["output_file"])
    if not output_file.exists():
        output_file.write_text("{}")
        print(f"Created initial data file: {output_file}")

    # Create log directory
    log_file = Path(config["log_file"])
    log_file.parent.mkdir(parents=True, exist_ok=True)

    print("Project setup complete!")
    print(f"   Data file: {output_file}")
    print(f"   Log file: {log_file}")

    if config["backup_enabled"]:
        backup_dir = Path(config["backup_directory"])
        print(f"   Backup directory: {backup_dir}")

    print("\nReady to track icebergs! Try:")
    print("   python cli.py scrape      # Get latest data")
    print("   python cli.py report      # Generate summary")
    print("   python cli.py --help      # See all options")


if __name__ == "__main__":
    setup_project()
