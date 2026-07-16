from typing import Any

from fastapi import APIRouter, HTTPException, Request, status

from ...config import LandingPage, get_config
from ...utils import (
    ClickFunnelsUtils,
    StructuredLogger,
    process_clickfunnels_webhook,
)
from .au_router import au_router
from .la_router import la_router

v1_router = APIRouter(prefix="/v1/webhooks/clickfunnels")
v1_router.include_router(la_router)  # type: ignore
v1_router.include_router(au_router)  # type: ignore

config = get_config()


async def _handle_webhook(
    request: Request,
    page: LandingPage,
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

    await process_clickfunnels_webhook.kiq(payload=payload, page_hint=page.label)  # type: ignore
    return {"ok": True}
