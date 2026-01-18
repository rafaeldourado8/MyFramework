import os
from typing import Any, Dict
from pathlib import Path
import json


class Config:
    """Configuration loader"""
    
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    @classmethod
    def from_env(cls, prefix: str = "") -> "Config":
        """Load from environment variables"""
        data = {}
        for key, value in os.environ.items():
            if not prefix or key.startswith(prefix):
                clean_key = key.replace(prefix, "").lower()
                data[clean_key] = value
        return cls(data)

    @classmethod
    def from_file(cls, path: str) -> "Config":
        """Load from JSON file"""
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        
        with open(file_path) as f:
            data = json.load(f)
        return cls(data)

    def get(self, key: str, default: Any = None) -> Any:
        """Get config value"""
        return self._data.get(key, default)

    def require(self, key: str) -> Any:
        """Get required config value"""
        if key not in self._data:
            raise ValueError(f"Required config key missing: {key}")
        return self._data[key]
