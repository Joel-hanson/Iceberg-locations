#!/usr/bin/env python3

from datetime import datetime

import requests
from bs4 import BeautifulSoup

print("Debugging scraper...")

scp_byu_html = requests.get(
    "https://www.scp.byu.edu/current_icebergs.html", verify=False
)
soup = BeautifulSoup(scp_byu_html.content, "lxml")

# Test date parsing
revised_date_str = soup.p.text[-17:]
print(f'Date string: "{revised_date_str}"')

try:
    revised_date = datetime.strptime(revised_date_str, "%H:%M:%S %m/%d/%y")
    print(f"Parsed date: {revised_date}")
    print(f'Formatted date: {revised_date.strftime("%m/%d/%y")}')
except Exception as e:
    print(f"Date parsing error: {e}")

# Test table parsing
print(f"\nTesting table parsing...")
table = soup.find("table")
if table:
    tables = table.find_all("table")
    print(f"Nested tables found: {len(tables)}")

    if len(tables) > 1:
        rows = tables[1].find_all("tr")
        print(f"Rows in second table: {len(rows)}")

        print("\nFirst few rows:")
        for i, row in enumerate(rows[:5]):
            cols = row.find_all("td")
            if cols:
                cols_text = [ele.text.strip() for ele in cols if ele.text.strip()]
                print(f"Row {i}: {cols_text[:6]}")  # First 6 non-empty cells
    else:
        print("No second table found")
else:
    print("No main table found")
