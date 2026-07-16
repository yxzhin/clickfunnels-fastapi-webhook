from datetime import datetime
from zoneinfo import ZoneInfo

from src.backend.app.utils.workflow import WorkflowPlan

LA = ZoneInfo("America/Los_Angeles")


async def test_workflow_plan_build_today_early() -> None:
    dt = datetime(2026, 7, 14, 12, 30, tzinfo=LA)
    plan = WorkflowPlan.build_today(dt)
    assert plan.custom_attributes == {
        "send_email1": 1,
        "send_email2": 1,
        "send_email3": 1,
    }
    assert len(plan.sms_templates) == 3


async def test_workflow_plan_build_today_mid() -> None:
    dt = datetime(2026, 7, 14, 13, 30, tzinfo=LA)
    plan = WorkflowPlan.build_today(dt)
    assert plan.custom_attributes == {
        "send_email1": 0,
        "send_email2": 1,
        "send_email3": 1,
    }
    assert len(plan.sms_templates) == 2


async def test_workflow_plan_build_today_late() -> None:
    dt = datetime(2026, 7, 14, 14, 30, tzinfo=LA)
    plan = WorkflowPlan.build_today(dt)
    assert plan.custom_attributes == {
        "send_email1": 0,
        "send_email2": 0,
        "send_email3": 1,
    }
    assert len(plan.sms_templates) == 1


async def test_workflow_plan_build_tomorrow() -> None:
    dt = datetime(2026, 7, 14, 9, 0, tzinfo=LA)
    plan = WorkflowPlan.build_tomorrow(dt)
    assert plan.custom_attributes == {}
    assert len(plan.sms_templates) == 4
