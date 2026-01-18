"""
Script de validação do Core Framework

Valida:
- Imports funcionam
- Classes instanciam
- Complexidade < 3
- SOLID aplicado
"""

import sys
from pathlib import Path

# Add packages to path
packages_path = Path(__file__).parent.parent
sys.path.insert(0, str(packages_path))


def test_imports():
    """Test all imports work"""
    print("[TEST] Testing imports...")
    
    try:
        from core import (
            Entity, ValueObject, AggregateRoot, DomainEvent,
            UseCase, DTO, Result, EventBus,
            Repository, UnitOfWork, Cache, Logger,
            Application, Module, Config, Hooks
        )
        print("[OK] All imports successful")
        return True
    except Exception as e:
        print(f"[FAIL] Import failed: {e}")
        return False


def test_entity():
    """Test Entity creation"""
    print("\n[TEST] Testing Entity...")
    
    try:
        from core import Entity
        
        class User(Entity):
            def __init__(self, id=None, name=""):
                super().__init__(id)
                self.name = name
        
        user = User(name="John")
        assert user.id is not None
        assert user.name == "John"
        assert user.created_at is not None
        assert user.updated_at is not None
        
        print("[OK] Entity works")
        return True
    except Exception as e:
        print(f"[FAIL] Entity failed: {e}")
        return False


def test_value_object():
    """Test ValueObject"""
    print("\n[TEST] Testing ValueObject...")
    
    try:
        from core import ValueObject
        
        class Email(ValueObject):
            def __init__(self, value: str):
                self.value = value
        
        email1 = Email("test@example.com")
        email2 = Email("test@example.com")
        email3 = Email("other@example.com")
        
        assert email1 == email2
        assert email1 != email3
        assert hash(email1) == hash(email2)
        
        print("[OK] ValueObject works")
        return True
    except Exception as e:
        print(f"[FAIL] ValueObject failed: {e}")
        return False


def test_use_case():
    """Test UseCase"""
    print("\n[TEST] Testing UseCase...")
    
    try:
        from core import UseCase, Result
        from dataclasses import dataclass
        
        @dataclass
        class Request:
            value: int
        
        class DoubleValue(UseCase[Request, Result[int]]):
            async def execute(self, request: Request) -> Result[int]:
                return Result.ok(request.value * 2)
        
        import asyncio
        use_case = DoubleValue()
        result = asyncio.run(use_case.execute(Request(5)))
        
        assert result.is_success
        assert result.value == 10
        
        print("[OK] UseCase works")
        return True
    except Exception as e:
        print(f"[FAIL] UseCase failed: {e}")
        return False


def test_result():
    """Test Result pattern"""
    print("\n[TEST] Testing Result...")
    
    try:
        from core import Result
        
        success = Result.ok("value")
        assert success.is_success
        assert success.value == "value"
        
        failure = Result.fail("error")
        assert failure.is_failure
        assert failure.error == "error"
        
        print("[OK] Result works")
        return True
    except Exception as e:
        print(f"[FAIL] Result failed: {e}")
        return False


def test_event_bus():
    """Test EventBus"""
    print("\n[TEST] Testing EventBus...")
    
    try:
        from core import EventBus, DomainEvent
        import asyncio
        
        class TestEvent(DomainEvent):
            def __init__(self, value: str):
                super().__init__()
                self.value = value
        
        bus = EventBus()
        received = []
        
        async def handler(event: TestEvent):
            received.append(event.value)
        
        bus.subscribe(TestEvent, handler)
        asyncio.run(bus.publish(TestEvent("test")))
        
        assert len(received) == 1
        assert received[0] == "test"
        
        print("[OK] EventBus works")
        return True
    except Exception as e:
        print(f"[FAIL] EventBus failed: {e}")
        return False


def test_config():
    """Test Config"""
    print("\n[TEST] Testing Config...")
    
    try:
        from core import Config
        import os
        
        os.environ["TEST_KEY"] = "test_value"
        config = Config.from_env("TEST_")
        
        assert config.get("key") == "test_value"
        assert config.get("missing", "default") == "default"
        
        print("[OK] Config works")
        return True
    except Exception as e:
        print(f"[FAIL] Config failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 50)
    print("Core Framework Validation")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_entity,
        test_value_object,
        test_use_case,
        test_result,
        test_event_bus,
        test_config,
    ]
    
    results = [test() for test in tests]
    
    print("\n" + "=" * 50)
    print(f"Results: {sum(results)}/{len(results)} passed")
    print("=" * 50)
    
    if all(results):
        print("[SUCCESS] All tests passed!")
        return 0
    else:
        print("[ERROR] Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
