from typing import List
from uuid import UUID
from .Entity import Entity
from .DomainEvent import DomainEvent


class AggregateRoot(Entity):
    """Aggregate root with domain events"""
    
    def __init__(self, id: UUID | None = None):
        super().__init__(id)
        self._domain_events: List[DomainEvent] = []

    @property
    def domain_events(self) -> List[DomainEvent]:
        return self._domain_events.copy()

    def add_domain_event(self, event: DomainEvent):
        self._domain_events.append(event)

    def clear_domain_events(self):
        self._domain_events.clear()
