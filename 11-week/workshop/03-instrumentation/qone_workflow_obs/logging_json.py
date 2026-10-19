"""Structured logger of the CP2 contract: one JSON object per line, trace fields injected."""

import json
import logging
import sys
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import TextIO

from .trace_context import TraceContext

SERVICE = "qone-workflow"
VERSION = "2.0.0"

current_trace: ContextVar[TraceContext | None] = ContextVar("current_trace", default=None)
current_correlation: ContextVar[str | None] = ContextVar("current_correlation", default=None)

# Fields of the "never log" list of CP2: dropped even if a caller passes them.
NEVER_LOG = {"password", "authorization", "token", "service_token", "email", "full_name", "idempotency_key"}


class JsonFormatter(logging.Formatter):
    def __init__(self, environment: str) -> None:
        super().__init__()
        self.environment = environment

    def format(self, record: logging.LogRecord) -> str:
        ctx = current_trace.get()
        line = {
            "timestamp": datetime.fromtimestamp(record.created, timezone.utc)
            .isoformat(timespec="milliseconds")
            .replace("+00:00", "Z"),
            "level": record.levelname,
            "service": SERVICE,
            "version": VERSION,
            "environment": self.environment,
            "trace_id": ctx.trace_id if ctx else None,
            "span_id": ctx.span_id if ctx else None,
            "correlation_id": current_correlation.get(),
            "event": getattr(record, "event", "log"),
            "message": record.getMessage(),
        }
        for key, value in getattr(record, "fields", {}).items():
            if key not in NEVER_LOG:
                line[key] = value
        return json.dumps(line, ensure_ascii=False)


def configure(environment: str = "develop", stream: TextIO | None = None) -> logging.Logger:
    logger = logging.getLogger(SERVICE)
    logger.handlers.clear()
    handler = logging.StreamHandler(stream or sys.stdout)
    handler.setFormatter(JsonFormatter(environment))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger


def log(logger: logging.Logger, level: int, event: str, message: str, **fields: object) -> None:
    logger.log(level, message, extra={"event": event, "fields": fields})
