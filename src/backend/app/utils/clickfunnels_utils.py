from hashlib import sha256
from hmac import compare_digest, new
from typing import Any

from ..config import LandingPage, RegisterType, get_config
from .helpers import Helpers
from .models import ClickFunnelsContact, PageContextDefinition, SmsTemplate
from .structured_logger import StructuredLogger
from .workflows import WORKFLOW_AU, WORKFLOW_LA

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
        contact_data = data.get("data") or {}  # //who the fuck made cf api :sob:
        contact = contact_data.get("data", {}) or {}
        id_ = data.get("contact_id")
        email = contact.get("email", {}).get("")
        phone_number = Helpers.normalize_phone(contact_data.get("phone_number") or "")
        contact_name = contact.get("name", "").split(" ")
        first_name, last_name = contact_name[0], contact_name[1]
        page_name = payload.get("page", {}).get("name")
        custom_attributes = data.get("custom_attributes") or {}

        return ClickFunnelsContact(
            id=id_,
            email=email,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            page_name=page_name,
            custom_attributes=custom_attributes,
        )

    @staticmethod
    def resolve_page(
        payload: dict[str, Any],
        page_hint: str,
    ) -> PageContextDefinition | None:
        page_name = Helpers.trim(
            page_hint or payload.get("page", {}).get("name")
        ).lower()

        if page_name == config.REGISTRATION_TODAY_LA_PAGE_NAME:
            return PageContextDefinition(
                page=LandingPage.REGISTRATION_TODAY_LA,
                register_type=RegisterType.TODAY,
                welcome_sms_template=SmsTemplate.WELCOME_LA,
                timezone=Helpers.LA_TZ,
                workflow_definition=WORKFLOW_LA,
            )

        if page_name == config.REGISTRATION_TODAY_AU_PAGE_NAME:
            return PageContextDefinition(
                page=LandingPage.REGISTRATION_TODAY_AU,
                register_type=RegisterType.TODAY,
                welcome_sms_template=SmsTemplate.WELCOME_AU,
                timezone=Helpers.AU_TZ,
                workflow_definition=WORKFLOW_AU,
            )

        if page_name == config.REGISTRATION_TOMORROW_LA_PAGE_NAME:
            return PageContextDefinition(
                page=LandingPage.REGISTRATION_TOMORROW_LA,
                register_type=RegisterType.TOMORROW,
                welcome_sms_template=SmsTemplate.WELCOME_LA,
                timezone=Helpers.LA_TZ,
                workflow_definition=WORKFLOW_LA,
            )

        if page_name == config.REGISTRATION_TOMORROW_AU_PAGE_NAME:
            return PageContextDefinition(
                page=LandingPage.REGISTRATION_TOMORROW_AU,
                register_type=RegisterType.TOMORROW,
                welcome_sms_template=SmsTemplate.WELCOME_AU,
                timezone=Helpers.AU_TZ,
                workflow_definition=WORKFLOW_AU,
            )

        return None
