<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       07-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 07

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Juan Diego Andrade Cardozo
- GITHUB_USER: DarksChoise
- TEAM: Quorum One
- SPRINT_GOAL: Pay the Cut 1 documentation debt in qone-docs and adopt the course branching policy for the documentation repository.
<!-- CONFIG-END -->

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| HU-WEB-001/002 | UX-UI evidence of the shipped v1.0.0 portal: screen catalog with screenshots, navigation map, design system | doing | https://github.com/code-corhuila/qone-docs/pull/4 |
| HU-PLT-002 | Governance and architecture documents aligned with the branching policy: git conventions, deployment, cross-cutting concerns, threat model, pattern decisions | doing | https://github.com/code-corhuila/qone-docs/pull/4 |

## 2. My individual contribution
- Adopted the branching policy and CODEOWNERS the professor added to qone-docs on Sep 14: from this week every documentation change goes through a `docs/` branch and a Pull Request to `main` with the teacher's approval.
- On Sep 16 wrote, in branch `docs/ux-ui-evidence-and-governance-review`: the screen catalog of v1.0.0 with real screenshots, its template and the capture script; the real navigation map and design system; the deployment, cross-cutting and threat-model documents; the filled pattern decision table with corrected ADR titles; `git-conventions.md` aligned with the policy; a fix to a broken link in the HU template.
- Opened qone-docs PR #4 on Sep 17 with all of it; the review left non-blocking recommendations to answer.

## 3. Blockers and risks
- `main` of qone-docs is now protected (teacher approval, CODEOWNERS): documentation lands only when the review is resolved, so it has to be planned ahead of the cut dates.

## 4. Plan for next week
- Answer every recommendation of the review of #4 and merge it.
- Document the v1.0.0 system as built: diagrams and the real API contracts.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [x] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...)
- [ ] Testable acceptance criteria
- [ ] Tests added/updated (unit / integration)
- [ ] DDD / hexagonal boundaries respected (domain has no I/O)
- [x] No secrets; config via environment variables

## 6. Evidence links
- qone-docs PR #4: https://github.com/code-corhuila/qone-docs/pull/4
- Branching policy adopted: https://github.com/code-corhuila/qone-docs/blob/main/00-governance/branching-policy.md
- Session material: https://code-corhuila.github.io/ova-web/2026-B/distribuidos/07-week/01-session/ and /02-session/
