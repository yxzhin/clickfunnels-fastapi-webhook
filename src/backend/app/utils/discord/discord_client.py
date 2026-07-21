from typing import Self

from httpx import AsyncClient

from ...config import get_config

config = get_config()


class DiscordAsyncClient(AsyncClient):
    def __init__(self: Self, *args, **kwargs) -> None:
        super().__init__(
            *args,
            **kwargs,
            timeout=15.0,
        )


class DiscordClient:
    def __init__(self: Self, httpx_client: DiscordAsyncClient) -> None:
        self._httpx_client = httpx_client

    async def post_webhook(
        self: Self,
        content: str,
    ) -> None:
        response = await self._httpx_client.post(
            config.DISCORD_WEBHOOK_URL,
            json={
                "content": content,
            },
        )
        response.raise_for_status()
