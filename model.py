
from abc import ABC, abstractmethod 
from datetime import date
import pdfplumber
import glob
from exchange_service import ExchangeRateService
from datetime import datetime
import number_utils
import time

class ReportService(ABC):
    # template method for processing reports in CDB reports
    def process_report(self, pattern: str):
        all_rows = []
        header = None
    
        for filepath in glob.glob(pattern):
            print(f"Processing {filepath}")
            with pdfplumber.open(filepath) as pdf:
                ## extract header from table being processed
                if header is None:
                    header = self.extract_header(pdf.pages)

                ## extracts rows from the table being processed
                rows = self.process(pdf.pages)
                all_rows.extend(rows)
        
        return all_rows, header

    
    @abstractmethod
    def extract_header(self, pages):
        pass

    # each report implementation must define its own process method
    @abstractmethod
    def process(self, pages):
        pass





class RedemptionsReportService(ReportService):
    def __init__(self, exchange_service: ExchangeRateService):
        self.exchange_service = exchange_service

    def extract_header(self, pages):
        first_page = pages[0]
        tables = first_page.extract_tables()
        redemptions = tables[3]  # 4th table for the CDI report
        header = []
        header = redemptions[0]
        header.append("BRLAUD Rate")
        return header

    def process(self, pages):
        result = []

        page = pages[0]
        tables = page.extract_tables()
        redemptions = tables[3]  # 4th table for the CDI report

        for row in redemptions[1:-1]:
            time.sleep(1) # sleep added to avoid being throttled by exchangerate host
            converted = [number_utils.continental_to_english(cell) for cell in row]
            # ignoring empty lines
            if len(row[0]) > 0:
                exchange_rate = self._add_aud_forex(converted[4])
                converted.append(exchange_rate)
                result.append(converted)
        
        return result


    def _add_aud_forex(self, rate_on_date):
        payment_date = rate_on_date
        parsed_date = datetime.strptime(payment_date, "%d/%m/%Y").date()
        return self.exchange_service.get_rate("BRL", "AUD", parsed_date)