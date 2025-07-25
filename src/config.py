#!/usr/bin/env python3
"""
Configuration settings for the Iceberg Location Tracker.
"""

import os
from pathlib import Path
from typing import Any, Dict

# Base configuration
BASE_CONFIG: Dict[str, Any] = {
    # URLs and endpoints
    "iceberg_url": "https://www.scp.byu.edu/current_icebergs.html",
    "full_database_url": "https://www.scp.byu.edu/data/iceberg/database1.html",
    "animation_base_url": "https://ftp.scp.byu.edu/data/misc/iceberg_animations/",
    # File paths
    "output_file": "iceberg_location.json",
    "log_file": "iceberg_scraper.log",
    "config_file": "config.json",
    # Request settings
    "request_timeout": 30,
    "max_retries": 3,
    "retry_delay": 1,
    "user_agent": "Mozilla/5.0 (Iceberg-Tracker/2.0; +https://github.com/Joel-hanson/Iceberg-locations)",
    # Logging settings
    "log_level": "INFO",
    "log_format": "%(asctime)s - %(levelname)s - %(message)s",
    "log_to_file": True,
    "log_to_console": True,
    # Data validation
    "min_latitude": -90.0,
    "max_latitude": -60.0,  # Antarctic region
    "min_longitude": -180.0,
    "max_longitude": 180.0,
    # Backup settings
    "backup_enabled": True,
    "backup_directory": "backups",
    "max_backups": 30,
    # API settings (for future extensions)
    "api_enabled": False,
    "api_host": "0.0.0.0",
    "api_port": 8000,
}


def get_config() -> Dict[str, Any]:
    """
    Get configuration with environment variable overrides.

    Returns:
        Configuration dictionary
    """
    config = BASE_CONFIG.copy()

    # Environment variable overrides
    env_mappings = {
        "ICEBERG_URL": "iceberg_url",
        "OUTPUT_FILE": "output_file",
        "LOG_LEVEL": "log_level",
        "REQUEST_TIMEOUT": "request_timeout",
        "BACKUP_ENABLED": "backup_enabled",
    }

    for env_var, config_key in env_mappings.items():
        if env_var in os.environ:
            value = os.environ[env_var]

            # Type conversion
            if config_key in [
                "request_timeout",
                "max_retries",
                "retry_delay",
                "api_port",
                "max_backups",
            ]:
                try:
                    config[config_key] = int(value)
                except ValueError:
                    pass
            elif config_key in [
                "backup_enabled",
                "api_enabled",
                "log_to_file",
                "log_to_console",
            ]:
                config[config_key] = value.lower() in ["true", "1", "yes", "on"]
            elif config_key in [
                "min_latitude",
                "max_latitude",
                "min_longitude",
                "max_longitude",
            ]:
                try:
                    config[config_key] = float(value)
                except ValueError:
                    pass
            else:
                config[config_key] = value

    return config


def create_directories(config: Dict[str, Any]) -> None:
    """
    Create necessary directories based on configuration.

    Args:
        config: Configuration dictionary
    """
    directories = []

    # Output file directory
    output_path = Path(config["output_file"])
    if output_path.parent != Path("."):
        directories.append(output_path.parent)

    # Log file directory
    log_path = Path(config["log_file"])
    if log_path.parent != Path("."):
        directories.append(log_path.parent)

    # Backup directory
    if config["backup_enabled"]:
        directories.append(Path(config["backup_directory"]))

    # Create directories
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
