<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       13-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 13

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Juan Diego Andrade Cardozo
- GITHUB_USER: DarksChoise
- TEAM: Quorum One
- SPRINT_GOAL: Model the threats of the boundary qone-advisor-api -> OpenAI and turn the top three into security stories of the team backlog, with a negative authorization test and security gates for the pipeline.
<!-- CONFIG-END -->

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| W13-TM | Threat model of qone-advisor-api -> OpenAI (STRIDE, in review) | doing | https://github.com/code-corhuila/qone-docs/pull/52 |
| SEC-ADV-001 | [security] A per-student quota keeps the advisor answering for everyone (D, risk 9, P0) | todo | https://github.com/code-corhuila/qone-docs/issues/53 |
| SEC-ADV-002 | [security] The advisor proposes an enrollment only when the student asks (T, risk 6, P1) | todo | https://github.com/code-corhuila/qone-docs/issues/54 |
| SEC-ADV-003 | [security] Only the data the advisor needs leaves Qampus, and only for its owner (I, risk 6, P1) | doing | https://github.com/code-corhuila/qone-docs/issues/55 |

## 2. My individual contribution
- Week 13 workshop, progress delivery, one push per checkpoint:
  CP0 setup and boundary claim ([qone-docs #51](https://github.com/code-corhuila/qone-docs/issues/51)) [bf19cf7](https://github.com/DarksChoise/sistemas-distribuidos-2026-b-g2/commit/bf19cf7);
  CP1 attack surface, six trust boundaries, asset inventory and entry points of TB6 [4508e3d](https://github.com/DarksChoise/sistemas-distribuidos-2026-b-g2/commit/4508e3d);
  CP2 STRIDE in the team docs, two pushes ([84e6358](https://github.com/code-corhuila/qone-docs/commit/84e6358), [6011a9a](https://github.com/code-corhuila/qone-docs/commit/6011a9a)) in [PR #52](https://github.com/code-corhuila/qone-docs/pull/52);
  CP3 three security stories with labels `security` and `P0`/`P1` in the Backlog column of the team board, linked in the README [8596df8](https://github.com/DarksChoise/sistemas-distribuidos-2026-b-g2/commit/8596df8);
  CP4 `security.yml` (gitleaks, pip-audit, authorization tests) and a negative test of `qone-advisor-api` that passes locally (3 passed) [44f6192](https://github.com/DarksChoise/sistemas-distribuidos-2026-b-g2/commit/44f6192), [83f0fdd](https://github.com/DarksChoise/sistemas-distribuidos-2026-b-g2/commit/83f0fdd).
- Library book (rule 11): Tanenbaum and Van Steen, *Sistemas distribuidos: principios y paradigmas*, 2nd ed.,
  Pearson Educacion, 2008, call number 005.4476 T15d Ej. 2; chapter 9, p. 378-380, 396-397, 413-414, 428.
  It marks six [B] items of the STRIDE table and the acceptance criteria of #53.

### Peer review (self-review: I am the only member of Quorum One)
Reviewed my STRIDE table of PR #52 against the ParkFlow example of the guide:
- **A threat I missed.** ParkFlow has an I row for error bodies that leak internals. My table has no row for
  AD-01 `GET /api/v1/advisor/health`: it is public and answers the provider model (`gpt-4o-mini`), and I
  listed it as entry point E6 in CP1 but never modeled it. Likelihood 3, impact 1, risk 3 (P2): it tells an
  attacker which model to tune a prompt injection for. Mitigation: answer only `llm: configured|missing`
  publicly and move `model` behind an ADMIN token.
- **A mitigation that does not fit the stack as a PR gate.** Criterion 3 of #54 runs 10 injection payloads
  against `gpt-4o-mini`. In a pull request that needs `OPENAI_API_KEY` as a CI secret, costs money on every
  push and is not deterministic. It stays as a manual release check; the PR gate is criteria 1 and 2,
  which run with the `ScriptedAgent` and no network.
- Both changes go into the table and the issues in CP6.

## 3. Blockers and risks
- I am the only member of the team: no teammate review on PR #52; the self-review above replaces it.
- `qone-docs` PR #52 stays open for the team lead review (rule 8: I do not merge my own PR).
- The security gates live in the fork as a proposal; they are not yet in the CI of `qone-advisor-api`.

## 4. Plan for next week
- CP6: answer the review on PR #52 (add the AD-01 row, move the eval to the release checklist).
- CP7: refine the three issues; CP8: run the negative test again, paste the output and validate `security.yml`.
- Implement #53 first (P0): a per-student quota on AD-05 and `max_tokens` on `ChatOpenAI`.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [x] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...)
- [x] Testable acceptance criteria
- [x] Tests added/updated (unit / integration)
- [x] DDD / hexagonal boundaries respected (domain has no I/O)
- [x] No secrets; config via environment variables

## 6. Evidence links
- Workshop folder: https://github.com/DarksChoise/sistemas-distribuidos-2026-b-g2/tree/main/13-week/workshop
- STRIDE Pull Request: https://github.com/code-corhuila/qone-docs/pull/52
- Claim issue: https://github.com/code-corhuila/qone-docs/issues/51
- Security stories: https://github.com/code-corhuila/qone-docs/issues/53, https://github.com/code-corhuila/qone-docs/issues/54, https://github.com/code-corhuila/qone-docs/issues/55
- Project board: https://github.com/orgs/code-corhuila/projects/26
