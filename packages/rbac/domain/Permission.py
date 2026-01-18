from core import Entity
from uuid import UUID


class Permission(Entity):
    """Permission entity"""
    
    def __init__(self, id: UUID = None, code: str = "", name: str = "", description: str = ""):
        super().__init__(id)
        self.code = code
        self.name = name
        self.description = description
