from typing import Any

from fastapi import APIRouter, Header, HTTPException, Request, status

from ...config import get_config
from ...utils import ClickFunnelsUtils, LandingPage, process_clickfunnels_webhook

v1_router = APIRouter(prefix="/v1/webhooks/clickfunnels")

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
    await process_clickfunnels_webhook.kiq(payload=payload, page_hint=page.label)  # type: ignore
    return {"ok": True}


@v1_router.post(
    "/la/registration-today",
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
    return await _handle_webhook(
        request,
        LandingPage.REGISTRATION_TODAY,
        x_webhook_clickfunnels_signature,
        x_webhook_clickfunnels_timestamp,
    )


@v1_router.post(
    "/la/registration-tomorrow",
    status_code=status.HTTP_200_OK,
)
async def registration_tomorrow_webhook(
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
    return await _handle_webhook(
        request,
        LandingPage.REGISTRATION_TOMORROW,
        x_webhook_clickfunnels_signature,
        x_webhook_clickfunnels_timestamp,
    )
