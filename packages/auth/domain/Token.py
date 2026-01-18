from core import ValueObject
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class TokenPayload:
    user_id: UUID
    email: str
    role: str
    exp: datetime
    type: str


class Token(ValueObject):
    """JWT Token value object"""
    
    def __init__(self, access_token: str, refresh_token: str = None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_type = "bearer"
