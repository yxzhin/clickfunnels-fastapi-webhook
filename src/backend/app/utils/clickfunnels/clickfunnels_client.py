from typing import Any, Self

from httpx import AsyncClient

from ...config import get_config

config = get_config()


class ClickFunnelsAsyncClient(AsyncClient):
    def __init__(self: Self, *args, **kwargs) -> None:
        headers = {
            "Authorization": f"Bearer {config.CLICKFUNNELS_API_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "clickfunnels-fastapi-webhook/1.0",
        }
        base_url = config.api_base_url
        super().__init__(
            *args,
            **kwargs,
            headers=headers,
            base_url=base_url,
            timeout=15.0,
        )


class ClickFunnelsClient:
    def __init__(self: Self, httpx_client: ClickFunnelsAsyncClient) -> None:
        self._httpx_client = httpx_client

    async def update_or_create_contact(
        self: Self,
        body: dict[str, Any],
    ) -> None:
        """update or create contact w/ given details"""
        response = await self._httpx_client.post("/contacts/upsert", json=body)

        response.raise_for_status()
