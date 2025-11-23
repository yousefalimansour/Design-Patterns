from .ReportFactory import ReportFactory
from ..products.headers.csv_header import CSVHeader
from ..products.bodies.csv_body import CSVBody
from ..products.footers.csv_footer import CSVFooter

class CSVFactory(ReportFactory):
    def create_Header(self):
        return CSVHeader()   
    def create_Footer(self):
        return CSVFooter()    
    def create_Body(self):
        return CSVBody()    