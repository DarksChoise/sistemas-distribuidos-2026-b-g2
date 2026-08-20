<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       01-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 01

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Juan Diego Andrade Cardozo
- GITHUB_USER: DarksChoise
- TEAM: Quorum One
- SPRINT_GOAL: Set up the working environment and build the conceptual baseline of the course (distributed system models, logical time, consistency trade-offs and the professional engineering standards the product must follow).
<!-- CONFIG-END -->

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| n/a | No user stories assigned yet - product backlog not opened in Week 01 | todo | n/a |

## 2. My individual contribution
- Attended both in-class sessions: Session 1 (distributed systems - models, time, consistency and trade-offs) and Session 2 (professional engineering foundations for distributed systems).
- Studied the Session 1 material: fallacies of distributed computing, system and failure models, logical clocks and causality, the consistency spectrum (CAP/PACELC), replication, partitioning and quorums, consensus, and communication/delivery semantics.
- Studied the Session 2 material: strategic and tactical DDD, hexagonal architecture (ports and adapters), SOLID and Clean Code, resilience patterns (Circuit Breaker, Saga, Outbox, CQRS), testing strategy, and ways of working (Scrum, Git flow, ADRs).
- Environment setup: forked the class repository, cloned it locally, configured Git and the local toolchain, and verified the `NN-week/hu-status/` structure used by the automated grader.
- Created and verified the profile repository `DarksChoise/DarksChoise` with the required CONFIG block (FULL_NAME + GITHUB_USER) so that the weekly deliverable can be attributed.

## 3. Blockers and risks
- Working as an individual team, so there is no peer to split the product workload with; the release scope must stay small enough to be delivered solo.
- No team product repository exists yet, so no code could be produced this week.
- The product backlog has not been defined, so no user story could be started.

## 4. Plan for next week
- Study the distributed architecture styles and choose one for the product with an explicit decision path.
- Map the problem domain into bounded contexts and draft the first ADR.
- Define the initial product backlog and write the first user stories so that Week 03 can start producing code.

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
- Session 1 material: https://code-corhuila.github.io/ova-web/2026-B/distribuidos/01-week/01-session/
- Session 2 material: https://code-corhuila.github.io/ova-web/2026-B/distribuidos/01-week/02-session/
