from typing import Any, Self

from httpx import AsyncClient


class ClickFunnelsClient:
    def __init__(self: Self, httpx_client: AsyncClient) -> None:
        self._httpx_client = httpx_client

    async def upsert_contact(
        self: Self,
        contact_id: str | int | None,
        body: dict[str, Any],
    ) -> None:
        """update contact details w/ given custom attributes"""
        if contact_id:
            url = f"/contacts/{contact_id}"
            response = await self._httpx_client.put(url, json=body)
        else:
            url = "/contacts"
            response = await self._httpx_client.post(url, json=body)

        response.raise_for_status()
