from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as UUID_PG
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base


class WebhookEvent(Base):
    __tablename__ = "webhook_events"

    id: Mapped[UUID] = mapped_column(
        UUID_PG(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    provider: Mapped[str] = mapped_column(String(50))

    event_id: Mapped[str] = mapped_column(String(255))

    payload: Mapped[str] = mapped_column(Text)

    status: Mapped[str] = mapped_column(
        String(20),
        default="processing",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    completed_at: Mapped[datetime | None]
