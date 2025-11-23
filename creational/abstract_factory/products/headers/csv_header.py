from .report_header import ReportHeader

class CSVHeader(ReportHeader):
    def render(self):
        return "name,amount,date\n"
