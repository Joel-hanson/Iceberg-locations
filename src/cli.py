#!/usr/bin/env python3
"""
Simple CLI for the Antarctic Iceberg Tracker.
"""

import argparse
import json
import os
import subprocess
import sys


def run_scraper():
    """Run the iceberg scraper."""
    print("Collecting latest iceberg data...")
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        iceberg_script = os.path.join(script_dir, "iceberg.py")

        result = subprocess.run(
            [sys.executable, iceberg_script], capture_output=True, text=True
        )

        print(result.stdout)
        if result.stderr:
            print(result.stderr)

        if result.returncode == 0:
            print("Data collection completed")
            return True
        else:
            print("Data collection failed")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def show_info():
    """Show information about the collected data."""
    # Look for data file in the data directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file = os.path.join(project_root, "data", "iceberg_location.json")

    if not os.path.exists(data_file):
        print("No data file found. Run 'python main.py scrape' first.")
        return False

    try:
        with open(data_file, "r") as f:
            data = json.load(f)

        total_dates = len(data)
        total_records = sum(len(icebergs) for icebergs in data.values())

        # Get latest date info (sort by actual date, not string)
        dates = sorted(data.keys()) if data else []
        try:
            from datetime import datetime

            dates_with_dt = [(d, datetime.strptime(d, "%m/%d/%y")) for d in dates]
            dates_with_dt.sort(key=lambda x: x[1])  # Sort by datetime
            latest_date = dates_with_dt[-1][0] if dates_with_dt else "Unknown"
        except:
            # Fallback to string sorting if date parsing fails
            latest_date = dates[-1] if dates else "Unknown"

        current_icebergs = len(data.get(latest_date, []))

        # Get unique icebergs
        unique_icebergs = set()
        for icebergs in data.values():
            for iceberg in icebergs:
                if iceberg.get("iceberg"):
                    unique_icebergs.add(iceberg["iceberg"])

        print("Antarctic Iceberg Data Summary:")
        print(f"   • {total_dates} data collection dates")
        print(f"   • {current_icebergs} current icebergs")
        print(f"   • {len(unique_icebergs)} unique icebergs tracked")
        print(f"   • {total_records:,} total records")
        print(f"   • Latest data collection: {latest_date}")

        # Show most recent iceberg observations
        if data.get(latest_date):
            recent_observations = []
            for iceberg in data[latest_date]:
                if iceberg.get("recent_observation"):
                    recent_observations.append(iceberg["recent_observation"])
            if recent_observations:
                most_recent_obs = sorted(set(recent_observations))[-1]
                print(f"   • Most recent iceberg observation: {most_recent_obs}")

        # Show data freshness note
        from datetime import datetime

        try:
            latest_dt = datetime.strptime(latest_date, "%m/%d/%y")
            today = datetime.now()
            days_old = (today - latest_dt).days
            if days_old == 0:
                print(f"   • Data status: Fresh (updated today)")
            elif days_old <= 7:
                print(f"   • Data status: Recent (updated {days_old} days ago)")
            else:
                print(f"   • Data status: Outdated (updated {days_old} days ago)")
                print(f"   • Note: NASA SCP updates 1-2x per week (Mon/Fri typically)")
        except:
            pass

        return True

    except Exception as e:
        print(f"Error reading data: {e}")
        return False


def get_animation_url(iceberg_name):
    """Get the animation URL for a specific iceberg."""
    from config import get_config

    config = get_config()
    base_url = config["animation_base_url"]

    # Convert iceberg name to lowercase for the filename
    filename = f"{iceberg_name.lower()}_movie.gif"
    return f"{base_url}{filename}"


def show_animations():
    """Show available animation URLs for current icebergs."""
    # Look for data file in the data directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file = os.path.join(project_root, "data", "iceberg_location.json")

    if not os.path.exists(data_file):
        print("No data file found. Run 'python main.py scrape' first.")
        return False

    try:
        with open(data_file, "r") as f:
            data = json.load(f)

        # Get latest date info (sort by actual date, not string)
        dates = sorted(data.keys()) if data else []
        try:
            from datetime import datetime

            dates_with_dt = [(d, datetime.strptime(d, "%m/%d/%y")) for d in dates]
            dates_with_dt.sort(key=lambda x: x[1])  # Sort by datetime
            latest_date = dates_with_dt[-1][0] if dates_with_dt else "Unknown"
        except:
            # Fallback to string sorting if date parsing fails
            latest_date = dates[-1] if dates else "Unknown"

        if not data.get(latest_date):
            print("No current iceberg data available.")
            return False

        print("Iceberg Movement Animations:")
        print(f"Data from: {latest_date}")
        print("Note: Animations show historical movement patterns from NASA SCP")
        print()

        # Show animation URLs for current icebergs
        current_icebergs = data[latest_date]
        for iceberg in current_icebergs:
            iceberg_name = iceberg.get("iceberg", "").strip()
            if iceberg_name:
                animation_url = get_animation_url(iceberg_name)
                lat = iceberg.get("dms_latitude", "N/A")
                lon = iceberg.get("dms_longitude", "N/A")
                coords = f"{lat}, {lon}"
                print(f"  {iceberg_name.upper():<8} | {coords:<20} | {animation_url}")

        print()
        print("Animation files show iceberg drift patterns over time.")
        print("Copy URLs to view GIF animations of iceberg movement.")

        return True

    except Exception as e:
        print(f"Error reading data: {e}")
        return False


def generate_map():
    """Generate a simple interactive map."""
    # Look for data file in the data directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file = os.path.join(project_root, "data", "iceberg_location.json")

    if not os.path.exists(data_file):
        print("No data file found. Run 'python main.py scrape' first.")
        return False

    print("Generating professional interactive map...")

    # Professional HTML map with shadcn/ui inspired design
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Antarctic Iceberg Tracker</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Bootstrap Icons -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
    <!-- Leaflet CSS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <!-- Inter Font for modern typography -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --background: 0 0% 100%;
            --foreground: 222.2 84% 4.9%;
            --card: 0 0% 100%;
            --card-foreground: 222.2 84% 4.9%;
            --popover: 0 0% 100%;
            --popover-foreground: 222.2 84% 4.9%;
            --primary: 222.2 47.4% 11.2%;
            --primary-foreground: 210 40% 98%;
            --secondary: 210 40% 96%;
            --secondary-foreground: 222.2 84% 4.9%;
            --muted: 210 40% 96%;
            --muted-foreground: 215.4 16.3% 46.9%;
            --accent: 210 40% 96%;
            --accent-foreground: 222.2 84% 4.9%;
            --destructive: 0 62.8% 30.6%;
            --destructive-foreground: 210 40% 98%;
            --border: 214.3 31.8% 91.4%;
            --input: 214.3 31.8% 91.4%;
            --ring: 222.2 47.4% 11.2%;
            --radius: 0.5rem;
        }
        
        * {
            border-color: hsl(var(--border));
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background-color: hsl(var(--background));
            color: hsl(var(--foreground));
            font-feature-settings: "rlig" 1, "calt" 1;
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        .shadcn-card {
            background: hsl(var(--card));
            border: 1px solid hsl(var(--border));
            border-radius: calc(var(--radius) + 2px);
            box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .shadcn-card:hover {
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        }
        
        .navbar {
            background: hsl(var(--background)) !important;
            border-bottom: 1px solid hsl(var(--border));
            backdrop-filter: blur(8px);
        }
        
        .navbar-brand {
            font-weight: 600;
            font-size: 1.5rem;
            color: hsl(var(--foreground)) !important;
        }
        
        #map { 
            height: calc(100vh - 120px);
            border-radius: var(--radius);
            border: 1px solid hsl(var(--border));
        }
        
        .stats-card {
            background: hsl(var(--primary));
            color: hsl(var(--primary-foreground));
            border: none;
            position: relative;
            overflow: hidden;
        }
        
        .stats-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
            pointer-events: none;
        }
        
        .control-section {
            padding: 1.5rem;
        }
        
        .control-section h6 {
            font-weight: 600;
            font-size: 0.875rem;
            color: hsl(var(--muted-foreground));
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 1rem;
        }
        
        .shadcn-button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            white-space: nowrap;
            border-radius: var(--radius);
            font-size: 0.875rem;
            font-weight: 500;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid hsl(var(--border));
            background: hsl(var(--background));
            color: hsl(var(--foreground));
            padding: 0.5rem 1rem;
            height: 2.5rem;
            text-decoration: none;
        }
        
        .shadcn-button:hover {
            background: hsl(var(--accent));
            color: hsl(var(--accent-foreground));
            border-color: hsl(var(--ring));
            transform: translateY(-1px);
            box-shadow: 0 4px 8px 0 rgb(0 0 0 / 0.12);
        }
        
        .shadcn-button:active {
            transform: translateY(0);
        }
        
        .shadcn-button-primary {
            background: hsl(var(--primary));
            color: hsl(var(--primary-foreground));
            border-color: hsl(var(--primary));
        }
        
        .shadcn-button-primary:hover {
            background: hsl(var(--primary));
            opacity: 0.9;
            color: hsl(var(--primary-foreground));
        }
        
        .status-indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
        }
        
        .status-fresh { background-color: hsl(120 100% 25%); }
        .status-recent { background-color: hsl(45 100% 35%); }
        .status-outdated { background-color: hsl(var(--destructive)); }
        
        .iceberg-series-a { background-color: hsl(var(--primary)); }
        .iceberg-series-b { background-color: hsl(215.4 16.3% 46.9%); }
        .iceberg-series-c { background-color: hsl(215.4 16.3% 36.9%); }
        .iceberg-series-d { background-color: hsl(215.4 16.3% 26.9%); }
        
        .form-check-input {
            border-color: hsl(var(--border));
        }
        
        .form-check-input:checked {
            background-color: hsl(var(--primary));
            border-color: hsl(var(--primary));
        }
        
        .form-check-label {
            font-size: 0.875rem;
            color: hsl(var(--foreground));
        }
        
        .loading-spinner {
            width: 20px;
            height: 20px;
            border: 2px solid hsl(var(--muted));
            border-top: 2px solid hsl(var(--primary));
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .leaflet-popup-content-wrapper {
            border-radius: var(--radius);
            border: 1px solid hsl(var(--border));
            box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
        }
        
        .iceberg-popup {
            font-family: 'Inter', sans-serif;
            padding: 0.5rem;
        }
        
        .iceberg-popup h6 {
            font-weight: 600;
            margin-bottom: 0.75rem;
            font-size: 1rem;
        }
        
        .popup-detail {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin: 0.5rem 0;
            font-size: 0.875rem;
            color: hsl(var(--muted-foreground));
        }
        
        .popup-detail strong {
            color: hsl(var(--foreground));
        }
        
        .popup-detail i {
            width: 16px;
            color: hsl(var(--muted-foreground));
        }
        
        .animation-btn {
            background: hsl(var(--primary));
            border: 1px solid hsl(var(--primary));
            color: hsl(var(--primary-foreground));
            padding: 0.375rem 0.75rem;
            border-radius: var(--radius);
            font-size: 0.75rem;
            font-weight: 500;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.375rem;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        }
        
        .animation-btn:hover {
            background: hsl(var(--primary));
            color: hsl(var(--primary-foreground));
            text-decoration: none;
            transform: translateY(-1px);
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
            opacity: 0.9;
        }
        
        .animation-btn:active {
            transform: translateY(0);
            box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        }
        
        .animation-unavailable {
            background: hsl(var(--muted));
            border: 1px solid hsl(var(--border));
            color: hsl(var(--muted-foreground));
            padding: 0.375rem 0.75rem;
            border-radius: var(--radius);
            font-size: 0.75rem;
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            gap: 0.375rem;
            cursor: not-allowed;
        }
        
        .badge {
            display: inline-flex;
            align-items: center;
            border-radius: calc(var(--radius) - 2px);
            padding: 0.25rem 0.75rem;
            font-size: 0.75rem;
            font-weight: 500;
            background: hsl(var(--secondary));
            color: hsl(var(--secondary-foreground));
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.5rem 0;
            font-size: 0.875rem;
        }
        
        .legend-color {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            flex-shrink: 0;
        }
        
        @media (max-width: 768px) {
            #map {
                height: calc(100vh - 200px);
            }
            
            .control-section {
                padding: 1rem;
            }
        }
        
        .leaflet-control-layers {
            border-radius: var(--radius);
            border: 1px solid hsl(var(--border));
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        }
        
        .data-metric {
            text-align: center;
            padding: 1rem 0;
        }
        
        .data-metric-value {
            font-size: 2rem;
            font-weight: 700;
            line-height: 1;
            margin-bottom: 0.25rem;
        }
        
        .data-metric-label {
            font-size: 0.875rem;
            color: hsl(var(--primary-foreground));
            opacity: 0.8;
        }
        
        .divider {
            height: 1px;
            background: rgba(255,255,255,0.1);
            margin: 1rem 0;
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg">
        <div class="container-fluid px-4">
            <a class="navbar-brand d-flex align-items-center gap-2" href="#">
                <i class="bi bi-snow3"></i>
                <span>Antarctic Iceberg Tracker</span>
            </a>
            <div class="d-flex align-items-center gap-2">
                <span class="badge">
                    <i class="bi bi-database me-1"></i>
                    Live Data
                </span>
            </div>
        </div>
    </nav>

    <div class="container-fluid p-4">
        <div class="row g-4">
            <!-- Sidebar -->
            <div class="col-xl-3 col-lg-4">
                <!-- Stats Card -->
                <div class="shadcn-card stats-card mb-4">
                    <div class="control-section">
                        <div class="data-metric">
                            <div id="stats-content">
                                <div class="d-flex justify-content-center">
                                    <div class="loading-spinner"></div>
                                </div>
                                <div class="data-metric-label mt-2">Loading data...</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Map Controls -->
                <div class="shadcn-card mb-4">
                    <div class="control-section">
                        <h6><i class="bi bi-sliders me-2"></i>Map Controls</h6>
                        <div class="d-grid gap-2">
                            <button class="shadcn-button" onclick="centerMap()">
                                <i class="bi bi-geo-alt me-2"></i>
                                Center Antarctica
                            </button>
                            <button class="shadcn-button" onclick="refreshData()">
                                <i class="bi bi-arrow-clockwise me-2"></i>
                                Refresh Data
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Display Options -->
                <div class="shadcn-card mb-4">
                    <div class="control-section">
                        <h6><i class="bi bi-eye me-2"></i>Display Options</h6>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="showLabels" checked>
                            <label class="form-check-label" for="showLabels">
                                Show iceberg names on hover
                            </label>
                        </div>
                    </div>
                </div>

                <!-- Legend -->
                <div class="shadcn-card">
                    <div class="control-section">
                        <h6><i class="bi bi-palette me-2"></i>Iceberg Series</h6>
                        <div class="legend-item">
                            <div class="legend-color iceberg-series-a"></div>
                            <div>
                                <div class="fw-medium">A-Series</div>
                                <div class="text-muted small">Weddell Sea region</div>
                            </div>
                        </div>
                        <div class="legend-item">
                            <div class="legend-color iceberg-series-b"></div>
                            <div>
                                <div class="fw-medium">B-Series</div>
                                <div class="text-muted small">90°W - 180° sector</div>
                            </div>
                        </div>
                        <div class="legend-item">
                            <div class="legend-color iceberg-series-c"></div>
                            <div>
                                <div class="fw-medium">C-Series</div>
                                <div class="text-muted small">90°E - 180° sector</div>
                            </div>
                        </div>
                        <div class="legend-item">
                            <div class="legend-color iceberg-series-d"></div>
                            <div>
                                <div class="fw-medium">D-Series</div>
                                <div class="text-muted small">0° - 90°E sector</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Map Container -->
            <div class="col-xl-9 col-lg-8">
                <div class="shadcn-card">
                    <div id="map"></div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <!-- Leaflet JS -->
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    
    <script>
        // Initialize map
        const map = L.map('map').setView([-70, 0], 3);
        
        // Add tile layer with better styling
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);
        
        // Add satellite layer as option
        const satellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            attribution: '© Esri'
        });
        
        // Layer control
        const baseMaps = {
            "Street Map": L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'),
            "Satellite": satellite
        };
        
        L.control.layers(baseMaps).addTo(map);
        
        // Variables for data management
        let icebergData = [];
        let markersGroup = L.layerGroup().addTo(map);
        let clustersEnabled = true;
        
        // Available animations (from NASA SCP FTP directory)
        const availableAnimations = [
            'a23a', 'a56', 'a57', 'a61', 'a62', 'a62a', 'a63', 'a64',
            'b09b', 'b09c', 'b09d', 'b09f', 'b09g', 'b15aa', 'b15ab', 'b15f', 'b15g',
            'b15j1', 'b15j', 'b15k', 'b15n', 'b15r', 'b15t', 'b15x', 'b15y', 'b15z',
            'b16', 'b17a', 'b21a', 'b22a', 'b27', 'b28', 'b29', 'b30', 'b31', 'b32',
            'c14a', 'c15', 'c16', 'c18b', 'c19c1', 'c19c', 'c21b', 'c24', 'c28a2', 'c28b',
            'd14', 'd15', 'd20', 'd20b', 'd21a', 'd21b', 'd22',
            'tk01', 'tk02', 'tk03', 'tk04', 'tk05', 'tk06', 'tk07', 'tk08', 'tk10',
            'tk12', 'tk13', 'tk16', 'tk17',
            'uk052', 'uk093', 'uk174', 'uk192', 'uk290', 'uk304', 'uk314', 'uk316',
            'uk318', 'uk319', 'uk320', 'uk321', 'uk321b', 'uk322'
        ];
        
        // Utility functions
        function getIcebergColor(iceberg) {
            const name = iceberg.iceberg.toLowerCase();
            if (name.startsWith('a')) return 'hsl(222.2 47.4% 11.2%)';      // Dark slate for A-series
            if (name.startsWith('b')) return 'hsl(215.4 16.3% 46.9%)';      // Medium gray for B-series  
            if (name.startsWith('c')) return 'hsl(215.4 16.3% 36.9%)';      // Darker gray for C-series
            if (name.startsWith('d')) return 'hsl(215.4 16.3% 26.9%)';      // Darkest gray for D-series
            return 'hsl(215.4 16.3% 56.9%)';                               // Light gray for others
        }
        
        function formatUserFriendlyDate(dateStr) {
            try {
                const [month, day, year] = dateStr.split('/');
                const date = new Date(2000 + parseInt(year), parseInt(month) - 1, parseInt(day));
                const monthNames = [
                    'January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December'
                ];
                return `${monthNames[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;
            } catch (e) {
                return dateStr; // fallback to original format
            }
        }
        
        function formatRelativeDate(dateStr) {
            try {
                const [month, day, year] = dateStr.split('/');
                const dataDate = new Date(2000 + parseInt(year), parseInt(month) - 1, parseInt(day));
                const today = new Date();
                const daysDiff = Math.floor((today - dataDate) / (1000 * 60 * 60 * 24));
                
                if (daysDiff === 0) return 'today';
                if (daysDiff === 1) return 'yesterday';
                if (daysDiff <= 7) return `${daysDiff} days ago`;
                if (daysDiff <= 30) return `${Math.floor(daysDiff / 7)} weeks ago`;
                if (daysDiff <= 365) return `${Math.floor(daysDiff / 30)} months ago`;
                return `${Math.floor(daysDiff / 365)} years ago`;
            } catch (e) {
                return 'unknown';
            }
        }
        
        function getDataFreshness(dateStr) {
            try {
                const [month, day, year] = dateStr.split('/');
                const dataDate = new Date(2000 + parseInt(year), parseInt(month) - 1, parseInt(day));
                const today = new Date();
                const daysDiff = Math.floor((today - dataDate) / (1000 * 60 * 60 * 24));
                const relativeDate = formatRelativeDate(dateStr);
                
                if (daysDiff === 0) return { status: 'fresh', indicator: 'status-fresh', text: `Updated ${relativeDate}` };
                if (daysDiff <= 7) return { status: 'recent', indicator: 'status-recent', text: `Updated ${relativeDate}` };
                return { status: 'outdated', indicator: 'status-outdated', text: `Updated ${relativeDate}` };
            } catch (e) {
                return { status: 'unknown', indicator: 'status-outdated', text: 'Update time unknown' };
            }
        }
        
        function createIcebergPopup(iceberg) {
            const color = getIcebergColor(iceberg);
            const observationDate = iceberg.recent_observation ? formatUserFriendlyDate(iceberg.recent_observation) : 'Unknown';
            const relativeObservation = iceberg.recent_observation ? formatRelativeDate(iceberg.recent_observation) : 'unknown';
            const animationUrl = `https://ftp.scp.byu.edu/data/misc/iceberg_animations/${iceberg.iceberg.toLowerCase()}_movie.gif`;
            
            // Check if animation is available
            const hasAnimation = availableAnimations.includes(iceberg.iceberg.toLowerCase());
            
            const animationSection = hasAnimation ? 
                `<a href="${animationUrl}" target="_blank" class="animation-btn">
                    <i class="bi bi-play-circle"></i>View Movement
                </a>
                <div class="small text-muted mt-1">Historical drift pattern</div>` :
                `<span class="animation-unavailable">
                    <i class="bi bi-x-circle"></i>No Animation Available
                </span>
                <div class="small text-muted mt-1">Animation not available</div>`;
            
            return `
                <div class="iceberg-popup">
                    <h6 style="color: ${color};" class="d-flex align-items-center gap-2">
                        <i class="bi bi-snow3"></i>
                        <span>${iceberg.iceberg.toUpperCase()}</span>
                    </h6>
                    <div class="popup-detail">
                        <i class="bi bi-geo-alt"></i> 
                        <div>
                            <strong>Position</strong><br>
                            <span>${parseFloat(iceberg.latitude || iceberg.lattitude).toFixed(3)}°, ${parseFloat(iceberg.longitude).toFixed(3)}°</span>
                        </div>
                    </div>
                    <div class="popup-detail">
                        <i class="bi bi-calendar3"></i> 
                        <div>
                            <strong>Last Observed</strong><br>
                            <span>${observationDate}</span>
                            <div class="small text-muted">${relativeObservation}</div>
                        </div>
                    </div>
                    <div class="popup-detail">
                        <i class="bi bi-compass"></i> 
                        <div>
                            <strong>Coordinates (DMS)</strong><br>
                            <span class="small text-muted">${iceberg.dms_lattitude}, ${iceberg.dms_longitude}</span>
                        </div>
                    </div>
                    <div class="popup-detail">
                        <i class="bi bi-camera-reels"></i> 
                        <div>
                            <strong>Movement Animation</strong><br>
                            ${animationSection}
                        </div>
                    </div>
                </div>
            `;
        }
        
        // Map control functions
        function centerMap() {
            map.setView([-70, 0], 3);
        }
        
        function refreshData() {
            document.getElementById('stats-content').innerHTML = `
                <div class="d-flex justify-content-center">
                    <div class="loading-spinner"></div>
                </div>
                <div class="data-metric-label mt-2">Refreshing data...</div>
            `;
            setTimeout(() => loadIcebergData(), 500);
        }
        
        // Main data loading function
        function loadIcebergData() {
            fetch('../data/iceberg_location.json')
                .then(response => response.json())
                .then(data => {
                    // Get latest date by parsing dates properly
                    const dates = Object.keys(data);
                    const dateObjects = dates.map(d => {
                        const [month, day, year] = d.split('/');
                        return {
                            str: d,
                            date: new Date(2000 + parseInt(year), parseInt(month) - 1, parseInt(day))
                        };
                    });
                    dateObjects.sort((a, b) => b.date - a.date);
                    
                    const latestDate = dateObjects[0].str;
                    const icebergs = data[latestDate] || [];
                    icebergData = icebergs;
                    
                    // Update stats with modern design
                    const freshness = getDataFreshness(latestDate);
                    const friendlyDate = formatUserFriendlyDate(latestDate);
                    
                    document.getElementById('stats-content').innerHTML = `
                        <div class="data-metric-value">${icebergs.length}</div>
                        <div class="data-metric-label">Active Icebergs</div>
                        <div class="divider"></div>
                        <div class="small d-flex align-items-center justify-content-center gap-2">
                            <i class="bi bi-calendar-check"></i>
                            <span>Data from ${friendlyDate}</span>
                        </div>
                        <div class="small d-flex align-items-center justify-content-center gap-1 mt-2">
                            <span class="status-indicator ${freshness.indicator}"></span>
                            <span>${freshness.text}</span>
                        </div>
                    `;
                    
                    // Clear existing markers
                    markersGroup.clearLayers();
                    
                    // Add icebergs to map
                    icebergs.forEach(iceberg => {
                        const lat = parseFloat(iceberg.latitude || iceberg.lattitude);
                        const lon = parseFloat(iceberg.longitude);
                        
                        if (lat && lon) {
                            let latitude = lat;
                            let longitude = lon;
                            
                            // Convert DMS format stored as decimal to actual decimal degrees
                            // The data comes in formats like:
                            // -7545.0 = 75°45'S = -75.75°
                            // -679.0 = 67°09'S = -67.15° (this was the bug!)
                            
                            // For latitude: always convert if it looks like DMS format
                            const absLat = Math.abs(latitude);
                            if (absLat >= 100) { // Any value >= 100 is likely in DMS format
                                let degrees, minutes;
                                if (absLat >= 1000) {
                                    // Format: DDMM.0 (e.g., 7545 = 75°45')
                                    degrees = Math.floor(absLat / 100);
                                    minutes = absLat % 100;
                                } else {
                                    // Format: DMM.0 (e.g., 679 = 67°09')
                                    const latStr = Math.floor(absLat).toString().padStart(3, '0');
                                    degrees = parseInt(latStr.substring(0, 2));
                                    minutes = parseInt(latStr.substring(2));
                                }
                                latitude = degrees + (minutes / 60);
                                if (lat < 0) latitude = -latitude;
                            }
                            
                            // For longitude: always convert if it looks like DMS format
                            const absLon = Math.abs(longitude);
                            if (absLon >= 100) { // Any value >= 100 is likely in DMS format
                                let degrees, minutes;
                                if (absLon >= 10000) {
                                    // Format: DDDMM.0 (e.g., 14917 = 149°17')
                                    degrees = Math.floor(absLon / 100);
                                    minutes = absLon % 100;
                                } else if (absLon >= 1000) {
                                    // Format: DDMM.0 (e.g., 7817 = 78°17')
                                    degrees = Math.floor(absLon / 100);
                                    minutes = absLon % 100;
                                } else {
                                    // Format: DMM.0 (e.g., 679 would be 67°09' if it were longitude)
                                    const lonStr = Math.floor(absLon).toString().padStart(3, '0');
                                    degrees = parseInt(lonStr.substring(0, 2));
                                    minutes = parseInt(lonStr.substring(2));
                                }
                                longitude = degrees + (minutes / 60);
                                if (lon < 0) longitude = -longitude;
                            }
                            
                            // Validate final coordinates
                            if (Math.abs(latitude) <= 90 && Math.abs(longitude) <= 180) {
                                const color = getIcebergColor(iceberg);
                                
                                const marker = L.circleMarker([latitude, longitude], {
                                    radius: 8,
                                    fillColor: color,
                                    color: 'white',
                                    weight: 2,
                                    fillOpacity: 0.9,
                                    className: 'iceberg-marker'
                                });
                                
                                marker.bindPopup(createIcebergPopup({
                                    ...iceberg,
                                    latitude: latitude,
                                    longitude: longitude
                                }));
                                
                                // Add tooltip with iceberg name
                                if (document.getElementById('showLabels').checked) {
                                    marker.bindTooltip(iceberg.iceberg.toUpperCase(), {
                                        permanent: false,
                                        direction: 'top',
                                        className: 'iceberg-tooltip'
                                    });
                                }
                                
                                markersGroup.addLayer(marker);
                            }
                        }
                    });
                })
                .catch(error => {
                    console.error('Error loading data:', error);
                    document.getElementById('stats-content').innerHTML = `
                        <div class="d-flex align-items-center justify-content-center gap-2 text-danger">
                            <i class="bi bi-exclamation-triangle"></i>
                            <span class="small">Failed to load data</span>
                        </div>
                    `;
                });
        }
        
        // Event listeners
        document.getElementById('showLabels').addEventListener('change', loadIcebergData);
        
        // Initialize
        loadIcebergData();
        
        // Auto-refresh every 5 minutes
        setInterval(() => {
            console.log('Auto-refreshing data...');
            loadIcebergData();
        }, 300000);
    </script>
</body>
</html>"""

    try:
        output_file = os.path.join(project_root, "output", "iceberg_map.html")
        with open(output_file, "w") as f:
            f.write(html_content)

        print(f"Interactive map generated: {output_file}")
        print("Open output/iceberg_map.html in your browser to view the map")
        return True

    except Exception as e:
        print(f"Error generating map: {e}")
        return False


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
        """.strip(),
    )

    parser.add_argument(
        "command",
        choices=["scrape", "info", "map", "animations"],
        help="Command to execute",
    )

    args = parser.parse_args()

    if args.command == "scrape":
        return 0 if run_scraper() else 1
    elif args.command == "info":
        return 0 if show_info() else 1
    elif args.command == "map":
        return 0 if generate_map() else 1
    elif args.command == "animations":
        return 0 if show_animations() else 1


if __name__ == "__main__":
    sys.exit(main())
