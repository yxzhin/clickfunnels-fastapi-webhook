from fastapi import APIRouter, Header, Request, status

from ...config import LandingPage
from .v1_router import _handle_webhook

la_router = APIRouter(prefix="/la")


@la_router.post(
    "/registration-today",
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
        LandingPage.REGISTRATION_TODAY_LA,
        x_webhook_clickfunnels_signature,
        x_webhook_clickfunnels_timestamp,
    )


@la_router.post(
    "/registration-tomorrow",
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
        LandingPage.REGISTRATION_TOMORROW_LA,
        x_webhook_clickfunnels_signature,
        x_webhook_clickfunnels_timestamp,
    )
