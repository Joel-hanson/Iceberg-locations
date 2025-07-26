#!/usr/bin/env python3
"""
Test suite for the Iceberg Location Tracker - Updated for Modular Architecture.
"""

import json
import os
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
            ],
            "01/15/25": [
                {
                    "iceberg": "B22A",
                    "latitude": -70.12,
                    "longitude": 156.45,
                    "dms_latitude": "70°7'S",
                    "dms_longitude": "156°27'E",
                    "recent_observation": "01/15/25",
                }
            ],
        }

    def test_data_structure_validity(self):
        """Test data structure validity."""
        self.assertIsInstance(self.sample_data, dict)
        for date, icebergs in self.sample_data.items():
            self.assertIsInstance(icebergs, list)
            for iceberg in icebergs:
                self.assertIn("iceberg", iceberg)
                self.assertIn("latitude", iceberg)
                self.assertIn("longitude", iceberg)
                self.assertIn("recent_observation", iceberg)

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

    def test_iceberg_naming_convention(self):
        """Test iceberg naming follows expected patterns."""
        for date, icebergs in self.sample_data.items():
            for iceberg in icebergs:
                name = iceberg["iceberg"]
                self.assertIsInstance(name, str)
                self.assertGreater(len(name), 0)
                # Most icebergs follow letter+number pattern
                self.assertTrue(any(c.isalpha() for c in name))


class TestTemplates(unittest.TestCase):
    """Test cases for template functionality."""

    def test_map_template_import(self):
        """Test that map template can be imported."""
        from templates.map_template import get_map_html_template

        self.assertTrue(callable(get_map_html_template))

    def test_map_template_content(self):
        """Test that map template returns valid HTML."""
        from templates.map_template import get_map_html_template

        html = get_map_html_template()
        self.assertIsInstance(html, str)
        self.assertTrue(html.startswith("<!DOCTYPE html>"))
        self.assertIn("<html", html)
        self.assertIn("</html>", html)
        self.assertIn("Antarctic Iceberg Tracker", html)

    def test_map_template_features(self):
        """Test that map template includes expected features."""
        from templates.map_template import get_map_html_template

        html = get_map_html_template()
        # Check for key JavaScript libraries
        self.assertIn("leaflet", html.lower())
        self.assertIn("bootstrap", html.lower())
        # Check for key functionality
        self.assertIn("loadIcebergData", html)
        self.assertIn("createIcebergPopup", html)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""

    def test_end_to_end_data_flow(self):
        """Test the complete data flow from loading to display."""
        # This would be a more complex test that verifies:
        # 1. Data can be loaded
        # 2. Latest date is correctly identified
        # 3. Info can be displayed
        # 4. Map can be generated
        # We'll keep it simple for now
        try:
            from utils.data_handler import get_data_file_path

            path = get_data_file_path()
            self.assertIsInstance(path, str)
            self.assertTrue(path.endswith(".json"))
        except Exception as e:
            self.fail(f"Data flow test failed: {e}")

    def test_modular_architecture_integrity(self):
        """Test that the modular architecture is properly structured."""
        # Verify all expected modules exist
        expected_modules = [
            "commands.scrape",
            "commands.info",
            "commands.map",
            "commands.animations",
            "commands.api",
            "utils.data_handler",
            "utils.info_display",
            "utils.animations",
            "utils.map_generator",
            "utils.process_runner",
            "templates.map_template",
        ]

        for module_name in expected_modules:
            try:
                __import__(module_name)
            except ImportError:
                self.fail(f"Required module {module_name} could not be imported")


class TestModularCLI(unittest.TestCase):
    """Test cases for the new modular CLI functionality."""

    def test_command_imports(self):
        """Test that all command modules can be imported."""
        from commands.animations import animations_command
        from commands.api import api_command
        from commands.info import info_command
        from commands.map import map_command
        from commands.scrape import scrape_command

        # All commands should be callable
        self.assertTrue(callable(scrape_command))
        self.assertTrue(callable(info_command))
        self.assertTrue(callable(map_command))
        self.assertTrue(callable(animations_command))
        self.assertTrue(callable(api_command))

    def test_utils_imports(self):
        """Test that all utility modules can be imported."""
        from utils.animations import get_animation_url, show_animations
        from utils.data_handler import get_latest_date, load_iceberg_data
        from utils.info_display import show_info
        from utils.map_generator import generate_map
        from utils.process_runner import generate_api, run_scraper

        # All utilities should be callable
        self.assertTrue(callable(load_iceberg_data))
        self.assertTrue(callable(get_latest_date))
        self.assertTrue(callable(show_info))
        self.assertTrue(callable(show_animations))
        self.assertTrue(callable(get_animation_url))
        self.assertTrue(callable(generate_map))
        self.assertTrue(callable(run_scraper))
        self.assertTrue(callable(generate_api))

    def test_main_cli_import(self):
        """Test that the main CLI can be imported."""
        import cli

        self.assertTrue(hasattr(cli, "main"))

    def test_direct_function_calls(self):
        """Test that direct function calls work."""
        # Test iceberg collection function
        from iceberg import collect_iceberg_data

        self.assertTrue(callable(collect_iceberg_data))

        # Test API generation function
        from api_generator import create_api_endpoints

        self.assertTrue(callable(create_api_endpoints))


class TestDataHandling(unittest.TestCase):
    """Test cases for data handling utilities."""

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
            ],
            "01/15/25": [
                {
                    "iceberg": "B22A",
                    "latitude": -70.12,
                    "longitude": 156.45,
                    "dms_latitude": "70°7'S",
                    "dms_longitude": "156°27'E",
                    "recent_observation": "01/15/25",
                }
            ],
        }

    def test_get_latest_date(self):
        """Test latest date extraction with proper chronological sorting."""
        from utils.data_handler import get_latest_date

        latest = get_latest_date(self.sample_data)
        # July 2025 should be later than January 2025
        self.assertEqual(latest, "07/02/25")

    def test_get_unique_icebergs(self):
        """Test unique iceberg extraction."""
        from utils.data_handler import get_unique_icebergs

        unique = get_unique_icebergs(self.sample_data)
        self.assertEqual(len(unique), 2)
        self.assertIn("A23A", unique)
        self.assertIn("B22A", unique)

    def test_data_freshness(self):
        """Test data freshness calculation."""
        from utils.data_handler import get_data_freshness

        # Test with old date
        old_status = get_data_freshness("01/01/20")
        self.assertIn("Outdated", old_status)

    @patch("os.path.exists")
    @patch("builtins.open")
    def test_load_iceberg_data_success(self, mock_open, mock_exists):
        """Test successful data loading."""
        from utils.data_handler import load_iceberg_data

        mock_exists.return_value = True
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(
            self.sample_data
        )

        data, error = load_iceberg_data()
        self.assertIsNotNone(data)
        self.assertIsNone(error)

    @patch("os.path.exists")
    def test_load_iceberg_data_missing_file(self, mock_exists):
        """Test data loading with missing file."""
        from utils.data_handler import load_iceberg_data

        mock_exists.return_value = False

        data, error = load_iceberg_data()
        self.assertIsNone(data)
        self.assertIsNotNone(error)
        self.assertTrue("No data file found" in str(error))


class TestAnimations(unittest.TestCase):
    """Test cases for animation functionality."""

    def test_get_animation_url(self):
        """Test animation URL generation."""
        from utils.animations import get_animation_url

        url = get_animation_url("A23A")
        self.assertTrue(url.startswith("https://"))
        self.assertTrue(url.endswith("a23a_movie.gif"))

    def test_animation_url_lowercase(self):
        """Test that iceberg names are converted to lowercase in URLs."""
        from utils.animations import get_animation_url

        url = get_animation_url("B22A")
        self.assertTrue("b22a_movie.gif" in url)
        self.assertFalse("B22A" in url)


class TestProcessRunner(unittest.TestCase):
    """Test cases for process runner (direct function calls)."""

    @patch("iceberg.collect_iceberg_data")
    def test_run_scraper_success(self, mock_collect):
        """Test successful scraper execution."""
        from utils.process_runner import run_scraper

        mock_collect.return_value = True
        result = run_scraper()
        self.assertTrue(result)
        mock_collect.assert_called_once()

    @patch("iceberg.collect_iceberg_data")
    def test_run_scraper_failure(self, mock_collect):
        """Test scraper execution failure."""
        from utils.process_runner import run_scraper

        mock_collect.return_value = False
        result = run_scraper()
        self.assertFalse(result)

    @patch("api_generator.create_api_endpoints")
    def test_generate_api_success(self, mock_create):
        """Test successful API generation."""
        from utils.process_runner import generate_api

        mock_create.return_value = None  # Function doesn't return anything on success
        result = generate_api()
        self.assertTrue(result)
        mock_create.assert_called_once()

    @patch("api_generator.create_api_endpoints")
    def test_generate_api_failure(self, mock_create):
        """Test API generation failure."""
        from utils.process_runner import generate_api

        mock_create.side_effect = Exception("Test error")
        result = generate_api()
        self.assertFalse(result)


class TestCommands(unittest.TestCase):
    """Test cases for CLI commands."""

    @patch("utils.process_runner.run_scraper")
    def test_scrape_command(self, mock_run):
        """Test scrape command execution."""
        from commands.scrape import scrape_command

        mock_run.return_value = True
        result = scrape_command()
        self.assertEqual(result, 0)

        mock_run.return_value = False
        result = scrape_command()
        self.assertEqual(result, 1)

    @patch("utils.info_display.show_info")
    def test_info_command(self, mock_show):
        """Test info command execution."""
        from commands.info import info_command

        mock_show.return_value = True
        result = info_command()
        self.assertEqual(result, 0)

        mock_show.return_value = False
        result = info_command()
        self.assertEqual(result, 1)

    @patch("utils.map_generator.generate_map")
    def test_map_command(self, mock_generate):
        """Test map command execution."""
        from commands.map import map_command

        mock_generate.return_value = True
        result = map_command()
        self.assertEqual(result, 0)

        mock_generate.return_value = False
        result = map_command()
        self.assertEqual(result, 1)

    @patch("utils.animations.show_animations")
    def test_animations_command(self, mock_show):
        """Test animations command execution."""
        from commands.animations import animations_command

        mock_show.return_value = True
        result = animations_command()
        self.assertEqual(result, 0)

        mock_show.return_value = False
        result = animations_command()
        self.assertEqual(result, 1)

    @patch("utils.process_runner.generate_api")
    def test_api_command(self, mock_generate):
        """Test API command execution."""
        from commands.api import api_command

        mock_generate.return_value = True
        result = api_command()
        self.assertEqual(result, 0)

        mock_generate.return_value = False
        result = api_command()
        self.assertEqual(result, 1)


class TestDirectFunctionCalls(unittest.TestCase):
    """Test cases for direct function calls vs subprocess."""

    def test_iceberg_function_exists(self):
        """Test that iceberg collection function exists and is callable."""
        from iceberg import collect_iceberg_data

        self.assertTrue(callable(collect_iceberg_data))

    def test_api_function_exists(self):
        """Test that API generation function exists and is callable."""
        from api_generator import create_api_endpoints

        self.assertTrue(callable(create_api_endpoints))

    @patch("iceberg.read_current_iceberg_location")
    @patch("iceberg.get_iceberg_details")
    @patch("iceberg.save_data_as_file")
    def test_collect_iceberg_data_success(self, mock_save, mock_details, mock_read):
        """Test successful iceberg data collection."""
        from iceberg import collect_iceberg_data

        # Mock successful data collection
        mock_read.return_value = ([{"test": "data"}], datetime.now())
        mock_details.return_value = [{"iceberg": "test"}]
        mock_save.return_value = None

        result = collect_iceberg_data()
        self.assertTrue(result)

    @patch("iceberg.read_current_iceberg_location")
    def test_collect_iceberg_data_failure(self, mock_read):
        """Test failed iceberg data collection."""
        from iceberg import collect_iceberg_data

        # Mock failed data collection
        mock_read.return_value = (None, None)

        result = collect_iceberg_data()
        self.assertFalse(result)


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
