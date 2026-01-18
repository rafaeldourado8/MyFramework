import json
import logging
from datetime import datetime
from typing import Dict, Any
from core.infrastructure import Logger, LogLevel


class StructuredLogger(Logger):
    """Structured JSON logger"""
    
    def __init__(self, name: str = "app"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)

    def log(self, level: LogLevel, message: str, context: Dict[str, Any] = None):
        """Log with structured context"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level.value,
            "message": message,
            **(context or {})
        }
        
        log_str = json.dumps(log_entry)
        
        if level == LogLevel.DEBUG:
            self.logger.debug(log_str)
        elif level == LogLevel.INFO:
            self.logger.info(log_str)
        elif level == LogLevel.WARNING:
            self.logger.warning(log_str)
        elif level == LogLevel.ERROR:
            self.logger.error(log_str)
        elif level == LogLevel.CRITICAL:
            self.logger.critical(log_str)
