<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       05-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 05

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Juan Diego Andrade Cardozo
- GITHUB_USER: DarksChoise
- TEAM: Quorum One
- SPRINT_GOAL: Ship MVP 1 - land every user story as per-HU branches and PRs, promote develop -> qa -> main, tag v1.0.0 and verify the release checklist with evidence.
<!-- CONFIG-END -->

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| HU-PLT-001 | Docker Compose walking skeleton | done | https://github.com/code-corhuila/quorum-one/pull/2 |
| HU-AUT-001 | Authentication with JWT and roles | done | https://github.com/code-corhuila/quorum-one/pull/3 |
| HU-CAT-001..003 | Curriculum catalog, sections and seats | done | https://github.com/code-corhuila/quorum-one/pull/4 |
| HU-BIL-001 | Tuition invoice, exactly-once simulated payment | done | https://github.com/code-corhuila/quorum-one/pull/5 |
| HU-ENR-001..003 | Enrollment gates, atomic seats, degree progress | done | https://github.com/code-corhuila/quorum-one/pull/6 |
| HU-ADV-001..003 | AI advisor with human-in-the-loop enrollment | done | https://github.com/code-corhuila/quorum-one/pull/7 |
| HU-CER-001 | PDF certificates with public verification | done | https://github.com/code-corhuila/quorum-one/pull/8 |
| HU-WEB-001/002 | Web portal and gateway | done | https://github.com/code-corhuila/quorum-one/pull/9 |
| HU-PLT-002 | CI pipeline, ADRs and release docs | done | https://github.com/code-corhuila/quorum-one/pull/10 |

## 2. My individual contribution
- Attended both in-class sessions: Session 1 (containerization with Docker) and Session 2 (release - shipping MVP 1: checklist, demo, retrospective).
- Landed the whole MVP 1 in the team repository `code-corhuila/quorum-one` as 9 feature Pull Requests (#2-#10), one per user story group, each on its `hu-xxx-dev` branch with the story, invariants and verification steps in the PR body.
- Promoted the increment through the environments via PRs (#11 develop -> qa, #12 qa -> main) and tagged **v1.0.0** with a GitHub Release: https://github.com/code-corhuila/quorum-one/releases/tag/v1.0.0
- Wrote **20 unit + integration tests** over the documented invariants (every enrollment gate with seat accounting before/after, exactly-once payment, prerequisite cycles, role boundaries, the agent's guardrails) and a CI pipeline (ruff + pytest + frontend build) gating every PR - green on every environment branch.
- Verified the release checklist end to end: `./up.sh` boots PostgreSQL + backend + gateway; the three saga outcomes are demoable with the seeded accounts (NO_SEATS, SCHEDULE_CONFLICT with the seat restored, CONFIRMED with the seat decremented); the AI advisor answers degree-audit questions grounded in real data and enrolls only after explicit confirmation.
- Recorded the architecture decisions: ADR-0002 (modular monolith first, with extraction triggers per the course decision path) and ADR-0003 (LLM provider), plus an honest README and the v1.0.0 CHANGELOG.
- Closed the Cut 1 board: user-story issues #13-#21 and the professor's HU-03 issue, all linked to their PRs and marked Done (DoD) in the org project.

## 3. Blockers and risks
- The team GitHub project board required an additional token scope (`project`) to automate item management - resolved with `gh auth refresh`.
- The AI advisor depends on an external LLM API: mitigated by design with a circuit breaker and a degraded mode (verified by tests), so the platform never blocks on the provider.
- Remaining documentation debt flagged by the professor's Aug 31 review (governance, data models, UX-UI sections in qone-docs) is scheduled before the cut closes.

## 4. Plan for next week
- Close Cut 1 in Moodle: c1-release evidence package, c1-sprints, retro forum post and the self/peer assessment questionnaires.
- Address the qone-docs review findings: clean the residual template markers in the domain map, write `06-data/models.md` from the real schema, document UX-UI (navigation map from the shipped portal) and adapt the governance section.
- Start Cut 2 planning: extraction triggers (ADR-0002), event-driven saga over a broker, and the advisor's CQRS projections.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [x] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...)
- [x] Testable acceptance criteria
- [x] Tests added/updated (unit / integration)
- [x] DDD / hexagonal boundaries respected (domain has no I/O)
- [x] No secrets; config via environment variables

## 6. Evidence links
- Release v1.0.0: https://github.com/code-corhuila/quorum-one/releases/tag/v1.0.0
- Team repository (develop/qa/main + PRs #2-#12): https://github.com/code-corhuila/quorum-one
- CI runs (green): https://github.com/code-corhuila/quorum-one/actions
- Project board (all Done): https://github.com/orgs/code-corhuila/projects/26
- ADR-0002 (modular monolith + extraction triggers): https://github.com/code-corhuila/quorum-one/blob/main/docs/adr/0002-modular-monolith-first.md
- Session material: https://code-corhuila.github.io/ova-web/2026-B/distribuidos/05-week/01-session/ and /02-session/
