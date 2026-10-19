"""A minimal qone-workflow: the first step of enroll-student (check-tuition) with the observability of CP2-CP4."""

import logging
import time

import httpx
from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from pydantic import BaseModel

from .billing_client import BillingClient
from .logging_json import configure, log
from .metrics import REGISTRY, SAGA_DURATION, SAGA_REQUESTS
from .middleware import TraceContextMiddleware


class EnrollStudent(BaseModel):
    studentId: str
    sectionId: str


def create_app(billing_http: httpx.AsyncClient, billing_url: str, environment: str = "develop") -> FastAPI:
    logger = configure(environment)
    billing = BillingClient(billing_http, billing_url)
    app = FastAPI(title="qone-workflow (week 11 instrumentation)")
    app.add_middleware(TraceContextMiddleware, logger=logger)

    @app.post("/api/v1/sagas/enroll-student", status_code=201)
    async def enroll_student(body: EnrollStudent) -> dict:
        start = time.perf_counter()
        log(logger, logging.INFO, "saga.started", "enroll-student started", saga_step="check-tuition",
            section_id=body.sectionId)
        try:
            invoice = await billing.current_invoice(body.studentId)
            paid = invoice.get("status") == "PAID"
            outcome = "completed" if paid else "compensated"
            reason = None if paid else "TUITION_UNPAID"
        except httpx.TimeoutException:
            outcome, reason = "error", "BILLING_TIMEOUT"
        elapsed = time.perf_counter() - start
        SAGA_REQUESTS.labels("enroll-student", outcome).inc()
        SAGA_DURATION.labels("enroll-student", outcome).observe(elapsed)
        level = logging.INFO if outcome == "completed" else logging.WARN
        log(logger, level, f"saga.{outcome}", f"enroll-student {outcome}", saga_step="check-tuition",
            rejection_reason=reason, duration_ms=round(elapsed * 1000))
        return {"status": outcome.upper(), "reason": reason}

    @app.get("/metrics")
    def metrics() -> Response:
        return Response(generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)

    return app
