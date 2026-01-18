from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List
from uuid import UUID

T = TypeVar('T')


class Repository(ABC, Generic[T]):
    """Repository pattern interface"""
    
    @abstractmethod
    async def save(self, entity: T) -> T:
        """Save entity"""
        pass

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[T]:
        """Find by ID"""
        pass

    @abstractmethod
    async def find_all(self) -> List[T]:
        """Find all entities"""
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> None:
        """Delete entity"""
        pass
