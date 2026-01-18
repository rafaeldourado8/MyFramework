# Video Streaming

Streaming de vídeo com MediaMTX e FFmpeg.

## Instalação

```bash
pip install -e packages/video-streaming
```

## Requisitos

- MediaMTX server rodando
- FFmpeg instalado
- Storage (S3/MinIO)

## Quick Start

```python
from video_streaming import StreamingService, MediaMTXClientImpl

# Setup
mediamtx = MediaMTXClientImpl(host="localhost", port=9997)
streaming = StreamingService(mediamtx, ffmpeg_service, storage_service)

# Start stream
stream = await streaming.start_stream(
    camera_id=camera_id,
    source_url="rtsp://192.168.1.100/stream"
)

# Start recording
recording = await streaming.start_recording(
    stream=stream,
    retention_days=30
)

# Stop recording
await streaming.stop_recording(recording)

# Stop stream
await streaming.stop_stream(stream)
```

## Entities

### Stream

```python
from video_streaming import Stream, StreamStatus

stream = Stream(
    camera_id=camera_id,
    source_url="rtsp://camera/stream"
)

stream.start()  # Status: STARTING
stream.mark_running()  # Status: RUNNING
stream.stop()  # Status: STOPPED
stream.mark_error()  # Status: ERROR

# Check if active
if stream.is_active():
    print("Stream is running")
```

### Recording

```python
from video_streaming import Recording, RetentionPolicy

recording = Recording(
    stream_id=stream.id,
    retention_policy=RetentionPolicy(30)  # 30 days
)

recording.stop()

# Check if should be deleted
if recording.should_be_deleted():
    await storage.delete_file(recording.storage_path)
```

## Services

### MediaMTXClient

Interface para MediaMTX server.

```python
from video_streaming import MediaMTXClient

class MyMediaMTXClient(MediaMTXClient):
    async def start_stream(self, stream_id: str, source_url: str) -> bool:
        # Implementation
        pass
    
    async def stop_stream(self, stream_id: str) -> bool:
        # Implementation
        pass
    
    async def get_stream_status(self, stream_id: str) -> dict:
        # Implementation
        pass
```

### FFmpegService

Interface para FFmpeg.

```python
from video_streaming import FFmpegService

class MyFFmpegService(FFmpegService):
    async def start_recording(self, recording_id: UUID, source_url: str, output_path: str) -> bool:
        # Implementation
        pass
    
    async def stop_recording(self, recording_id: UUID) -> bool:
        # Implementation
        pass
```

### StorageService

Interface para storage (S3/MinIO).

```python
from video_streaming import StorageService

class MyStorageService(StorageService):
    async def upload_file(self, local_path: str, remote_path: str) -> str:
        # Implementation
        pass
    
    async def get_file_url(self, remote_path: str, expires_in: int = 3600) -> str:
        # Implementation
        pass
```

## Configuração

### MediaMTX

```yaml
# mediamtx.yml
paths:
  all:
    source: publisher
    runOnReady: ffmpeg -i rtsp://localhost:$RTSP_PORT/$MTX_PATH -c copy -f flv rtmp://localhost/$MTX_PATH
```

### FFmpeg

```bash
# Instalar FFmpeg
apt-get install ffmpeg

# Verificar instalação
ffmpeg -version
```

## Casos de Uso

### Sistema de Vigilância

```python
# Register cameras
cameras = [
    {"id": 1, "url": "rtsp://192.168.1.100/stream"},
    {"id": 2, "url": "rtsp://192.168.1.101/stream"},
]

# Start all streams
streams = []
for camera in cameras:
    stream = await streaming.start_stream(camera["id"], camera["url"])
    streams.append(stream)

# Start recordings
recordings = []
for stream in streams:
    recording = await streaming.start_recording(stream, retention_days=30)
    recordings.append(recording)
```

### Live Streaming

```python
# Start stream from RTSP camera
stream = await streaming.start_stream(camera_id, "rtsp://camera/stream")

# Get HLS URL for playback
hls_url = f"http://mediamtx:8888/{stream.id}/index.m3u8"
```

## API Reference

### StreamingService

- `start_stream(camera_id, source_url)` → Result[Stream]
- `stop_stream(stream)` → Result[Stream]
- `start_recording(stream, retention_days)` → Result[Recording]
- `stop_recording(recording)` → Result[Recording]

### Stream

- `start()` - Iniciar stream
- `mark_running()` - Marcar como rodando
- `stop()` - Parar stream
- `mark_error()` - Marcar erro
- `is_active()` → bool

### Recording

- `stop()` - Parar gravação
- `mark_error()` - Marcar erro
- `is_active()` → bool
- `should_be_deleted()` → bool

## Troubleshooting

### Stream não inicia

- Verificar se MediaMTX está rodando
- Verificar URL RTSP da câmera
- Verificar conectividade de rede

### Recording falha

- Verificar se FFmpeg está instalado
- Verificar permissões de escrita
- Verificar espaço em disco

### Storage error

- Verificar credenciais S3/MinIO
- Verificar conectividade
- Verificar permissões de bucket
