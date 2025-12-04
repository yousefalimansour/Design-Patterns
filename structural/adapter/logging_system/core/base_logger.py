from abc import ABC, abstractmethod
from .log_level import LogLevel


class BaseLogger(ABC):
    @abstractmethod
    def log(self, level: LogLevel, message: str) -> None:
        pass

    @abstractmethod
    def info(self, message: str) -> None:
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        pass

    @abstractmethod
    def warning(self, message: str) -> None:
        pass