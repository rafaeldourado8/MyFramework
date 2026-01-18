from typing import List
from core import Result
from ..domain import Role, Permission


class RBACService:
    """Role-Based Access Control service"""
    
    @staticmethod
    def can_access(role: Role, permission_code: str) -> bool:
        """Check if role has permission"""
        return role.has_permission(permission_code)

    @staticmethod
    def can_access_any(role: Role, permission_codes: List[str]) -> bool:
        """Check if role has any of the permissions"""
        return any(role.has_permission(code) for code in permission_codes)

    @staticmethod
    def can_access_all(role: Role, permission_codes: List[str]) -> bool:
        """Check if role has all permissions"""
        return all(role.has_permission(code) for code in permission_codes)

    @staticmethod
    def grant_permission(role: Role, permission: Permission) -> Result[Role]:
        """Grant permission to role"""
        role.add_permission(permission)
        return Result.ok(role)

    @staticmethod
    def revoke_permission(role: Role, permission: Permission) -> Result[Role]:
        """Revoke permission from role"""
        role.remove_permission(permission)
        return Result.ok(role)
