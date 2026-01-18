"""
Observability Package - Metrics and Logging

Provides:
- Prometheus metrics
- Structured JSON logging
- FastAPI middleware for metrics
"""

from .metrics.Metrics import Metrics
from .metrics.MetricsMiddleware import MetricsMiddleware
from .logging.StructuredLogger import StructuredLogger

__version__ = "1.0.0"

__all__ = [
    'Metrics',
    'MetricsMiddleware',
    'StructuredLogger'
]
