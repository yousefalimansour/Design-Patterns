import unittest
from ..adapters.python_logger_adapter import PythonLoggerAdapter
from ..adapters.loguru_logger_adapter import LoguruLoggerAdapter
from ..adapters.sentry_logger_adapter import SentryLoggerAdapter
from ..adapters.file_logger_adapter import FileLoggerAdapter
from ..core.log_level import LogLevel


class TestAdapters(unittest.TestCase):
    def test_python_logger_adapter_creation(self):
        adapter = PythonLoggerAdapter()
        self.assertIsNotNone(adapter)

    def test_loguru_logger_adapter_creation(self):
        adapter = LoguruLoggerAdapter()
        self.assertIsNotNone(adapter)

    def test_sentry_logger_adapter_creation(self):
        adapter = SentryLoggerAdapter()
        self.assertIsNotNone(adapter)

    def test_file_logger_adapter_creation(self):
        adapter = FileLoggerAdapter()
        self.assertIsNotNone(adapter)


if __name__ == "__main__":
    unittest.main()