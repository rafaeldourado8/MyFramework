from abc import ABC, abstractmethod


class Connection(ABC):
    """Database connection interface"""
    
    @abstractmethod
    async def connect(self):
        """Establish connection"""
        pass

    @abstractmethod
    async def disconnect(self):
        """Close connection"""
        pass

    @abstractmethod
    async def execute(self, query: str, params: dict = None):
        """Execute query"""
        pass
