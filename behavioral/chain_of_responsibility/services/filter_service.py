from ..handlers.keyword_spam_handler import KeywordSpamHandler
from ..handlers.blacklisted_sender_handler import BlacklistedSenderHandler
from ..handlers.suspicious_links_handler import SuspiciousLinksHandler
from ..handlers.final_clean_handler import FinalCleanHandler

class FilterService:
    def __init__(self):
        self.chain = self.setup_chain()

    def setup_chain(self):
        keyword = KeywordSpamHandler()
        blacklisted = BlacklistedSenderHandler()
        suspicious = SuspiciousLinksHandler()
        final = FinalCleanHandler()

        keyword.set_next(blacklisted)
        blacklisted.set_next(suspicious)
        suspicious.set_next(final)

        return keyword

    def run(self, email):
        return self.chain.handle(email)
            


