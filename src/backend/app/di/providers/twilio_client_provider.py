from typing import Self

from dishka import Provider, Scope, provide

from ...utils.twilio_client import TwilioClient


class TwilioClientProvider(Provider):
    def __init__(
        self: Self,
        account_sid: str,
        auth_token: str,
        from_number: str,
    ) -> None:
        super().__init__()
        self._account_sid = account_sid
        self._auth_token = auth_token
        self._from_number = from_number

    @provide(scope=Scope.APP)
    async def twilio_client(self: Self) -> TwilioClient:
        return TwilioClient(
            account_sid=self._account_sid,
            account_auth_token=self._auth_token,
            from_number=self._from_number,
        )
