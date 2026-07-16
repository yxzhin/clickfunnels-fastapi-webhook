from enum import StrEnum
from typing import Self


class LandingPage(StrEnum):
    REGISTRATION_TODAY = "registration-today"
    REGISTRATION_TOMORROW = "registration-tomorrow"

    @property
    def label(self: Self) -> str:
        return {
            LandingPage.REGISTRATION_TODAY: "регистрация на сегодня",
            LandingPage.REGISTRATION_TOMORROW: "регистрация на завтра",
        }[self]


class SmsTemplate(StrEnum):
    WELCOME = "SMS_TEMPLATE_WELCOME"
    FOLLOW_UP_2 = "SMS_TEMPLATE_2"
    FOLLOW_UP_3 = "SMS_TEMPLATE_3"
    FOLLOW_UP_4 = "SMS_TEMPLATE_4"
    FOLLOW_UP_5 = "SMS_TEMPLATE_5"

    @property
    def text(self: Self) -> str:
        return self.value
