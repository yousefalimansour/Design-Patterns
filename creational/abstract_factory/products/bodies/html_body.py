from .report_body import ReportBody

class HTMLBody(ReportBody):
    def render(self, data):
        html_rows = "".join(
            f"<tr><td>{row['name']}</td><td>{row['amount']}</td><td>{row['date']}</td></tr>"
            for row in data
        )
        return f"<table>{html_rows}</table>"
