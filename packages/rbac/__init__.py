"""
RBAC Package - Role-Based Access Control

Provides:
- Role and Permission entities
- RBAC service for access control
- FastAPI permission decorators
"""

from .domain import Permission, Role
from .application import RBACService
from .infrastructure import require_permission, require_any_permission

__version__ = "1.0.0"

__all__ = [
    'Permission',
    'Role',
    'RBACService',
    'require_permission',
    'require_any_permission'
]
