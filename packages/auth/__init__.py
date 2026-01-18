"""
Auth Package - Authentication and Authorization

Provides:
- Password hashing and validation
- JWT token generation and verification
- FastAPI authentication dependencies
"""

from .domain import Password, Token, TokenPayload
from .application import JWTService, AuthService
from .infrastructure import create_auth_dependency

__version__ = "1.0.0"

__all__ = [
    'Password',
    'Token',
    'TokenPayload',
    'JWTService',
    'AuthService',
    'create_auth_dependency'
]
