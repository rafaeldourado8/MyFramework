# MyFramework Observability

Prometheus metrics and structured JSON logging.

## Installation

```bash
pip install myframework-observability
```

## Usage

```python
from myframework.observability import Metrics, StructuredLogger

metrics = Metrics()
metrics.record_http_request("GET", "/users", 200, 0.5)

logger = StructuredLogger("my-service")
logger.info("User created", user_id=123)
```

See [documentation](https://github.com/rafaeldourado8/MyFramework/blob/master/docs/observability.md) for details.
