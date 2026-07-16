from datetime import datetime

from pytest import fixture

from src.backend.app.config import get_config
from src.backend.app.utils import (
    ClickFunnelsUtils,
    PageContextDefinition,
    WorkflowBuilder,
)

config = get_config()


@fixture
async def page_context_la() -> PageContextDefinition:
    return ClickFunnelsUtils.resolve_page(
        {},
        config.REGISTRATION_TODAY_LA_PAGE_NAME,
    )  # type: ignore


@fixture
async def page_context_au() -> PageContextDefinition:
    return ClickFunnelsUtils.resolve_page(
        {},
        config.REGISTRATION_TODAY_AU_PAGE_NAME,
    )  # type: ignore


# la


async def test_workflow_plan_build_today_early_la(
    page_context_la: PageContextDefinition,
) -> None:
    dt = datetime(2026, 7, 14, 12, 30, tzinfo=page_context_la.timezone)
    plan = WorkflowBuilder.build_today(page_context_la.workflow_definition, dt)
    assert plan.custom_attributes == {
        "send_email1": 1,
        "send_email2": 1,
        "send_email3": 1,
    }
    assert len(plan.sms_templates) == 3


async def test_workflow_plan_build_today_mid_la(
    page_context_la: PageContextDefinition,
) -> None:
    dt = datetime(2026, 7, 14, 13, 30, tzinfo=page_context_la.timezone)
    plan = WorkflowBuilder.build_today(page_context_la.workflow_definition, dt)
    assert plan.custom_attributes == {
        "send_email1": 0,
        "send_email2": 1,
        "send_email3": 1,
    }
    assert len(plan.sms_templates) == 2


async def test_workflow_plan_build_today_late_la(
    page_context_la: PageContextDefinition,
) -> None:
    dt = datetime(2026, 7, 14, 14, 30, tzinfo=page_context_la.timezone)
    plan = WorkflowBuilder.build_today(page_context_la.workflow_definition, dt)
    assert plan.custom_attributes == {
        "send_email1": 0,
        "send_email2": 0,
        "send_email3": 1,
    }
    assert len(plan.sms_templates) == 1


async def test_workflow_plan_build_tomorrow_la(
    page_context_la: PageContextDefinition,
) -> None:
    dt = datetime(2026, 7, 14, 9, 0, tzinfo=page_context_la.timezone)
    plan = WorkflowBuilder.build_tomorrow(page_context_la.workflow_definition, dt)
    assert plan.custom_attributes == {}
    assert len(plan.sms_templates) == 4


# au


async def test_workflow_plan_build_today_early_au(
    page_context_au: PageContextDefinition,
) -> None:
    dt = datetime(2026, 7, 14, 16, 30, tzinfo=page_context_au.timezone)
    plan = WorkflowBuilder.build_today(page_context_au.workflow_definition, dt)
    assert plan.custom_attributes == {
        "send_email1_au": 1,
        "send_email2_au": 1,
        "send_email3_au": 1,
    }
    assert len(plan.sms_templates) == 3


async def test_workflow_plan_build_today_mid_au(
    page_context_au: PageContextDefinition,
) -> None:
    dt = datetime(2026, 7, 14, 17, 30, tzinfo=page_context_au.timezone)
    plan = WorkflowBuilder.build_today(page_context_au.workflow_definition, dt)
    assert plan.custom_attributes == {
        "send_email1_au": 0,
        "send_email2_au": 1,
        "send_email3_au": 1,
    }
    assert len(plan.sms_templates) == 2


async def test_workflow_plan_build_today_late_au(
    page_context_au: PageContextDefinition,
) -> None:
    dt = datetime(2026, 7, 14, 18, 30, tzinfo=page_context_au.timezone)
    plan = WorkflowBuilder.build_today(page_context_au.workflow_definition, dt)
    assert plan.custom_attributes == {
        "send_email1_au": 0,
        "send_email2_au": 0,
        "send_email3_au": 1,
    }
    assert len(plan.sms_templates) == 1


async def test_workflow_plan_build_tomorrow_au(
    page_context_au: PageContextDefinition,
) -> None:
    dt = datetime(2026, 7, 14, 9, 0, tzinfo=page_context_au.timezone)
    plan = WorkflowBuilder.build_tomorrow(page_context_au.workflow_definition, dt)
    assert plan.custom_attributes == {}
    assert len(plan.sms_templates) == 4
