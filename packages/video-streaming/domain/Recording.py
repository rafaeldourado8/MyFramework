from core import Entity
from uuid import UUID
from datetime import datetime
from .ValueObjects import RecordingStatus, RetentionPolicy


class Recording(Entity):
    """Recording entity"""
    
    def __init__(self, id: UUID = None, stream_id: UUID = None, 
                 retention_policy: RetentionPolicy = None,
                 status: RecordingStatus = RecordingStatus.RECORDING,
                 storage_path: str = None, file_size_mb: float = 0.0):
        super().__init__(id)
        self.stream_id = stream_id
        self.retention_policy = retention_policy or RetentionPolicy(30)
        self.status = status
        self.started_at = datetime.utcnow()
        self.stopped_at = None
        self.storage_path = storage_path
        self.file_size_mb = file_size_mb
        self.duration_seconds = 0

    def stop(self):
        self.status = RecordingStatus.STOPPED
        self.stopped_at = datetime.utcnow()
        if self.started_at:
            self.duration_seconds = int((self.stopped_at - self.started_at).total_seconds())
        self._touch()

    def mark_error(self):
        self.status = RecordingStatus.ERROR
        self._touch()

    def is_active(self) -> bool:
        return self.status == RecordingStatus.RECORDING

    def should_be_deleted(self) -> bool:
        if not self.stopped_at:
            return False
        days_old = (datetime.utcnow() - self.stopped_at).days
        return days_old > self.retention_policy.days
