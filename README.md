# Antarctic Iceberg Tracker

A Python tool for tracking large icebergs in Antarctic waters using satellite data from NASA's Scatterometer Climate Record Pathfinder (SCP).

## Features

- **Real-time Data**: Scrapes latest iceberg positions from NASA SCP website
- **Location Tracking**: Precise latitude/longitude coordinates with DMS conversion
- **Interactive Map**: Generate beautiful web-based visualizations with movement animations
- **GitHub Pages Deployment**: Automatically deploy to a live website
- **Data Analysis**: Summary statistics and iceberg movement tracking
- **JSON Export**: Save data in structured format for further analysis
- **Simple CLI**: Easy-to-use command-line interface

## Live Demo

🌐 **View the live Antarctic Iceberg Tracker**: [https://joel-hanson.github.io/Iceberg-locations/](https://joel-hanson.github.io/Iceberg-locations/)

The live site is automatically updated daily with the latest iceberg data and includes interactive features.

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

# View iceberg movement animations
python main.py animations
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
- **Movement animation links** in each popup
- Real-time statistics display

### `animations` - Movement Animations

Shows URLs to animated GIF files demonstrating historical iceberg movement patterns.

```bash
python main.py animations
```

**Example output:**

```
Iceberg Movement Animations:
Data from: 07/02/25
Note: Animations show historical movement patterns from NASA SCP

  A23A     | N/A, 39 7'W          | https://ftp.scp.byu.edu/data/misc/iceberg_animations/a23a_movie.gif
  C18B     | N/A, 78 17'E         | https://ftp.scp.byu.edu/data/misc/iceberg_animations/c18b_movie.gif
```

Copy the URLs to view GIF animations showing iceberg drift patterns over time.

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

**Current Data:** <https://www.scp.byu.edu/data/ice_tracking/antarctic.html>
**Movement Animations:** <https://ftp.scp.byu.edu/data/misc/iceberg_animations/>

The animation files show historical movement patterns of icebergs over time, providing valuable insights into iceberg drift patterns in Antarctic waters.

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

## Deployment to GitHub Pages

This project supports automatic deployment to GitHub Pages for a live, publicly accessible website.

### Quick Setup

1. **Enable GitHub Pages**: Go to repository Settings → Pages → Source: "GitHub Actions"
2. **Automatic Deployment**: The workflow runs daily and deploys updates automatically
3. **Manual Deployment**: Use the "Deploy to GitHub Pages" workflow in the Actions tab

Your site will be available at: `https://joel-hanson.github.io/Iceberg-locations/`

### Features of the Deployed Site

- **Real-time Updates**: Automatically refreshed daily at 6:00 AM UTC
- **Interactive Map**: Full-featured map with clickable iceberg markers
- **Movement Animations**: Direct links to NASA animation GIFs in popups
- **Mobile Responsive**: Works perfectly on all devices
- **Professional Design**: Clean, modern interface with Bootstrap

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## Development

### Local Development Server

```bash
# Navigate to your project root
cd /Users/joelhanson/Desktop/Personal/Iceberg-locations

# Generate the map first
python main.py map

# Start a simple HTTP server

python -m http.server 8000
http://localhost:8000/output/iceberg_map.html

## License

MIT License - see [LICENSE](LICENSE) file for details.
```
