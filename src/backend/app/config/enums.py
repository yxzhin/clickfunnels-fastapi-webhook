from enum import StrEnum
from typing import Self


class LandingPage(StrEnum):
    REGISTRATION_TODAY_LA = "registration-today-la"
    REGISTRATION_TOMORROW_LA = "registration-tomorrow-la"
    REGISTRATION_TODAY_AU = "registration-today-au"
    REGISTRATION_TOMORROW_AU = "registration-tomorrow-au"


class SmsTemplate(StrEnum):
    WELCOME_LA = "WELCOME_LA"
    LA_2_HOURS_BEFORE = "LA_2_HOURS_BEFORE"
    LA_1_HOUR_BEFORE = "LA_1_HOUR_BEFORE"
    LA_START = "LA_START"
    LA_MORNING_REMINDER = "LA_MORNING_REMINDER"

    WELCOME_AU = "WELCOME_AU"
    AU_2_HOURS_BEFORE = "AU_2_HOURS_BEFORE"
    AU_1_HOUR_BEFORE = "AU_1_HOUR_BEFORE"
    AU_START = "AU_START"
    AU_MORNING_REMINDER = "AU_MORNING_REMINDER"

    @property
    def text(self: Self) -> str:
        return self.value


class RegisterType(StrEnum):
    TODAY = "today"
    TOMORROW = "tomorrow"
