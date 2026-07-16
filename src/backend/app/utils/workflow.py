from datetime import datetime, time, timedelta
from typing import Self

from .enums import SmsTemplate


class WorkflowPlan:
    def __init__(
        self: Self,
        custom_attributes: dict[str, int],
        sms_templates: list[tuple[SmsTemplate, datetime]],
    ):
        self.custom_attributes = custom_attributes
        self.sms_templates = sms_templates

    @classmethod
    def build_today(cls: type[Self], now: datetime) -> Self:
        t = now.time()

        bucket1_end = time(13, 1)
        bucket2_end = time(14, 1)
        bucket3_end = time(15, 1)

        if t < bucket1_end:
            return cls(
                custom_attributes={
                    "send_email1": 1,
                    "send_email2": 1,
                    "send_email3": 1,
                },
                sms_templates=[
                    (
                        SmsTemplate.FOLLOW_UP_2,
                        now.replace(hour=13, minute=0, second=0, microsecond=0),
                    ),
                    (
                        SmsTemplate.FOLLOW_UP_3,
                        now.replace(hour=14, minute=0, second=0, microsecond=0),
                    ),
                    (
                        SmsTemplate.FOLLOW_UP_4,
                        now.replace(hour=15, minute=0, second=0, microsecond=0),
                    ),
                ],
            )

        if t < bucket2_end:
            return cls(
                custom_attributes={
                    "send_email1": 0,
                    "send_email2": 1,
                    "send_email3": 1,
                },
                sms_templates=[
                    (
                        SmsTemplate.FOLLOW_UP_3,
                        now.replace(hour=14, minute=0, second=0, microsecond=0),
                    ),
                    (
                        SmsTemplate.FOLLOW_UP_4,
                        now.replace(hour=15, minute=0, second=0, microsecond=0),
                    ),
                ],
            )

        if t < bucket3_end:
            return cls(
                custom_attributes={
                    "send_email1": 0,
                    "send_email2": 0,
                    "send_email3": 1,
                },
                sms_templates=[
                    (
                        SmsTemplate.FOLLOW_UP_4,
                        now.replace(hour=15, minute=0, second=0, microsecond=0),
                    ),
                ],
            )

        return cls(
            custom_attributes={"send_email1": 0, "send_email2": 0, "send_email3": 0},
            sms_templates=[],
        )

    @classmethod
    def build_tomorrow(cls: type[Self], now: datetime) -> Self:
        tomorrow = (now + timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        return cls(
            custom_attributes={},
            sms_templates=[
                (
                    SmsTemplate.FOLLOW_UP_5,
                    tomorrow.replace(hour=10, minute=0, second=0, microsecond=0),
                ),
                (
                    SmsTemplate.FOLLOW_UP_2,
                    tomorrow.replace(hour=13, minute=0, second=0, microsecond=0),
                ),
                (
                    SmsTemplate.FOLLOW_UP_3,
                    tomorrow.replace(hour=14, minute=0, second=0, microsecond=0),
                ),
                (
                    SmsTemplate.FOLLOW_UP_4,
                    tomorrow.replace(hour=15, minute=0, second=0, microsecond=0),
                ),
            ],
        )
