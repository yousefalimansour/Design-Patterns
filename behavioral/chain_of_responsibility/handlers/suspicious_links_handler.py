from .base_handler import BaseHandler
from ..domain.email_entities import Email
import re

SUSPICIOUS_DOMAINS = ["xyz", "clickme", "cheapstuff"]


class SuspiciousLinksHandler(BaseHandler):
    def handle(self, email: Email) -> str:
        links = re.findall(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", email.body)

        for link in links:
            if any(domain in link for domain in SUSPICIOUS_DOMAINS):
                email.is_spam = True
                return "Spam detected"

        return super().handle(email)