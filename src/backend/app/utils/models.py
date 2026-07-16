from dataclasses import dataclass
from typing import Any

from .helpers import Helpers


@dataclass(slots=True)
class ClickFunnelsContact:
    id: str | int | None
    email: str | None
    phone_number: str | None
    first_name: str | None
    last_name: str | None
    page_name: str | None
    custom_attributes: dict[str, Any]

    @property
    def full_name(self) -> str:
        parts = [p for p in [self.first_name, self.last_name] if p]
        return Helpers.trim(" ".join(parts))

    @property
    def has_phone(self) -> bool:
        return bool(self.phone_number and Helpers.trim(self.phone_number))
