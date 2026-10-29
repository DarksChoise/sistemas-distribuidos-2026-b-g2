# Week 13 workshop - Threat modeling and security backlog on Qampus

<!-- CONFIG-START -->
- FULL_NAME: Juan Diego Andrade Cardozo
- GITHUB_USER: DarksChoise
- TEAM: Quorum One
- DOCS_REPO: https://github.com/code-corhuila/qone-docs
- BOUNDARY: qone-advisor-api -> OpenAI Chat Completions API (the AI advisor calling the LLM provider)
- CLAIM_ISSUE: https://github.com/code-corhuila/qone-docs/issues/51
- REFLECTION_DOC: https://docs.google.com/document/d/1G6fSZGhlKsXHe-54xqXnRHISlr_feH0EjTqZKILvTrI/edit
- LIBRARY_BOOK:
- LIBRARY_RECORD_TIME:
<!-- CONFIG-END -->

Project: **Qampus**, the university platform of team Quorum One (identity, catalog, enrollment,
billing and the AI advisor; twenty `qone-*` repositories in `code-corhuila`, release `v2.1.0`).

My boundary is the only one where Qampus data leaves our own infrastructure: `qone-advisor-api`
sends the student's question, the conversation history and the results of its tools to OpenAI
(ADR-003), and takes back text and tool calls that the agent then runs (INV-ADV-001..003).

| Checkpoint | Where |
|---|---|
| CP1 Attack surface and trust boundaries | [01-attack-surface.md](01-attack-surface.md) |
| CP2 STRIDE on my boundary | Pull Request in `qone-docs`: `05-architecture/security/stride-DarksChoise.md` |
| CP3 Security backlog | three `[security]` issues in `qone-docs` (STORIES above) |
| CP4 Security gates and negative test | [04-security-ci/](04-security-ci/) |
