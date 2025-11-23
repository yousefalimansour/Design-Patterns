from .report_header import ReportHeader

class HTMLHeader(ReportHeader):
    def render(self):
        return "<h1>Sales Report</h1>"
