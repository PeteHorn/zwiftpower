from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
import os
import csv
import logging
from pathlib import Path
 
def write(path, data):
    header = [
        "date", 
        "weight", 
        "zftp", 
        "zftp_wkg", 
        "racing_score",
        "15s_w", 
        "1m_w", 
        "5m_w", 
        "20m_w",
        "15s_wkg", 
        "1m_wkg", 
        "5m_wkg", 
        "20m_wkg"
    ]

    path = Path(path)
    existing_dates = set()

    # Check if file exists and read existing dates
    if path.exists():
        with path.open("r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if "date" in row:
                    existing_dates.add(row["date"])

    # Skip writing if date already exists
    if data["date"] in existing_dates:
        logging.info(f"⚠️ Duplicate date '{data['date']}' found. Skipping write.")
        return

    # Validate fields
    missing_keys = set(header) - set(data)
    if missing_keys:
        raise ValueError(f"Missing fields in data: {missing_keys}")

    # Append data
    file_exists = path.exists()
    with path.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

    logging.info(f"📁 Data written to {path}")