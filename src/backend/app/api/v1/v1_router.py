from hashlib import sha256
from json import JSONDecodeError, loads

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from httpx import AsyncClient

from ...config import Config
from ...utils import Helpers, RedisClient, StructuredLogger

v1_router = APIRouter(prefix="/v1", route_class=DishkaRoute)


@v1_router.post("/webhooks/clickfunnels")
async def clickfunnels_webhook(
    request: Request,
    config: FromDishka[Config],
    x_webhook_clickfunnels_signature: str | None = Header(
        default=None,
        alias="X-Webhook-ClickFunnels-Signature",
    ),
    x_webhook_clickfunnels_timestamp: str | None = Header(
        default=None,
        alias="X-Webhook-ClickFunnels-Timestamp",
    ),
):
    raw_body = await request.body()

    if not Helpers.verify_signature(
        raw_body,
        x_webhook_clickfunnels_signature,
        x_webhook_clickfunnels_timestamp,
        config.CLICKFUNNELS_WEBHOOK_SECRET,
    ):
        raise HTTPException(status_code=401, detail="invalid clickfunnels signature")

    try:
        payload = loads(raw_body)
    except JSONDecodeError as e:
        raise HTTPException(status_code=400, detail="invalid json payload") from e

    if config.LOG_RAW_PAYLOAD:
        StructuredLogger.info("incoming.payload", payload=payload)

    event_id = (
        str(
            payload.get("event_id")
            or payload.get("id")
            or payload.get("data", {}).get("id")
        )
        or sha256(raw_body).hexdigest()
    )

    acquired = await RedisClient.set(
        f"cf:event:{event_id}",
        "1",
        ex=config.EVENT_TTL_SECONDS,
        nx=True,
    )
    if not acquired:
        return JSONResponse({"ok": True, "duplicate": True, "event_id": event_id})

    email = Helpers.extract_email(payload)
    if not email:
        raise HTTPException(
            status_code=400, detail="could not find contact email in webhook payload"
        )

    hhmm = Helpers.current_hhmm(config.TIME_ZONE)
    flags = Helpers.compute_flags(hhmm)

    async with AsyncClient(timeout=20) as client:
        result = await Helpers.upsert_contact(
            client=client,
            api_base_url=config.api_base_url,
            workspace_id=config.CLICKFUNNELS_WORKSPACE_ID,
            token=config.CLICKFUNNELS_API_TOKEN,
            email=email,
            custom_attributes=flags,
        )

    await RedisClient.set_json(
        f"cf:event:{event_id}",
        {"email": email, "hhmm": hhmm, "flags": flags, "result": result},
        ex=config.EVENT_TTL_SECONDS,
    )

    return {
        "ok": True,
        "event_id": event_id,
        "email": email,
        "hhmm": hhmm,
        "flags": flags,
    }
