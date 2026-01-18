# Core Framework - Estrutura Visual

## Camadas e Responsabilidades

```
┌─────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   UseCase    │  │     DTO      │  │    Result    │      │
│  │              │  │              │  │              │      │
│  │  Orquestra   │  │  Transfere   │  │   Success/   │      │
│  │  operações   │  │    dados     │  │   Failure    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  ┌──────────────────────────────────────────────────┐       │
│  │              EventBus (Pub/Sub)                  │       │
│  └──────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │
                            │ usa
                            │
┌─────────────────────────────────────────────────────────────┐
│                      DOMAIN LAYER                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │    Entity    │  │ ValueObject  │  │ AggregateRoot│      │
│  │              │  │              │  │              │      │
│  │  Identidade  │  │   Imutável   │  │  Entity +    │      │
│  │  Timestamps  │  │  Equality    │  │   Events     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ DomainEvent  │  │ DomainExcept │  │  Repository  │      │
│  │              │  │              │  │              │      │
│  │   Eventos    │  │   Exceções   │  │  Interface   │      │
│  │  de negócio  │  │  de negócio  │  │ persistência │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │
                            │ implementa
                            │
┌─────────────────────────────────────────────────────────────┐
│                  INFRASTRUCTURE LAYER                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  UnitOfWork  │  │  Connection  │  │MessageBroker │      │
│  │              │  │              │  │              │      │
│  │  Transações  │  │   Database   │  │    Filas     │      │
│  │              │  │              │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │    Cache     │  │    Logger    │                         │
│  │              │  │              │                         │
│  │   Interface  │  │  Estruturado │                         │
│  │              │  │              │                         │
│  └──────────────┘  └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │
                            │ usa
                            │
┌─────────────────────────────────────────────────────────────┐
│                       APP LAYER                              │
│  ┌──────────────────────────────────────────────────┐       │
│  │                  Application                      │       │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐ │       │
│  │  │   Config   │  │   Hooks    │  │  EventBus  │ │       │
│  │  └────────────┘  └────────────┘  └────────────┘ │       │
│  │                                                   │       │
│  │  ┌────────────────────────────────────────────┐ │       │
│  │  │         Modules (Plugáveis)                │ │       │
│  │  │  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  │ │       │
│  │  │  │Module│  │Module│  │Module│  │Module│  │ │       │
│  │  │  │  1   │  │  2   │  │  3   │  │  N   │  │ │       │
│  │  │  └──────┘  └──────┘  └──────┘  └──────┘  │ │       │
│  │  └────────────────────────────────────────────┘ │       │
│  │                                                   │       │
│  │  ┌────────────────────────────────────────────┐ │       │
│  │  │            FastAPI App                     │ │       │
│  │  └────────────────────────────────────────────┘ │       │
│  └──────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

## Fluxo de Dados

```
HTTP Request
     │
     ▼
┌─────────────────┐
│  FastAPI Route  │
└─────────────────┘
     │
     ▼
┌─────────────────┐
│   Use Case      │ ◄─── DTO (Request)
└─────────────────┘
     │
     ├─► Repository ──► Database
     │
     ├─► Domain Logic
     │   └─► Entity/ValueObject
     │   └─► Business Rules
     │
     ├─► Domain Events
     │   └─► EventBus ──► Handlers
     │
     ▼
┌─────────────────┐
│     Result      │ ───► DTO (Response)
└─────────────────┘
     │
     ▼
HTTP Response
```

## Lifecycle

```
Application Start
     │
     ▼
┌─────────────────┐
│  Load Config    │
└─────────────────┘
     │
     ▼
┌─────────────────┐
│ Register Modules│
└─────────────────┘
     │
     ▼
┌─────────────────┐
│  Run Startup    │
│   Hooks         │
└─────────────────┘
     │
     ├─► Connect Database
     ├─► Initialize Cache
     ├─► Connect Message Broker
     ├─► Run Migrations
     │
     ▼
┌─────────────────┐
│ Module Startup  │
│   (each module) │
└─────────────────┘
     │
     ▼
┌─────────────────┐
│ Register Routes │
└─────────────────┘
     │
     ▼
┌─────────────────┐
│  App Running    │
└─────────────────┘
     │
     ▼
┌─────────────────┐
│ Module Shutdown │
│   (each module) │
└─────────────────┘
     │
     ▼
┌─────────────────┐
│  Run Shutdown   │
│    Hooks        │
└─────────────────┘
     │
     ├─► Close Connections
     ├─► Flush Logs
     ├─► Cleanup
     │
     ▼
Application Stop
```

## Exemplo de Uso

```python
# 1. Domain
class Email(ValueObject):
    def __init__(self, value: str):
        self.value = value

class User(Entity):
    def __init__(self, id=None, email: Email = None):
        super().__init__(id)
        self.email = email

# 2. Application
@dataclass
class CreateUserRequest(DTO):
    email: str

class CreateUser(UseCase[CreateUserRequest, Result[User]]):
    async def execute(self, request):
        email = Email(request.email)
        user = User(email=email)
        return Result.ok(user)

# 3. Module
class UserModule(Module):
    @property
    def name(self) -> str:
        return "users"
    
    def register_routes(self, app):
        @app.fastapi.post("/users")
        async def create(email: str):
            use_case = CreateUser()
            result = await use_case.execute(
                CreateUserRequest(email=email)
            )
            return {"id": str(result.value.id)}

# 4. Application
config = Config.from_env()
app = Application(config)
app.register_module(UserModule())
app.run()
```

## Princípios SOLID

```
┌─────────────────────────────────────────────────────────┐
│ S - Single Responsibility                               │
│     Cada classe tem UMA responsabilidade                │
│     Entity: Identidade                                  │
│     UseCase: Orquestração                               │
│     Repository: Persistência                            │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ O - Open/Closed                                         │
│     Extensível via Module                               │
│     Fechado para modificação no core                    │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ L - Liskov Substitution                                 │
│     Qualquer Repository pode substituir outro           │
│     Qualquer Cache pode substituir outro                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ I - Interface Segregation                               │
│     Interfaces pequenas e focadas                       │
│     Cache: get, set, delete                             │
│     Logger: log, debug, info, error                     │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ D - Dependency Inversion                                │
│     Dependências de abstrações                          │
│     UseCase depende de Repository (interface)           │
│     Não depende de PostgreSQLRepository (implementação) │
└─────────────────────────────────────────────────────────┘
```
