from abc import ABC, abstractmethod

class ReportFooter(ABC):
    @abstractmethod
    def render(self):
        pass
