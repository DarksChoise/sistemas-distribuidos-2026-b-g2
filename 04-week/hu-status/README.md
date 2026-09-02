<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       04-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 04

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Juan Diego Andrade Cardozo
- GITHUB_USER: DarksChoise
- TEAM: Quorum One
- SPRINT_GOAL: Pivot the product to Qampus (academic planning and enrollment), rewrite the SDD documentation for the new domain, and build the walking skeleton of the MVP 1 monolith.
<!-- CONFIG-END -->

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| HU-PLT-001 | Docker Compose walking skeleton | doing | Local spike this week; landed as https://github.com/code-corhuila/quorum-one/pull/2 |
| HU-AUT-001 | Authentication with JWT and roles | doing | Local spike this week; landed as https://github.com/code-corhuila/quorum-one/pull/3 |
| HU-CAT-001..003 | Curriculum catalog, sections and seats | doing | Local spike this week; landed as https://github.com/code-corhuila/quorum-one/pull/4 |
| HU-ENR-001..003 | Enrollment gates and degree progress | doing | Local spike this week; landed as https://github.com/code-corhuila/quorum-one/pull/6 |

## 2. My individual contribution
- Attended both in-class sessions: Session 1 (building a service - structure, layers and the walking skeleton) and Session 2 (planning the MVP 1 sprint - contract-first, estimation, scope).
- Pivoted the product: the team's system is now **Qampus** - academic planning and enrollment (curriculum/pensum, sections with real seat capacity, schedule-conflict validation, tuition) with an **AI agent** that advises students and enrolls subjects on their behalf under explicit confirmation.
- Rewrote the full SDD documentation for the new domain in `qone-docs` (context, domain map with 4 bounded contexts, entities with invariants, 15-event catalog, product vision, 18 user stories, NFRs) - commit `9f2a7cf`.
- Decided and recorded the MVP 1 architecture following the course decision path: **modular monolith with explicit extraction triggers** (later formalized as ADR-0002) - real boundaries exist, but no independent scaling/deploy need yet.
- Built the local development spike of the monolith following the walking-skeleton session: hexagonal-modular FastAPI app (domain rules without I/O, commands/queries, routers per bounded context), React frontend and nginx gateway.

## 3. Blockers and risks
- One-person team versus a full-product sprint: mitigated by the monolith decision and a strict MoSCoW cut line (professor/export features live in Cut 2).
- Docker Desktop could not start on the development machine (virtualization/WSL missing) - resolved by installing the Windows Subsystem for Linux component and rebooting.
- The pivot invalidated the previously presented weekly material; documentation was rewritten the same week to keep the SDD source of truth consistent.

## 4. Plan for next week
- Ship MVP 1: land the spike as per-HU branches and Pull Requests into the team repository, promote develop -> qa -> main and tag v1.0.0.
- Add tests over the documented invariants and a CI pipeline (lint + tests + frontend build) gating every PR.
- Submit the release evidence in Moodle (c1-release) and complete the Cut 1 activities.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [ ] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...)
- [x] Testable acceptance criteria
- [ ] Tests added/updated (unit / integration)
- [x] DDD / hexagonal boundaries respected (domain has no I/O)
- [x] No secrets; config via environment variables

Notes: this week's code lived as a local spike (branches/PRs and the test suite landed at the start of week 5 - see the next report). Acceptance criteria are written in Given/When/Then in `qone-docs/04-requirements/user-stories.md`, each traced to documented invariants.

## 6. Evidence links
- Docs pivot to Qampus: https://github.com/code-corhuila/qone-docs/commit/9f2a7cf
- User stories with testable AC: https://github.com/code-corhuila/qone-docs/blob/main/04-requirements/user-stories.md
- Session 1 material: https://code-corhuila.github.io/ova-web/2026-B/distribuidos/04-week/01-session/
- Session 2 material: https://code-corhuila.github.io/ova-web/2026-B/distribuidos/04-week/02-session/
