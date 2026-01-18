# Guia de Contribuição

Obrigado por considerar contribuir para o Framework Interno!

## Código de Conduta

- Seja respeitoso
- Seja colaborativo
- Seja construtivo

## Como Contribuir

### Reportar Bugs

Abra uma issue com:
- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs atual
- Versão do Python e packages

### Sugerir Features

Abra uma issue com:
- Descrição clara da feature
- Casos de uso
- Exemplos de código (se aplicável)

### Pull Requests

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/amazing`)
3. Faça suas mudanças
4. Adicione testes
5. Rode os testes (`pytest`)
6. Commit (`git commit -m 'Add amazing feature'`)
7. Push (`git push origin feature/amazing`)
8. Abra um Pull Request

## Padrões de Código

### Python

- Python 3.11+
- Type hints obrigatórios
- Docstrings em todas as classes e funções públicas
- Complexidade ciclomática < 3
- SOLID principles

### Exemplo

```python
from core import Entity
from uuid import UUID

class User(Entity):
    """User entity with name and email"""
    
    def __init__(self, id: UUID = None, name: str = "", email: str = ""):
        """
        Initialize user
        
        Args:
            id: User ID (auto-generated if None)
            name: User name
            email: User email
        """
        super().__init__(id)
        self.name = name
        self.email = email
    
    def update_name(self, name: str) -> None:
        """Update user name"""
        self.name = name
        self._touch()
```

### Testes

```python
import pytest
from uuid import uuid4

def test_user_creation():
    user = User(name="John", email="john@example.com")
    assert user.name == "John"
    assert user.email == "john@example.com"
    assert user.id is not None

def test_user_update_name():
    user = User(name="John")
    old_updated_at = user.updated_at
    
    user.update_name("Jane")
    
    assert user.name == "Jane"
    assert user.updated_at > old_updated_at
```

## Estrutura de Commits

Use conventional commits:

- `feat:` Nova feature
- `fix:` Bug fix
- `docs:` Documentação
- `refactor:` Refatoração
- `test:` Testes
- `chore:` Manutenção

Exemplos:
```
feat: add video streaming support
fix: resolve authentication token expiry
docs: update README with examples
refactor: simplify use case pattern
test: add tests for recording entity
chore: update dependencies
```

## Processo de Review

1. Automated checks (CI)
2. Code review por maintainer
3. Aprovação
4. Merge

## Dúvidas?

Abra uma discussion ou entre em contato.
