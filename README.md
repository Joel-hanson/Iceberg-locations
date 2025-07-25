# Antarctic Iceberg Tracker

A Python tool for tracking large icebergs in Antarctic waters using satellite data from NASA's Scatterometer Climate Record Pathfinder (SCP).

## Features

- **Real-time Data**: Scrapes latest iceberg positions from NASA SCP website
- **Location Tracking**: Precise latitude/longitude coordinates with DMS conversion
- **Interactive Map**: Generate beautiful web-based visualizations
- **Data Analysis**: Summary statistics and iceberg movement tracking
- **JSON Export**: Save data in structured format for further analysis
- **Simple CLI**: Easy-to-use command-line interface

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Joel-hanson/Iceberg-locations.git
cd Iceberg-locations

# Install dependencies
pip install -r requirement.txt
```

### Usage

```bash
# Collect latest iceberg data
python main.py scrape

# Show data summary
python main.py info

# Generate interactive map
python main.py map
```

## Commands

### `scrape` - Collect Data

Fetches the latest iceberg position data from NASA SCP website and saves it to `iceberg_location.json`.

```bash
python main.py scrape
```

### `info` - Data Summary

Displays statistics about the collected iceberg data including number of icebergs, observation dates, and data coverage.

```bash
python main.py info
```

**Example output:**

```
Antarctic Iceberg Data Summary:
   • 37 observation dates
   • 53 current icebergs
   • 97 unique icebergs tracked
   • 1,832 total records
   • Latest data: 11/11/21
```

### `map` - Interactive Visualization

Generates an interactive HTML map showing iceberg positions with clickable markers.

```bash
python main.py map
```

Opens `output/iceberg_map.html` in your browser with:

- Interactive Antarctica-focused map
- Clickable iceberg markers with details
- Real-time statistics display

## Project Structure

```
Iceberg-locations/
├── main.py                 # Main entry point
├── src/                    # Source code
│   ├── __init__.py         # Package initialization
│   ├── iceberg.py          # Core scraper script
│   ├── cli.py              # Command-line interface
│   ├── config.py           # Configuration settings
│   └── tests.py            # Test suite
├── data/                   # Data storage
│   └── iceberg_location.json  # Scraped data (generated)
├── output/                 # Generated outputs
│   └── iceberg_map.html    # Interactive map (generated)
├── docs/                   # Documentation
├── assets/                 # Static assets
├── requirement.txt         # Python dependencies
├── README.md               # This file
├── LICENSE                 # MIT License
├── .github/workflows/      # GitHub Actions
├── Dockerfile              # Docker container setup
├── Makefile                # Build automation
└── setup.py                # Package installation
```

## Data Source

Data is collected from the **NASA Scatterometer Climate Record Pathfinder (SCP)** database:

**Source:** <https://www.scp.byu.edu/data/ice_tracking/antarctic.html>

## Data Format

```json
{
  "11/11/21": [
    {
      "iceberg": "a23a",
      "latitude": -75.42,
      "longitude": -39.83,
      "dms_latitude": "75°25'S",
      "dms_longitude": "39°50'W",
      "recent_observation": "11/11/21"
    }
  ]
}
```

## Development

### Navigate to your project root

cd /Users/joelhanson/Desktop/Personal/Iceberg-locations

### Generate the map first

python main.py map

### Start a simple HTTP server

python -m http.server 8000
http://localhost:8000/output/iceberg_map.html

## License

MIT License - see [LICENSE](LICENSE) file for details.
