from ..core.base_logger import BaseLogger
from ..core.log_level import LogLevel


class PythonLoggerAdapter(BaseLogger):
    def __init__(self):
        pass

    def log(self, level: LogLevel, message: str) -> None:
        pass

    def info(self, message: str) -> None:
        pass

    def error(self, message: str) -> None:
        pass

    def warning(self, message: str) -> None:
        pass