from abc import ABC
from abc import abstractmethod

class ReportFactory(ABC):
    @abstractmethod
    def create_Header(self):
        pass    

    @abstractmethod
    def create_Body(self):
        pass    

    @abstractmethod
    def create_Footer(self):
        pass    

    