from .report_footer import ReportFooter

class CSVFooter(ReportFooter):
    def render(self):
        return "generated_by,csv_system\n"
