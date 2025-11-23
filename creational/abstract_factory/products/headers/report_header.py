from abc import ABC, abstractmethod

class ReportHeader(ABC):
    @abstractmethod
    def render(self):
        pass
