from .ReportFactory import ReportFactory
from ..products.headers.html_header import HTMLHeader
from ..products.footers.html_footer import HTMLFooter
from ..products.bodies.html_body import HTMLBody

class HTMLFactory(ReportFactory):
    def create_Header(self):
        return HTMLHeader()   
    def create_Footer(self):
        return HTMLFooter()    
    def create_Body(self):
        return HTMLBody()    