from ..core.base_logger import BaseLogger
from ..core.log_level import LogLevel


class LoggerService:
    def __init__(self, logger: BaseLogger):
        self.logger = logger

    def write(self, message: str, level: str = "INFO") -> None:
        log_level = LogLevel(level)
        self.logger.log(log_level, message)