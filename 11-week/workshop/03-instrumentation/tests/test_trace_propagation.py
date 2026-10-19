"""The trace_id that reaches qone-workflow is the trace_id it sends to qone-billing-api."""

import io
import json

import httpx
from fastapi.testclient import TestClient

from qone_workflow_obs import logging_json
from qone_workflow_obs.app import create_app

TRACE_ID = "7a3f9c1e5b2d4f60a1c8e9b0d2f4a6c8"
INCOMING = f"00-{TRACE_ID}-a0b1c2d3e4f50617-01"
LAURA = "11111111-1111-4111-8111-111111111111"
ISW_604_G1 = "55555555-5555-4555-8555-555555555505"


def billing_stub(seen: list[httpx.Request], status: str = "PAID") -> httpx.AsyncClient:
    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"status": status, "term": "2026-B"})

    return httpx.AsyncClient(transport=httpx.MockTransport(handler))


def test_trace_id_received_is_the_trace_id_sent_to_billing():
    seen: list[httpx.Request] = []
    client = TestClient(create_app(billing_stub(seen), "http://qone-billing-api:8000", "qa"))

    response = client.post("/api/v1/sagas/enroll-student", json={"studentId": LAURA, "sectionId": ISW_604_G1},
                           headers={"traceparent": INCOMING, "x-correlation-id": "saga-3f1c2b7e"})

    assert response.status_code == 201 and response.json()["status"] == "COMPLETED"
    downstream = seen[0].headers["traceparent"].split("-")
    assert seen[0].url.path == f"/api/v1/billing/students/{LAURA}/invoices/current"
    assert downstream[1] == TRACE_ID
    assert downstream[2] != "a0b1c2d3e4f50617"
    assert seen[0].headers["x-correlation-id"] == "saga-3f1c2b7e"
    assert response.headers["traceparent"].split("-")[1] == TRACE_ID


def test_logs_follow_the_cp2_contract_and_metrics_count_the_outcome():
    seen: list[httpx.Request] = []
    app = create_app(billing_stub(seen, status="ISSUED"), "http://qone-billing-api:8000", "qa")
    buffer = io.StringIO()
    logging_json.configure("qa", buffer)
    client = TestClient(app)

    client.post("/api/v1/sagas/enroll-student", json={"studentId": LAURA, "sectionId": ISW_604_G1},
                headers={"traceparent": INCOMING})

    lines = [json.loads(line) for line in buffer.getvalue().splitlines()]
    assert {line["trace_id"] for line in lines} == {TRACE_ID}
    assert {"timestamp", "level", "service", "version", "environment", "span_id", "correlation_id",
            "event", "message"} <= set(lines[0])
    assert any(line["event"] == "saga.compensated" and line["rejection_reason"] == "TUITION_UNPAID" for line in lines)
    metrics = client.get("/metrics").text
    assert 'workflow_saga_requests_total{outcome="compensated",saga="enroll-student"} 1.0' in metrics
