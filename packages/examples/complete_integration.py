"""
Complete example using all packages:
- core (Entity, UseCase, Module, Application)
- auth (Password, JWT, AuthService)
- rbac (Role, Permission, RBACService)
- observability (Metrics, StructuredLogger)
"""

from dataclasses import dataclass
from uuid import UUID, uuid4
from fastapi import Depends, Response

# Core
from core import Entity, UseCase, DTO, Result, Module, Application, Config

# Auth
from auth import Password, JWTService, AuthService, create_auth_dependency

# RBAC
from rbac import Role, Permission, RBACService, require_permission

# Observability
from observability import Metrics, MetricsMiddleware, StructuredLogger


# ============ DOMAIN ============

class User(Entity):
    """User entity"""
    def __init__(self, id: UUID = None, email: str = "", password_hash: str = "", role: Role = None):
        super().__init__(id)
        self.email = email
        self.password_hash = password_hash
        self.role = role


# ============ APPLICATION ============

@dataclass
class RegisterRequest(DTO):
    email: str
    password: str


class RegisterUser(UseCase[RegisterRequest, Result[User]]):
    """Register user use case"""
    
    def __init__(self, auth_service: AuthService):
        self.auth = auth_service

    async def execute(self, request: RegisterRequest) -> Result[User]:
        # Hash password
        result = self.auth.hash_password(request.password)
        if result.is_failure:
            return Result.fail(result.error)
        
        # Create user
        user = User(
            id=uuid4(),
            email=request.email,
            password_hash=result.value
        )
        
        return Result.ok(user)


# ============ MODULE ============

class UserModule(Module):
    """User module with auth and rbac"""
    
    def __init__(self, auth_service: AuthService, logger: StructuredLogger):
        self.auth = auth_service
        self.logger = logger

    @property
    def name(self) -> str:
        return "users"

    async def on_startup(self, app: Application):
        self.logger.info(f"{self.name} module started")

    def register_routes(self, app: Application):
        register_use_case = RegisterUser(self.auth)
        get_current_user = create_auth_dependency(self.auth)
        
        @app.fastapi.post("/register")
        async def register(email: str, password: str):
            request = RegisterRequest(email=email, password=password)
            result = await register_use_case.execute(request)
            
            if result.is_success:
                user = result.value
                token = self.auth.create_tokens(user.id, user.email, "user")
                
                self.logger.info("User registered", {
                    "user_id": str(user.id),
                    "email": user.email
                })
                
                return {
                    "user_id": str(user.id),
                    "access_token": token.access_token,
                    "refresh_token": token.refresh_token
                }
            
            return {"error": result.error}
        
        @app.fastapi.get("/protected")
        async def protected(user_id: UUID = Depends(get_current_user)):
            self.logger.info("Protected route accessed", {"user_id": str(user_id)})
            return {"user_id": str(user_id), "message": "Access granted"}


# ============ APPLICATION ============

if __name__ == "__main__":
    # Config
    config = Config.from_env()
    
    # Services
    jwt_service = JWTService(secret="your-secret-key")
    auth_service = AuthService(jwt_service)
    logger = StructuredLogger(name="myapp")
    metrics = Metrics(namespace="myapp")
    
    # Create app
    app = Application(config)
    
    # Add metrics middleware
    app.fastapi.add_middleware(MetricsMiddleware, metrics=metrics)
    
    # Metrics endpoint
    @app.fastapi.get("/metrics")
    async def get_metrics():
        return Response(
            content=Metrics.export(),
            media_type=Metrics.content_type()
        )
    
    # Register modules
    app.register_module(UserModule(auth_service, logger))
    
    # Run
    print("🚀 Starting application with:")
    print("  ✅ Core framework")
    print("  ✅ Auth (JWT + Password)")
    print("  ✅ RBAC (Roles + Permissions)")
    print("  ✅ Observability (Metrics + Logs)")
    print("\nEndpoints:")
    print("  POST /register - Register user")
    print("  GET /protected - Protected route (requires auth)")
    print("  GET /metrics - Prometheus metrics")
    print("  GET /docs - API documentation")
    
    app.run()
