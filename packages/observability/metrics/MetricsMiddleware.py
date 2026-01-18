from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
from .Metrics import Metrics


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to collect metrics"""
    
    def __init__(self, app, metrics: Metrics):
        super().__init__(app)
        self.metrics = metrics

    async def dispatch(self, request: Request, call_next):
        start = time.time()
        
        response = await call_next(request)
        
        duration = time.time() - start
        method = request.method
        endpoint = request.url.path
        status = response.status_code
        
        self.metrics.record_request(method, endpoint, status)
        self.metrics.record_duration(method, endpoint, duration)
        
        return response
