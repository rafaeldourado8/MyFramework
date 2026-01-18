# Core Framework

Framework DDD opinioso com SOLID e baixa complexidade.

## Instalação

```bash
pip install -e packages/core
```

## Conceitos

### Entity

Entidade com identidade única e timestamps automáticos.

```python
from core import Entity
from uuid import UUID

class User(Entity):
    def __init__(self, id: UUID = None, name: str = ""):
        super().__init__(id)
        self.name = name

# Uso
user = User(name="John Doe")
print(user.id)  # UUID gerado automaticamente
print(user.created_at)  # Timestamp de criação
```

### Value Object

Objeto imutável com igualdade por valor.

```python
from core import ValueObject, ValidationException

class Email(ValueObject):
    def __init__(self, value: str):
        if "@" not in value:
            raise ValidationException("Invalid email")
        self.value = value

# Uso
email1 = Email("user@example.com")
email2 = Email("user@example.com")
assert email1 == email2  # True (igualdade por valor)
```

### Use Case

Orquestração de operações de negócio.

```python
from core import UseCase, DTO, Result
from dataclasses import dataclass

@dataclass
class CreateUserRequest(DTO):
    name: str
    email: str

class CreateUser(UseCase[CreateUserRequest, Result[User]]):
    async def execute(self, request: CreateUserRequest) -> Result[User]:
        user = User(name=request.name)
        return Result.ok(user)

# Uso
use_case = CreateUser()
result = await use_case.execute(CreateUserRequest(name="John", email="john@example.com"))

if result.is_success:
    user = result.value
```

### Application

Bootstrap da aplicação com lifecycle.

```python
from core import Application, Config, Module

class UserModule(Module):
    @property
    def name(self) -> str:
        return "users"
    
    def register_routes(self, app: Application):
        @app.fastapi.get("/users")
        async def list_users():
            return {"users": []}

# Uso
config = Config.from_env()
app = Application(config)
app.register_module(UserModule())
app.run()
```

## API Reference

### Domain Layer

- **Entity**: Base entity com id e timestamps
- **ValueObject**: Objeto imutável
- **AggregateRoot**: Entity com domain events
- **DomainEvent**: Evento de domínio
- **DomainException**: Exceções de negócio
- **Repository**: Interface de persistência

### Application Layer

- **UseCase**: Interface para use cases
- **DTO**: Data Transfer Object
- **Result**: Result pattern (success/failure)
- **EventBus**: Pub/sub para eventos

### Infrastructure Layer

- **UnitOfWork**: Transações
- **Connection**: Pool de conexões
- **MessageBroker**: Interface para filas
- **Cache**: Interface para cache
- **Logger**: Logger estruturado

### App Layer

- **Application**: Bootstrap da aplicação
- **Module**: Módulos plugáveis
- **Config**: Carregamento de configuração
- **Hooks**: Lifecycle hooks

## Princípios

### SOLID

- **S**ingle Responsibility: Uma responsabilidade por classe
- **O**pen/Closed: Extensível via Module
- **L**iskov Substitution: Interfaces substituíveis
- **I**nterface Segregation: Interfaces pequenas
- **D**ependency Inversion: Dependências de abstrações

### Complexidade

Todas as funções têm complexidade ciclomática < 3.

### Type Safety

Type hints em todo código para melhor IDE support.

## Exemplos

Veja [examples/complete_example.py](../packages/core/examples/complete_example.py) para exemplo completo.
