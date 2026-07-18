from fastapi import APIRouter, Header, Request, status

from .handle_webhook import handle_webhook

au_router = APIRouter(prefix="/au")


@au_router.post(
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
    return await handle_webhook(
        request,
        x_webhook_clickfunnels_signature,
        x_webhook_clickfunnels_timestamp,
    )


@au_router.post(
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
    return await handle_webhook(
        request,
        x_webhook_clickfunnels_signature,
        x_webhook_clickfunnels_timestamp,
    )
