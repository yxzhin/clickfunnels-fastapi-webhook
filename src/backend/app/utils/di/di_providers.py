from collections.abc import AsyncGenerator
from typing import Any, Self

from dishka import Provider, Scope, provide
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from ...config import get_config
from ..clickfunnels import ClickFunnelsAsyncClient, ClickFunnelsClient
from ..db import Database
from ..discord import DiscordAsyncClient, DiscordClient, DiscordLogger
from ..services import WebhookEventService
from ..twilio import TwilioClient

config = get_config()


class AsyncClientProvider(Provider):
    def __init__(self: Self, httpx_client: AsyncClient | None = None) -> None:
        super().__init__()
        self._httpx_client = httpx_client

    @provide(scope=Scope.APP)
    async def clickfunnels_async_client(
        self: Self,
    ) -> AsyncGenerator[ClickFunnelsAsyncClient, Any]:
        if self._httpx_client is not None:
            yield self._httpx_client  # type: ignore
        else:
            async with ClickFunnelsAsyncClient() as httpx_client:
                yield httpx_client

    @provide(scope=Scope.APP)
    async def discord_async_client(
        self: Self,
    ) -> AsyncGenerator[DiscordAsyncClient, Any]:
        if self._httpx_client is not None:
            yield self._httpx_client  # type: ignore
        else:
            async with DiscordAsyncClient() as httpx_client:
                yield httpx_client


class ClickFunnelsClientProvider(Provider):
    @provide(scope=Scope.APP)
    async def clickfunnels_client(
        self: Self,
        httpx_client: ClickFunnelsAsyncClient,
    ) -> ClickFunnelsClient:
        return ClickFunnelsClient(httpx_client)


class DiscordClientProvider(Provider):
    @provide(scope=Scope.APP)
    async def discord_client(
        self: Self,
        httpx_client: DiscordAsyncClient,
    ) -> DiscordClient:
        return DiscordClient(httpx_client)


class TwilioClientProvider(Provider):
    def __init__(
        self: Self,
        account_sid: str,
        auth_token: str,
        from_number: str,
    ) -> None:
        super().__init__()
        self._account_sid = account_sid
        self._auth_token = auth_token
        self._from_number = from_number

    @provide(scope=Scope.APP)
    async def twilio_client(self: Self) -> TwilioClient:
        return TwilioClient(
            account_sid=self._account_sid,
            account_auth_token=self._auth_token,
            from_number=self._from_number,
        )


class ServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def webhook_event_service(
        self: Self,
        db_sess: AsyncSession,
    ) -> WebhookEventService:
        return WebhookEventService(db_sess)


class DBSessionProvider(Provider):
    def __init__(
        self: Self,
        db_sess: AsyncSession | None = None,
    ):
        super().__init__()
        self._db_sess = db_sess

    @provide(scope=Scope.REQUEST)
    async def db_sess(self: Self) -> AsyncGenerator[AsyncSession, Any]:
        if self._db_sess:
            yield self._db_sess
        else:
            async with Database.get_session() as session:
                yield session


class DiscordLoggerProvider(Provider):
    async def _send(self: Self, message: str) -> None:
        from ..taskiq.tasks import post_discord_webhook_task

        await post_discord_webhook_task.kiq(message)  # type: ignore

    @provide(scope=Scope.APP)
    async def discord_logger(self: Self) -> DiscordLogger:
        return DiscordLogger(self._send)
