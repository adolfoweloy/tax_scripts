from datetime import datetime
import time
import number_utils
from service.exchange_service import ExchangeRateService
from .model import ReportService
import re

class BalanceReportService(ReportService):
    def __init__(self, exchange_service: ExchangeRateService):
        self.exchange_service = exchange_service

    def extract_header(self, pages):
        first_page = pages[0]
        tables = first_page.extract_tables()
        balance_table = tables[1]  # 2nd table for the CDI report

        header = balance_table[0]
        header.append("Previous Balance Date")
        header.append("BRLAUD Rate")
        return header

    def process(self, pages):
        result = []

        page = pages[0]
        tables = page.extract_tables()

        previous_balance_date = self._extract_balance_date(page)
        exchange_rate = self._br_to_aud_forex(previous_balance_date)

        balance_table = tables[1]  # 2nd table for the CDI report

        for row in balance_table[1:-1]:
            time.sleep(1) # sleep added to avoid being throttled by exchangerate host
            converted = [number_utils.continental_to_english(cell) for cell in row]
            # ignoring empty lines
            if len(row[0]) > 0:
                converted.append(previous_balance_date)
                converted.append(exchange_rate)
                result.append(converted)
        
        return result
    

    def _extract_balance_date(self, page):
        previous_balance_date = None
        text = page.extract_text()
        match = re.search(r"Saldo Anterior em (\d{2}/\d{2}/\d{4})", text)
        if match:
            previous_balance_date = match.group(1)
        if previous_balance_date is None:
            raise ValueError("Previous balance date not found in the document.")
        return previous_balance_date
    

    def _br_to_aud_forex(self, rate_on_date):
        payment_date = rate_on_date
        parsed_date = datetime.strptime(payment_date, "%d/%m/%Y").date()
        return self.exchange_service.get_rate("BRL", "AUD", parsed_date)