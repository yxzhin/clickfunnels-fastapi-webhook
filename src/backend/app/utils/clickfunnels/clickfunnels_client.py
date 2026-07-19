from typing import Any, Self

from httpx import AsyncClient


class ClickFunnelsClient:
    def __init__(self: Self, httpx_client: AsyncClient) -> None:
        self._httpx_client = httpx_client

    async def update_or_create_contact(
        self: Self,
        body: dict[str, Any],
    ) -> None:
        """update or create contact w/ given details"""
        response = await self._httpx_client.post("/contacts/upsert", json=body)

        response.raise_for_status()
