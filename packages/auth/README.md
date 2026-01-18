# Auth Package

Authentication package with JWT tokens and password hashing.

## Features

- Password hashing with bcrypt
- Password strength validation
- JWT token generation (access + refresh)
- Token verification
- FastAPI authentication dependency

## Usage

### Password Hashing

```python
from auth import Password

# Create and hash password
password = Password(plain="MyPassword123")
hashed = password.hash

# Verify password
password = Password(hashed=hashed)
is_valid = password.verify("MyPassword123")  # True
```

### JWT Tokens

```python
from auth import JWTService, AuthService
from uuid import uuid4

# Setup
jwt_service = JWTService(secret="your-secret-key")
auth_service = AuthService(jwt_service)

# Create tokens
user_id = uuid4()
token = auth_service.create_tokens(user_id, "user@example.com", "user")

# Verify token
result = auth_service.verify_access_token(token.access_token)
if result.is_success:
    user_id = result.value
```

### FastAPI Integration

```python
from fastapi import FastAPI, Depends
from auth import JWTService, AuthService, create_auth_dependency
from uuid import UUID

app = FastAPI()

# Setup
jwt_service = JWTService(secret="your-secret-key")
auth_service = AuthService(jwt_service)
get_current_user = create_auth_dependency(auth_service)

# Protected route
@app.get("/protected")
async def protected(user_id: UUID = Depends(get_current_user)):
    return {"user_id": str(user_id)}
```

## Password Requirements

- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit

## Token Types

- **Access Token**: Short-lived (default 60 minutes)
- **Refresh Token**: Long-lived (default 7 days)

## Configuration

```python
jwt_service = JWTService(
    secret="your-secret-key",
    algorithm="HS256",
    access_expire_minutes=60,
    refresh_expire_days=7
)
```
