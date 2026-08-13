import contextvars
import datetime
import json
import logging
import sys
import time
import uuid
from collections.abc import ItemsView, KeysView, ValuesView
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any
from zoneinfo import ZoneInfo

from loguru import logger

# Context for trace_id and start_time
trace_id_var = contextvars.ContextVar("trace_id", default=None)
start_time_var = contextvars.ContextVar("time_start", default=None)


class StructuredLogger:
    """
    Structured logger with context support and simplified objects.
    Logs events in JSON format with additional context fields,
    such as trace_id and time passed from startup.
    """

    @staticmethod
    def _get_trace_id() -> str:
        """Returns the current trace_id or generates a new one"""
        return trace_id_var.get() or str(uuid.uuid4())

    @staticmethod
    def _add_context(kwargs: dict[Any, Any]) -> dict[str, Any]:
        """Adds context fields to log data."""
        start_time = start_time_var.get() or time.time()
        return {
            "trace_id": StructuredLogger._get_trace_id(),
            "time_from_start_ms": round((time.time() - start_time) * 1000, 2),
            **kwargs,
        }

    @staticmethod
    def info(event: str, **kwargs: Any) -> None:
        """Logs info message with context"""
        logger.bind(**StructuredLogger._add_context(kwargs)).info(event)

    @staticmethod
    def warning(event: str, **kwargs: Any) -> None:
        """Logs warning message with context"""
        logger.bind(**StructuredLogger._add_context(kwargs)).warning(event)

    @staticmethod
    def error(event: str, **kwargs: Any) -> None:
        """Logs error message with context"""
        logger.bind(**StructuredLogger._add_context(kwargs)).error(event)

    @staticmethod
    def exception(event: str, **kwargs: Any) -> None:
        """Logs exceptions with context"""
        logger.bind(**StructuredLogger._add_context(kwargs)).exception(event)

    @staticmethod
    def debug(event: str, **kwargs: Any) -> None:
        """Logs debug message with exceptions"""
        logger.bind(**StructuredLogger._add_context(kwargs)).debug(event)

    @staticmethod
    def simplify(value: Any, max_depth: int = 5) -> Any:
        """Simplifies the logging object, avoiding cyclic links and limiting link depth."""
        return StructuredLogger._simplify_internal(
            value, visited_ids=set(), depth=0, max_depth=max_depth
        )

    @staticmethod
    def _simplify_internal(
        value: Any, visited_ids: set[int], depth: int, max_depth: int
    ) -> Any:
        """Inner recursive function for object simplification"""
        if depth > max_depth:
            return f"<max-depth-exceeded-{type(value).__name__}>"

        if id(value) in visited_ids:
            return f"<circular-ref {type(value).__name__}>"

        visited_ids.add(id(value))

        if isinstance(value, Enum):
            return value.value

        elif isinstance(value, uuid.UUID):
            return value.hex

        elif isinstance(value, (KeysView, ValuesView, ItemsView)):
            return StructuredLogger._simplify_internal(
                list(value),  # type: ignore
                visited_ids,
                depth + 1,
                max_depth,  # type: ignore
            )

        elif hasattr(value, "__dict__"):
            return {
                k: StructuredLogger._simplify_internal(
                    v, visited_ids, depth + 1, max_depth
                )
                for k, v in value.__dict__.items()
            }

        elif isinstance(value, dict):
            return {
                StructuredLogger._simplify_internal(
                    k, visited_ids, depth + 1, max_depth
                ): StructuredLogger._simplify_internal(
                    v, visited_ids, depth + 1, max_depth
                )
                for k, v in value.items()  # type: ignore
            }

        elif isinstance(value, (list, tuple, set)):
            return [
                StructuredLogger._simplify_internal(
                    v, visited_ids, depth + 1, max_depth
                )
                for v in value  # type: ignore
            ]

        elif is_dataclass(value) and hasattr(value, "to_json"):
            return value.to_json()  # type: ignore

        elif is_dataclass(value):
            return asdict(value)  # type: ignore

        elif isinstance(value, datetime.datetime):
            return value.isoformat()

        elif isinstance(value, ZoneInfo):
            return value.key

        else:
            return value

    @staticmethod
    def setup() -> None:
        """Configures the logger for structured logging in JSON format."""
        global logger
        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
        logger.remove()

        def serialize(record: Any) -> str:
            """Serializes the log entry into JSON"""
            return json.dumps(
                {
                    "timestamp": record["time"].timestamp(),
                    "timestamp_readable": f"{datetime.datetime.now()}",
                    "level": record["level"].name,
                    "message": record["message"],
                    "trace_id": record["extra"].pop("trace_id"),
                    "time_from_start_ms": record["extra"].pop("time_from_start_ms"),
                    "extra": StructuredLogger.simplify(record["extra"]),
                    **(
                        {"exception": str(record["exception"])}
                        if record["exception"]
                        else {}
                    ),
                }
            )

        # On top of the patch, add it to extra.serialized
        logger = logger.patch(
            lambda record: record["extra"].update({"serialized": serialize(record)})
        )

        # Use the format with {extra[serialized]} as JSON
        logger.add(
            sys.stdout,
            level="INFO",
            format="{extra[serialized]}\n",
            serialize=False,
        )

        StructuredLogger.info("init.logger_initialized")
