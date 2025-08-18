from datetime import datetime
import time

import pdfplumber
from pdfplumber.page import Page
import number_utils
from service.exchange_service import ExchangeRateService
from .model import ReportService

class RedemptionsReportService(ReportService):
    def __init__(self, exchange_service: ExchangeRateService):
        self.exchange_service = exchange_service

    def extract_header(self, pages: list[Page]):
        first_page = pages[0]
        tables = first_page.extract_tables()
        redemptions = tables[3]  # 4th table for the CDI report
        header = []
        header = redemptions[0]
        header.append("BRLAUD Rate")
        return header

    def process(self, pages: list[Page]):
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