"""check-tuition step: the call to qone-billing-api carries a child span of the saga's trace."""

import httpx

from .logging_json import current_correlation, current_trace
from .trace_context import new_trace


class BillingClient:
    def __init__(self, http: httpx.AsyncClient, base_url: str, timeout_s: float = 3.0) -> None:
        self._http = http
        self._base = base_url.rstrip("/")
        self._timeout = timeout_s

    async def current_invoice(self, student_id: str) -> dict:
        span = (current_trace.get() or new_trace()).child()
        headers = {"traceparent": span.header(), "x-correlation-id": current_correlation.get() or ""}
        response = await self._http.get(
            f"{self._base}/api/v1/billing/students/{student_id}/invoices/current",
            headers=headers,
            timeout=self._timeout,
        )
        response.raise_for_status()
        return response.json()
