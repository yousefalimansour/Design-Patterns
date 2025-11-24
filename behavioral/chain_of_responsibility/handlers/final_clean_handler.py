from .base_handler import BaseHandler
from ..domain.email_entities import Email

class FinalCleanHandler(BaseHandler):
    def handle(self, email: Email) -> str:
        email.is_spam = False
        return "Email cleaned"
