from collections.abc import Callable
from typing import Any, Self

from ..common import StructuredLogger


class DiscordExceptionsLogger:
    def __init__(self: Self, sender: Callable[[str], Any]) -> None:
        self._sender = sender

    def _format_message(self, event: str, **kwargs: Any) -> str:
        context = StructuredLogger._add_context(kwargs)
        attrs = [f"- {key} => {value}" for key, value in context.items()]
        return f"# {event}\n{attrs}"

    async def warning(self: Self, event: str, **kwargs: Any) -> None:
        message = self._format_message(event=event, kwargs=kwargs)
        await self._sender(message)
        return StructuredLogger.warning(event, **kwargs)

    async def error(self: Self, event: str, **kwargs: Any) -> None:
        message = self._format_message(event=event, kwargs=kwargs)
        await self._sender(message)
        return StructuredLogger.error(event, **kwargs)

    async def exception(self: Self, event: str, **kwargs: Any) -> None:
        message = self._format_message(event=event, kwargs=kwargs)
        await self._sender(message)
        return StructuredLogger.exception(event, **kwargs)
