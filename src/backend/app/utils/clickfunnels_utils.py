from hashlib import sha256
from hmac import compare_digest, new
from typing import Any

from ..config import get_config
from .enums import LandingPage
from .helpers import Helpers
from .models import ClickFunnelsContact
from .structured_logger import StructuredLogger

config = get_config()


class ClickFunnelsUtils:
    @staticmethod
    def verify_clickfunnels_signature(
        raw_body: bytes,
        signature_header: str | None,
        timestamp_header: str | None,
        secret: str,
    ) -> bool:
        if not raw_body:
            StructuredLogger.exception(
                "helpers.verify_clickfunnels_signature.empty_webhook_body"
            )
            return False
        if not signature_header or not timestamp_header:
            StructuredLogger.exception(
                "helpers.verify_clickfunnels_signature.missing_signature_headers"
            )
            return False
        if not secret:
            StructuredLogger.exception(
                "helpers.verify_clickfunnels_signature.missing_webhook_secret"
            )
            return False

        # ClickFunnels docs: expected payload is `timestamp.payload`
        # and the signature is HMAC-SHA256 over that value using the webhook secret.
        payload = timestamp_header.encode("utf-8") + b"." + raw_body
        expected = new(secret.encode("utf-8"), payload, sha256).hexdigest()

        if not compare_digest(expected, signature_header):
            StructuredLogger.exception(
                "helpers.verify_clickfunnels_signature.invalid_webhook_signature"
            )
            return False

        return True

    @staticmethod
    def extract_contact(payload: dict[str, Any]) -> ClickFunnelsContact:
        data = payload.get("data") or {}
        custom_attributes = data.get("custom_attributes") or {}
        page_name = (
            payload.get("page_name")
            or data.get("page_name")
            or payload.get("page", {}).get("name")
        )

        return ClickFunnelsContact(
            id=data.get("id") or payload.get("subject_id"),
            email=data.get("email_address") or data.get("email"),
            phone_number=data.get("phone_number") or data.get("phone"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            page_name=page_name,
            custom_attributes=custom_attributes,
        )

    @staticmethod
    def resolve_page(
        payload: dict[str, Any],
        page_hint: str,
    ) -> LandingPage | None:
        data = payload.get("data") or {}
        page_name = Helpers.trim(
            page_hint
            or payload.get("page_name")
            or data.get("page_name")
            or payload.get("page", {}).get("name")
            or ""
        ).lower()

        if page_name == "регистрация на сегодня":
            return LandingPage.REGISTRATION_TODAY
        if page_name == "регистрация на завтра":
            return LandingPage.REGISTRATION_TOMORROW
        return None
