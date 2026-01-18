from abc import ABC, abstractmethod
from typing import AsyncContextManager


class UnitOfWork(ABC):
    """Unit of Work pattern for transactions"""
    
    @abstractmethod
    async def commit(self):
        """Commit transaction"""
        pass

    @abstractmethod
    async def rollback(self):
        """Rollback transaction"""
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
