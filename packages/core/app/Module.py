from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Application import Application


class Module(ABC):
    """Pluggable module interface"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Module name"""
        pass

    async def on_startup(self, app: "Application"):
        """Startup hook"""
        pass

    async def on_shutdown(self, app: "Application"):
        """Shutdown hook"""
        pass

    def register_routes(self, app: "Application"):
        """Register routes"""
        pass
