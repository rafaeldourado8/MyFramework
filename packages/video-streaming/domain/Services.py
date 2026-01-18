from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional


class MediaMTXClient(ABC):
    """MediaMTX streaming server client"""
    
    @abstractmethod
    async def start_stream(self, stream_id: str, source_url: str) -> bool:
        pass

    @abstractmethod
    async def stop_stream(self, stream_id: str) -> bool:
        pass

    @abstractmethod
    async def get_stream_status(self, stream_id: str) -> dict:
        pass


class FFmpegService(ABC):
    """FFmpeg video processing service"""
    
    @abstractmethod
    async def start_recording(self, recording_id: UUID, source_url: str, output_path: str) -> bool:
        pass

    @abstractmethod
    async def stop_recording(self, recording_id: UUID) -> bool:
        pass

    @abstractmethod
    async def is_recording(self, recording_id: UUID) -> bool:
        pass


class StorageService(ABC):
    """Video storage service (S3/MinIO)"""
    
    @abstractmethod
    async def upload_file(self, local_path: str, remote_path: str) -> str:
        pass

    @abstractmethod
    async def delete_file(self, remote_path: str) -> bool:
        pass

    @abstractmethod
    async def get_file_url(self, remote_path: str, expires_in: int = 3600) -> Optional[str]:
        pass

    @abstractmethod
    async def file_exists(self, remote_path: str) -> bool:
        pass
