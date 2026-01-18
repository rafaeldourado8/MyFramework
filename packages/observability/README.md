# Observability Package

Metrics and structured logging.

## Features

- Prometheus metrics (HTTP requests, duration, custom metrics)
- Structured JSON logging
- FastAPI middleware

## Usage

### Metrics

```python
from observability import Metrics

metrics = Metrics(namespace="myapp")

# Record HTTP request
metrics.record_request("GET", "/users", 200)

# Record duration
metrics.record_duration("GET", "/users", 0.123)

# Custom metric
metrics.set_active_users(42)

# Export for Prometheus
data = Metrics.export()
```

### FastAPI Integration

```python
from fastapi import FastAPI, Response
from observability import Metrics, MetricsMiddleware

app = FastAPI()
metrics = Metrics(namespace="myapp")

# Add middleware
app.add_middleware(MetricsMiddleware, metrics=metrics)

# Metrics endpoint
@app.get("/metrics")
async def get_metrics():
    return Response(
        content=Metrics.export(),
        media_type=Metrics.content_type()
    )
```

### Structured Logging

```python
from observability import StructuredLogger

logger = StructuredLogger(name="myapp")

# Log with context
logger.info("User logged in", {
    "user_id": "123",
    "ip": "192.168.1.1"
})

# Output: {"timestamp": "2024-01-01T12:00:00", "level": "info", 
#          "message": "User logged in", "user_id": "123", "ip": "192.168.1.1"}
```

## Metrics Collected

- `{namespace}_http_requests_total` - Total HTTP requests
- `{namespace}_http_request_duration_seconds` - Request duration
- `{namespace}_active_users` - Active users count
