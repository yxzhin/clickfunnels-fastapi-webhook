from typing import Any, Self

from httpx import AsyncClient

from ..config import get_config

config = get_config()


class ClickFunnelsClient:
    def __init__(self: Self, httpx_client: AsyncClient) -> None:
        self._httpx_client = httpx_client

    async def upsert_contact(
        self: Self,
        contact_id: str | int | None,
        body: dict[str, Any],
    ) -> None:
        """update contact details w/ given custom attributes"""
        workspace_id = config.CLICKFUNNELS_WORKSPACE_ID
        if contact_id:
            url = f"{config.api_base_url}/api/v2/workspaces/{workspace_id}/contacts/{contact_id}"
            response = await self._httpx_client.put(url, json=body)
        else:
            url = f"{config.api_base_url}/api/v2/workspaces/{workspace_id}/contacts"
            response = await self._httpx_client.post(url, json=body)

        response.raise_for_status()
