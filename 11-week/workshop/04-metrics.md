# CP4 - Golden signals and metric catalog

One table per component of the `enroll-student` journey (CP1). Names follow Prometheus conventions:
snake_case, the unit as suffix (`_seconds`, `_bytes`), `_total` for counters. Every PromQL is a panel
of the Grafana that `qone-infra` already runs (`observability/prometheus.yml`).

## qone-api-gateway (NGINX)

| Signal | Metric | Type | Labels | PromQL |
|---|---|---|---|---|
| Latency | `gateway_request_duration_seconds` | histogram | `route`, `method` | `histogram_quantile(0.95, sum by (le, route) (rate(gateway_request_duration_seconds_bucket{route="/api/v1/sagas"}[5m])))` |
| Traffic | `gateway_requests_total` | counter | `route`, `method`, `status_class` | `sum by (route) (rate(gateway_requests_total[5m]))` |
| Errors | `gateway_requests_total` | counter | `status_class="5xx"` | `sum(rate(gateway_requests_total{route="/api/v1/sagas",status_class="5xx"}[5m])) / sum(rate(gateway_requests_total{route="/api/v1/sagas"}[5m]))` |
| Saturation | `gateway_rate_limited_total` | counter | `route` | `sum(rate(gateway_rate_limited_total[5m]))` (requests rejected by the 20 r/s limit) |

## qone-workflow (the saga)

| Signal | Metric | Type | Labels | PromQL |
|---|---|---|---|---|
| Latency | `workflow_saga_duration_seconds` | histogram | `saga`, `outcome` | `histogram_quantile(0.95, sum by (le) (rate(workflow_saga_duration_seconds_bucket{saga="enroll-student"}[5m])))` |
| Traffic | `workflow_saga_requests_total` | counter | `saga`, `outcome` | `sum(rate(workflow_saga_requests_total{saga="enroll-student"}[5m]))` |
| Errors | `workflow_saga_requests_total` | counter | `outcome="error"` | `sum(rate(workflow_saga_requests_total{outcome="error"}[5m])) / sum(rate(workflow_saga_requests_total[5m]))` |
| Saturation | `workflow_sagas_in_flight` | gauge | `saga` | `max(workflow_sagas_in_flight{saga="enroll-student"})` (open sagas in Redis) |

`outcome` is `completed`, `compensated` (a business gate said no: not an error) or `error` (a step
failed or timed out). Only `error` burns the availability budget.

## qone-billing-api, qone-enrollment-api, qone-catalog-api (the participants)

| Signal | Metric | Type | Labels | PromQL |
|---|---|---|---|---|
| Latency | `http_server_request_duration_seconds` | histogram | `service`, `route`, `method` | `histogram_quantile(0.95, sum by (le, service) (rate(http_server_request_duration_seconds_bucket{route=~"/api/v1/billing/students/.+/invoices/current\|/api/v1/enrollment/eligibility-checks\|/api/v1/catalog/sections/.+/reservations"}[5m])))` |
| Traffic | `http_server_requests_total` | counter | `service`, `route`, `status_class` | `sum by (service) (rate(http_server_requests_total[5m]))` |
| Errors | `http_server_requests_total` | counter | `status_class="5xx"` | `sum by (service) (rate(http_server_requests_total{status_class="5xx"}[5m]))` |
| Saturation | `db_pool_connections_in_use` | gauge | `service` | `max by (service) (db_pool_connections_in_use / db_pool_connections_max)` |
| Domain | `catalog_seat_reservations_total` | counter | `result` (`reserved`, `no_seats`, `released`, `committed`) | `sum by (result) (rate(catalog_seat_reservations_total[15m]))` |

## qone-worker and RabbitMQ (the async hop)

| Signal | Metric | Type | Labels | PromQL |
|---|---|---|---|---|
| Latency | `worker_outbox_relay_lag_seconds` | histogram | `source` (billing, catalog, enrollment, advisor) | `histogram_quantile(0.95, sum by (le, source) (rate(worker_outbox_relay_lag_seconds_bucket[5m])))` |
| Traffic | `worker_events_published_total` | counter | `source`, `event_type` | `sum by (event_type) (rate(worker_events_published_total[5m]))` |
| Errors | `worker_publish_failures_total` | counter | `source` | `sum(rate(worker_publish_failures_total[5m]))` |
| Saturation | `worker_outbox_pending` | gauge | `source` | `max by (source) (worker_outbox_pending)` (rows not yet relayed) |

## Cardinality

| Label | Values | Estimate |
|---|---|---|
| `saga` | `enroll-student` | 1 |
| `outcome` | completed, compensated, error | 3 |
| `route` | the templated route of the contract (`/api/v1/catalog/sections/{id}/reservations`), never the raw URL | about 50 operations of `07-api` |
| `method`, `status_class` | 5 methods, 5 classes | 25 |
| `service` | the 5 APIs plus workflow | 6 |
| `source`, `event_type` | 4 outboxes; `SeatReserved`, `SeatCommitted`, `SeatReleased`, `EnrollmentConfirmed`, `TuitionPaid`, `InvoiceIssued`... | 4 x about 10 |

Forbidden labels: `student_id`, `section_id`, `saga_id`, `reservation_id`, the raw URL and the e-mail.
They are unbounded (thousands of students, every saga is new). They go to the logs of CP2, where one
`trace_id` finds them; a metric keeps only the route template and the outcome.

## Latency buckets

`workflow_saga_duration_seconds` uses `0.1, 0.25, 0.5, 1, 2, 3, 5, 10` seconds. In the enrollment page
the student presses "Enroll in group N" and waits looking at "Enrolling...": under 1 s feels instant,
3 s is the timeout of each participant call, and 10 s is when the portal stops waiting. The buckets are
dense below 1 s, where the five calls of a healthy saga land (about 0.2 s on the local platform), and
have edges at 3 s and 10 s so the SLO of CP6 can count "slower than the timeout" directly.
