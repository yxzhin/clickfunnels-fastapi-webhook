from collections.abc import AsyncGenerator
from typing import Any, Self

from dishka import Provider, Scope, provide
from httpx import AsyncClient

from ...config import get_config

config = get_config()


class AsyncClientProvider(Provider):
    def __init__(self: Self, httpx_client: AsyncClient | None = None) -> None:
        super().__init__()
        self._httpx_client = httpx_client
        self._headers = {
            "Authorization": f"Bearer {config.CLICKFUNNELS_API_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "clickfunnels-fastapi-webhook/1.0",
        }
        self._base_url = f"{config.api_base_url}/api/v2/workspaces/{config.CLICKFUNNELS_WORKSPACE_ID}"

    @provide(scope=Scope.APP)
    async def async_client(self: Self) -> AsyncGenerator[AsyncClient, Any]:
        if self._httpx_client is not None:
            yield self._httpx_client
        else:
            async with AsyncClient(
                timeout=15.0,
                headers=self._headers,
                base_url=self._base_url,
            ) as httpx_client:
                yield httpx_client
