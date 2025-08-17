from .model import ReportService
from .redemptions_report_service import RedemptionsReportService
from service.exchange_service import ExchangeRateService

class ReportServiceFactory:
    @staticmethod
    def create_report_service(report_type: str, exchange_service: ExchangeRateService) -> ReportService:
        
        if report_type == "redemptions":
            return RedemptionsReportService(exchange_service)
        
        # Add more report types as needed
        raise ValueError(f"Unknown report type: {report_type}")