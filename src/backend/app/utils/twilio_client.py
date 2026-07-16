from asyncio import to_thread
from typing import Self

from twilio.rest import Client

from ..config import get_config
from .enums import SmsTemplate

config = get_config()


class TwilioClient:
    def __init__(self: Self) -> None:
        self._twilio_client = Client(
            config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN
        )

    def _send_sync(
        self: Self,
        to_phone: str,
        text: str,
    ) -> str:
        message = self._twilio_client.messages.create(
            to=to_phone,
            from_=config.TWILIO_FROM_NUMBER,
            body=text,
        )
        return str(message.sid)

    async def send_sms(
        self: Self,
        to_phone: str,
        template: SmsTemplate,
    ) -> str:
        return await to_thread(self._send_sync, to_phone, template.text)
