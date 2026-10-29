# How to run the negative authorization test

**Service and endpoints:** `qone-advisor-api`, AD-02 `POST /api/v1/advisor/conversations` and AD-05
`POST /api/v1/advisor/conversations/{id}/messages` (the only trigger of the call to OpenAI).

**Story and criterion it covers:** [qone-docs #55](https://github.com/code-corhuila/qone-docs/issues/55) "Only the data the advisor needs leaves Qampus, and only for its owner" (STRIDE I, risk 6, P1), acceptance criterion 1:
*"A request from a caller who does not own the conversation, or who is not a person, gets 403 or 404 and
no request reaches the LLM provider."* The third test also guards row E of the STRIDE table (a tool
outside the caller's role never runs).

The `ScriptedAgent` of the service's own tests stands in for OpenAI: every element of
`agent.requests` is a request that would have left Qampus. No API key and no network are needed.

## Locally (Windows, PowerShell)

From the folder that holds the `qone-*` repositories (`qampus\`):

```powershell
cd qone-advisor-api
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
Copy-Item ..\..\sistemas-distribuidos-2026-b-g2\13-week\workshop\04-security-ci\test_advisor_negative_authz.py tests\
python -m pytest tests\test_advisor_negative_authz.py -v
Remove-Item tests\test_advisor_negative_authz.py
```

## In CI

[security.yml](security.yml) runs the same file in the job `authorization-tests`, next to `gitleaks`
and `pip-audit`, on every `pull_request`.
