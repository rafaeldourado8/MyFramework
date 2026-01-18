# Auth Package

Autenticação JWT com password hashing usando bcrypt.

## Instalação

```bash
pip install -e packages/auth
```

## Dependências

- `passlib[bcrypt]>=1.7.4`
- `python-jose[cryptography]>=3.3.0`
- `fastapi>=0.104.0`

## Quick Start

```python
from auth import AuthService, JWTService, create_auth_dependency
from uuid import uuid4

# Setup
jwt_service = JWTService(
    secret="your-secret-key-change-in-production",
    algorithm="HS256",
    access_expire_minutes=60,
    refresh_expire_days=7
)
auth_service = AuthService(jwt_service)

# Hash password
result = auth_service.hash_password("MyPassword123")
if result.is_success:
    hashed = result.value

# Verify password
is_valid = auth_service.verify_password("MyPassword123", hashed)

# Create tokens
user_id = uuid4()
token = auth_service.create_tokens(user_id, "user@example.com", "user")
print(token.access_token)
print(token.refresh_token)

# Verify token
result = auth_service.verify_access_token(token.access_token)
if result.is_success:
    user_id = result.value
```

## FastAPI Integration

```python
from fastapi import FastAPI, Depends
from auth import AuthService, JWTService, create_auth_dependency
from uuid import UUID

app = FastAPI()

# Setup
jwt_service = JWTService(secret="your-secret-key")
auth_service = AuthService(jwt_service)
get_current_user = create_auth_dependency(auth_service)

# Public route
@app.post("/login")
async def login(email: str, password: str):
    # Verify user credentials (your logic)
    user = get_user_by_email(email)
    
    if not auth_service.verify_password(password, user.password_hash):
        return {"error": "Invalid credentials"}
    
    # Create tokens
    token = auth_service.create_tokens(user.id, user.email, user.role)
    
    return {
        "access_token": token.access_token,
        "refresh_token": token.refresh_token,
        "token_type": "bearer"
    }

# Protected route
@app.get("/me")
async def get_me(user_id: UUID = Depends(get_current_user)):
    user = get_user_by_id(user_id)
    return {"user": user}

# Refresh token
@app.post("/refresh")
async def refresh_token(refresh_token: str):
    result = auth_service.verify_refresh_token(refresh_token)
    
    if result.is_failure:
        return {"error": "Invalid refresh token"}
    
    user_id = result.value
    user = get_user_by_id(user_id)
    
    # Create new tokens
    token = auth_service.create_tokens(user.id, user.email, user.role)
    
    return {
        "access_token": token.access_token,
        "refresh_token": token.refresh_token
    }
```

## API Reference

### Password

Value object para password com hashing e validação.

```python
from auth import Password

# Create with plain password
password = Password(plain="MyPassword123")
hashed = password.hash

# Create with hash
password = Password(hashed=hashed)

# Verify
is_valid = password.verify("MyPassword123")  # True
```

**Requisitos de senha:**
- Mínimo 8 caracteres
- Pelo menos uma letra maiúscula
- Pelo menos uma letra minúscula
- Pelo menos um dígito

### JWTService

Serviço para geração e verificação de tokens JWT.

```python
from auth import JWTService
from uuid import uuid4

jwt = JWTService(
    secret="your-secret-key",
    algorithm="HS256",
    access_expire_minutes=60,
    refresh_expire_days=7
)

# Create token
token = jwt.create_token(
    user_id=uuid4(),
    email="user@example.com",
    role="user"
)

# Verify access token
payload = jwt.verify_token(token.access_token, "access")
if payload:
    print(payload.user_id)
    print(payload.email)
    print(payload.role)

# Verify refresh token
payload = jwt.verify_token(token.refresh_token, "refresh")
```

### AuthService

Serviço de autenticação completo.

```python
from auth import AuthService, JWTService

auth = AuthService(JWTService(secret="key"))

# Hash password
result = auth.hash_password("password")
hashed = result.value

# Verify password
is_valid = auth.verify_password("password", hashed)

# Create tokens
token = auth.create_tokens(user_id, email, role)

# Verify access token
result = auth.verify_access_token(token.access_token)
user_id = result.value

# Verify refresh token
result = auth.verify_refresh_token(token.refresh_token)
user_id = result.value
```

## Configuração

### Variáveis de Ambiente

```bash
JWT_SECRET=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Carregar do .env

```python
import os
from auth import JWTService

jwt = JWTService(
    secret=os.getenv("JWT_SECRET"),
    algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
    access_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)),
    refresh_expire_days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
)
```

## Segurança

### Secret Key

**NUNCA** use a secret key padrão em produção. Gere uma chave segura:

```python
import secrets
secret = secrets.token_urlsafe(32)
print(secret)
```

### HTTPS

Sempre use HTTPS em produção para proteger os tokens em trânsito.

### Token Storage

**Frontend:**
- Armazene access token em memória (variável)
- Armazene refresh token em httpOnly cookie

**Não armazene tokens em:**
- localStorage (vulnerável a XSS)
- sessionStorage (vulnerável a XSS)

## Troubleshooting

### Token inválido

- Verificar se secret key está correta
- Verificar se token não expirou
- Verificar se algoritmo está correto

### Password não valida

- Verificar requisitos de senha (8+ chars, upper, lower, digit)
- Verificar se hash está correto

### 401 Unauthorized

- Verificar se token está sendo enviado no header
- Formato: `Authorization: Bearer <token>`
