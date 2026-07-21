from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal
from zoneinfo import ZoneInfo

from dataclasses_json import config, dataclass_json

from ...config import LandingPage, RegisterType, SmsTemplate
from ..common import Helpers


@dataclass(slots=True)
class ClickFunnelsContact:
    id: str | int | None
    email: str | None
    phone_number: str | None
    first_name: str | None
    last_name: str | None
    page_name: str
    custom_attributes: dict[str, Any]

    @property
    def full_name(self) -> str:
        parts = [p for p in [self.first_name, self.last_name] if p]
        return Helpers.trim(" ".join(parts))

    @property
    def has_phone(self) -> bool:
        return bool(self.phone_number and Helpers.trim(self.phone_number))


@dataclass_json
@dataclass(slots=True, frozen=True)
class WorkflowPlan:
    custom_attributes: dict[str | None, str]
    sms_templates: list[tuple[SmsTemplate, datetime]] = field(
        metadata=config(
            encoder=lambda smstmpl: [
                (
                    i[0],
                    i[1].isoformat(),
                )
                for i in smstmpl
            ],
            decoder=None,
        )
    )


@dataclass_json
@dataclass(slots=True, frozen=True)
class Time:
    hours: int = 0
    minutes: int = 0
    days: int = 0


@dataclass_json
@dataclass(slots=True, frozen=True)
class SmsStep:
    attribute: str | None
    template: SmsTemplate
    send_at: Time
    send_at_type: Literal["replace", "increment"]


@dataclass(slots=True, frozen=True)
class WorkflowDefinition:
    today: list[SmsStep]
    tomorrow: list[SmsStep]


@dataclass_json
@dataclass(slots=True, frozen=True)
class PageContextDefinition:
    page: LandingPage
    register_type: RegisterType
    welcome_sms_template: SmsTemplate
    timezone: ZoneInfo = field(
        metadata=config(
            encoder=lambda tz: tz.key,
            decoder=ZoneInfo,
        )
    )
    workflow_definition: WorkflowDefinition
    web_start_hour: int
