from enum import Enum
from core import ValueObject, ValidationException


class StreamStatus(Enum):
    STOPPED = "STOPPED"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    ERROR = "ERROR"


class RecordingStatus(Enum):
    RECORDING = "RECORDING"
    STOPPED = "STOPPED"
    ERROR = "ERROR"


class RetentionPolicy(ValueObject):
    """Retention policy for recordings"""
    
    ALLOWED_DAYS = [7, 15, 30, 60, 90]
    
    def __init__(self, days: int):
        if days not in self.ALLOWED_DAYS:
            raise ValidationException(f"Retention days must be one of {self.ALLOWED_DAYS}")
        self.days = days
