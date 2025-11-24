from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Email
from .services.filter_service import FilterService


class FilterEmailAPIView(APIView):
    def post(self, request):
        sender = request.data.get("sender")
        subject = request.data.get("subject")
        body = request.data.get("body")

        if not all([sender, subject, body]):
            return Response(
                {"error": "sender, subject and body are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        email = Email(
            sender=sender,
            subject=subject,
            body=body
        )

        service = FilterService()
        # The service.run method expects an email object and returns a result string
        # It modifies the email object in place (setting is_spam)
        result = service.run(email)

        email.save()

        return Response(
            {
                "sender": email.sender,
                "subject": email.subject,
                "body": email.body,
                "is_spam": email.is_spam,
                "result": result
            },
            status=status.HTTP_200_OK
        )
