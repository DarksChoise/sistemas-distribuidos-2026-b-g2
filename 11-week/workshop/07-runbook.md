# CP8 - Runbook: EnrollStudentSagaFastBurn

**Alert:** `EnrollStudentSagaFastBurn` ([06-alerts.yml](06-alerts.yml)), severity `page`, team `quorum-one`.
**Meaning:** more than 7.2 % of `POST /api/v1/sagas/enroll-student` end in `outcome="error"` over the last
hour and the last 5 minutes. At this rate the 30-day budget of SLO 1 (24 failed sagas) is gone in about
2 days; during the first day of enrollment, in about one hour.

## 1. Symptoms

- Students press "Enroll in group N" in the enrollment portal and get "The enrollment could not be
  completed" with a saga id, instead of "Enrollment confirmed" or a clear rejection reason.
- `GET /api/v1/sagas/{id}` answers `status: COMPENSATED` with `failedStep` set but no business `reason`,
  or the saga stays in a step for more than 30 s.
- In `qone-workflow` logs: `saga.step.timeout` and `saga.compensated` lines without a `rejection_reason`.

## 2. Confirm (5 minutes)

Is it real, and which participant? The error ratio, then the step that fails:

```promql
qampus:saga_error_ratio:rate5m
```

```promql
sum by (service) (rate(http_server_requests_total{service=~"qone-billing-api|qone-enrollment-api|qone-catalog-api", status_class="5xx"}[5m]))
```

```promql
histogram_quantile(0.95, sum by (le, service) (rate(http_server_request_duration_seconds_bucket[5m])))
```

Take one failed saga id from a student report or from the logs and follow its trace (CP2 contract). Until
the logs are centralized this is done on the host, from `qampus\qone-infra`, in PowerShell:

```powershell
docker compose --env-file .env logs --since 30m qone-workflow | Select-String '"event": "saga.compensated"' | Select-Object -Last 5
docker compose --env-file .env logs --since 30m qone-workflow qone-billing-api qone-enrollment-api qone-catalog-api | Select-String "7a3f9c1e5b2d4f60a1c8e9b0d2f4a6c8"
& "C:\Program Files\Git\bin\sh.exe" scripts/smoke.sh
```

The participant whose lines show `saga.step.timeout` or a 5xx for that `trace_id` is the cause. Each call
from the saga is tried 3 times with a 10 s timeout (connect 3 s) before the step is `Unavailable`.

## 3. Mitigate, ordered by risk (lowest first)

| # | Action | When | How | Risk |
|---|---|---|---|---|
| 1 | Restart the failing participant | one container is unhealthy, out of DB connections or stuck | `docker compose --env-file .env restart qone-billing-api` (or the service found in step 2), then `docker compose ps` until it is `healthy` | low: in-flight sagas get `Unavailable` and compensate; Redis keeps the saga state, so nothing is half-done |
| 2 | Roll back the service that changed last | the burn started right after a promotion to `main` | check out the previous tag (`git -C ..\qone-catalog-api checkout v2.0.0`), `docker compose --env-file .env up -d --build qone-catalog-api` | medium: the fix of the new version is lost until a hotfix; migrations of `-db` repositories are not rolled back by this step |
| 3 | Pause new enrollments at the gateway | the cause is unknown and failures keep burning the budget | in `qone-api-gateway/nginx/routes/workflow.conf` answer `POST /api/v1/sagas/enroll-student` with 503 and the common error envelope ("enrollment is paused, try again in a few minutes"), reload NGINX | high: no student can enroll, but nobody gets a half-done saga and the budget stops burning |

Not available in Qampus today: **scale out** (every service has a fixed `container_name` in its compose
file, so there is one replica) and a **circuit breaker in `qone-workflow`** (only `qone-advisor-api` has
one, for the LLM). Both are action items of the postmortem in CP9.

## 4. Escalation

| Role | Who | When |
|---|---|---|
| On-call developer | Juan Diego Andrade Cardozo (Quorum One, owner of the 20 `qone-*` repositories) | at the page |
| Data owner of the failing domain | same person today; in a larger team, the owner of `qone-billing-api`, `qone-enrollment-api` or `qone-catalog-api` | if mitigation 1 does not stop the burn in 15 minutes |
| Academic office (product owner of Qampus) | the person who opens the enrollment window | if step 3 is used or the outage passes 30 minutes: they decide whether to extend the window and tell the students |

## 5. Verify recovery

1. `qampus:saga_error_ratio:rate5m` below 0.005 (the SLO) for 15 minutes, and the alert resolved.
2. `scripts/smoke.sh` prints `OK: the platform answers through the gateway with a token issued by identity`.
3. One real enrollment through the portal ends `COMPLETED`; its `trace_id` shows the five steps
   (`check-tuition` to `commit-seat`) in the logs with no `saga.step.timeout`.
4. No reservation left in `RESERVED` older than 15 minutes in `catalog.seat_reservation` (no seat leaked
   by the failed sagas).
5. Write the incident in the team log and start the postmortem (CP9) if the budget spent passed 25 %.
