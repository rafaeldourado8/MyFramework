"""
Video Streaming Package

Provides:
- Stream and Recording entities
- MediaMTX client integration
- FFmpeg service integration
- Storage service integration
- Streaming orchestration
"""

from .domain import (
    Stream, Recording,
    StreamStatus, RecordingStatus, RetentionPolicy,
    MediaMTXClient, FFmpegService, StorageService
)
from .application import StreamingService
from .infrastructure import MediaMTXClientImpl

__version__ = "1.0.0"

__all__ = [
    'Stream', 'Recording',
    'StreamStatus', 'RecordingStatus', 'RetentionPolicy',
    'MediaMTXClient', 'FFmpegService', 'StorageService',
    'StreamingService',
    'MediaMTXClientImpl'
]
