<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       09-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 09

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Juan Diego Andrade Cardozo
- GITHUB_USER: DarksChoise
- TEAM: Quorum One
- SPRINT_GOAL: Adopt the course repository norm for Cut 2 - twenty-repository topology, stack per piece and an orchestrated enrollment saga - and close the v1.0.0 documentation.
<!-- CONFIG-END -->

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| HU-PLT-002 | Diagrams of v1.0.0 and the API contracts, checked against the running system | done | https://github.com/code-corhuila/qone-docs/pull/7 |
| HU-PLT-001 | Repository topology per the course norm (ADR-006) and the repository register | done | https://github.com/code-corhuila/qone-docs/pull/8 |
| HU-ENR-002 | Orchestrated enrollment saga (ADR-008) and the stack per piece (ADR-007) | done | https://github.com/code-corhuila/qone-docs/pull/9 |

## 2. My individual contribution
- Applied the review of qone-docs #7 and corrected the contracts with 79 live probes against the running v1.0.0; #7 merged on Sep 28.
- Wrote ADR-006 (adopt the course repository norm: the twenty `qone-*` repositories, one database per domain, the prototype `quorum-one` frozen) with the repository register, and ADR-007 (stack per piece) and ADR-008 (the enrollment saga orchestrated by `qone-workflow` instead of choreography). PRs #8 and #9 opened Sep 28, merged Oct 1.
- The twenty `qone-*` repositories were created in the organization on Sep 28, ready for Cut 2.

## 3. Blockers and risks
- Cut 2 needs the v1 contracts rewritten to the common contract of the norm (camelCase, error envelope, RS256, pagination, Idempotency-Key) before any service is built; that is a large documentation step with little time to the Oct 11 cut.

## 4. Plan for next week
- Write the v2 documentation contract-first: common contract, the OpenAPI contract of every service, the data model per domain, the service pages and the DevOps guides.
- Create the user-story issues of Cut 2 and start the web layer: the shell and the first portal.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [x] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...)
- [ ] Testable acceptance criteria
- [ ] Tests added/updated (unit / integration)
- [ ] DDD / hexagonal boundaries respected (domain has no I/O)
- [x] No secrets; config via environment variables

## 6. Evidence links
- qone-docs PR #7: https://github.com/code-corhuila/qone-docs/pull/7
- ADR-006 and repository register (PR #8): https://github.com/code-corhuila/qone-docs/pull/8
- ADR-007 and ADR-008 (PR #9): https://github.com/code-corhuila/qone-docs/pull/9
- Session material: https://code-corhuila.github.io/ova-web/2026-B/distribuidos/09-week/01-session/ and /02-session/
