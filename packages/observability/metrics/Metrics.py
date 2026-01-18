from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST


class Metrics:
    """Prometheus metrics"""
    
    def __init__(self, namespace: str = "app"):
        self.namespace = namespace
        
        # HTTP metrics
        self.http_requests = Counter(
            f"{namespace}_http_requests_total",
            "Total HTTP requests",
            ["method", "endpoint", "status"]
        )
        
        self.http_duration = Histogram(
            f"{namespace}_http_request_duration_seconds",
            "HTTP request duration",
            ["method", "endpoint"]
        )
        
        # Business metrics
        self.active_users = Gauge(
            f"{namespace}_active_users",
            "Number of active users"
        )

    def record_request(self, method: str, endpoint: str, status: int):
        """Record HTTP request"""
        self.http_requests.labels(method=method, endpoint=endpoint, status=status).inc()

    def record_duration(self, method: str, endpoint: str, duration: float):
        """Record request duration"""
        self.http_duration.labels(method=method, endpoint=endpoint).observe(duration)

    def set_active_users(self, count: int):
        """Set active users count"""
        self.active_users.set(count)

    @staticmethod
    def export():
        """Export metrics"""
        return generate_latest()

    @staticmethod
    def content_type():
        """Get content type"""
        return CONTENT_TYPE_LATEST
