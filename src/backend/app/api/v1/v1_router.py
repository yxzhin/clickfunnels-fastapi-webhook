from typing import Any

from fastapi import APIRouter, Header, HTTPException, Request, status

from ...config import get_config
from ...utils.clickfunnels import ClickFunnelsUtils
from ...utils.common import StructuredLogger
from ...utils.taskiq import process_clickfunnels_webhook

config = get_config()

v1_router = APIRouter(prefix="/v1/webhooks/clickfunnels")


@v1_router.post(
    "/webinar-reg",
    status_code=status.HTTP_200_OK,
)
async def registration_today_webhook(
    request: Request,
    x_webhook_clickfunnels_signature: str | None = Header(
        default=None,
        alias="X-Webhook-ClickFunnels-Signature",
    ),
    x_webhook_clickfunnels_timestamp: str | None = Header(
        default=None,
        alias="X-Webhook-ClickFunnels-Timestamp",
    ),
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
