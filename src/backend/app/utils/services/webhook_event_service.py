from typing import Self
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import WebhookEvent


class WebhookEventService:
    def __init__(self, db_sess: AsyncSession) -> None:
        self._db_sess = db_sess

    async def get_by_event_id(self: Self, event_id: UUID) -> WebhookEvent | None:
        query = await self._db_sess.execute(
            select(WebhookEvent).where(WebhookEvent.event_id == event_id)
        )
        webhook_event = query.scalar_one_or_none()
        return webhook_event

    async def create_if_not_exists(
        self: Self,
        event_id: UUID,
    ) -> bool:
        if await self.get_by_event_id(event_id):
            return False

        event = WebhookEvent(event_id=event_id)

        self._db_sess.add(event)
        await self._db_sess.commit()

        return True
