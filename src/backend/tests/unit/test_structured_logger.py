from datetime import UTC, datetime, time
from zoneinfo import ZoneInfo

from pytest import fixture

from src.backend.app.config import LandingPage, RegisterType, SmsTemplate
from src.backend.app.utils.common import StructuredLogger
from src.backend.app.utils.models import (
    PageContextDefinition,
    SmsStep,
    WorkflowBuilder,
    WorkflowDefinition,
)


@fixture(scope="session")
async def workflow_definition() -> WorkflowDefinition:
    return WorkflowDefinition(
        today=[
            SmsStep("test1", SmsTemplate.LA_1_HOUR_BEFORE, time(13, 0)),
        ],
        tomorrow=[
            SmsStep("test2", SmsTemplate.LA_2_HOURS_BEFORE, time(12, 0)),
        ],
    )


async def test_serialize_page_context_definition(
    workflow_definition: WorkflowDefinition,
):
    StructuredLogger.info(
        "test.serialize_page_context_definition",
        page_context_definition=PageContextDefinition(
            page=LandingPage.REGISTRATION_TODAY_LA,
            register_type=RegisterType.TODAY,
            welcome_sms_template=SmsTemplate.WELCOME_LA,
            timezone=ZoneInfo("America/Los_Angeles"),
            workflow_definition=workflow_definition,
        ),
    )


async def test_serialize_workflow_plan(workflow_definition: WorkflowDefinition):
    StructuredLogger.info(
        "test.serialize_workflow_plan",
        workflow_plan=WorkflowBuilder.build_today(
            definition=workflow_definition,
            now=datetime.now(UTC),
        ),
    )
