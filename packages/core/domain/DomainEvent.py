from abc import ABC
from datetime import datetime
from uuid import UUID, uuid4


class DomainEvent(ABC):
    """Base domain event"""
    
    def __init__(self):
        self.event_id: UUID = uuid4()
        self.occurred_on: datetime = datetime.utcnow()
