from datetime import datetime, time, timedelta

from ...config import SmsTemplate
from ..models import SmsStep, WorkflowDefinition, WorkflowPlan


class WorkflowBuilder:
    @staticmethod
    def build_today(
        definition: WorkflowDefinition,
        now: datetime,
    ) -> WorkflowPlan:
        custom_attributes: dict[str | None, str] = {}
        sms_templates: list[tuple[SmsTemplate, datetime]] = []

        for step in definition.today:
            enabled = True

            if step.send_at_type == "replace":
                send_datetime = now.replace(
                    hour=step.send_at.hour,
                    minute=step.send_at.minute,
                    second=0,
                    microsecond=0,
                )
                enabled = now < send_datetime
                custom_attributes[step.attribute] = str(int(enabled))

            elif step.send_at_type == "increment":
                send_datetime = now + timedelta(
                    hours=step.send_at.hour,
                    minutes=step.send_at.minute,
                )

            if enabled:
                sms_templates.append((step.template, send_datetime))

        return WorkflowPlan(
            custom_attributes=custom_attributes,
            sms_templates=sms_templates,
        )

    @staticmethod
    def build_tomorrow(
        definition: WorkflowDefinition,
        now: datetime,
    ) -> WorkflowPlan:
        custom_attributes: dict[str | None, str] = {}
        sms_templates: list[tuple[SmsTemplate, datetime]] = []
        tomorrow = (now + timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        for step in definition.tomorrow:
            if step.send_at_type == "replace":
                send_datetime = tomorrow.replace(
                    hour=step.send_at.hour,
                    minute=step.send_at.minute,
                    second=0,
                    microsecond=0,
                )

            elif step.send_at_type == "increment":
                send_datetime = now + timedelta(
                    hours=step.send_at.hour,
                    minutes=step.send_at.minute,
                )

            sms_templates.append((step.template, send_datetime))

        return WorkflowPlan(
            custom_attributes=custom_attributes,
            sms_templates=sms_templates,
        )


WORKFLOW_LA = WorkflowDefinition(
    today=[
        SmsStep("send_email1", SmsTemplate.LA_2_HOURS_BEFORE, time(13, 0), "replace"),
        SmsStep("send_email2", SmsTemplate.LA_1_HOUR_BEFORE, time(14, 0), "replace"),
        SmsStep("send_email3", SmsTemplate.LA_START, time(15, 0), "replace"),
    ],
    tomorrow=[
        SmsStep(None, SmsTemplate.LA_MORNING_REMINDER, time(10, 0), "replace"),
        SmsStep(None, SmsTemplate.LA_2_HOURS_BEFORE, time(13, 0), "replace"),
        SmsStep(None, SmsTemplate.LA_1_HOUR_BEFORE, time(14, 0), "replace"),
        SmsStep(None, SmsTemplate.LA_START, time(15, 0), "replace"),
    ],
)

WORKFLOW_AU = WorkflowDefinition(
    today=[
        SmsStep(
            "send_email1_au", SmsTemplate.AU_2_HOURS_BEFORE, time(17, 0), "replace"
        ),
        SmsStep("send_email2_au", SmsTemplate.AU_1_HOUR_BEFORE, time(18, 0), "replace"),
        SmsStep("send_email3_au", SmsTemplate.AU_START, time(19, 0), "replace"),
    ],
    tomorrow=[
        SmsStep(None, SmsTemplate.AU_MORNING_REMINDER, time(10, 0), "replace"),
        SmsStep(None, SmsTemplate.AU_2_HOURS_BEFORE, time(17, 0), "replace"),
        SmsStep(None, SmsTemplate.AU_1_HOUR_BEFORE, time(18, 0), "replace"),
        SmsStep(None, SmsTemplate.AU_START, time(19, 0), "replace"),
    ],
)
