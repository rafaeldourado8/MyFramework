# Core Framework

Framework opinioso para DDD com SOLID, baixa complexidade ciclomática e Clean Code.

## 🎯 Filosofia

- **Opinioso**: Decisões arquiteturais já tomadas
- **SOLID**: Princípios aplicados em todo código
- **Baixa Complexidade**: Funções com complexidade < 3
- **DDD**: Building blocks corretos
- **Imutável**: Core não muda, apenas estende

## 📦 Estrutura

```
core/
├── domain/           # DDD building blocks
│   ├── Entity
│   ├── ValueObject
│   ├── AggregateRoot
│   ├── DomainEvent
│   ├── DomainException
│   └── Repository
├── application/      # Use cases
│   ├── UseCase
│   ├── DTO
│   ├── Result
│   └── EventBus
├── infrastructure/   # Contratos
│   ├── UnitOfWork
│   ├── Connection
│   ├── MessageBroker
│   ├── Cache
│   └── Logger
└── app/             # Lifecycle
    ├── Application
    ├── Module
    ├── Config
    └── Hooks
```

## 🚀 Quick Start

```python
from core import Application, Config, Module

# 1. Configuração
config = Config.from_env()

# 2. Criar aplicação
app = Application(config)

# 3. Registrar módulos
app.register_module(MyModule())

# 4. Rodar
app.run()
```

## 📖 Exemplos

### Entity

```python
from core import Entity

class User(Entity):
    def __init__(self, id=None, name: str = ""):
        super().__init__(id)
        self.name = name
```

### Value Object

```python
from core import ValueObject

class Email(ValueObject):
    def __init__(self, value: str):
        if "@" not in value:
            raise ValueError("Invalid email")
        self.value = value
```

### Use Case

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
```

### Module

```python
from core import Module, Application

class UserModule(Module):
    @property
    def name(self) -> str:
        return "users"
    
    async def on_startup(self, app: Application):
        print("User module started")
    
    def register_routes(self, app: Application):
        @app.fastapi.get("/users")
        async def list_users():
            return {"users": []}
```

## 🎨 SOLID Aplicado

### Single Responsibility
Cada classe tem uma única responsabilidade:
- Entity: Identidade
- ValueObject: Valor imutável
- UseCase: Orquestração
- Repository: Persistência

### Open/Closed
Extensível via Module, sem modificar core.

### Liskov Substitution
Todas interfaces podem ser substituídas.

### Interface Segregation
Interfaces pequenas e focadas.

### Dependency Inversion
Dependências de abstrações, não implementações.

## 📊 Complexidade

Todas funções têm complexidade ciclomática < 3:
- Entity.__init__: 1
- UseCase.execute: 1-2
- Application.startup: 2

## 🔒 Imutabilidade

O core é imutável. Não modifique:
- Domain building blocks
- Application patterns
- Infrastructure contracts

Estenda via:
- Módulos (packages/)
- Apps (apps/)

## 📚 Próximos Passos

1. Criar módulos reutilizáveis (auth, rbac, observability)
2. Migrar apps para usar o core
3. Validar boundaries
4. Documentar decisões arquiteturais
