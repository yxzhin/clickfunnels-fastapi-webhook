from datetime import time
from zoneinfo import ZoneInfo

from src.backend.app.config import LandingPage, RegisterType, SmsTemplate
from src.backend.app.utils import (
    PageContextDefinition,
    SmsStep,
    StructuredLogger,
    WorkflowDefinition,
)


async def test_serialize_page_context_definition():
    StructuredLogger.info(
        "test.serialize_dataclass",
        page_context_definition=PageContextDefinition(
            page=LandingPage.REGISTRATION_TODAY_LA,
            register_type=RegisterType.TODAY,
            welcome_sms_template=SmsTemplate.WELCOME_LA,
            timezone=ZoneInfo("America/Los_Angeles"),
            workflow_definition=WorkflowDefinition(
                today=[
                    SmsStep("test1", SmsTemplate.LA_1_HOUR_BEFORE, time(13, 0)),
                ],
                tomorrow=[
                    SmsStep("test2", SmsTemplate.LA_2_HOURS_BEFORE, time(12, 0)),
                ],
            ),
        ),
    )
