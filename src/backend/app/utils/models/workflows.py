from datetime import datetime, timedelta

from ...config import SmsTemplate
from ..models import SmsStep, Time, WorkflowDefinition, WorkflowPlan


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
                    day=step.send_at.days,
                    hour=step.send_at.hours,
                    minute=step.send_at.minutes,
                    second=0,
                    microsecond=0,
                )

                enabled = now < send_datetime
                if step.attribute is not None:
                    custom_attributes[step.attribute] = str(int(enabled))

            elif step.send_at_type == "increment":
                send_datetime = now + timedelta(
                    days=step.send_at.days,
                    hours=step.send_at.hours,
                    minutes=step.send_at.minutes,
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
                    day=step.send_at.days,
                    hour=step.send_at.hours,
                    minute=step.send_at.minutes,
                    second=0,
                    microsecond=0,
                )

            elif step.send_at_type == "increment":
                send_datetime = now + timedelta(
                    days=step.send_at.days,
                    hours=step.send_at.hours,
                    minutes=step.send_at.minutes,
                )

            sms_templates.append((step.template, send_datetime))

        return WorkflowPlan(
            custom_attributes=custom_attributes,
            sms_templates=sms_templates,
        )


WORKFLOW_LA = WorkflowDefinition(
    today=[
        # SmsStep(None, SmsTemplate.AFTER_REG_5_MINUTES, time(0, 5), "increment"),
        # SmsStep(None, SmsTemplate.AFTER_REG_1_HOUR, time(1, 0), "increment"),
        SmsStep("send_email15", SmsTemplate.LA_2_HOURS_BEFORE, Time(13, 0), "replace"),
        SmsStep("send_email17", SmsTemplate.LA_1_HOUR_BEFORE, Time(14, 0), "replace"),
        SmsStep("send_email19", SmsTemplate.LA_START, Time(15, 0), "replace"),
        SmsStep(None, SmsTemplate.LA_15_MINUTES_AFTER_START, Time(15, 15), "replace"),
        SmsStep(None, SmsTemplate.LA_1_HOUR_AFTER_START, Time(16, 0), "replace"),
        SmsStep(None, SmsTemplate.LA_1_DAY_AFTER_WEB, Time(24, 0), "increment"),
        SmsStep(None, SmsTemplate.LA_2_DAYS_AFTER_WEB, Time(48, 0), "increment"),
    ],
    tomorrow=[
        # SmsStep(None, SmsTemplate.AFTER_REG_5_MINUTES, time(0, 5), "increment"),
        # SmsStep(None, SmsTemplate.AFTER_REG_1_HOUR, time(1, 0), "increment"),
        SmsStep(None, SmsTemplate.LA_MORNING_REMINDER, Time(10, 0), "replace"),
        SmsStep(None, SmsTemplate.LA_2_HOURS_BEFORE, Time(13, 0), "replace"),
        SmsStep(None, SmsTemplate.LA_1_HOUR_BEFORE, Time(14, 0), "replace"),
        SmsStep(None, SmsTemplate.LA_START, Time(15, 0), "replace"),
        SmsStep(None, SmsTemplate.LA_15_MINUTES_AFTER_START, Time(15, 15), "replace"),
        SmsStep(None, SmsTemplate.LA_1_HOUR_AFTER_START, Time(16, 0), "replace"),
        SmsStep(None, SmsTemplate.LA_1_DAY_AFTER_WEB, Time(48, 0), "increment"),
        SmsStep(None, SmsTemplate.LA_2_DAYS_AFTER_WEB, Time(72, 0), "increment"),
    ],
)

WORKFLOW_AU = WorkflowDefinition(
    today=[
        # SmsStep(None, SmsTemplate.AFTER_REG_5_MINUTES, time(0, 5), "increment"),
        # SmsStep(None, SmsTemplate.AFTER_REG_1_HOUR, time(1, 0), "increment"),
        SmsStep(
            "send_email1_au", SmsTemplate.AU_2_HOURS_BEFORE, Time(17, 0), "replace"
        ),
        SmsStep("send_email2_au", SmsTemplate.AU_1_HOUR_BEFORE, Time(18, 0), "replace"),
        SmsStep("send_email3_au", SmsTemplate.AU_START, Time(19, 0), "replace"),
        SmsStep(None, SmsTemplate.AU_15_MINUTES_AFTER_START, Time(19, 15), "replace"),
        SmsStep(None, SmsTemplate.AU_1_HOUR_AFTER_START, Time(20, 0), "replace"),
        SmsStep(None, SmsTemplate.AU_1_DAY_AFTER_WEB, Time(24, 0), "increment"),
        SmsStep(None, SmsTemplate.AU_2_DAYS_AFTER_WEB, Time(48, 0), "increment"),
    ],
    tomorrow=[
        # SmsStep(None, SmsTemplate.AFTER_REG_5_MINUTES, time(0, 5), "increment"),
        # SmsStep(None, SmsTemplate.AFTER_REG_1_HOUR, time(1, 0), "increment"),
        SmsStep(None, SmsTemplate.AU_MORNING_REMINDER, Time(10, 0), "replace"),
        SmsStep(None, SmsTemplate.AU_2_HOURS_BEFORE, Time(17, 0), "replace"),
        SmsStep(None, SmsTemplate.AU_1_HOUR_BEFORE, Time(18, 0), "replace"),
        SmsStep(None, SmsTemplate.AU_START, Time(19, 0), "replace"),
        SmsStep(None, SmsTemplate.AU_15_MINUTES_AFTER_START, Time(19, 15), "replace"),
        SmsStep(None, SmsTemplate.AU_1_HOUR_AFTER_START, Time(20, 0), "replace"),
        SmsStep(None, SmsTemplate.AU_1_DAY_AFTER_WEB, Time(48, 0), "increment"),
        SmsStep(None, SmsTemplate.AU_2_DAYS_AFTER_WEB, Time(72, 0), "increment"),
    ],
)

LIVE_ONLINE_WEBINAR_SMS_STEPS = [
    SmsStep(
        None,
        SmsTemplate.LIVE_ONLINE_WEBINAR_1_DAY_AFTER_REG,
        Time(24, 0),
        "increment",
    ),
    SmsStep(
        None,
        SmsTemplate.LIVE_ONLINE_WEBINAR_1_DAY_BEFORE_WEB,
        Time(10, 0, 18),
        "replace",
    ),
    SmsStep(
        None,
        SmsTemplate.LIVE_ONLINE_WEBINAR_MORNING_REMINDER,
        Time(9, 0, 19),
        "replace",
    ),
    SmsStep(
        None,
        SmsTemplate.LIVE_ONLINE_WEBINAR_3_HOURS_BEFORE,
        Time(15, 0, 19),
        "replace",
    ),
    SmsStep(
        None,
        SmsTemplate.LIVE_ONLINE_WEBINAR_1_HOUR_BEFORE,
        Time(17, 0, 19),
        "replace",
    ),
    SmsStep(
        None,
        SmsTemplate.LIVE_ONLINE_WEBINAR_START,
        Time(18, 0, 19),
        "replace",
    ),
    SmsStep(
        None,
        SmsTemplate.LIVE_ONLINE_WEBINAR_10_MINUTES_AFTER_START,
        Time(18, 10, 19),
        "replace",
    ),
    SmsStep(
        None,
        SmsTemplate.LIVE_ONLINE_WEBINAR_AFTER_WEB,
        Time(19, 30, 19),
        "replace",
    ),
    SmsStep(
        None,
        SmsTemplate.LIVE_ONLINE_WEBINAR_AFTER_WEB_2,
        Time(21, 0, 19),
        "replace",
    ),
    SmsStep(
        None,
        SmsTemplate.LIVE_ONLINE_WEBINAR_1_DAY_AFTER,
        Time(10, 0, 20),
        "replace",
    ),
    SmsStep(
        None,
        SmsTemplate.LIVE_ONLINE_WEBINAR_2_DAYS_AFTER,
        Time(10, 0, 21),
        "replace",
    ),
]

WORKFLOW_LIVE_ONLINE_WEBINAR = WorkflowDefinition(
    today=LIVE_ONLINE_WEBINAR_SMS_STEPS,
    tomorrow=LIVE_ONLINE_WEBINAR_SMS_STEPS,
)
