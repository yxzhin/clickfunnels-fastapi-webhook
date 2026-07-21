from typing import Self

from httpx import AsyncClient

from ...config import get_config

config = get_config()


class DiscordAsyncClient(AsyncClient):
    def __init__(self: Self, *args, **kwargs) -> None:
        base_url = config.DISCORD_WEBHOOK_URL
        super().__init__(
            *args,
            **kwargs,
            base_url=base_url,
            timeout=15.0,
        )


class DiscordClient:
    def __init__(self: Self, httpx_client: DiscordAsyncClient) -> None:
        self._httpx_client = httpx_client

    async def post_webhook(
        self: Self,
        message: str,
    ) -> None:
        response = await self._httpx_client.post(
            "/",
            json={
                "message": message,
            },
        )
        response.raise_for_status()
