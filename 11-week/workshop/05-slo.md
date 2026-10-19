# CP6 - SLIs, SLOs and error budget

Journey of CP1: a student enrolls in a section through the `enroll-student` saga
(`POST /api/v1/sagas/enroll-student` on `qone-workflow`, then `qone-billing-api`, `qone-enrollment-api`,
`qone-catalog-api`, and the events relayed by `qone-worker` to RabbitMQ). Metrics are the ones of CP4.

## Three SLOs

| # | SLO | SLI (good / valid) | Target | Window |
|---|---|---|---|---|
| 1 | Availability of the saga | sagas that end `completed` or `compensated` / all sagas | 99.5 % | 30 days |
| 2 | Latency of the saga | sagas that reach their final state in 3 s or less / all sagas | 99 % | 30 days |
| 3 | Freshness of the enrollment events | events relayed to `qampus.events` within 60 s of the outbox write / all events relayed | 99 % | 30 days |

A `compensated` saga is a good event: a gate said no (`SCHEDULE_CONFLICT`, `NO_SEATS`, `TUITION_UNPAID`,
`PREREQ_MISSING`, `DUPLICATE`) and the student got a clear answer with nothing half-done. Only `error`
(a step failed, timed out or a compensation failed) burns the availability budget.

The third SLO matters because the advisor and the enrollment pages read projections: if
`EnrollmentConfirmed` or `SeatCommitted` arrive late, the advisor proposes a section the student already
has, or shows seats that are gone.

### PromQL

SLO 1, availability:

```promql
sum(rate(workflow_saga_requests_total{saga="enroll-student", outcome=~"completed|compensated"}[30d]))
/
sum(rate(workflow_saga_requests_total{saga="enroll-student"}[30d]))
```

SLO 2, latency (3 s is a bucket edge of `workflow_saga_duration_seconds`, chosen in CP4 for this):

```promql
sum(rate(workflow_saga_duration_seconds_bucket{saga="enroll-student", le="3.0"}[30d]))
/
sum(rate(workflow_saga_duration_seconds_count{saga="enroll-student"}[30d]))
```

SLO 3, freshness (`worker_outbox_relay_lag_seconds` needs a bucket at 60 s):

```promql
sum(rate(worker_outbox_relay_lag_seconds_bucket{source=~"catalog|enrollment", le="60"}[30d]))
/
sum(rate(worker_outbox_relay_lag_seconds_count{source=~"catalog|enrollment"}[30d]))
```

## Traffic and budget

Estimate for one term of the program that Qampus serves today (Ingenieria de Software, the 14 subjects
and 11 sections of the seed, scaled to a real program):

- About 600 active students, each enrolling about 5 sections; with rejected attempts (a full group, a
  schedule conflict) a student starts about 8 sagas: **about 4,800 sagas per term**.
- Almost all of them happen in the enrollment window of two weeks, so the 30-day window of the SLO sees
  practically the whole term: **4,800 sagas in 30 days**, with a peak of about 1,000 on the first day.
- Each completed saga writes 3 events (`SeatReserved`, `EnrollmentConfirmed`, `SeatCommitted`); with
  about 3,000 completed sagas: **about 9,000 events in 30 days**.

| SLO | Budget (100 % - target) | In requests (30 days) | In minutes of full outage (30 days = 43,200 min) |
|---|---|---|---|
| 1 Availability 99.5 % | 0.5 % | 0.5 % of 4,800 = **24 failed sagas** | 0.5 % of 43,200 = **216 min** |
| 2 Latency 99 % | 1 % | 1 % of 4,800 = **48 sagas over 3 s** | 1 % of 43,200 = **432 min** |
| 3 Freshness 99 % | 1 % | 1 % of 9,000 = **90 late events** | **432 min** |

The minutes assume traffic spread evenly. Ours is not: most of the 1,000 sagas of the first day arrive
in the first two or three hours after the window opens, so one hour of outage then fails about 400
requests, which is 16 times the availability budget. In Qampus the budget in requests is the number to
watch, not the minutes.

## Error budget policy (team Quorum One)

| Budget consumed | What we do |
|---|---|
| 50 % | Warning in the team channel. Every new change to `qone-workflow`, `qone-catalog-api` or `qone-enrollment-api` needs an extra review and a green run of the acceptance battery on `qa` before it is promoted. |
| 75 % | Freeze of features on the saga path during the enrollment window: only fixes and observability work reach `qa`. The next sprint starts with the top cause found in the logs by `trace_id`. |
| 100 % | Stop shipping to `main` on the saga path until the SLI is back above target for 7 days. Write a postmortem (like CP9) and add its action items to the next sprint before any new story. |
