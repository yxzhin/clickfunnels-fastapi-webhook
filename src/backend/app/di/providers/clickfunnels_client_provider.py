from typing import Self

from dishka import Provider, Scope, provide
from httpx import AsyncClient

from ...utils import ClickFunnelsClient


class ClickFunnelsClientProvider(Provider):
    @provide(scope=Scope.APP)
    async def clickfunnels_client(
        self: Self,
        httpx_client: AsyncClient,
    ) -> ClickFunnelsClient:
        return ClickFunnelsClient(httpx_client)
