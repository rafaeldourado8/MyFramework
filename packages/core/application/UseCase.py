from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TRequest = TypeVar('TRequest')
TResponse = TypeVar('TResponse')


class UseCase(ABC, Generic[TRequest, TResponse]):
    """Base use case"""
    
    @abstractmethod
    async def execute(self, request: TRequest) -> TResponse:
        """Execute use case"""
        pass
