from enum import StrEnum
from typing import Self


class LandingPage(StrEnum):
    REGISTRATION_TODAY_LA = "registration-today-la"
    REGISTRATION_TOMORROW_LA = "registration-tomorrow-la"
    REGISTRATION_TODAY_AU = "registration-today-au"
    REGISTRATION_TOMORROW_AU = "registration-tomorrow-au"


class SmsTemplate(StrEnum):
    LA_WELCOME_TODAY = "Hi, you’re registered for Yuliya’s FREE Russian Manicure webinar today at 3 PM PT / 6 PM ET. Save the time – your join link will arrive before we start."
    LA_WELCOME_TOMORROW = "Hi, you’re registered for Yuliya’s FREE Russian Manicure webinar tomorrow at 3 PM PT / 6 PM ET. Save the time – your join link will arrive before we start."
    LA_MORNING_REMINDER = "We’re going live today at 3 PM PT / 6 PM ET. You’ll see the Russian Manicure process on a real model and learn what affects retention, speed, and clean results."
    LA_2_HOURS_BEFORE = "We’re going live in 2 hours. See the Russian Manicure process on a real model and learn what causes lifting, bulky shape, and inconsistent results. Save the time: 3 PM PT / 6 PM ET."
    LA_1_HOUR_BEFORE = "Starting in 1 hour. Join Yuliya’s FREE Russian Manicure webinar here: https://start.bizon365.ru/room/ybprofessional/veb_online"
    LA_START = "We’re LIVE now. Join the Russian Manicure webinar here: https://start.bizon365.ru/room/ybprofessional/veb_online"
    LA_15_MINUTES_AFTER_START = "We’re already inside the live demo. Join now to see clean cuticle work, proper prep, and how to avoid lifting: https://start.bizon365.ru/room/ybprofessional/veb_online"
    LA_1_HOUR_AFTER_START = "Ready to improve your technique and create premium-looking results? Get access to Yuliya’s full online training here: https://cf.ybcourses.online/learnrussian-manicure?utm_source=web_email"
    LA_1_DAY_AFTER_WEB = "Still dealing with lifting, uneven structure, or sets that take too long? Learn the full system step by step. Your special offer is still available: https://cf.ybcourses.online/learnrussian-manicure?utm_source=web_email"
    LA_2_DAYS_AFTER_WEB = "Last chance to get the special webinar offer for Yuliya’s online nail courses. Upgrade your skills and work with more confidence: https://cf.ybcourses.online/learnrussian-manicure?utm_source=web_email"

    AU_WELCOME_TODAY = "Hi, you’re registered for Yuliya’s FREE Russian Manicure webinar today at 7 PM Sydney Time. Save the time – your join link will arrive before we start."
    AU_WELCOME_TOMORROW = "Hi, you’re registered for Yuliya’s FREE Russian Manicure webinar tomorrow at 7 PM Sydney Time. Save the time – your join link will arrive before we start."
    AU_MORNING_REMINDER = "We’re going live today at 7 PM Sydney Time. You’ll see the Russian Manicure process on a real model and learn what affects retention, speed, and clean results."
    AU_2_HOURS_BEFORE = "We’re going live in 2 hours. See the Russian Manicure process on a real model and learn what causes lifting, bulky shape, and inconsistent results. Save the time: 7 PM Sydney Time."
    AU_1_HOUR_BEFORE = "Starting in 1 hour. Join Yuliya’s FREE Russian Manicure webinar here: https://start.bizon365.ru/room/ybprofessional/webinar"
    AU_START = "We’re LIVE now. Join the Russian Manicure webinar here: https://start.bizon365.ru/room/ybprofessional/webinar"
    AU_15_MINUTES_AFTER_START = "We’re already inside the live demo. Join now to see clean cuticle work, proper prep, and how to avoid lifting: https://start.bizon365.ru/room/ybprofessional/webinar"
    AU_1_HOUR_AFTER_START = "Ready to improve your technique and create premium-looking results? Get access to Yuliya’s full online training here: https://cf.ybcourses.online/learnrussian-manicure?utm_source=web_email"
    AU_1_DAY_AFTER_WEB = "Still dealing with lifting, uneven structure, or sets that take too long? Learn the full system step by step. Your special offer is still available: https://cf.ybcourses.online/learnrussian-manicure?utm_source=web_email"
    AU_2_DAYS_AFTER_WEB = "Last chance to get the special webinar offer for Yuliya’s online nail courses. Upgrade your skills and work with more confidence: https://cf.ybcourses.online/learnrussian-manicure?utm_source=web_email"

    # AFTER_REG_5_MINUTES = "AFTER_REG_5_MINUTES"
    # AFTER_REG_1_HOUR = "AFTER_REG_1_HOUR"

    @property
    def text(self: Self) -> str:
        return self.value


class RegisterType(StrEnum):
    TODAY = "today"
    TOMORROW = "tomorrow"
