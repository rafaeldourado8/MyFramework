from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from uuid import UUID
from ..application import AuthService

security = HTTPBearer()


def create_auth_dependency(auth_service: AuthService):
    """Factory for auth dependency"""
    
    async def get_current_user(credentials = Depends(security)) -> UUID:
        """Get current authenticated user"""
        result = auth_service.verify_access_token(credentials.credentials)
        
        if result.is_failure:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return result.value
    
    return get_current_user
