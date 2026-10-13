<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       10-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 10

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Juan Diego Andrade Cardozo
- GITHUB_USER: DarksChoise
- TEAM: Quorum One
- SPRINT_GOAL: Specify Cut 2 contract-first (common contract, service contracts, data model, service pages) and start the web layer: the shell and the catalog portal.
<!-- CONFIG-END -->

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| HU-PLT-001 | v2 documentation: common contract, seven OpenAPI contracts, data model, service pages, DevOps guides (qone-docs #10-#34) | doing | https://github.com/code-corhuila/qone-docs/pull/10 |
| HU-WEB-001 | Shell (Module Federation host): error envelope, session, shared HTTP client, layout, remotes registry, image | done | https://github.com/code-corhuila/qone-front/pull/8 |
| HU-AUT-001 | Shell sign-in routes and the development sign-in of the norm | done | https://github.com/code-corhuila/qone-front/pull/4 |
| HU-CAT-003 | Catalog portal: subjects list and subject detail with its sections | done | https://github.com/code-corhuila/qone-catalog-portal/pull/3 |
| HU-CAT-001 | Catalog portal: admin form that creates a subject with prerequisites | done | https://github.com/code-corhuila/qone-catalog-portal/pull/5 |
| HU-CAT-002 | Catalog portal: admin form that opens a section | doing | https://github.com/code-corhuila/qone-catalog-portal/pull/6 |
| HU-WEB-002 | Catalog portal: the professor's own sections | doing | https://github.com/code-corhuila/qone-catalog-portal/pull/7 |

## 2. My individual contribution
- Wrote the v2 documentation as a stack of 25 pull requests in qone-docs (#10-#34, opened Oct 7): the v1 contracts frozen under `v1/`, the common contract as shared OpenAPI components, the REST guidelines and RS256 authentication, the endpoint catalog, the contracts of identity, billing, catalog, enrollment (with certificates), advisor and the `enroll-student` saga, the v2 data model and data dictionary, the twenty-repository service catalog and one page per piece, and the DevOps guides. Plus ADR-009 (front tooling and testing, #49).
- Created the fourteen Cut 2 user-story issues (qone-docs #35-#48) so every code pull request references its story.
- Built the shell `qone-front` with TDD (Vitest, MSW): PRs #1-#9 merged on Oct 7, #10 opened (mocks of every portal loaded into the shell).
- Built the catalog portal `qone-catalog-portal`: PRs #1-#5 merged on Oct 8; #6-#9 opened (section form, professor view, mocks, mount-relative links).

## 3. Blockers and risks
- The documentation stack waits for the teacher's approval on `main` of qone-docs; the code repositories sync their contract copies from the docs branch meanwhile.
- The backend services were not started before the Cut 2 window closed on Oct 11; they are the focus of week 11.

## 4. Plan for next week
- Build every backend repository of Cut 2 (identity, billing, catalog, enrollment, advisor databases and APIs, workflow, worker, gateway) and the remaining portals, hexagonal and test-first.
- Compose the platform in `qone-infra`, verify it end to end, and release v2.0.0 through develop -> qa -> main.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [x] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...)
- [x] Testable acceptance criteria
- [x] Tests added/updated (unit / integration)
- [x] DDD / hexagonal boundaries respected (domain has no I/O)
- [x] No secrets; config via environment variables

## 6. Evidence links
- qone-docs v2 stack (#10-#34) and ADR-009 (#49): https://github.com/code-corhuila/qone-docs/pulls?q=is%3Apr+created%3A2026-10-07
- Cut 2 user-story issues: https://github.com/code-corhuila/qone-docs/issues?q=is%3Aissue+created%3A2026-10-07
- qone-front pull requests: https://github.com/code-corhuila/qone-front/pulls?q=is%3Apr
- qone-catalog-portal pull requests: https://github.com/code-corhuila/qone-catalog-portal/pulls?q=is%3Apr
- Session material: https://code-corhuila.github.io/ova-web/2026-B/distribuidos/10-week/01-session/ and /02-session/
