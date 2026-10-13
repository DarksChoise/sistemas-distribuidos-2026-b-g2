<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       08-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 08

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Juan Diego Andrade Cardozo
- GITHUB_USER: DarksChoise
- TEAM: Quorum One
- SPRINT_GOAL: Close the review of the documentation pull request and document the shipped system: diagrams and the real API contracts.
<!-- CONFIG-END -->

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| HU-WEB-001/002 | UX-UI evidence of the shipped v1.0.0 portal | done | https://github.com/code-corhuila/qone-docs/pull/4 |
| HU-PLT-002 | Governance and architecture documents aligned with the branching policy | done | https://github.com/code-corhuila/qone-docs/pull/4 |
| HU-PLT-002 | Diagrams of v1.0.0 and the real API contracts in qone-docs | doing | https://github.com/code-corhuila/qone-docs/pull/7 |

## 2. My individual contribution
- Answered the review of qone-docs #4 (Sep 21): a compatibility table between the course policy and our conventions, one ADR registry with aligned identifiers, and the shared-database exception of Cut 1 recorded. #4 merged on Sep 21; the two follow-up pull requests (#5, #6) were closed because their content went into #4.
- Opened qone-docs #7 on Sep 24: renamed `08-uml` to `08-diagrams`, added the v1.0.0 diagrams and the API contracts as the system really answers.
- Pushed the class material of week 08, session 2 to my fork (Sep 23): SDD specification, ADR and diagrams of the `simple-stock-flow` example.

## 3. Blockers and risks
- The documented API contracts must match what v1.0.0 actually answers; a mismatch would make the contract-first work of Cut 2 start from wrong assumptions. To be verified against the running system before merging #7.

## 4. Plan for next week
- Apply the review of #7 and check every documented operation against the running v1.0.0.
- Adopt the course repository norm for Cut 2 (repository topology, stack per piece, saga style) as ADRs.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [x] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...)
- [ ] Testable acceptance criteria
- [ ] Tests added/updated (unit / integration)
- [ ] DDD / hexagonal boundaries respected (domain has no I/O)
- [x] No secrets; config via environment variables

## 6. Evidence links
- qone-docs PR #4 (merged): https://github.com/code-corhuila/qone-docs/pull/4
- qone-docs PR #7: https://github.com/code-corhuila/qone-docs/pull/7
- Class material in my fork: https://github.com/DarksChoise/sistemas-distribuidos-2026-b-g2/commit/171d077
- Session material: https://code-corhuila.github.io/ova-web/2026-B/distribuidos/08-week/01-session/ and /02-session/
