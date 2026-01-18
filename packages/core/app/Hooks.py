from typing import Callable, Awaitable, List


class Hooks:
    """Lifecycle hooks"""
    
    def __init__(self):
        self._startup: List[Callable[[], Awaitable[None]]] = []
        self._shutdown: List[Callable[[], Awaitable[None]]] = []

    def on_startup(self, func: Callable[[], Awaitable[None]]):
        """Register startup hook"""
        self._startup.append(func)
        return func

    def on_shutdown(self, func: Callable[[], Awaitable[None]]):
        """Register shutdown hook"""
        self._shutdown.append(func)
        return func

    async def run_startup(self):
        """Execute all startup hooks"""
        for hook in self._startup:
            await hook()

    async def run_shutdown(self):
        """Execute all shutdown hooks"""
        for hook in self._shutdown:
            await hook()
