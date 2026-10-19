"""HTTP middleware of qone-workflow: read or create the trace context, return it, log the request."""

import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from .logging_json import current_correlation, current_trace, log
from .trace_context import from_header


class TraceContextMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, logger: logging.Logger) -> None:
        super().__init__(app)
        self.logger = logger

    async def dispatch(self, request: Request, call_next) -> Response:
        ctx = from_header(request.headers.get("traceparent"))
        correlation = request.headers.get("x-correlation-id") or f"wf-{ctx.trace_id[:8]}"
        trace_token = current_trace.set(ctx)
        correlation_token = current_correlation.set(correlation)
        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            log(self.logger, logging.ERROR, "http.request.failed", f"{request.method} {request.url.path}",
                duration_ms=round((time.perf_counter() - start) * 1000))
            raise
        else:
            response.headers["traceparent"] = ctx.header()
            response.headers["x-correlation-id"] = correlation
            log(self.logger, logging.INFO, "http.request.completed", f"{request.method} {request.url.path}",
                status=response.status_code, duration_ms=round((time.perf_counter() - start) * 1000))
            return response
        finally:
            current_trace.reset(trace_token)
            current_correlation.reset(correlation_token)
