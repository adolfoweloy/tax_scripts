
from abc import ABC, abstractmethod 
import pdfplumber
import glob

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
