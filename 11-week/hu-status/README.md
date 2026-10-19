<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       11-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 11

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Juan Diego Andrade Cardozo
- GITHUB_USER: DarksChoise
- TEAM: Quorum One
- SPRINT_GOAL: Build every Cut 2 service and portal, compose the platform, and release v2.0.0 through develop -> qa -> main (status as of Oct 13).
<!-- CONFIG-END -->

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| HU-PLT-001 | Local environment with Docker Compose | done | https://github.com/code-corhuila/qone-infra/releases/tag/v2.0.0 |
| HU-PLT-002 | CI pipeline per service | done | https://github.com/code-corhuila/qone-infra/pull/9 |
| HU-AUT-001 | Sign in and register | done | https://github.com/code-corhuila/qone-identity-api/releases/tag/v2.0.0 |
| HU-WEB-001 | Student portal | done | https://github.com/code-corhuila/qone-front/releases/tag/v2.0.0 |
| HU-CAT-001 | Manage subjects and the pensum | done | https://github.com/code-corhuila/qone-catalog-api/releases/tag/v2.0.0 |
| HU-CAT-002 | Open sections with schedule and capacity | done | https://github.com/code-corhuila/qone-catalog-api/releases/tag/v2.0.0 |
| HU-CAT-003 | Browse catalog, pensum and seat availability | done | https://github.com/code-corhuila/qone-catalog-portal/releases/tag/v2.0.0 |
| HU-ENR-001 | Academic record and degree progress | done | https://github.com/code-corhuila/qone-enrollment-api/releases/tag/v2.0.0 |
| HU-BIL-001 | Semester invoice and simulated payment | done | https://github.com/code-corhuila/qone-billing-api/releases/tag/v2.0.0 |
| HU-ENR-002 | Request enrollment (saga start, fail-fast gates) | done | https://github.com/code-corhuila/qone-workflow/releases/tag/v2.0.0 |
| HU-CER-001 | Verifiable certificates | done | https://github.com/code-corhuila/qone-enrollment-portal/releases/tag/v2.0.0 |
| HU-ADV-002 | Ask the agent: degree audit and planning | done | https://github.com/code-corhuila/qone-advisor-api/releases/tag/v2.0.0 |
| HU-ADV-003 | Enroll by chat, with explicit confirmation | done | https://github.com/code-corhuila/qone-advisor-portal/releases/tag/v2.0.0 |
| HU-WEB-002 | Professor view | done | https://github.com/code-corhuila/qone-enrollment-portal/pull/14 |
| HU-PLT-002 | Observability workshop, delivery 1: journey and trace map, log contract, instrumentation with test, metric catalog | done | https://github.com/DarksChoise/sistemas-distribuidos-2026-b-g2/tree/main/11-week/workshop |

## 2. My individual contribution
- Built the backend of Cut 2 test-first and hexagonal (Python 3.12, FastAPI, PostgreSQL with Flyway): `qone-identity-db/api` (RS256 tokens), `qone-billing-db/api`, `qone-catalog-db/api` (seat reservations under a row lock), `qone-enrollment-db/api` (record, pensum, certificates with PDF, projections), `qone-workflow` (the orchestrated `enroll-student` saga with compensation, state in Redis), `qone-worker` (outbox relay to RabbitMQ, plan expiry, LLM cache prune), `qone-advisor-db/api` (LangChain agent with tools closed over the caller, circuit breaker, plans confirmed into the saga with the advisor's token) and `qone-api-gateway` (NGINX).
- Built the remaining portals as Module Federation remotes: identity (sign in and registration), billing, enrollment (with the certificate PDF download through the shell's client) and advisor (chat and plan card).
- Composed the whole platform in `qone-infra` and verified it end to end: rebuilt from zero (five schemas migrated and seeded), smoke checks green, and an acceptance battery through the gateway of **64 of 64** checks on `develop` and again on `qa`.
- Every feature change entered `develop` through a pull request with green CI that references its story issue, split to stay under 400 changed lines (tests and generated files excluded). Promotion to `qa` was by re-application (`cherry-pick -x`, 20 pull requests with the story of every commit), and `release/2.0.0` was cut from `main` with one commit per validated story; the 20 release pull requests were approved and merged, and every repository carries tag `v2.0.0` with a GitHub Release.
- Recorded the findings of the automated course review on the 20 release pull requests, checked each one, and kept the answers for the checkpoint defence.

- Week 11 workshop, delivery 1 (Oct 19, in class), applied to the `enroll-student` saga of Qampus, one push per checkpoint:
  CP0 setup [147f1fa](https://github.com/DarksChoise/sistemas-distribuidos-2026-b-g2/commit/147f1fa) and reflection link [b5e91a3](https://github.com/DarksChoise/sistemas-distribuidos-2026-b-g2/commit/b5e91a3); CP1 journey and trace map [1b7dc6d](https://github.com/DarksChoise/sistemas-distribuidos-2026-b-g2/commit/1b7dc6d);
  CP2 structured log contract [73f80b7](https://github.com/DarksChoise/sistemas-distribuidos-2026-b-g2/commit/73f80b7); CP3 `qone_workflow_obs` (traceparent middleware, JSON logger, context sent to
  `qone-billing-api`, two Prometheus metrics, a passing test) [3295c94](https://github.com/DarksChoise/sistemas-distribuidos-2026-b-g2/commit/3295c94), [5efe0b7](https://github.com/DarksChoise/sistemas-distribuidos-2026-b-g2/commit/5efe0b7), [cc5f3fe](https://github.com/DarksChoise/sistemas-distribuidos-2026-b-g2/commit/cc5f3fe);
  CP4 golden signals and metric catalog [f523b4d](https://github.com/DarksChoise/sistemas-distribuidos-2026-b-g2/commit/f523b4d).

## 3. Blockers and risks
- The v2 documentation stack (qone-docs #49) needs the teacher's approval again: the earlier approval was dismissed by a later push. Until it merges, the code repositories cite their contracts from a `docs/` branch.
- The automated review cites a newer version of the course norm (Annex J: one shared PostgreSQL instance per engine in a `<abbr>-infra-postgres` repository, one application user per domain, MongoDB, a backend in at least two languages). Our topology follows the earlier version (one instance per domain); adopting it is a structural change to assess.
- Known gaps from the review: seat reservations have no expiry job if a saga stops halfway; services connect to their schema with the owner user.
- The `qa/` branch prefix of the policy cannot coexist with the `qa` branch in git; the promotion branches were named `promote-qa/` and the conventions document must be updated.

## 4. Plan for next week
- Request the teacher's review of qone-docs #49 again and, once merged, sync every contract copy to `main`.
- Assess Annex J and the other new rules of the norm and plan the changes for Cut 3.
- Close the real gaps raised by the review: reservation expiry, one database user per domain, per-domain rate-limit zones in the gateway.

- Workshop delivery 2 (until Oct 20): SLOs and error budget, burn-rate alerts, runbook, incident drill with postmortem.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [x] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...)
- [x] Testable acceptance criteria
- [x] Tests added/updated (unit / integration)
- [x] DDD / hexagonal boundaries respected (domain has no I/O)
- [x] No secrets; config via environment variables

## 6. Evidence links
- MVP 2 evidence (15 screenshots, acceptance battery 64/64 and its log): https://github.com/DarksChoise/sistemas-distribuidos-2026-b-g2/tree/main/11-week/02-session/mvp2-evidence
- Releases v2.0.0 (one per repository), e.g. https://github.com/code-corhuila/qone-infra/releases/tag/v2.0.0
- Week 11 workshop: https://github.com/DarksChoise/sistemas-distribuidos-2026-b-g2/tree/main/11-week/workshop
- Promotion to qa (one pull request per repository), e.g. https://github.com/code-corhuila/qone-catalog-api/pull/11
- Release pull requests to main, e.g. https://github.com/code-corhuila/qone-catalog-api/pull/12
- Cut 2 user-story issues: https://github.com/code-corhuila/qone-docs/issues?q=is%3Aissue+created%3A2026-10-07
- Project board: https://github.com/orgs/code-corhuila/projects/26
- Session material: https://code-corhuila.github.io/ova-web/2026-B/distribuidos/11-week/01-session/ and /02-session/
