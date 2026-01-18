from fastapi import HTTPException, status
from typing import Callable, List
from ..domain import Role
from ..application import RBACService


def require_permission(permission_code: str):
    """Decorator to require permission"""
    def decorator(func: Callable):
        async def wrapper(*args, role: Role = None, **kwargs):
            if not role or not RBACService.can_access(role, permission_code):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission required: {permission_code}"
                )
            return await func(*args, role=role, **kwargs)
        return wrapper
    return decorator


def require_any_permission(permission_codes: List[str]):
    """Decorator to require any of the permissions"""
    def decorator(func: Callable):
        async def wrapper(*args, role: Role = None, **kwargs):
            if not role or not RBACService.can_access_any(role, permission_codes):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"One of these permissions required: {permission_codes}"
                )
            return await func(*args, role=role, **kwargs)
        return wrapper
    return decorator
