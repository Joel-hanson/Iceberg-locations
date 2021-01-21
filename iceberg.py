# -*- coding: utf-8 -*-
import requests
import re
import json

from bs4 import BeautifulSoup
from datetime import datetime, timedelta


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
    
    dms_str = re.sub(r'\s', '', dms_str)
    
    sign = -1 if re.search('[swSW]', dms_str) else 1
    
    numbers = list(filter(len, re.split('\D+', dms_str, maxsplit=4)))

    degree = numbers[0]
    minute = numbers[1] if len(numbers) >= 2 else '0'
    second = numbers[2] if len(numbers) >= 3 else '0'
    frac_seconds = numbers[3] if len(numbers) >= 4 else '0'
    
    second += "." + frac_seconds
    return sign * (int(degree) + float(minute) / 60 + float(second) / 3600)


def read_current_iceberg_location():
    """
    Reads the webpage and remove unwanted tags
    """
    scp_byu_html = requests.get("https://www.scp.byu.edu/current_icebergs.html")

    soup = BeautifulSoup(scp_byu_html.content, 'lxml')

    revised_date_str = soup.p.text[-17:]
    revised_date = datetime.strptime(revised_date_str, "%H:%M:%S %m/%d/%y")

    data = []
    rows = []
    tables = soup.table.find_all('table')
    if len(tables) > 0:
        rows = tables[1].table.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values

    return data, revised_date


def get_iceberg_details(location_data, revised_date):
    """
    The formatted location data is returned with last updated data
    """
    result = []
    for index, row in enumerate(location_data):
        if index == 0:
            continue
        result.append({
            "iceberg": row[0],
            "dms_longitude": row[1],
            "dms_lattitude": row[2],
            "longitude": dms2dec(row[1]),
            "lattitude": dms2dec(row[2]),
            "recent_observation": get_update_datetime(int(row[3]), revised_date),
        })
    return result


def save_data_as_file(location_details, revised_date):
    formatted_date = revised_date.strftime("%m/%d/%y")
    with open("iceberg_location.json", 'r+') as fp:
        current_location_details = fp.read()
        if current_location_details:
            current_location_details = json.loads(current_location_details)
            current_location_details[formatted_date] = location_details
        else:
            current_location_details = {
                formatted_date: location_details
            }
        json_location_details = json.dumps(current_location_details)
        fp.seek(0)
        fp.truncate(0)
        fp.write(json_location_details)
        fp.close()


current_location_data, revised_date = read_current_iceberg_location()
detailed_location_details = get_iceberg_details(current_location_data, revised_date)
save_data_as_file(detailed_location_details, revised_date)
