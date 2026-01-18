import httpx
from ..domain import MediaMTXClient


class MediaMTXClientImpl(MediaMTXClient):
    """MediaMTX HTTP API client implementation"""
    
    def __init__(self, host: str = "localhost", port: int = 9997):
        self.base_url = f"http://{host}:{port}"

    async def start_stream(self, stream_id: str, source_url: str) -> bool:
        """Start stream via MediaMTX API"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/v3/config/paths/add/{stream_id}",
                    json={"source": source_url}
                )
                return response.status_code == 200
            except:
                return False

    async def stop_stream(self, stream_id: str) -> bool:
        """Stop stream via MediaMTX API"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.delete(
                    f"{self.base_url}/v3/config/paths/remove/{stream_id}"
                )
                return response.status_code == 200
            except:
                return False

    async def get_stream_status(self, stream_id: str) -> dict:
        """Get stream status from MediaMTX"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/v3/paths/get/{stream_id}"
                )
                return response.json() if response.status_code == 200 else {}
            except:
                return {}
