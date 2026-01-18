from typing import Dict, List, Callable, Awaitable
from ..domain.DomainEvent import DomainEvent


class EventBus:
    """Simple event bus for domain events"""
    
    def __init__(self):
        self._handlers: Dict[type, List[Callable[[DomainEvent], Awaitable[None]]]] = {}

    def subscribe(self, event_type: type, handler: Callable[[DomainEvent], Awaitable[None]]):
        """Subscribe to event"""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    async def publish(self, event: DomainEvent):
        """Publish event to all subscribers"""
        event_type = type(event)
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                await handler(event)
