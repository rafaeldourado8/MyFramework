"""
Camera Management Package

Provides:
- Camera entity
- Camera status management
- RTSP URL validation
"""

from core import Entity, ValueObject, ValidationException
from uuid import UUID
from enum import Enum


class CameraStatus(Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    ERROR = "ERROR"


class RTSPUrl(ValueObject):
    """RTSP URL value object"""
    def __init__(self, url: str):
        if not url.startswith("rtsp://"):
            raise ValidationException("URL must start with rtsp://")
        self.url = url


class Camera(Entity):
    """Camera entity"""
    def __init__(self, id: UUID = None, name: str = "", rtsp_url: RTSPUrl = None,
                 status: CameraStatus = CameraStatus.OFFLINE):
        super().__init__(id)
        self.name = name
        self.rtsp_url = rtsp_url
        self.status = status

    def mark_online(self):
        self.status = CameraStatus.ONLINE
        self._touch()

    def mark_offline(self):
        self.status = CameraStatus.OFFLINE
        self._touch()

    def mark_error(self):
        self.status = CameraStatus.ERROR
        self._touch()


class CameraService:
    """Camera management service"""
    
    def register_camera(self, name: str, rtsp_url: str) -> Camera:
        """Register new camera"""
        url = RTSPUrl(rtsp_url)
        return Camera(name=name, rtsp_url=url)

    def check_status(self, camera: Camera) -> bool:
        """Check camera status (placeholder)"""
        # Implementation would ping RTSP URL
        return camera.status == CameraStatus.ONLINE


__version__ = "1.0.0"
__all__ = ['Camera', 'CameraStatus', 'RTSPUrl', 'CameraService']
