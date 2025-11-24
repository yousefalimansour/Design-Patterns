from .base_handler import BaseHandler
from ..domain.email_entities import Email

BLACKLIST = ["spam@example.com", "ads@marketing.com"]

class BlacklistedSenderHandler(BaseHandler):
    def handle(self, email: Email) -> str:
        if email.sender in BLACKLIST:
            email.is_spam = True
            return "Blacklisted sender detected"
        
        return super().handle(email)
        
