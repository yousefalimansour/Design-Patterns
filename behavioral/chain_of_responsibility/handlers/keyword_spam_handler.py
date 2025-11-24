from .base_handler import BaseHandler
from ..domain.email_entities import Email

SPAM_KEYWORDS = ["free", "win", "click here", "money", "offer"]

class KeywordSpamHandler(BaseHandler):
    def handle(self, email: Email) -> str:
        body = email.body.lower()
        subject = email.subject.lower()

        if any(keyword in body or subject for keyword in SPAM_KEYWORDS):
            email.is_spam = True
            return "Spam detected"

        return super().handle(email)
        
        
