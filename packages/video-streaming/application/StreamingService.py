from uuid import UUID
from core import Result
from ..domain import Stream, Recording, StreamStatus, RecordingStatus, RetentionPolicy
from ..domain import MediaMTXClient, FFmpegService, StorageService


class StreamingService:
    """Video streaming orchestration service"""
    
    def __init__(self, mediamtx: MediaMTXClient, ffmpeg: FFmpegService, storage: StorageService):
        self.mediamtx = mediamtx
        self.ffmpeg = ffmpeg
        self.storage = storage

    async def start_stream(self, camera_id: UUID, source_url: str) -> Result[Stream]:
        """Start video stream"""
        stream = Stream(camera_id=camera_id, source_url=source_url)
        stream.start()
        
        success = await self.mediamtx.start_stream(str(stream.id), source_url)
        if not success:
            stream.mark_error()
            return Result.fail("Failed to start stream")
        
        stream.mark_running()
        return Result.ok(stream)

    async def stop_stream(self, stream: Stream) -> Result[Stream]:
        """Stop video stream"""
        success = await self.mediamtx.stop_stream(str(stream.id))
        if not success:
            return Result.fail("Failed to stop stream")
        
        stream.stop()
        return Result.ok(stream)

    async def start_recording(self, stream: Stream, retention_days: int = 30) -> Result[Recording]:
        """Start recording stream"""
        if not stream.is_active():
            return Result.fail("Stream is not active")
        
        recording = Recording(
            stream_id=stream.id,
            retention_policy=RetentionPolicy(retention_days)
        )
        
        output_path = f"/recordings/{recording.id}.mp4"
        success = await self.ffmpeg.start_recording(recording.id, stream.source_url, output_path)
        
        if not success:
            recording.mark_error()
            return Result.fail("Failed to start recording")
        
        recording.storage_path = output_path
        return Result.ok(recording)

    async def stop_recording(self, recording: Recording) -> Result[Recording]:
        """Stop recording"""
        success = await self.ffmpeg.stop_recording(recording.id)
        if not success:
            return Result.fail("Failed to stop recording")
        
        recording.stop()
        return Result.ok(recording)
