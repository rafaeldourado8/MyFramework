from abc import ABC, abstractmethod
from typing import Any, Dict
from enum import Enum


class LogLevel(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class Logger(ABC):
    """Structured logger interface"""
    
    @abstractmethod
    def log(self, level: LogLevel, message: str, context: Dict[str, Any] = None):
        """Log with context"""
        pass

    def debug(self, message: str, context: Dict[str, Any] = None):
        self.log(LogLevel.DEBUG, message, context)

    def info(self, message: str, context: Dict[str, Any] = None):
        self.log(LogLevel.INFO, message, context)

    def warning(self, message: str, context: Dict[str, Any] = None):
        self.log(LogLevel.WARNING, message, context)

    def error(self, message: str, context: Dict[str, Any] = None):
        self.log(LogLevel.ERROR, message, context)

    def critical(self, message: str, context: Dict[str, Any] = None):
        self.log(LogLevel.CRITICAL, message, context)
