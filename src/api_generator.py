import json
import os
from datetime import datetime


def create_api_endpoints():
    """Create simplified API endpoints for external access"""

    # Load the main data file
    data_file = "data/iceberg_location.json"
    if not os.path.exists(data_file):
        print("No data file found")
        return

    with open(data_file, "r") as f:
        iceberg_data = json.load(f)

    # Create API directory
    os.makedirs("api", exist_ok=True)

    # 1. Latest data endpoint (most recent date)
    if iceberg_data:
        latest_date = max(iceberg_data.keys())
        latest_data = {
            "last_updated": latest_date,
            "total_icebergs": len(iceberg_data[latest_date]),
            "icebergs": iceberg_data[latest_date],
        }

        with open("api/latest.json", "w") as f:
            json.dump(latest_data, f, indent=2)

    # 2. Summary statistics
    total_records = sum(len(records) for records in iceberg_data.values())
    unique_icebergs = set()
    for records in iceberg_data.values():
        for record in records:
            unique_icebergs.add(record.get("iceberg", ""))

    summary = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "total_observation_dates": len(iceberg_data),
        "total_records": total_records,
        "unique_icebergs": len(unique_icebergs),
        "date_range": {
            "earliest": min(iceberg_data.keys()) if iceberg_data else None,
            "latest": max(iceberg_data.keys()) if iceberg_data else None,
        },
        "sample_icebergs": list(unique_icebergs)[:10],  # First 10 for preview
    }

    with open("api/summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    # 3. JSONP wrapper for CORS compatibility
    latest_jsonp = f"window.icebergDataCallback({json.dumps(latest_data, indent=2)});"
    with open("api/latest.jsonp", "w") as f:
        f.write(latest_jsonp)

    # 4. Lightweight data for web integration (last 30 days only)
    recent_dates = (
        sorted(iceberg_data.keys())[-30:]
        if len(iceberg_data) > 30
        else sorted(iceberg_data.keys())
    )
    lightweight_data = {date: iceberg_data[date] for date in recent_dates}

    with open("api/recent.json", "w") as f:
        json.dump(lightweight_data, f, indent=2)

    print("API endpoints created:")
    print("  - api/latest.json (most recent iceberg data)")
    print("  - api/summary.json (statistics and overview)")
    print("  - api/latest.jsonp (CORS-friendly version)")
    print("  - api/recent.json (last 30 days of data)")
    print(f"  - Total unique icebergs: {len(unique_icebergs)}")
    print(f"  - Total records: {total_records}")


if __name__ == "__main__":
    create_api_endpoints()
