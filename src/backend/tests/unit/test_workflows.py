from datetime import datetime

from pytest import fixture

from src.backend.app.config import get_config
from src.backend.app.utils.clickfunnels import ClickFunnelsUtils
from src.backend.app.utils.models import (
    PageContextDefinition,
    WorkflowBuilder,
)

config = get_config()


@fixture
async def page_context_la() -> PageContextDefinition:
    return ClickFunnelsUtils.resolve_page(
        config.REGISTRATION_TODAY_LA_PAGE_NAME,
    )  # type: ignore


@fixture
async def page_context_au() -> PageContextDefinition:
    return ClickFunnelsUtils.resolve_page(
        config.REGISTRATION_TODAY_AU_PAGE_NAME,
    )  # type: ignore


# la


async def test_workflow_plan_build_today_earliest_la(
    page_context_la: PageContextDefinition,
) -> None:
    dt = datetime(2026, 7, 14, 10, 30, tzinfo=page_context_la.timezone)
    plan = WorkflowBuilder.build_today(page_context_la.workflow_definition, dt)
    assert plan.custom_attributes == {
        "send_email11_00_la": "1",
        "send_email12_00_la": "1",
        "send_email13_00_la": "1",
        "send_email14_00_la": "1",
        "send_email14_50_la": "1",
    }
    assert len(plan.sms_templates) == 11


async def test_workflow_plan_build_today_earlier_la(
    page_context_la: PageContextDefinition,
) -> None:
    dt = datetime(2026, 7, 14, 11, 30, tzinfo=page_context_la.timezone)
    plan = WorkflowBuilder.build_today(page_context_la.workflow_definition, dt)
    assert plan.custom_attributes == {
        "send_email11_00_la": "0",
        "send_email12_00_la": "1",
        "send_email13_00_la": "1",
        "send_email14_00_la": "1",
        "send_email14_50_la": "1",
    }
    assert len(plan.sms_templates) == 10


async def test_workflow_plan_build_today_early_la(
    page_context_la: PageContextDefinition,
) -> None:
    dt = datetime(2026, 7, 14, 12, 30, tzinfo=page_context_la.timezone)
    plan = WorkflowBuilder.build_today(page_context_la.workflow_definition, dt)
    assert plan.custom_attributes == {
        "send_email11_00_la": "0",
        "send_email12_00_la": "0",
        "send_email13_00_la": "1",
        "send_email14_00_la": "1",
        "send_email14_50_la": "1",
    }
    assert len(plan.sms_templates) == 9


async def test_workflow_plan_build_today_mid_la(
    page_context_la: PageContextDefinition,
) -> None:
    dt = datetime(2026, 7, 14, 13, 30, tzinfo=page_context_la.timezone)
    plan = WorkflowBuilder.build_today(page_context_la.workflow_definition, dt)
    assert plan.custom_attributes == {
        "send_email11_00_la": "0",
        "send_email12_00_la": "0",
        "send_email13_00_la": "0",
        "send_email14_00_la": "1",
        "send_email14_50_la": "1",
    }
    assert len(plan.sms_templates) == 8


async def test_workflow_plan_build_today_late_la(
    page_context_la: PageContextDefinition,
) -> None:
    dt = datetime(2026, 7, 14, 14, 30, tzinfo=page_context_la.timezone)
    plan = WorkflowBuilder.build_today(page_context_la.workflow_definition, dt)
    assert plan.custom_attributes == {
        "send_email11_00_la": "0",
        "send_email12_00_la": "0",
        "send_email13_00_la": "0",
        "send_email14_00_la": "0",
        "send_email14_50_la": "1",
    }
    assert len(plan.sms_templates) == 7


async def test_workflow_plan_build_today_latest_la(
    page_context_la: PageContextDefinition,
) -> None:
    dt = datetime(2026, 7, 14, 14, 55, tzinfo=page_context_la.timezone)
    plan = WorkflowBuilder.build_today(page_context_la.workflow_definition, dt)
    assert plan.custom_attributes == {
        "send_email11_00_la": "0",
        "send_email12_00_la": "0",
        "send_email13_00_la": "0",
        "send_email14_00_la": "0",
        "send_email14_50_la": "0",
    }
    assert len(plan.sms_templates) == 6


async def test_workflow_plan_build_tomorrow_la(
    page_context_la: PageContextDefinition,
) -> None:
    dt = datetime(2026, 7, 14, 9, 0, tzinfo=page_context_la.timezone)
    plan = WorkflowBuilder.build_tomorrow(page_context_la.workflow_definition, dt)
    assert plan.custom_attributes == {}
    assert len(plan.sms_templates) == 10


# //au is temporarily deprecated


async def test_workflow_plan_build_today_early_au(
    page_context_au: PageContextDefinition,
) -> None:
    dt = datetime(2026, 7, 14, 16, 30, tzinfo=page_context_au.timezone)
    plan = WorkflowBuilder.build_today(page_context_au.workflow_definition, dt)
    assert plan.custom_attributes == {
        "send_email1_au": "1",
        "send_email2_au": "1",
        "send_email3_au": "1",
    }
    assert len(plan.sms_templates) == 7


async def test_workflow_plan_build_today_mid_au(
    page_context_au: PageContextDefinition,
) -> None:
    dt = datetime(2026, 7, 14, 17, 30, tzinfo=page_context_au.timezone)
    plan = WorkflowBuilder.build_today(page_context_au.workflow_definition, dt)
    assert plan.custom_attributes == {
        "send_email1_au": "0",
        "send_email2_au": "1",
        "send_email3_au": "1",
    }
    assert len(plan.sms_templates) == 6


async def test_workflow_plan_build_today_late_au(
    page_context_au: PageContextDefinition,
) -> None:
    dt = datetime(2026, 7, 14, 18, 30, tzinfo=page_context_au.timezone)
    plan = WorkflowBuilder.build_today(page_context_au.workflow_definition, dt)
    assert plan.custom_attributes == {
        "send_email1_au": "0",
        "send_email2_au": "0",
        "send_email3_au": "1",
    }
    assert len(plan.sms_templates) == 5


async def test_workflow_plan_build_tomorrow_au(
    page_context_au: PageContextDefinition,
) -> None:
    dt = datetime(2026, 7, 14, 9, 0, tzinfo=page_context_au.timezone)
    plan = WorkflowBuilder.build_tomorrow(page_context_au.workflow_definition, dt)
    assert plan.custom_attributes == {}
    assert len(plan.sms_templates) == 8


async def test_workflow_plan_build_today_after_web_la(
    page_context_la: PageContextDefinition,
) -> None:
    dt = datetime(2026, 7, 14, 17, 30, tzinfo=page_context_la.timezone)
    plan = WorkflowBuilder.build_today(page_context_la.workflow_definition, dt)
    assert plan.custom_attributes == {
        "send_email11_00_la": "0",
        "send_email12_00_la": "0",
        "send_email13_00_la": "0",
        "send_email14_00_la": "0",
        "send_email14_50_la": "0",
    }
    assert len(plan.sms_templates) == 3


async def test_workflow_plan_build_today_after_web_au(
    page_context_au: PageContextDefinition,
) -> None:
    dt = datetime(2026, 7, 14, 21, 30, tzinfo=page_context_au.timezone)
    plan = WorkflowBuilder.build_today(page_context_au.workflow_definition, dt)
    assert plan.custom_attributes == {
        "send_email1_au": "0",
        "send_email2_au": "0",
        "send_email3_au": "0",
    }
    assert len(plan.sms_templates) == 2
