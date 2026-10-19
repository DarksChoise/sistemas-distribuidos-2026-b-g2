# CP2 - Structured log contract

One JSON object per line, UTF-8, written to stdout by every `qone-*` service (Docker collects it).
The same field names in the gateway, `qone-workflow`, `qone-billing-api`, `qone-enrollment-api`,
`qone-catalog-api`, `qone-worker` and the consumers let us filter the whole `enroll-student` saga by one
`trace_id`.

## Fields

| Field | Type | Required | Example | Why it exists |
|---|---|---|---|---|
| `timestamp` | string, ISO-8601 UTC with ms | yes | `2026-10-19T14:02:11.482Z` | order events across services |
| `level` | `ERROR` `WARN` `INFO` `DEBUG` | yes | `INFO` | filter by severity |
| `service` | string | yes | `qone-workflow` | which repository wrote it |
| `version` | semver | yes | `2.1.0` | link a behaviour to a release tag |
| `environment` | `develop` `qa` `main` | yes | `qa` | the three environments of the norm |
| `trace_id` | 32 hex | yes | `7a3f9c1e5b2d4f60a1c8e9b0d2f4a6c8` | joins every span of one request |
| `span_id` | 16 hex | yes | `b1c2d3e4f5a60718` | the hop that wrote the line |
| `correlation_id` | string | yes | `saga-3f1c2b7e` | business id the student can quote (`X-Correlation-Id`, the saga id) |
| `event` | `domain.action.result` | yes | `saga.step.completed` | stable name to count and alert on |
| `message` | string | yes | `seat reserved` | short human text |
| `duration_ms` | integer | optional | `42` | latency of the operation that ended |

Domain fields of Qampus:

| Field | Example | Why it exists |
|---|---|---|
| `saga_id` | `3f1c2b7e-...` | the `enroll-student` saga in Redis; same value as `GET /api/v1/sagas/{id}` |
| `saga_step` | `reserve-seat` | one of `check-tuition`, `check-eligibility`, `reserve-seat`, `confirm-enrollment`, `commit-seat` |
| `section_id` | `55555555-5555-4555-8555-555555555505` | the `catalog.section` being enrolled (ISW-604 group 1) |
| `subject_code` | `ISW-604` | readable subject of the section |
| `reservation_id` | `ec183527-...` | row of `catalog.seat_reservation` taken by the saga |
| `rejection_reason` | `SCHEDULE_CONFLICT` | the gate that stopped the saga (`TUITION_UNPAID`, `PREREQ_MISSING`, `NO_SEATS`, `SCHEDULE_CONFLICT`, `DUPLICATE`) |
| `student_ref` | `stu_9c41e2` | first 6 hex of SHA-256 of the student id: groups lines of one student without exposing who it is |

## Never log

| Data in Qampus | Where it appears | How it is masked |
|---|---|---|
| Passwords | `POST /api/v1/identity/auth/login` body | never read into a log; the login logs only `event=auth.login.failed` |
| JWT and service tokens | `Authorization` header, `SERVICE_TOKEN` | header dropped; log only `role` and `token_kind` |
| E-mail, full name, student code | identity users, invoices | not logged; `student_ref` instead |
| Payment data | `POST /api/v1/billing/invoices/{id}/pay` | log `invoice_id` and the provider reference, never card or bank data |
| Grades and academic record | enrollment record, advisor prompts | not logged; the advisor logs token counts, not the prompt text |
| `Idempotency-Key` value | every create | log its SHA-256 prefix only |

## Seven lines of one failed saga (same trace_id)

```json
{"timestamp":"2026-10-19T14:02:11.482Z","level":"INFO","service":"qone-api-gateway","version":"2.0.0","environment":"qa","trace_id":"7a3f9c1e5b2d4f60a1c8e9b0d2f4a6c8","span_id":"a0b1c2d3e4f50617","correlation_id":"saga-3f1c2b7e","event":"http.request.received","message":"POST /api/v1/sagas/enroll-student","duration_ms":null}
{"timestamp":"2026-10-19T14:02:11.495Z","level":"INFO","service":"qone-workflow","version":"2.0.0","environment":"qa","trace_id":"7a3f9c1e5b2d4f60a1c8e9b0d2f4a6c8","span_id":"b1c2d3e4f5a60718","correlation_id":"saga-3f1c2b7e","event":"saga.started","message":"enroll-student started","saga_id":"3f1c2b7e","section_id":"55555555-5555-4555-8555-555555555506","subject_code":"ISW-604","student_ref":"stu_9c41e2"}
{"timestamp":"2026-10-19T14:02:14.501Z","level":"WARN","service":"qone-workflow","version":"2.0.0","environment":"qa","trace_id":"7a3f9c1e5b2d4f60a1c8e9b0d2f4a6c8","span_id":"c2d3e4f5a6071829","correlation_id":"saga-3f1c2b7e","event":"saga.step.timeout","message":"qone-billing-api did not answer, retrying","saga_id":"3f1c2b7e","saga_step":"check-tuition","duration_ms":3002}
{"timestamp":"2026-10-19T14:02:14.689Z","level":"INFO","service":"qone-billing-api","version":"2.0.0","environment":"qa","trace_id":"7a3f9c1e5b2d4f60a1c8e9b0d2f4a6c8","span_id":"d3e4f5a607182930","correlation_id":"saga-3f1c2b7e","event":"invoice.current.read","message":"current invoice is PAID","duration_ms":21}
{"timestamp":"2026-10-19T14:02:14.702Z","level":"INFO","service":"qone-workflow","version":"2.0.0","environment":"qa","trace_id":"7a3f9c1e5b2d4f60a1c8e9b0d2f4a6c8","span_id":"c2d3e4f5a6071829","correlation_id":"saga-3f1c2b7e","event":"saga.step.completed","message":"check-tuition ok after 1 retry","saga_id":"3f1c2b7e","saga_step":"check-tuition","duration_ms":3207}
{"timestamp":"2026-10-19T14:02:14.744Z","level":"INFO","service":"qone-enrollment-api","version":"2.0.0","environment":"qa","trace_id":"7a3f9c1e5b2d4f60a1c8e9b0d2f4a6c8","span_id":"e4f5a60718293a4b","correlation_id":"saga-3f1c2b7e","event":"eligibility.rejected","message":"group 2 overlaps ISW-601 on TUE and THU 08:00-10:00","section_id":"55555555-5555-4555-8555-555555555506","rejection_reason":"SCHEDULE_CONFLICT","duration_ms":38}
{"timestamp":"2026-10-19T14:02:14.751Z","level":"WARN","service":"qone-workflow","version":"2.0.0","environment":"qa","trace_id":"7a3f9c1e5b2d4f60a1c8e9b0d2f4a6c8","span_id":"b1c2d3e4f5a60718","correlation_id":"saga-3f1c2b7e","event":"saga.compensated","message":"enroll-student stopped at check-eligibility","saga_id":"3f1c2b7e","saga_step":"check-eligibility","rejection_reason":"SCHEDULE_CONFLICT","duration_ms":3256}
```

Filtered by `trace_id`, the lines tell the story: the gateway receives the request, the saga starts,
billing times out once (3 s), answers on the retry, enrollment rejects the group for a schedule
conflict, and the saga compensates. Nothing was reserved, so there is no seat to release.

## Levels

| Level | When Qampus uses it | Example |
|---|---|---|
| `ERROR` | the request failed and needs a person; a compensation that itself failed | `saga.compensation.failed` when `DELETE .../reservations/{rid}` answers 5xx |
| `WARN` | degraded but handled: retry, timeout, business rejection, circuit breaker open | `saga.step.timeout` to `qone-billing-api`; `advisor.llm.degraded` |
| `INFO` | a business fact or the end of a request | `saga.step.completed`, `enrollment.confirmed`, `seat.committed` |
| `DEBUG` | detail for local development only, off in `qa` and `main` | the parsed eligibility input of `POST /eligibility-checks` |
