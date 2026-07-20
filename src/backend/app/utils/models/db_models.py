from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID as UUID_PG
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base


class WebhookEvent(Base):
    __tablename__ = "webhook_events"

    event_id: Mapped[UUID] = mapped_column(
        UUID_PG(as_uuid=True),
        primary_key=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
