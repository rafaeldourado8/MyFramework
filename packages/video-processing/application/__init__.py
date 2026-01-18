from uuid import UUID
from core import Result
from ..domain import Thumbnail, Clip, ThumbnailService, ClipService


class VideoProcessingService:
    """Video processing orchestration"""
    
    def __init__(self, thumbnail_service: ThumbnailService, clip_service: ClipService):
        self.thumbnail = thumbnail_service
        self.clip = clip_service

    async def generate_thumbnails(self, video_id: UUID, video_path: str, 
                                   interval: int = 10) -> Result[list]:
        """Generate thumbnails at intervals"""
        timestamps = list(range(0, 3600, interval))  # Example: every N seconds
        urls = await self.thumbnail.generate(video_path, timestamps)
        
        thumbnails = [
            Thumbnail(video_id=video_id, timestamp=ts, url=url)
            for ts, url in zip(timestamps, urls)
        ]
        return Result.ok(thumbnails)

    async def create_clip(self, video_id: UUID, video_path: str, 
                         start: float, duration: float) -> Result[Clip]:
        """Create video clip"""
        output = f"/clips/{video_id}_{start}_{duration}.mp4"
        success = await self.clip.create(video_path, start, duration, output)
        
        if not success:
            return Result.fail("Failed to create clip")
        
        clip = Clip(video_id=video_id, start=start, duration=duration, url=output)
        return Result.ok(clip)
