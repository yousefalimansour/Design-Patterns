from abc import ABC, abstractmethod

class ReportBody(ABC):
    @abstractmethod
    def render(self,data):
        pass
