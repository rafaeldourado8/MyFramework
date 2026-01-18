# Decisões Arquiteturais - Core Framework

## ADR-001: Core Imutável

**Status**: Aceito

**Contexto**: Precisamos de um framework estável que não mude entre projetos.

**Decisão**: O core é imutável. Contém apenas:
- Building blocks DDD (Entity, ValueObject, AggregateRoot)
- Padrões de aplicação (UseCase, DTO, Result)
- Contratos de infraestrutura (interfaces)
- Lifecycle da aplicação (Application, Module)

**Consequências**:
- ✅ Estabilidade garantida
- ✅ Sem breaking changes
- ✅ Fácil de entender
- ⚠️ Extensões via módulos externos

---

## ADR-002: Complexidade Ciclomática < 3

**Status**: Aceito

**Contexto**: Código complexo é difícil de manter e testar.

**Decisão**: Toda função no core tem complexidade < 3.

**Consequências**:
- ✅ Código simples
- ✅ Fácil de testar
- ✅ Fácil de entender
- ⚠️ Mais funções pequenas

**Exemplos**:
```python
# ✅ Complexidade 1
def __init__(self, id=None):
    self._id = id or uuid4()

# ✅ Complexidade 2
async def execute(self, request):
    if not valid:
        return Result.fail("error")
    return Result.ok(value)
```

---

## ADR-003: SOLID em Todo Código

**Status**: Aceito

**Contexto**: SOLID garante código extensível e manutenível.

**Decisão**: Aplicar SOLID em todas as classes:
- **SRP**: Uma responsabilidade por classe
- **OCP**: Extensível via Module
- **LSP**: Interfaces substituíveis
- **ISP**: Interfaces pequenas
- **DIP**: Dependências de abstrações

**Consequências**:
- ✅ Código extensível
- ✅ Fácil de testar
- ✅ Baixo acoplamento
- ⚠️ Mais interfaces

---

## ADR-004: Abstrações na Infraestrutura

**Status**: Aceito

**Contexto**: Implementações concretas criam acoplamento.

**Decisão**: Core tem apenas interfaces:
- Repository (não PostgreSQLRepository)
- Cache (não RedisCache)
- Logger (não ElasticsearchLogger)

**Consequências**:
- ✅ Sem acoplamento
- ✅ Testável com mocks
- ✅ Troca de implementação fácil
- ⚠️ Implementações em packages/

---

## ADR-005: Module Pattern para Extensibilidade

**Status**: Aceito

**Contexto**: Apps precisam compor funcionalidades.

**Decisão**: Módulos plugáveis via Module interface:
```python
class Module(ABC):
    @property
    def name(self) -> str: pass
    async def on_startup(self, app): pass
    def register_routes(self, app): pass
```

**Consequências**:
- ✅ Composição fácil
- ✅ Módulos independentes
- ✅ Lifecycle controlado
- ⚠️ Comunicação via eventos

---

## ADR-006: EventBus para Desacoplamento

**Status**: Aceito

**Contexto**: Módulos não devem depender uns dos outros.

**Decisão**: Comunicação via eventos:
```python
# Módulo A publica
event_bus.publish(UserCreated(user_id))

# Módulo B escuta
event_bus.subscribe(UserCreated, handler)
```

**Consequências**:
- ✅ Desacoplamento total
- ✅ Extensível
- ✅ Testável
- ⚠️ Debugging mais difícil

---

## ADR-007: Config Opinioso

**Status**: Aceito

**Contexto**: Cada app carrega config de forma diferente.

**Decisão**: Config padronizado:
```python
config = Config.from_env()  # Variáveis de ambiente
config = Config.from_file("config.json")  # Arquivo
```

**Consequências**:
- ✅ Padrão único
- ✅ Fácil de usar
- ✅ Type-safe
- ⚠️ Menos flexibilidade

---

## ADR-008: FastAPI como Base

**Status**: Aceito

**Contexto**: Precisamos de um framework web.

**Decisão**: Application encapsula FastAPI:
```python
app = Application(config)
app.fastapi  # Acesso ao FastAPI
```

**Consequências**:
- ✅ FastAPI features disponíveis
- ✅ Lifecycle gerenciado
- ✅ Familiar para devs
- ⚠️ Acoplamento ao FastAPI

---

## ADR-009: Timestamps Automáticos

**Status**: Aceito

**Contexto**: Toda entidade precisa de auditoria básica.

**Decisão**: Entity tem created_at e updated_at:
```python
class Entity:
    def __init__(self):
        self._created_at = datetime.utcnow()
        self._updated_at = datetime.utcnow()
    
    def _touch(self):
        self._updated_at = datetime.utcnow()
```

**Consequências**:
- ✅ Auditoria automática
- ✅ Sem código repetido
- ✅ Padrão consistente
- ⚠️ Overhead mínimo

---

## ADR-010: Result Pattern para Erros

**Status**: Aceito

**Contexto**: Exceptions são caras e difíceis de rastrear.

**Decisão**: Use cases retornam Result:
```python
result = await use_case.execute(request)
if result.is_success:
    value = result.value
else:
    error = result.error
```

**Consequências**:
- ✅ Erros explícitos
- ✅ Type-safe
- ✅ Fácil de testar
- ⚠️ Mais verboso

---

## Resumo

| ADR | Decisão | Impacto |
|-----|---------|---------|
| 001 | Core imutável | Alto |
| 002 | Complexidade < 3 | Alto |
| 003 | SOLID | Alto |
| 004 | Abstrações infra | Médio |
| 005 | Module pattern | Alto |
| 006 | EventBus | Médio |
| 007 | Config opinioso | Baixo |
| 008 | FastAPI base | Alto |
| 009 | Timestamps auto | Baixo |
| 010 | Result pattern | Médio |
