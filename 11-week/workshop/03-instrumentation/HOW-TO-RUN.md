# How to run - qone_workflow_obs

A minimal `qone-workflow` (Python 3.12, FastAPI, the stack of the team) with the first step of the
`enroll-student` saga, `check-tuition`, and its observability:

- `trace_context.py` - W3C `traceparent`: read, create, child span.
- `logging_json.py` - the CP2 log contract, one JSON line per event, with `trace_id` and `span_id`.
- `middleware.py` - reads or creates the trace context, returns it in the response, logs the request.
- `billing_client.py` - the call to `qone-billing-api` (`GET /api/v1/billing/students/{studentId}/invoices/current`) carries a child span.
- `metrics.py` + `GET /metrics` - `workflow_saga_requests_total` (counter by outcome) and `workflow_saga_duration_seconds` (histogram).
- `tests/test_trace_propagation.py` - the trace_id received is the trace_id sent to billing.

## Install, run the tests (Windows, PowerShell)

```powershell
cd 11-week\workshop\03-instrumentation
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m pytest -v
```

Output on my machine (2026-10-19):

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-8.4.2, pluggy-1.7.0
rootdir: C:\Users\Usuario\Desktop\Sistemas Distribuidos\sistemas-distribuidos-2026-b-g2\11-week\workshop\03-instrumentation
plugins: anyio-4.15.1
collecting ... collected 2 items
tests/test_trace_propagation.py::test_trace_id_received_is_the_trace_id_sent_to_billing PASSED [ 50%]
tests/test_trace_propagation.py::test_logs_follow_the_cp2_contract_and_metrics_count_the_outcome PASSED [100%]
======================== 2 passed, 1 warning in 0.98s =========================
```

## What the logs look like

One `POST /api/v1/sagas/enroll-student` for Laura (ISW-604 group 1) with an incoming `traceparent`
and billing answering `PAID`. The three lines keep the caller's `trace_id`, the service answers with
the same trace in its `traceparent` header, and `/metrics` counts the outcome:

```
{"timestamp": "2026-10-19T14:26:29.692Z", "level": "INFO", "service": "qone-workflow", "version": "2.0.0", "environment": "qa", "trace_id": "7a3f9c1e5b2d4f60a1c8e9b0d2f4a6c8", "span_id": "6ffdbf1ac8c2aaae", "correlation_id": "wf-7a3f9c1e", "event": "saga.started", "message": "enroll-student started", "saga_step": "check-tuition", "section_id": "55555555-5555-4555-8555-555555555505"}
{"timestamp": "2026-10-19T14:26:29.692Z", "level": "INFO", "service": "qone-workflow", "version": "2.0.0", "environment": "qa", "trace_id": "7a3f9c1e5b2d4f60a1c8e9b0d2f4a6c8", "span_id": "6ffdbf1ac8c2aaae", "correlation_id": "wf-7a3f9c1e", "event": "saga.completed", "message": "enroll-student completed", "saga_step": "check-tuition", "rejection_reason": null, "duration_ms": 1}
{"timestamp": "2026-10-19T14:26:29.693Z", "level": "INFO", "service": "qone-workflow", "version": "2.0.0", "environment": "qa", "trace_id": "7a3f9c1e5b2d4f60a1c8e9b0d2f4a6c8", "span_id": "6ffdbf1ac8c2aaae", "correlation_id": "wf-7a3f9c1e", "event": "http.request.completed", "message": "POST /api/v1/sagas/enroll-student", "status": 201, "duration_ms": 3}
response 201 {'status': 'COMPLETED', 'reason': None} 00-7a3f9c1e5b2d4f60a1c8e9b0d2f4a6c8-6ffdbf1ac8c2aaae-01
workflow_saga_requests_total{outcome="completed",saga="enroll-student"} 1.0
```

## What broke and how it was solved

`prometheus_client` was not in the Python environment I use for the Qampus services, so the first
import failed. The module now has its own `requirements.txt` and `.venv` (ignored by git). Starlette
prints a deprecation warning about `httpx` in its test client; it does not affect the tests.
