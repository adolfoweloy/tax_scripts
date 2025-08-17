import sys
import pdfplumber
import glob
import csv
import re
import time
import os
from datetime import datetime
import argparse
from exchange_service import ExchangeRateService, DefaultExchangeRateService, LocalExchangeRateService

def add_aud_forex(row, exchange_service: ExchangeRateService):
    payment_date = row[4]
    parsed_date = datetime.strptime(payment_date, "%d/%m/%Y").date()
    rate = exchange_service.get_rate("BRL", "AUD", parsed_date)
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

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process financial data from PDFs')
    parser.add_argument('directory', nargs='?', default="", help='Directory containing PDF files')
    parser.add_argument('--dry-run', action='store_true', help='Run without making external API calls')
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Choose the exchange rate service based on dry run mode
    exchange_service = LocalExchangeRateService() if args.dry_run else DefaultExchangeRateService()

    all_redemptions = []
    header = None

    # if a directory is given, then search for all pdfs within that directory
    # otherwise, read all pdfs within the current directory
    directory = args.directory
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
                    converted = add_aud_forex(converted, exchange_service)
                    all_redemptions.append(converted)

    # Generating the CSV report
    output_file = "redemptions.csv"
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        if header:
            writer.writerow(header)
        writer.writerows(all_redemptions)

    print(f"CSV '{output_file}' created with {len(all_redemptions)} lines.")

if __name__ == "__main__":
    main()