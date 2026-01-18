from core import Entity
from uuid import UUID
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List


class Thumbnail(Entity):
    """Video thumbnail"""
    def __init__(self, id: UUID = None, video_id: UUID = None, timestamp: float = 0.0, url: str = ""):
        super().__init__(id)
        self.video_id = video_id
        self.timestamp = timestamp
        self.url = url


class Clip(Entity):
    """Video clip"""
    def __init__(self, id: UUID = None, video_id: UUID = None, start: float = 0.0, 
                 duration: float = 0.0, url: str = ""):
        super().__init__(id)
        self.video_id = video_id
        self.start = start
        self.duration = duration
        self.url = url


class ThumbnailService(ABC):
    """Thumbnail generation service"""
    @abstractmethod
    async def generate(self, video_path: str, timestamps: List[float]) -> List[str]:
        pass


class ClipService(ABC):
    """Clip creation service"""
    @abstractmethod
    async def create(self, video_path: str, start: float, duration: float, output: str) -> bool:
        pass
