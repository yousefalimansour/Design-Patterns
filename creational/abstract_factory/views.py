from django.http import HttpResponse
from django.views.generic import View
from .factories.ReportFactory import ReportFactory

from .factories.CSVFactory import CSVFactory
from .factories.HTMLFactory import HTMLFactory


class ReportView(View):
    def get(self, request):
        format_type = request.GET.get('format', 'html')

        data = [
            {"name": "Item A", "amount": 120, "date": "2025-01-01"},
            {"name": "Item B", "amount": 300, "date": "2025-01-02"},
        ]

        factory = HTMLFactory() if format_type == 'html' else CSVFactory()

        header = factory.create_Header()
        body = factory.create_Body()
        footer = factory.create_Footer()

        response_content = header.render() + body.render(data) + footer.render()

        content_type = "text/html" if format_type == "html" else "text/csv"

        return HttpResponse(response_content, content_type=content_type)
        