from abc import ABC
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4


class Entity(ABC):
    """Base entity with identity and timestamps"""
    
    def __init__(self, id: UUID | None = None):
        self._id = id or uuid4()
        self._created_at = datetime.utcnow()
        self._updated_at = datetime.utcnow()

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    def _touch(self):
        """Update timestamp"""
        self._updated_at = datetime.utcnow()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
