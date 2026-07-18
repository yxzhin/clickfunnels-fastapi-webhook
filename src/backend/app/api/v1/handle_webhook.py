from typing import Any

from fastapi import HTTPException, Request, status

from ...config import get_config
from ...utils import (
    ClickFunnelsUtils,
    StructuredLogger,
    process_clickfunnels_webhook,
)

config = get_config()


async def handle_webhook(
    request: Request,
    x_webhook_clickfunnels_signature: str | None,
    x_webhook_clickfunnels_timestamp: str | None,
) -> dict[str, bool]:
    raw_body = await request.body()

    if not ClickFunnelsUtils.verify_clickfunnels_signature(
        raw_body=raw_body,
        signature_header=x_webhook_clickfunnels_signature,
        timestamp_header=x_webhook_clickfunnels_timestamp,
        secret=config.CLICKFUNNELS_WEBHOOK_SECRET,
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    payload: dict[str, Any] = await request.json()
    if config.LOG_RAW_PAYLOAD:
        StructuredLogger.info("request.raw_payload", payload=payload)

    await process_clickfunnels_webhook.kiq(payload=payload)  # type: ignore
    return {"ok": True}
