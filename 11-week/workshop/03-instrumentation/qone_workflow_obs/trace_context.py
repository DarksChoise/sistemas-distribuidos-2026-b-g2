"""W3C trace context for the enroll-student saga of qone-workflow.

traceparent = 00-<trace_id 32 hex>-<span_id 16 hex>-<flags 2 hex>
"""

import re
import secrets
from dataclasses import dataclass

_TRACEPARENT = re.compile(r"^00-([0-9a-f]{32})-([0-9a-f]{16})-([0-9a-f]{2})$")


@dataclass(frozen=True)
class TraceContext:
    trace_id: str
    span_id: str
    parent_span_id: str | None = None
    sampled: bool = True

    def child(self) -> "TraceContext":
        """A new span of the same trace, for an outbound call (billing, enrollment, catalog)."""
        return TraceContext(self.trace_id, secrets.token_hex(8), self.span_id, self.sampled)

    def header(self) -> str:
        return f"00-{self.trace_id}-{self.span_id}-{'01' if self.sampled else '00'}"


def new_trace() -> TraceContext:
    return TraceContext(secrets.token_hex(16), secrets.token_hex(8))


def from_header(value: str | None) -> TraceContext:
    """Continue the caller's trace with a new span; a missing or malformed header starts a new trace."""
    match = _TRACEPARENT.match((value or "").strip().lower())
    if not match:
        return new_trace()
    trace_id, parent_span_id, flags = match.groups()
    if trace_id == "0" * 32 or parent_span_id == "0" * 16:
        return new_trace()
    return TraceContext(trace_id, secrets.token_hex(8), parent_span_id, flags == "01")
