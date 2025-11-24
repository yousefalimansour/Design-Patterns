from abc import ABC, abstractmethod
from ..domain.email_entities import Email
from typing import Optional

class BaseHandler(ABC):
    def __init__(self):
        self._next_handler: Optional['BaseHandler'] = None

    def set_next(self, handler: 'BaseHandler') -> 'BaseHandler':
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, email: Email) -> str:
        """
        Default behavior: pass the request to the next handler.
        """
        if self._next_handler:
            return self._next_handler.handle(email)
        return "Email processed"