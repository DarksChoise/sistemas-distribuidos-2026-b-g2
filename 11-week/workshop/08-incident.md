# CP9 - Incident drill and blameless postmortem

## The drill

Assumed incident on the hop `qone-workflow` -> `qone-billing-api` (step 3 of CP1, `check-tuition`,
`GET /api/v1/billing/students/{studentId}/invoices/current`): during **40 minutes**, from 08:10 to 08:50 of
the first day of enrollment, billing answers in **3 s for 25 %** of the requests. Assumed cause for the
drill: the connection pool of `qone-billing-api` to `billing-db` is too small for the first-day peak, so
one request in four waits about 3 s for a free connection.

Traffic at that hour (CP6): about 400 sagas per hour, so **about 267 sagas** in the 40 minutes and
**about 67 slow ones**.

## Trace of one slow request (span tree with durations)

- `POST /api/v1/sagas/enroll-student` - `qone-api-gateway` - **3,412 ms**
  - `saga enroll-student` - `qone-workflow` - 3,398 ms
    - `check-tuition` - `qone-workflow` -> `qone-billing-api` - **3,021 ms**
      - `GET .../invoices/current` - `qone-billing-api` - 3,004 ms (2,981 ms waiting for a `billing-db` connection, 18 ms of query)
    - `check-eligibility` - `qone-enrollment-api` - 64 ms
    - `reserve-seat` - `qone-catalog-api` - 88 ms
    - `confirm-enrollment` - `qone-enrollment-api` - 97 ms
    - `commit-seat` - `qone-catalog-api` - 71 ms
  - `outbox relay EnrollmentConfirmed` - `qone-worker` - 1,200 ms after the commit (async, same trace_id)

The saga is slow but it does not fail: `qone-workflow` waits up to 10 s per call (3 attempts) before a
step is `Unavailable`, so a 3 s answer is accepted. CP2 and CP4 assumed a 3 s timeout; the real client in
`qone-workflow` (`adapter/outbound/participants/http.py`) uses 10 s, which is why this incident is a
latency problem and not an availability one.

## Four log lines of that trace (CP2 format)

```json
{"timestamp":"2026-10-19T13:22:04.118Z","level":"INFO","service":"qone-workflow","version":"2.0.0","environment":"main","trace_id":"c41d7e2a9b0f43158a6e2d9c7b5a3f10","span_id":"5a6b7c8d9e0f1a2b","correlation_id":"saga-8e21d4c0","event":"saga.started","message":"enroll-student started","saga_id":"8e21d4c0","section_id":"55555555-5555-4555-8555-555555555505","subject_code":"ISW-604","student_ref":"stu_31b7aa"}
{"timestamp":"2026-10-19T13:22:07.122Z","level":"WARN","service":"qone-billing-api","version":"2.0.0","environment":"main","trace_id":"c41d7e2a9b0f43158a6e2d9c7b5a3f10","span_id":"6b7c8d9e0f1a2b3c","correlation_id":"saga-8e21d4c0","event":"db.pool.wait","message":"waited for a billing-db connection","duration_ms":2981}
{"timestamp":"2026-10-19T13:22:07.143Z","level":"INFO","service":"qone-workflow","version":"2.0.0","environment":"main","trace_id":"c41d7e2a9b0f43158a6e2d9c7b5a3f10","span_id":"7c8d9e0f1a2b3c4d","correlation_id":"saga-8e21d4c0","event":"saga.step.completed","message":"check-tuition ok","saga_step":"check-tuition","duration_ms":3021}
{"timestamp":"2026-10-19T13:22:07.516Z","level":"INFO","service":"qone-workflow","version":"2.0.0","environment":"main","trace_id":"c41d7e2a9b0f43158a6e2d9c7b5a3f10","span_id":"5a6b7c8d9e0f1a2b","correlation_id":"saga-8e21d4c0","event":"saga.completed","message":"enroll-student completed","saga_id":"8e21d4c0","duration_ms":3398}
```

## SLIs during the incident

| SLO (CP6) | SLI in the 40 minutes | Effect on the 30-day budget |
|---|---|---|
| 1 Availability 99.5 % | 100 % (no saga ends in `error`) | 0 of 24 failed sagas |
| 2 Latency 99 % within 3 s | 200 of 267 = **75 %** | 67 slow sagas of a budget of 48: **140 %, the latency budget is gone** |
| 3 Freshness 99 % within 60 s | 100 % (the worker is not affected) | 0 |

## Which alert fires first

**None of the alerts of CP7.** They watch SLO 1, and no saga fails. The first signal is a student report
to the academic office at about **minute 15** (08:25). A latency burn-rate alert on SLO 2 would have fired
first: the error ratio of SLO 2 is 25 %, a burn rate of 25 against a budget of 1 %, above 14.4, so the
same 1 h and 5 min rule would fire at about **minute 7** (5 minutes of window plus 2 minutes of `for`).

## Which runbook step stops the bleeding

Runbook CP8, step 2 (confirm): the PromQL of p95 latency by service shows `qone-billing-api` at 3.0 s
while enrollment and catalog stay under 100 ms. Mitigation 1 (restart `qone-billing-api`) at minute 36
(08:46) frees the waiting connections; latency is back under 1 s at minute 38, before the peak ends.

## Blameless postmortem

**Timeline (first day of enrollment)**

| Time | Minute | Event |
|---|---|---|
| 08:10 | 0 | Peak starts; 25 % of `check-tuition` calls take about 3 s |
| 08:25 | 15 | Academic office forwards student reports: "Enrolling..." takes long |
| 08:31 | 21 | On-call confirms with the runbook PromQL: billing p95 = 3.0 s, error ratio 0 % |
| 08:40 | 30 | Logs by `trace_id` show `db.pool.wait` lines in `qone-billing-api` |
| 08:46 | 36 | Mitigation 1: restart `qone-billing-api` |
| 08:48 | 38 | p95 of the saga back to 0.3 s |
| 08:50 | 40 | End of the incident window |

**Impact:** about 267 sagas in the window, 67 of them over 3 s (no failed enrollment, no seat lost);
latency budget of the month spent at 140 %; in minutes, 40 min x 25 % = 10 bad minutes of a 432-minute
budget (2.3 %), which shows again that for Qampus the budget in requests is the meaningful one.

**Root cause:** the pool of connections from `qone-billing-api` to `billing-db` was sized for normal
traffic, not for the first-day peak.

**Contributing factors:** only availability is alerted (CP7); the Prometheus of `qone-infra` does not
scrape the services yet; the documents assumed a 3 s timeout while the client waits 10 s; one replica
per service.

**Action items**

1. *As the on-call developer, I want a burn-rate alert on the latency SLO of `enroll-student`, so that a
   slow participant pages me before students do.*
   Acceptance: a `promtool test rules` case with 25 % of sagas over 3 s for 10 minutes fires
   `EnrollStudentSagaLatencyFastBurn` by minute 7; with 0.5 % it does not fire.
2. *As a student, I want the saga to stop waiting on billing after 3 s, so that I get an answer instead of
   a long "Enrolling...".*
   Acceptance: with `qone-billing-api` answering in 5 s, `POST /api/v1/sagas/enroll-student` ends
   `COMPENSATED` with reason `BILLING_UNAVAILABLE` in less than 4 s, and no seat stays `RESERVED`.
3. *As the maintainer of `qone-infra`, I want Prometheus to scrape `/metrics` of `qone-workflow` and the
   three participants, so that the SLIs of CP6 exist outside the workshop.*
   Acceptance: after `scripts/up.sh` and `scripts/smoke.sh`, `up{job="qone-workflow"} == 1` and
   `workflow_saga_requests_total` returns a series in Prometheus.
