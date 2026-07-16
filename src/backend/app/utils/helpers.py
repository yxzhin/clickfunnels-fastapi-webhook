from datetime import datetime, timedelta
from string import whitespace
from typing import ClassVar, Self
from zoneinfo import ZoneInfo


class Helpers:
    """utility class w/ general helper functions so I don't repeat myself"""

    _clear_whitespace_trans_table: ClassVar[dict[int, int | None]] = str.maketrans(
        "", "", whitespace
    )
    LA_TZ: ClassVar[ZoneInfo] = ZoneInfo("America/Los_Angeles")

    @classmethod
    def clear_whitespace(cls: type[Self], value: str) -> str:
        return value.translate(cls._clear_whitespace_trans_table)

    @staticmethod
    def trim(value: str) -> str:
        """trim sounds cooler so why not"""
        return value.strip()

    @classmethod
    def now_la(cls: type[Self]) -> datetime:
        return datetime.now(cls.LA_TZ)

    @classmethod
    def to_la(cls: type[Self], dt: datetime) -> datetime:
        return dt.astimezone(cls.LA_TZ)

    @staticmethod
    def same_day_time(
        base: datetime,
        hour: int,
        minute: int = 0,
    ) -> datetime:
        return base.replace(hour=hour, minute=minute, second=0, microsecond=0)

    @staticmethod
    def next_day_time(
        base: datetime,
        hour: int,
        minute: int = 0,
    ) -> datetime:
        tomorrow = base + timedelta(days=1)
        return tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)
