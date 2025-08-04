import sys
import pdfplumber
import glob
import csv
import re
import requests
from datetime import datetime, date
import time
import os

def parse_date_with_format(date_str: str, fmt: str) -> date:
    # returns date object after parsing date string
    return datetime.strptime(date_str, fmt).date()

def fetch_rate_brl_to_aud(on_date: date) -> float:
    # fetches the exchange rate for BRL to AUD on a given date
    url = "https://api.exchangerate.host/historical"
    access_key = os.getenv("EXCHANGE_RATE_HOST_API_ACCESS_KEY")
    resp = requests.get(url, params={
        "date": on_date.isoformat(),
        "source": "BRL", 
        "currencies": "AUD", 
        "access_key": access_key})
    resp.raise_for_status()
    return resp.json()["quotes"]["BRLAUD"]

def add_aud_forex(row):
    payment_date = row[4]
    parsed_date = parse_date_with_format(payment_date, "%d/%m/%Y")
    rate = fetch_rate_brl_to_aud(parsed_date)
    row.append(rate)
    return row

def br_to_us(cell):
    """
    Convert numeric strings from Brazilian format to US
    e.g. "1.234,56 to 1,234.56
    """
    cell = cell.strip()
    if re.fullmatch(r'[\d\.\,]+', cell):
        return cell.replace('.', '').replace(',', '.')
    return cell

all_redemptions = []
header = None

# if a directory is given, then search for all pdfs within that directory
# otherwise, read all pdfs within the current directory
directory = sys.argv[1] if len(sys.argv) > 1 else ""
pattern = os.path.join(directory, "*.pdf") if directory else "*.pdf"

# iterate over all pdfs within the given path pattern 
for filepath in glob.glob(pattern):
    print(f"Processing {filepath}")
    with pdfplumber.open(filepath) as pdf:
        page = pdf.pages[0]
        tables = page.extract_tables()
        redemptions = tables[3]  # 4th table for the CDI report
        # Capturing the header only once
        if header is None:
            header = redemptions[0]
        # Processing each line in the table
        for row in redemptions[1:-1]:
            time.sleep(1) # sleep added to avoid being throttled by exchangerate host
            converted = [br_to_us(cell) for cell in row]
            # ignoring empty lines
            if len(row[0]) > 0:
                converted = add_aud_forex(converted)
                all_redemptions.append(converted)

# Generating the CSV report
output_file = "redemptions.csv"
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    if header:
        writer.writerow(header)
    writer.writerows(all_redemptions)

print(f"CSV '{output_file}' created with {len(all_redemptions)} lines.")

