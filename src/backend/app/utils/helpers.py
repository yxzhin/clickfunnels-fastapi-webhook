from datetime import datetime
from hashlib import sha256
from hmac import compare_digest, new
from string import whitespace
from typing import ClassVar
from zoneinfo import ZoneInfo

from httpx import AsyncClient


class Helpers:
    """utility class w/ general helper functions so I don't repeat yourself"""

    _clear_whitespace_trans_table: ClassVar[dict[int, int | None]] = str.maketrans(
        "", "", whitespace
    )

    @classmethod
    def clear_whitespace(cls, value: str) -> str:
        return value.translate(cls._clear_whitespace_trans_table)

    @staticmethod
    def trim(value: str) -> str:
        """trim sounds cooler so why not"""
        return value.strip()

    @staticmethod
    def current_hhmm(time_zone: str) -> int:
        """get current hours && minutes in given timezone"""
        now = datetime.now(tz=ZoneInfo(time_zone))
        return now.hour * 100 + now.minute

    @staticmethod
    def compute_flags(hhmm: int) -> dict[str, int]:
        """compute new custom attributes of a client"""
        if hhmm <= 1500:
            return {"send_email15": 1, "send_email17": 1, "send_email18": 1}
        if 1501 <= hhmm <= 1700:
            return {"send_email15": 0, "send_email17": 1, "send_email18": 1}
        if 1701 <= hhmm <= 1800:
            return {"send_email15": 0, "send_email17": 0, "send_email18": 1}
        return {"send_email15": 0, "send_email17": 0, "send_email18": 0}

    @staticmethod
    def verify_signature(
        raw_body: bytes,
        signature: str | None,
        timestamp: str | None,
        secret: str,
    ) -> bool:
        """verify clickfunnels signature"""
        if not raw_body or not signature or not timestamp or not secret:
            return False

        try:
            ts = int(timestamp)
        except ValueError:
            return False

        now = int(datetime.now(tz=ZoneInfo("UTC")).timestamp())
        if abs(now - ts) > 600:
            return False

        signature_payload = f"{timestamp}.".encode() + raw_body
        expected = new(secret.encode("utf-8"), signature_payload, sha256).hexdigest()
        return compare_digest(expected, signature)

    @staticmethod
    def extract_email(payload: dict) -> str | None:
        """get the email of a contact"""
        data = payload.get("data") or payload.get("contact") or {}
        candidates = [
            data.get("email"),
            data.get("primary_email"),
            data.get("contact_email"),
            data.get("email_address"),
        ]

        contact = data.get("contact") or {}
        candidates.extend(
            [
                contact.get("email"),
                contact.get("primary_email"),
                contact.get("contact_email"),
                contact.get("email_address"),
            ]
        )

        for value in candidates:
            if isinstance(value, str) and value.strip():
                return value.strip().lower()

        # last resort: search common nested structures for an email-like field
        for key in ("fields", "form_fields", "answers"):
            items = data.get(key)
            if isinstance(items, list):
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    for nested_key in ("email", "value", "answer"):
                        val = item.get(nested_key)
                        if isinstance(val, str) and "@" in val:
                            return val.strip().lower()
        return None

    @staticmethod
    async def upsert_contact(
        client: AsyncClient,
        api_base_url: str,
        workspace_id: int,
        token: str,
        email: str,
        custom_attributes: dict[str, int],
    ) -> dict:
        """update contact details w/ given custom attributes"""
        url = f"{api_base_url}/workspaces/{workspace_id}/contacts/upsert"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "clickfunnels-fastapi-webhook/1.0",
        }
        payload = {
            "contact": {
                "email": email,
                "custom_attributes": custom_attributes,
            }
        }

        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()

        if response.content:
            try:
                return response.json()

            except Exception:
                return {"raw": response.text}

        return {"ok": True}
