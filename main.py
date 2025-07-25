#!/usr/bin/env python3
"""
Main entry point for the Antarctic Iceberg Tracker.
This script imports and runs the CLI from the src directory.
"""

import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from cli import main

if __name__ == "__main__":
    sys.exit(main())
