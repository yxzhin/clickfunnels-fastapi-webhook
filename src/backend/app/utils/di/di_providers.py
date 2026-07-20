from collections.abc import AsyncGenerator
from typing import Any, Self

from dishka import Provider, Scope, provide
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from ...config import get_config
from ..clickfunnels import ClickFunnelsClient
from ..db import Database
from ..services import WebhookEventService
from ..twilio import TwilioClient

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
        self._base_url = config.api_base_url

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


class ClickFunnelsClientProvider(Provider):
    @provide(scope=Scope.APP)
    async def clickfunnels_client(
        self: Self,
        httpx_client: AsyncClient,
    ) -> ClickFunnelsClient:
        return ClickFunnelsClient(httpx_client)


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
    async def webhook_event_service_provider(
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
