# CP7 - Burn-rate alert policy

The rules are in [06-alerts.yml](06-alerts.yml), checked with the `promtool` of the Prometheus that
`qone-infra` runs (`docker exec qone-prometheus promtool check rules 06-alerts.yml`: `SUCCESS: 7 rules found`).
They protect SLO 1 of [05-slo.md](05-slo.md):
99.5 % of `enroll-student` sagas end `completed` or `compensated` over 30 days, budget 0.5 % =
**24 failed sagas** in a term of about 4,800 sagas.

## How much budget each alert means before it fires

Burn rate = error ratio / 0.005. A burn rate of 1 spends exactly the whole budget in 30 days.

| Alert | Condition | Error ratio | Budget spent when it fires | In Qampus numbers |
|---|---|---|---|---|
| `EnrollStudentSagaFastBurn` (page) | burn 14.4 over 1 h and over 5 min, for 2 min | > 7.2 % | 14.4 x 1 h / 720 h = **2 %** of the 30-day budget | at the first-day peak (about 400 sagas per hour) 7.2 % is about 29 failed sagas in one hour: more than the whole term budget of 24. It fires within 5 to 7 minutes of a real break. |
| `EnrollStudentSagaSlowBurn` (ticket) | burn 6 over 6 h and over 30 min, for 15 min | > 3 % | 6 x 6 h / 720 h = **5 %** of the 30-day budget | outside the peak, with about 30 sagas per hour, 3 % over 6 h is about 5 failed sagas: a participant that fails now and then (a slow `qone-billing-api`, a flaky connection pool). |

Two choices that come from our traffic:

- **Minimum traffic on the fast alert** (`qampus:saga_requests:increase1h > 20`). Outside the enrollment
  window Qampus has a handful of sagas per hour; one failure out of three would be a 33 % error ratio
  and would page someone at night for a single student. Below 20 sagas per hour the slow alert covers it.
- **Severity follows the window.** The fast alert is `page` because during the enrollment window an hour
  is enough to burn the whole term budget. The slow alert is `ticket`: it is read the next working morning.

## Cause-based alerts we will NOT create

| Alert | Why not |
|---|---|
| CPU of the `qone-workflow` container above 80 % | The saga mostly waits on HTTP calls and Redis; high CPU does not mean students are failing, and students can be failing (a participant timing out) with idle CPU. The burn-rate alert already sees the symptom that matters. |
| Length of a RabbitMQ queue on `qampus.events` above a fixed number | A queue grows normally right after the enrollment window opens and drains in seconds. The user-facing effect, events arriving late to the projections, is SLO 3 (freshness); if we need an alert there, it will be a burn-rate alert on that SLO, not on the queue length. |
