from abc import ABC, abstractmethod
from typing import Callable, Awaitable


class MessageBroker(ABC):
    """Message broker interface"""
    
    @abstractmethod
    async def publish(self, topic: str, message: dict):
        """Publish message"""
        pass

    @abstractmethod
    async def subscribe(self, topic: str, handler: Callable[[dict], Awaitable[None]]):
        """Subscribe to topic"""
        pass

    @abstractmethod
    async def connect(self):
        """Connect to broker"""
        pass

    @abstractmethod
    async def disconnect(self):
        """Disconnect from broker"""
        pass
