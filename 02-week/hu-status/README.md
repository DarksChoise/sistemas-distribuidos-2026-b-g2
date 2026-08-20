<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       02-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 02

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Juan Diego Andrade Cardozo
- GITHUB_USER: DarksChoise
- TEAM: Quorum One
- SPRINT_GOAL: Compare the distributed architecture styles and prepare the architectural decision for the product (bounded contexts and ADR), while finishing the local development environment.
<!-- CONFIG-END -->

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| n/a | No user stories assigned yet - product backlog still not defined | todo | n/a |

## 2. My individual contribution
- Attended both in-class sessions: Session 1 (distributed architectures - client-server, P2P, SOA, microservices) and Session 2 (planning - choosing your architecture, bounded contexts and the ADR).
- Studied the Session 1 material: architecture as boundaries plus communication, when each style fits, splitting microservices by business capability, and the coupling/scaling/failure trade-offs of each style.
- Studied the Session 2 material: mapping the domain into bounded contexts, choosing an architecture through an explicit decision path instead of by fashion, recording it as an Architecture Decision Record, and turning that decision into the sprint backlog.
- Continued the environment setup: verified the local toolchain against the course standards and kept the fork synchronised with the upstream class repository.

## 3. Blockers and risks
- Still working as an individual team, which limits how much product scope can be committed per sprint.
- The team product repository has not been created yet, so the architecture decision cannot be recorded as an ADR inside the product yet.
- Without a defined backlog there is still no user story to branch from, which delays the start of the per-environment Git workflow.

## 4. Plan for next week
- Apply DDD and hexagonal architecture to the product domain: entities, value objects, aggregates and domain events.
- Create the product repository and commit the first ADR with the chosen architecture and its decision path.
- Write the first user stories with testable acceptance criteria and open the corresponding `hu-xxx-dev` branch.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [ ] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...)
- [ ] Testable acceptance criteria
- [ ] Tests added/updated (unit / integration)
- [ ] DDD / hexagonal boundaries respected (domain has no I/O)
- [x] No secrets; config via environment variables

Unchecked items are not applicable this week: no user stories were assigned and no product code was written yet.

## 6. Evidence links
- Fork: https://github.com/DarksChoise/sistemas-distribuidos-2026-b-g2
- Profile repo with CONFIG block: https://github.com/DarksChoise/DarksChoise
- Session 1 material: https://code-corhuila.github.io/ova-web/2026-B/distribuidos/02-week/01-session/
- Session 2 material: https://code-corhuila.github.io/ova-web/2026-B/distribuidos/02-week/02-session/
