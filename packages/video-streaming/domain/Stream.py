from core import Entity
from uuid import UUID
from datetime import datetime
from .ValueObjects import StreamStatus


class Stream(Entity):
    """Stream entity"""
    
    def __init__(self, id: UUID = None, camera_id: UUID = None, source_url: str = "",
                 status: StreamStatus = StreamStatus.STOPPED, started_at: datetime = None):
        super().__init__(id)
        self.camera_id = camera_id
        self.source_url = source_url
        self.status = status
        self.started_at = started_at
        self.stopped_at = None

    def start(self):
        self.status = StreamStatus.STARTING
        self.started_at = datetime.utcnow()
        self.stopped_at = None
        self._touch()

    def mark_running(self):
        self.status = StreamStatus.RUNNING
        self._touch()

    def stop(self):
        self.status = StreamStatus.STOPPED
        self.stopped_at = datetime.utcnow()
        self._touch()

    def mark_error(self):
        self.status = StreamStatus.ERROR
        self._touch()

    def is_active(self) -> bool:
        return self.status in [StreamStatus.STARTING, StreamStatus.RUNNING]
