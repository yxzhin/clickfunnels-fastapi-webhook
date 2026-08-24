from enum import Enum, StrEnum
from typing import Self


class LandingPage(StrEnum):
    REGISTRATION_TODAY_LA = "registration-today-la"
    REGISTRATION_TOMORROW_LA = "registration-tomorrow-la"
    REGISTRATION_TODAY_AU = "registration-today-au"
    REGISTRATION_TOMORROW_AU = "registration-tomorrow-au"

    REGISTRATION_LIVE_ONLINE_WEBINAR = "registration-live-online-webinar"


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

    LIVE_ONLINE_WEBINAR_WELCOME = "Hi, you’re registered for Yuliya’s FREE Russian Manicure webinar August 19 at 3 PM PT / 6 PM ET. Save the time – your join link will arrive before we start."
    LIVE_ONLINE_WEBINAR_1_DAY_AFTER_REG = "Reminder: live Russian Manicure webinar — August 19, 6 PM PT / 9 PM ET. RM, Hard Gel, Dual Forms & $100+ services. Join: https://start.bizon365.ru/room/ybprofessional/veb27"
    LIVE_ONLINE_WEBINAR_1_DAY_BEFORE_WEB = "Tomorrow: live webinar with Yuliya at 6 PM PT / 9 PM ET. Russian Manicure, Hard Gel & Dual Forms. Join: https://start.bizon365.ru/room/ybprofessional/veb27"
    LIVE_ONLINE_WEBINAR_MORNING_REMINDER = "Today at 6 PM PT / 9 PM ET. Yuliya will show Russian Manicure + Dual Forms process videos. Join: https://start.bizon365.ru/room/ybprofessional/veb27"
    LIVE_ONLINE_WEBINAR_3_HOURS_BEFORE = "Starting in 3 hours. Russian Manicure, Hard Gel & Dual Forms. Join the live webinar: https://start.bizon365.ru/room/ybprofessional/veb27"
    LIVE_ONLINE_WEBINAR_2_HOURS_BEFORE = "Starting in 2 hours. Join the live webinar: https://start.bizon365.ru/room/ybprofessional/veb27"
    LIVE_ONLINE_WEBINAR_1_HOUR_BEFORE = "Starting in 1 hour. Join the live webinar: https://start.bizon365.ru/room/ybprofessional/veb27"
    LIVE_ONLINE_WEBINAR_10_MINUTES_BEFORE = "We’re starting in 10 minutes. Join here: https://start.bizon365.ru/room/ybprofessional/veb27"
    LIVE_ONLINE_WEBINAR_START = (
        "We’re live now. Join here: https://start.bizon365.ru/room/ybprofessional/veb27"
    )
    LIVE_ONLINE_WEBINAR_10_MINUTES_AFTER_START = "We’re live — Russian Manicure, Hard Gel, Dual Forms & premium results. Join: https://start.bizon365.ru/room/ybprofessional/veb27"
    LIVE_ONLINE_WEBINAR_AFTER_WEB = "Thank you for joining the webinar 💅 Your special offer is open: get the Complete Nail System for $399 instead of $787. Enroll here: https://cf.ybcourses.online/learnrussian-manicure?utm_source=web_email"
    LIVE_ONLINE_WEBINAR_AFTER_WEB_2 = "Ready to stop guessing and start working with a real system? Russian Manicure + Hard Gel + Dual Forms are now available in one package for $399 instead of $787. Join here: https://cf.ybcourses.online/learnrussian-manicure?utm_source=web_email"
    LIVE_ONLINE_WEBINAR_1_DAY_AFTER = "Reminder: your webinar discount is still active. Get the full combo course for $399 instead of $787 and learn the system behind $100–150 nail services. Secure your access: https://cf.ybcourses.online/learnrussian-manicure?utm_source=web_email"
    LIVE_ONLINE_WEBINAR_2_DAYS_AFTER = "Last chance to get the Complete Nail System for $399 instead of $787. After the offer closes, the regular price returns. Join now: https://cf.ybcourses.online/learnrussian-manicure?utm_source=web_email"

    @property
    def text(self: Self) -> str:
        return self.value


class RegisterType(StrEnum):
    TODAY = "today"
    TOMORROW = "tomorrow"


class WebinarTime(Enum):
    LA_WEB_START_TIME = 15
    AU_WEB_START_TIME = 19
