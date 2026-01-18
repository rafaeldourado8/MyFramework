"""
Core Framework - DDD Building Blocks

Opiniated framework for Domain-Driven Design with:
- Domain layer: Entity, ValueObject, AggregateRoot, DomainEvent
- Application layer: UseCase, DTO, Result, EventBus
- Infrastructure layer: Repository, UnitOfWork, Cache, Logger
- App layer: Application, Module, Config, Hooks
"""

from .domain import (
    Entity,
    ValueObject,
    AggregateRoot,
    DomainEvent,
    DomainException,
    ValidationException,
    BusinessRuleViolationException,
    NotFoundException,
    Repository
)

from .application import (
    UseCase,
    DTO,
    Result,
    EventBus
)

from .infrastructure import (
    UnitOfWork,
    Connection,
    MessageBroker,
    Cache,
    Logger,
    LogLevel
)

from .app import (
    Application,
    Module,
    Config,
    Hooks
)

__version__ = "1.0.0"

__all__ = [
    # Domain
    'Entity',
    'ValueObject',
    'AggregateRoot',
    'DomainEvent',
    'DomainException',
    'ValidationException',
    'BusinessRuleViolationException',
    'NotFoundException',
    'Repository',
    # Application
    'UseCase',
    'DTO',
    'Result',
    'EventBus',
    # Infrastructure
    'UnitOfWork',
    'Connection',
    'MessageBroker',
    'Cache',
    'Logger',
    'LogLevel',
    # App
    'Application',
    'Module',
    'Config',
    'Hooks'
]
