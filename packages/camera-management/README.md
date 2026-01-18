# MyFramework Camera Management

RTSP camera management with validation.

## Installation

```bash
pip install myframework-camera-management
```

## Usage

```python
from myframework.camera_management import Camera, RTSPUrl

url = RTSPUrl("rtsp://admin:pass@192.168.1.100:554/stream")
camera = Camera.create("Camera 1", url, "Living Room")
```
