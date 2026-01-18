from abc import ABC, abstractmethod
from typing import Optional, Any


class Cache(ABC):
    """Cache interface"""
    
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get value"""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int = None):
        """Set value with optional TTL"""
        pass

    @abstractmethod
    async def delete(self, key: str):
        """Delete key"""
        pass

    @abstractmethod
    async def clear(self):
        """Clear all cache"""
        pass
