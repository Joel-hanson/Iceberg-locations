#!/usr/bin/env python3
"""
Test suite for the Iceberg Location Tracker.
"""

import json
import os
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from config import get_config


class TestConfig(unittest.TestCase):
    """Test cases for configuration."""

    def test_get_config(self):
        """Test configuration loading."""
        config = get_config()
        self.assertIsInstance(config, dict)
        self.assertIn("iceberg_url", config)
        self.assertIn("output_file", config)
        self.assertIn("log_file", config)

    def test_config_values(self):
        """Test configuration values are reasonable."""
        config = get_config()
        self.assertTrue(config["iceberg_url"].startswith("https://"))
        self.assertTrue(config["output_file"].endswith(".json"))
        self.assertGreater(config["request_timeout"], 0)


class TestDataProcessing(unittest.TestCase):
    """Test cases for data processing functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.sample_data = {
            "07/02/25": [
                {
                    "iceberg": "A23A",
                    "latitude": -75.42,
                    "longitude": -39.83,
                    "dms_latitude": "75°25'S",
                    "dms_longitude": "39°50'W",
                    "recent_observation": "07/02/25",
                }
            ]
        }

    def test_data_structure(self):
        """Test data structure validity."""
        self.assertIsInstance(self.sample_data, dict)
        for date, icebergs in self.sample_data.items():
            self.assertIsInstance(icebergs, list)
            for iceberg in icebergs:
                self.assertIn("iceberg", iceberg)
                self.assertIn("latitude", iceberg)
                self.assertIn("longitude", iceberg)

    def test_coordinate_ranges(self):
        """Test coordinate ranges are valid."""
        for date, icebergs in self.sample_data.items():
            for iceberg in icebergs:
                lat = iceberg["latitude"]
                lon = iceberg["longitude"]
                self.assertGreaterEqual(lat, -90)
                self.assertLessEqual(lat, 90)
                self.assertGreaterEqual(lon, -180)
                self.assertLessEqual(lon, 180)

    def test_antarctic_coordinates(self):
        """Test that sample coordinates are in Antarctic region."""
        for date, icebergs in self.sample_data.items():
            for iceberg in icebergs:
                lat = iceberg["latitude"]
                # Antarctic region is typically south of -60°
                self.assertLess(lat, -60, "Iceberg should be in Antarctic region")


class TestCLI(unittest.TestCase):
    """Test cases for CLI functionality."""

    def test_imports(self):
        """Test that CLI modules can be imported."""
        import cli

        self.assertTrue(hasattr(cli, "main"))
        self.assertTrue(hasattr(cli, "run_scraper"))
        self.assertTrue(hasattr(cli, "show_info"))
        self.assertTrue(hasattr(cli, "generate_map"))

    def test_iceberg_import(self):
        """Test that iceberg module can be imported."""
        import iceberg

        # Should be able to import without errors
        self.assertTrue(True)


class TestFileOperations(unittest.TestCase):
    """Test cases for file operations."""

    def test_json_creation(self):
        """Test JSON file creation and reading."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            test_data = {"test": "data"}
            json.dump(test_data, f)
            temp_path = f.name

        try:
            with open(temp_path, "r") as f:
                loaded_data = json.load(f)
            self.assertEqual(loaded_data, test_data)
        finally:
            os.unlink(temp_path)

    def test_directory_structure(self):
        """Test that required directories exist or can be created."""
        project_root = Path(__file__).parent.parent
        data_dir = project_root / "data"
        output_dir = project_root / "output"

        # These should exist or be creatable
        for directory in [data_dir, output_dir]:
            if not directory.exists():
                directory.mkdir(parents=True, exist_ok=True)
            self.assertTrue(directory.exists())

    def test_project_files_exist(self):
        """Test that essential project files exist."""
        project_root = Path(__file__).parent.parent
        essential_files = ["main.py", "setup.py", "requirement.txt", "README.md"]

        for filename in essential_files:
            file_path = project_root / filename
            self.assertTrue(file_path.exists(), f"{filename} should exist")


class TestDateHandling(unittest.TestCase):
    """Test cases for date handling."""

    def test_date_format(self):
        """Test date format consistency."""
        test_date = "07/02/25"
        # Should be MM/DD/YY format
        parts = test_date.split("/")
        self.assertEqual(len(parts), 3)
        self.assertEqual(len(parts[0]), 2)  # Month
        self.assertEqual(len(parts[1]), 2)  # Day
        self.assertEqual(len(parts[2]), 2)  # Year

    def test_date_parsing(self):
        """Test date parsing functionality."""
        test_date = "07/02/25"
        try:
            parsed = datetime.strptime(test_date, "%m/%d/%y")
            self.assertIsInstance(parsed, datetime)
        except ValueError:
            self.fail("Date parsing failed")


if __name__ == "__main__":
    print("Running Iceberg Location Tracker tests...")
    unittest.main(verbosity=2)
