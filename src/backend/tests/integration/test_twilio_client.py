from pytest import fixture

from src.backend.app.config import SmsTemplate, get_config
from src.backend.app.utils.twilio_client import TwilioClient

config = get_config()


@fixture(scope="session")
async def twilio_client() -> TwilioClient:
    return TwilioClient(
        account_sid=config.TWILIO_TEST_ACCOUNT_SID,
        account_auth_token=config.TWILIO_TEST_AUTH_TOKEN,
        from_number=config.TWILIO_TEST_PHONE_NUMBER,
    )


async def test_send_sms(twilio_client: TwilioClient) -> None:
    assert (
        await twilio_client.send_sms(
            to_phone=config.TWILIO_TEST_PHONE_NUMBER,
            template=SmsTemplate.WELCOME_LA,
        )
        is not None
    )
