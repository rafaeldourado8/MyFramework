# MyFramework Video Streaming

Video streaming with MediaMTX and FFmpeg integration.

## Installation

```bash
pip install myframework-video-streaming
```

## Usage

```python
from myframework.video_streaming import StreamingService, MediaMTXClient

client = MediaMTXClient("http://localhost:9997")
service = StreamingService(client)
```

See [documentation](https://github.com/rafaeldourado8/MyFramework/blob/master/docs/video-streaming.md) for details.
