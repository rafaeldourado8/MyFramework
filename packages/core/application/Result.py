from typing import Generic, TypeVar, Optional

T = TypeVar('T')


class Result(Generic[T]):
    """Result pattern for success/failure"""
    
    def __init__(self, success: bool, value: Optional[T] = None, error: Optional[str] = None):
        self._success = success
        self._value = value
        self._error = error

    @property
    def is_success(self) -> bool:
        return self._success

    @property
    def is_failure(self) -> bool:
        return not self._success

    @property
    def value(self) -> T:
        if not self._success:
            raise ValueError("Cannot get value from failed result")
        return self._value

    @property
    def error(self) -> str:
        return self._error

    @staticmethod
    def ok(value: T = None) -> 'Result[T]':
        return Result(True, value)

    @staticmethod
    def fail(error: str) -> 'Result[T]':
        return Result(False, error=error)
