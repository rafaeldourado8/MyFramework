# MyFramework Video Workers

Background workers for video recording, cleanup and thumbnails.

## Installation

```bash
pip install myframework-video-workers
```

## Usage

```python
from myframework.video_workers import Worker, CleanupWorker

worker = CleanupWorker()
worker.start()
```
