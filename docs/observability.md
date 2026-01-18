# Observability Package

Métricas Prometheus e logs estruturados.

## Instalação

```bash
pip install -e packages/observability
```

## Quick Start

### Metrics

```python
from observability import Metrics, MetricsMiddleware
from fastapi import FastAPI, Response

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

# Custom metrics
@app.post("/users")
async def create_user(data: dict):
    metrics.set_active_users(get_user_count())
    return {"user": data}
```

### Structured Logging

```python
from observability import StructuredLogger

logger = StructuredLogger(name="myapp")

# Log with context
logger.info("User logged in", {
    "user_id": "123",
    "ip": "192.168.1.1",
    "user_agent": "Mozilla/5.0"
})

# Output:
# {"timestamp": "2024-01-01T12:00:00", "level": "info", 
#  "message": "User logged in", "user_id": "123", "ip": "192.168.1.1"}

# Different levels
logger.debug("Debug message", {"detail": "value"})
logger.warning("Warning message", {"reason": "timeout"})
logger.error("Error occurred", {"error": "connection failed"})
```

## API Reference

### Metrics

```python
from observability import Metrics

metrics = Metrics(namespace="myapp")

# HTTP metrics (automatic with middleware)
metrics.record_request("GET", "/users", 200)
metrics.record_duration("GET", "/users", 0.123)

# Custom metrics
metrics.set_active_users(42)

# Export for Prometheus
data = Metrics.export()
content_type = Metrics.content_type()
```

**Métricas coletadas:**
- `{namespace}_http_requests_total` - Total de requests HTTP
- `{namespace}_http_request_duration_seconds` - Duração dos requests
- `{namespace}_active_users` - Usuários ativos (custom)

### MetricsMiddleware

```python
from observability import MetricsMiddleware
from fastapi import FastAPI

app = FastAPI()
metrics = Metrics(namespace="myapp")

# Add middleware
app.add_middleware(MetricsMiddleware, metrics=metrics)

# Automatically collects:
# - HTTP request count
# - HTTP request duration
# - Status codes
```

### StructuredLogger

```python
from observability import StructuredLogger
from core.infrastructure import LogLevel

logger = StructuredLogger(name="myapp")

# Log methods
logger.debug("Debug", {"key": "value"})
logger.info("Info", {"key": "value"})
logger.warning("Warning", {"key": "value"})
logger.error("Error", {"key": "value"})
logger.critical("Critical", {"key": "value"})

# Generic log
logger.log(LogLevel.INFO, "Message", {"key": "value"})
```

## Prometheus Integration

### Setup Prometheus

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'myapp'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

### Run Prometheus

```bash
docker run -d \
  -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
```

### Query Metrics

```promql
# Request rate
rate(myapp_http_requests_total[5m])

# Average duration
rate(myapp_http_request_duration_seconds_sum[5m]) / 
rate(myapp_http_request_duration_seconds_count[5m])

# Active users
myapp_active_users

# Requests by status
sum by (status) (myapp_http_requests_total)
```

## Grafana Dashboards

### Setup Grafana

```bash
docker run -d \
  -p 3000:3000 \
  grafana/grafana
```

### Add Prometheus Data Source

1. Go to Configuration → Data Sources
2. Add Prometheus
3. URL: `http://prometheus:9090`

### Create Dashboard

**HTTP Requests Panel:**
```promql
sum(rate(myapp_http_requests_total[5m])) by (method, endpoint)
```

**Response Time Panel:**
```promql
histogram_quantile(0.95, 
  rate(myapp_http_request_duration_seconds_bucket[5m])
)
```

**Active Users Panel:**
```promql
myapp_active_users
```

## ELK Stack Integration

### Logstash Config

```ruby
# logstash.conf
input {
  file {
    path => "/var/log/myapp/*.log"
    codec => json
  }
}

filter {
  json {
    source => "message"
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "myapp-%{+YYYY.MM.dd}"
  }
}
```

### Elasticsearch Query

```json
GET /myapp-*/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "level": "error" } },
        { "range": { "timestamp": { "gte": "now-1h" } } }
      ]
    }
  }
}
```

## Casos de Uso

### API Monitoring

```python
from observability import Metrics, StructuredLogger, MetricsMiddleware
from fastapi import FastAPI

app = FastAPI()
metrics = Metrics(namespace="api")
logger = StructuredLogger(name="api")

app.add_middleware(MetricsMiddleware, metrics=metrics)

@app.post("/users")
async def create_user(data: dict):
    logger.info("Creating user", {"email": data["email"]})
    
    try:
        user = create_user_in_db(data)
        metrics.set_active_users(get_user_count())
        
        logger.info("User created", {"user_id": str(user.id)})
        return {"user": user}
    
    except Exception as e:
        logger.error("Failed to create user", {
            "error": str(e),
            "email": data["email"]
        })
        raise
```

### Business Metrics

```python
# Track business events
@app.post("/orders")
async def create_order(data: dict):
    order = create_order_in_db(data)
    
    # Custom metrics
    metrics.orders_total.inc()
    metrics.revenue_total.inc(order.amount)
    
    logger.info("Order created", {
        "order_id": str(order.id),
        "amount": order.amount,
        "user_id": str(order.user_id)
    })
    
    return {"order": order}
```

### Error Tracking

```python
@app.exception_handler(Exception)
async def exception_handler(request, exc):
    logger.error("Unhandled exception", {
        "error": str(exc),
        "path": request.url.path,
        "method": request.method,
        "traceback": traceback.format_exc()
    })
    
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )
```

## Best Practices

### Logging

- Use structured logging (JSON)
- Include context (user_id, request_id, etc)
- Log errors with stack traces
- Don't log sensitive data (passwords, tokens)

### Metrics

- Use meaningful metric names
- Add labels for dimensions
- Don't create too many metrics
- Use histograms for latencies

### Alerting

```promql
# High error rate
rate(myapp_http_requests_total{status=~"5.."}[5m]) > 0.05

# High latency
histogram_quantile(0.95, 
  rate(myapp_http_request_duration_seconds_bucket[5m])
) > 1

# Low active users
myapp_active_users < 10
```
