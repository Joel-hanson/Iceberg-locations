# -*- coding: utf-8 -*-
import json
import os
import re
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup


def get_update_datetime(days, revised_date):
    revised_year = revised_date.year
    if days > revised_date.timetuple().tm_yday:
        revised_year = revised_year - 1
    date = datetime(revised_year, 1, 1) + timedelta(days - 1)
    return date.strftime("%m/%d/%y")


def dms2dec(dms_str):
    """Return decimal representation of DMS

    >>> dms2dec(utf8(48°53'10.18"N))
    48.8866111111F

    >>> dms2dec(utf8(2°20'35.09"E))
    2.34330555556F

    >>> dms2dec(utf8(48°53'10.18"S))
    -48.8866111111F

    >>> dms2dec(utf8(2°20'35.09"W))
    -2.34330555556F

    """

    dms_str = re.sub(r"\s", "", dms_str)

    sign = -1 if re.search("[swSW]", dms_str) else 1

    numbers = list(filter(len, re.split(r"\D+", dms_str, maxsplit=4)))

    degree = numbers[0]
    minute = numbers[1] if len(numbers) >= 2 else "0"
    second = numbers[2] if len(numbers) >= 3 else "0"
    frac_seconds = numbers[3] if len(numbers) >= 4 else "0"

    second += "." + frac_seconds
    return sign * (int(degree) + float(minute) / 60 + float(second) / 3600)


def read_current_iceberg_location():
    """
    Reads the webpage and remove unwanted tags
    """
    print("Fetching iceberg data from NASA SCP website...")
    scp_byu_html = requests.get(
        "https://www.scp.byu.edu/current_icebergs.html", verify=False
    )

    print(f"📡 Response status: {scp_byu_html.status_code}")
    soup = BeautifulSoup(scp_byu_html.content, "lxml")

    # Find the paragraph with the revision date
    print("Looking for revision date...")
    p_tags = soup.find_all("p")
    revised_date_str = None
    for p in p_tags:
        if p.text and "Last revised:" in p.text:
            revised_date_str = p.text[-17:]
            print(f"📅 Found revision date: {revised_date_str}")
            break

    if not revised_date_str:
        print("Could not find revision date")
        return [], None

    revised_date = datetime.strptime(revised_date_str, "%H:%M:%S %m/%d/%y")

    print("Looking for iceberg data table...")
    data = []

    # Find all tables and look for the one with iceberg data
    tables = soup.find_all("table")
    print(f"Found {len(tables)} tables")

    iceberg_table = None
    for i, table in enumerate(tables):
        rows = table.find_all("tr")
        if rows:
            # Check if this table has iceberg data by looking for expected headers
            first_row_cells = rows[0].find_all("td")
            if first_row_cells and len(first_row_cells) >= 4:
                first_cell_text = first_row_cells[0].get_text().strip().lower()
                if "iceberg" in first_cell_text:
                    iceberg_table = table
                    print(f"🎯 Found iceberg table at index {i}")
                    break

    if not iceberg_table:
        print("Could not find iceberg data table")
        return [], revised_date

    rows = iceberg_table.find_all("tr")
    print(f"📋 Found {len(rows)} rows in iceberg table")

    for i, row in enumerate(rows):
        cols = row.find_all("td")
        if cols and len(cols) >= 4:
            cols_text = [ele.get_text().strip() for ele in cols]
            # Skip header row
            if i == 0 and "iceberg" in cols_text[0].lower():
                continue
            data.append([ele for ele in cols_text if ele])  # Get rid of empty values

    print(f"Extracted {len(data)} iceberg records")
    return data, revised_date


def get_iceberg_details(location_data, revised_date):
    """
    The formatted location data is returned with last updated data
    """
    result = []
    for index, row in enumerate(location_data):
        if index == 0:
            continue

        observation_date = 0
        if len(row) >= 4:
            observation_date = int(row[3])

        result.append(
            {
                "iceberg": row[0],
                "dms_longitude": row[1],
                "dms_lattitude": row[2],
                "longitude": dms2dec(row[1]),
                "lattitude": dms2dec(row[2]),
                "recent_observation": get_update_datetime(
                    observation_date, revised_date
                ),
            }
        )
    return result


def save_data_as_file(location_details, revised_date):
    """
    Save iceberg location data to JSON file.

    Data structure explanation:
    - Top-level keys: Data collection dates (when webpage was scraped)
    - Each entry contains list of icebergs with 'recent_observation' field
    - 'recent_observation': Actual satellite observation date for each iceberg

    Example: {"02/12/21": [{"iceberg": "a23a", "recent_observation": "02/09/21", ...}]}
    """
    formatted_date = revised_date.strftime("%m/%d/%y")
    print(f"Saving {len(location_details)} icebergs for date {formatted_date}")

    # Save data to the data directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_file = os.path.join(project_root, "data", "iceberg_location.json")
    print(f"📁 Data file path: {data_file}")

    with open(data_file, "r+" if os.path.exists(data_file) else "w") as fp:
        current_location_details = fp.read()
        if current_location_details:
            current_location_details = json.loads(current_location_details)
            current_location_details[formatted_date] = location_details
        else:
            current_location_details = {formatted_date: location_details}
        json_location_details = json.dumps(current_location_details, indent=2)
        fp.seek(0)
        fp.truncate(0)
        fp.write(json_location_details)
        fp.close()

    print(f"Data saved successfully to {data_file}")


def collect_iceberg_data():
    """Main function to collect and save iceberg data.

    Returns:
        bool: True if successful, False otherwise
    """
    print("Starting iceberg data collection...")
    try:
        current_location_data, revised_date = read_current_iceberg_location()

        if revised_date and current_location_data:
            detailed_location_details = get_iceberg_details(
                current_location_data, revised_date
            )
            save_data_as_file(detailed_location_details, revised_date)
            print(
                f"Collection complete! Found {len(detailed_location_details)} icebergs"
            )
            return True
        else:
            print("Failed to collect iceberg data")
            return False
    except Exception as e:
        print(f"Error during data collection: {e}")
        return False


if __name__ == "__main__":
    # Only run when called as a script, not when imported
    collect_iceberg_data()
