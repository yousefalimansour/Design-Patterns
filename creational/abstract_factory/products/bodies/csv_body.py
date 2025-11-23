from .report_body import ReportBody

class CSVBody(ReportBody):
    def render(self,data):
        return "".join(f"{row['name']},{row['amount']},{row['date']}\n" for row in data)
    