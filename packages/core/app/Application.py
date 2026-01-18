from typing import List, Optional
from fastapi import FastAPI
from .Config import Config
from .Module import Module
from .Hooks import Hooks
from ..application.EventBus import EventBus


class Application:
    """Framework application"""
    
    def __init__(self, config: Config, fastapi_app: Optional[FastAPI] = None):
        self.config = config
        self.fastapi = fastapi_app or FastAPI()
        self.modules: List[Module] = []
        self.hooks = Hooks()
        self.event_bus = EventBus()

    def register_module(self, module: Module):
        """Register module"""
        self.modules.append(module)
        module.register_routes(self)

    async def startup(self):
        """Startup lifecycle"""
        await self.hooks.run_startup()
        for module in self.modules:
            await module.on_startup(self)

    async def shutdown(self):
        """Shutdown lifecycle"""
        for module in self.modules:
            await module.on_shutdown(self)
        await self.hooks.run_shutdown()

    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """Run application"""
        import uvicorn
        
        @self.fastapi.on_event("startup")
        async def on_startup():
            await self.startup()

        @self.fastapi.on_event("shutdown")
        async def on_shutdown():
            await self.shutdown()

        uvicorn.run(self.fastapi, host=host, port=port)
