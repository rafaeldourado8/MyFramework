from uuid import UUID
from core import Result
from ..domain import Password, Token
from .JWTService import JWTService


class AuthService:
    """Authentication service"""
    
    def __init__(self, jwt_service: JWTService):
        self.jwt = jwt_service

    def hash_password(self, plain: str) -> Result[str]:
        """Hash password"""
        try:
            password = Password(plain=plain)
            return Result.ok(password.hash)
        except Exception as e:
            return Result.fail(str(e))

    def verify_password(self, plain: str, hashed: str) -> bool:
        """Verify password"""
        password = Password(hashed=hashed)
        return password.verify(plain)

    def create_tokens(self, user_id: UUID, email: str, role: str) -> Token:
        """Create authentication tokens"""
        return self.jwt.create_token(user_id, email, role)

    def verify_access_token(self, token: str) -> Result[UUID]:
        """Verify access token"""
        payload = self.jwt.verify_token(token, "access")
        if not payload:
            return Result.fail("Invalid token")
        return Result.ok(payload.user_id)

    def verify_refresh_token(self, token: str) -> Result[UUID]:
        """Verify refresh token"""
        payload = self.jwt.verify_token(token, "refresh")
        if not payload:
            return Result.fail("Invalid refresh token")
        return Result.ok(payload.user_id)
