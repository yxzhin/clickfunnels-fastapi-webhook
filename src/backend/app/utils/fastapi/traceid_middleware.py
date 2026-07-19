import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from ..common import StructuredLogger, start_time_var, trace_id_var


class TraceIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware for generation and addition of trace_id to every entering HTTP request.
    Trace_id is used for tracking requests in the logs
    """

    async def dispatch(self, request: Request, call_next):
        """Processes the incoming HTTP request by adding the trace_id and logging the beginning and end of the request."""
        trace_id = str(uuid.uuid4())  # Generate trace_id
        trace_id_var.set(
            trace_id  # type: ignore
        )  # Put trace_id into request context
        start_time_var.set(time.time())  # type: ignore
        ip = (
            request.headers.get("X-Forwarded-For") or request.client.host
            if request.client
            else "unknown"
        )
        request.state.trace_id = trace_id  # Add trace_id into the request state
        request.state.ip = ip
        StructuredLogger.info("request.start", client_ip=ip)

        response = await call_next(request)  # Execute the actual request

        StructuredLogger.info(
            "request.end",
        )

        return response
