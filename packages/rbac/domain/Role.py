from core import Entity
from uuid import UUID
from typing import List
from .Permission import Permission


class Role(Entity):
    """Role entity with permissions"""
    
    def __init__(self, id: UUID = None, code: str = "", name: str = "", 
                 permissions: List[Permission] = None):
        super().__init__(id)
        self.code = code
        self.name = name
        self.permissions = permissions or []

    def add_permission(self, permission: Permission):
        if permission not in self.permissions:
            self.permissions.append(permission)
            self._touch()

    def remove_permission(self, permission: Permission):
        if permission in self.permissions:
            self.permissions.remove(permission)
            self._touch()

    def has_permission(self, code: str) -> bool:
        return any(p.code == code for p in self.permissions)
