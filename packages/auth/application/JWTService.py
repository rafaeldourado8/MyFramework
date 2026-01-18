from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID
from jose import JWTError, jwt
from ..domain import Token, TokenPayload


class JWTService:
    """JWT token service"""
    
    def __init__(self, secret: str, algorithm: str = "HS256", 
                 access_expire_minutes: int = 60, refresh_expire_days: int = 7):
        self.secret = secret
        self.algorithm = algorithm
        self.access_expire = access_expire_minutes
        self.refresh_expire = refresh_expire_days

    def create_token(self, user_id: UUID, email: str, role: str) -> Token:
        """Create access and refresh tokens"""
        access = self._create_access(user_id, email, role)
        refresh = self._create_refresh(user_id)
        return Token(access, refresh)

    def _create_access(self, user_id: UUID, email: str, role: str) -> str:
        expire = datetime.utcnow() + timedelta(minutes=self.access_expire)
        payload = {
            "sub": str(user_id),
            "email": email,
            "role": role,
            "exp": expire,
            "type": "access"
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def _create_refresh(self, user_id: UUID) -> str:
        expire = datetime.utcnow() + timedelta(days=self.refresh_expire)
        payload = {
            "sub": str(user_id),
            "exp": expire,
            "type": "refresh"
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def verify_token(self, token: str, token_type: str = "access") -> Optional[TokenPayload]:
        """Verify and decode token"""
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            if payload.get("type") != token_type:
                return None
            
            return TokenPayload(
                user_id=UUID(payload["sub"]),
                email=payload.get("email", ""),
                role=payload.get("role", ""),
                exp=datetime.fromtimestamp(payload["exp"]),
                type=payload["type"]
            )
        except JWTError:
            return None
