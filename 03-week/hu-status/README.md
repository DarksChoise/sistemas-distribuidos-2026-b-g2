<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       03-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 03

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Juan Diego Andrade Cardozo
- GITHUB_USER: DarksChoise
- TEAM: Quorum One
- SPRINT_GOAL: Define the product (domain and stack) and apply DDD to it: bounded contexts, entities, invariants and domain events documented in the team documentation repository.
<!-- CONFIG-END -->

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| n/a | No formal user stories yet - the backlog is written from the domain model completed this week (user stories are next week's first deliverable) | todo | n/a |

## 2. My individual contribution
- Attended both in-class sessions: Session 1 (Domain-Driven Design & hexagonal architecture) and Session 2 (planning - service design, data ownership and contracts).
- Defined the product: **Qommerce**, a reduced e-commerce platform (Orders / Payments / Inventory) plus an AI assistant with read-only access to the system's data. Stack decided within the professor's authorized options: Python + FastAPI (backend), React (frontend), PostgreSQL per service, RabbitMQ as message broker.
- Completed the Discovery phase of the SDD documentation in the team docs repository (`qone-docs`), following the week-1 fill order of the SDD guide:
  - `01-context/`: system overview, MVP scope (in/out, assumptions, constraints) and an 18-term glossary.
  - `02-domain/`: domain map with 4 bounded contexts (Order Management as core, Inventory, Payments, AI Assistant), entities with explicit invariants (`Order`, `Product`, `Payment`, `Conversation`), value objects (`Money`, `SKU`), and a 12-event catalog with the order-confirmation saga (choreography with compensation: stock is reserved before payment; a rejected payment releases the reservation).
- Applied the DDD concepts from Session 1 directly: aggregate boundaries define where transactions end and where the saga begins; the AI assistant context is designed as a CQRS read side (projections built from domain events, read-only tools for the LLM, never a saga participant).
- Rebuilt the full development environment on a new Windows machine: Git identity and credential helper, GitHub CLI authenticated, the three course repositories cloned and the fork's upstream remote configured.

## 3. Blockers and risks
- One-person team: the weekly documentation cadence of the SDD guide plus implementation of three services and a frontend is the main capacity risk for Cut 1.
- The fork has diverged from upstream (the professor added the governance reference material); syncing requires a merge commit, pending to keep week folders up to date.
- The LLM provider for the AI assistant is not decided yet (needs its own ADR in `05-architecture/decisions/`); the assistant is scheduled for Cut 2 so it does not block MVP 1.

## 4. Plan for next week
- Write the first 10-15 user stories of the MVP with testable acceptance criteria in `04-requirements/user-stories.md`, derived from the domain events documented this week, plus measurable NFRs.
- Complete `03-product/` (problem framing and vision) and `05-architecture/overview.md` (C4), and record the first own ADRs (stack, message broker, saga style, read-only AI assistant).
- Scaffold the three services in the product repository following the hexagonal template of `_stacks/python-fastapi.md`, opening the first `hu-xxx-dev` branches with their PRs to `develop`.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [ ] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...)
- [ ] Testable acceptance criteria
- [ ] Tests added/updated (unit / integration)
- [x] DDD / hexagonal boundaries respected (domain has no I/O)
- [x] No secrets; config via environment variables

Notes: the documentation repository intentionally has no branches/PRs (professor's instruction: docs go straight to `main`), and no HU branches exist yet because the backlog starts next week. Testable acceptance criteria and tests apply from the first user stories onward. DDD boundaries are checked at the design level: every aggregate documents its invariants and the domain model has no I/O concerns.

## 6. Evidence links
- Docs commit (context): https://github.com/code-corhuila/qone-docs/commit/1492c20
- Docs commit (domain model): https://github.com/code-corhuila/qone-docs/commit/46f216c
- Documentation repository: https://github.com/code-corhuila/qone-docs
- Product repository (branch model + first ADR): https://github.com/DarksChoise/sd-2026b-quorum-one
- Session 1 material: https://code-corhuila.github.io/ova-web/2026-B/distribuidos/03-week/01-session/
- Session 2 material: https://code-corhuila.github.io/ova-web/2026-B/distribuidos/03-week/02-session/
