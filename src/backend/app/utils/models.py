from dataclasses import dataclass
from datetime import datetime, time
from typing import Any
from zoneinfo import ZoneInfo

from ..config import LandingPage, RegisterType, SmsTemplate
from .helpers import Helpers


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


@dataclass(slots=True, frozen=True)
class WorkflowPlan:
    custom_attributes: dict[str | None, int]
    sms_templates: list[tuple[SmsTemplate, datetime]]


@dataclass(slots=True, frozen=True)
class SmsStep:
    attribute: str | None
    template: SmsTemplate
    send_at: time


@dataclass(slots=True, frozen=True)
class WorkflowDefinition:
    today: list[SmsStep]
    tomorrow: list[SmsStep]


@dataclass(slots=True, frozen=True)
class PageContextDefinition:
    page: LandingPage
    register_type: RegisterType
    welcome_sms_template: SmsTemplate
    timezone: ZoneInfo
    workflow_definition: WorkflowDefinition
