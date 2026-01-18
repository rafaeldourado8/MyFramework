"""
Exemplo completo de uso do Core Framework

Demonstra:
- Entity e ValueObject
- UseCase com Result
- Module plugável
- Application lifecycle
"""

from dataclasses import dataclass
from uuid import UUID
from core import (
    Entity, ValueObject, UseCase, DTO, Result,
    Module, Application, Config, ValidationException
)


# ============ DOMAIN LAYER ============

class Email(ValueObject):
    """Email value object"""
    def __init__(self, value: str):
        if "@" not in value:
            raise ValidationException("Invalid email")
        self.value = value


class User(Entity):
    """User entity"""
    def __init__(self, id: UUID = None, name: str = "", email: Email = None):
        super().__init__(id)
        self.name = name
        self.email = email


# ============ APPLICATION LAYER ============

@dataclass
class CreateUserRequest(DTO):
    name: str
    email: str


class CreateUser(UseCase[CreateUserRequest, Result[User]]):
    """Create user use case"""
    
    async def execute(self, request: CreateUserRequest) -> Result[User]:
        try:
            email = Email(request.email)
            user = User(name=request.name, email=email)
            return Result.ok(user)
        except ValidationException as e:
            return Result.fail(str(e))


# ============ MODULE ============

class UserModule(Module):
    """User module"""
    
    @property
    def name(self) -> str:
        return "users"
    
    async def on_startup(self, app: Application):
        print(f"✅ {self.name} module started")
    
    def register_routes(self, app: Application):
        create_user = CreateUser()
        
        @app.fastapi.post("/users")
        async def create_user_endpoint(name: str, email: str):
            request = CreateUserRequest(name=name, email=email)
            result = await create_user.execute(request)
            
            if result.is_success:
                user = result.value
                return {
                    "id": str(user.id),
                    "name": user.name,
                    "email": user.email.value
                }
            return {"error": result.error}


# ============ APPLICATION ============

if __name__ == "__main__":
    # 1. Config
    config = Config.from_env()
    
    # 2. Create app
    app = Application(config)
    
    # 3. Register modules
    app.register_module(UserModule())
    
    # 4. Run
    print("🚀 Starting application...")
    app.run()
