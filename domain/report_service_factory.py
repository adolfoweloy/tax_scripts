from service.exchange_service import ExchangeRateService
from .model import ReportService
from .redemptions_report_service import RedemptionsReportService
from .balance_report_service import BalanceReportService

class ReportServiceFactory:
    @staticmethod
    def create_report_service(report_type: str, exchange_service: ExchangeRateService) -> ReportService:
        
        if report_type == "redemptions":
            return RedemptionsReportService(exchange_service)
        
        if report_type == "previous_balance":
            return BalanceReportService(exchange_service)
        

        # Add more report types as needed
        raise ValueError(f"Unknown report type: {report_type}")