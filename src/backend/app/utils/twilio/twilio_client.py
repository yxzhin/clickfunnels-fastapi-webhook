from asyncio import to_thread
from typing import Self

from twilio.rest import Client

from ...config import SmsTemplate


class TwilioClient:
    def __init__(
        self: Self,
        account_sid: str,
        account_auth_token: str,
        from_number: str,
    ) -> None:
        self._twilio_client = Client(
            username=account_sid,
            password=account_auth_token,
        )
        self._from_number = from_number

    def _send_sync(
        self: Self,
        to_phone: str,
        text: str,
    ) -> str | None:
        message = self._twilio_client.messages.create(
            to=to_phone,
            from_=self._from_number,
            body=text,
        )
        return message.sid

    async def send_sms(
        self: Self,
        to_phone: str,
        template: SmsTemplate,
    ) -> str | None:
        return await to_thread(self._send_sync, to_phone, template.text)
