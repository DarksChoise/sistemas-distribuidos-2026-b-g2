# Week 05 — Progress (Quorum One)

Platform work this week: **MVP 1 released — Qampus v1.0.0.**

- Attended sessions 1 (containerization with Docker) and 2 (release: shipping MVP 1).
- Nine feature Pull Requests (#2–#10) into `develop`, promotion `develop → qa → main`
  (#11, #12) and tag **v1.0.0** with a GitHub Release.
- 20 unit + integration tests over the documented invariants; CI (ruff + pytest + frontend build)
  green on every environment branch.
- Release checklist verified with evidence: `docker compose up` against PostgreSQL, happy path and
  error paths, no secrets, README + ADRs + CHANGELOG.
- Project board closed: all Cut 1 items Done (DoD).

Evidence: [`hu-status/README.md`](hu-status/README.md) ·
[`02-session/mvp1-evidence/`](02-session/mvp1-evidence/README.md) (16 screenshots of the
running system) · https://github.com/code-corhuila/quorum-one/releases/tag/v1.0.0.
