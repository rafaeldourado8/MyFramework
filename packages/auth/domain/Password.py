from core import ValueObject, ValidationException
from passlib.context import CryptContext
import re

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Password(ValueObject):
    """Password value object with hashing and validation"""
    
    def __init__(self, plain: str = None, hashed: str = None):
        if plain:
            if not self._validate(plain):
                raise ValidationException("Password must be 8+ chars with upper, lower, and digit")
            self._hashed = pwd_context.hash(plain[:72])
        elif hashed:
            self._hashed = hashed
        else:
            raise ValidationException("Password or hash required")

    @staticmethod
    def _validate(password: str) -> bool:
        return (len(password) >= 8 and 
                re.search(r"[A-Z]", password) and 
                re.search(r"[a-z]", password) and 
                re.search(r"\d", password))

    def verify(self, plain: str) -> bool:
        return pwd_context.verify(plain[:72], self._hashed)

    @property
    def hash(self) -> str:
        return self._hashed
