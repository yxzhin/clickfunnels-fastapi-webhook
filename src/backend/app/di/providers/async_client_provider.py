from collections.abc import AsyncGenerator
from typing import Any, Self

from dishka import Provider, Scope, provide
from httpx import AsyncClient

from ...config import get_config

config = get_config()


class AsyncClientProvider(Provider):
    def __init__(self: Self) -> None:
        super().__init__()
        self._headers = {
            "Authorization": f"Bearer {config.CLICKFUNNELS_API_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "clickfunnels-fastapi-webhook/1.0",
        }

    @provide(scope=Scope.APP)
    async def async_client(self: Self) -> AsyncGenerator[AsyncClient, Any]:
        async with AsyncClient(timeout=15.0, headers=self._headers) as httpx_client:
            yield httpx_client
