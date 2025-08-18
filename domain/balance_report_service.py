from datetime import datetime

from pdfplumber.page import Page
import number_utils
from service.exchange_service import ExchangeRateService
from .model import ReportService
import re
import pdf_utils.tables as pdf_tables

class BalanceReportService(ReportService):
    def __init__(self, exchange_service: ExchangeRateService):
        self.exchange_service = exchange_service

    def extract_header(self, pages: list[Page]):
        first_page = pages[0]
        tables = first_page.extract_tables()
        balance_table = tables[1]  # 2nd table for the CDI report

        header = balance_table[0]
        header.append("Balance Date")
        header.append("BRLAUD Rate")
        return header

    def process(self, pages: list[Page]):
        result = []
        page_number = 0

        page = pages[page_number]
        tables = page.extract_tables()

        # processing previous balance date
        previous_balance_date = self._extract_balance_date(page, r"Saldo Anterior em (\d{2}/\d{2}/\d{4})")
        exchange_rate_previous_balance = self._br_to_aud_forex(previous_balance_date)
        
        balance_table = tables[1]  # 2nd table for the CDI report

        for row in balance_table[1:-1]:
            converted = [number_utils.continental_to_english(cell) for cell in row]
            # ignoring empty lines
            if len(row[0]) > 0:
                converted.append(previous_balance_date)
                converted.append(exchange_rate_previous_balance)
                result.append(converted)
        
        # processing current balance date searching across pages
        current_balance_date, balance_table = pdf_tables.extract_current_balance_data(pages)
        exchange_rate_current_balance = self._br_to_aud_forex(current_balance_date)
        
        for row in balance_table[1:]:
            if row[0] == "Total":
                break

            if len(row) == 12: # it has "renda no mes"
                row = row[:-1]

            converted = [number_utils.continental_to_english(cell) for cell in row]
            # ignoring empty lines
            if len(row[0]) > 0:
                converted.append(current_balance_date)
                converted.append(exchange_rate_current_balance)
                result.append(converted)

        return result
    

    def _extract_balance_date(self, page, pattern: re.Pattern) -> str | None:
        balance_date = None
        text = page.extract_text()
        match = re.search(pattern, text)
        if match:
            balance_date = match.group(1)
        return balance_date
    

    def _br_to_aud_forex(self, rate_on_date):
        payment_date = rate_on_date
        parsed_date = datetime.strptime(payment_date, "%d/%m/%Y").date()
        return self.exchange_service.get_rate("BRL", "AUD", parsed_date)