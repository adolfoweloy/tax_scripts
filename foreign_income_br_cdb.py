import csv
import os
import argparse
from exchange_service import DefaultExchangeRateService, LocalExchangeRateService
from model import RedemptionsReportService



def parse_arguments():
    parser = argparse.ArgumentParser(description='Process financial data from PDFs')
    parser.add_argument('directory', nargs='?', default="", help='Directory containing PDF files')
    parser.add_argument('--dry-run', action='store_true', help='Run without making external API calls')
    parser.add_argument('--output', type=str, default="output.csv", help='Output filename (default: output.csv)')
    parser.add_argument('--report', type=str, choices=['redemptions', 'previous_balance', 'investments'], 
                        default="redemptions", help='Report type to process (default: redemptions)')
    return parser.parse_args()



def main():
    args = parse_arguments()

    # Choose the exchange rate service based on dry run mode
    exchange_service = LocalExchangeRateService() if args.dry_run else DefaultExchangeRateService()

    csv_rows = []
    header = None

    # if a directory is given, then search for all pdfs within that directory
    # otherwise, read all pdfs within the current directory
    directory = args.directory
    pattern = os.path.join(directory, "*.pdf") if directory else "*.pdf"

    # iterate over all pdfs within the given path pattern
    report_service = RedemptionsReportService(exchange_service)
    csv_rows, header = report_service.process_report(pattern)

    # Generating the CSV report
    output_file = args.output
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        if header:
            writer.writerow(header)
        writer.writerows(csv_rows)

    print(f"CSV '{output_file}' created with {len(csv_rows)} lines.")




if __name__ == "__main__":
    main()