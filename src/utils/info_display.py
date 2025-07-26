"""
Data information display utilities for the Antarctic Iceberg Tracker.
"""

from .data_handler import (
    get_data_freshness,
    get_latest_date,
    get_unique_icebergs,
    load_iceberg_data,
)


def show_info():
    """Show information about the collected data."""
    data, error = load_iceberg_data()
    if error or data is None:
        print(error or "Failed to load data")
        return False

    try:
        total_dates = len(data)
        total_records = sum(len(icebergs) for icebergs in data.values())

        latest_date = get_latest_date(data)
        current_icebergs = len(data.get(latest_date, []))
        unique_icebergs = get_unique_icebergs(data)

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
        freshness_status = get_data_freshness(latest_date)
        print(f"   • Data status: {freshness_status}")
        if "Outdated" in freshness_status:
            print(f"   • Note: NASA SCP updates 1-2x per week (Mon/Fri typically)")

        return True

    except Exception as e:
        print(f"Error reading data: {e}")
        return False
