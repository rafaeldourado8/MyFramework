"""
Video Processing Package

Provides:
- Thumbnail generation
- Clip creation
- Video processing utilities
"""

from .domain import Thumbnail, Clip, ThumbnailService, ClipService
from .application import VideoProcessingService

__version__ = "1.0.0"

__all__ = ['Thumbnail', 'Clip', 'ThumbnailService', 'ClipService', 'VideoProcessingService']
