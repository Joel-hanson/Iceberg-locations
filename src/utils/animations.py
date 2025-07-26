"""
Animation utilities for the Antarctic Iceberg Tracker.
"""

from config import get_config

from .data_handler import get_latest_date, load_iceberg_data


def get_animation_url(iceberg_name):
    """Get the animation URL for a specific iceberg."""
    config = get_config()
    base_url = config["animation_base_url"]

    # Convert iceberg name to lowercase for the filename
    filename = f"{iceberg_name.lower()}_movie.gif"
    return f"{base_url}{filename}"


def show_animations():
    """Show available animation URLs for current icebergs."""
    data, error = load_iceberg_data()
    if error or data is None:
        print(error or "Failed to load data")
        return False

    try:
        latest_date = get_latest_date(data)

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
