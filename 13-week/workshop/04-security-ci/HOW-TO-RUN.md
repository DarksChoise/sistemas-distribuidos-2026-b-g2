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

## Real run (CP8, 2026-10-30, Windows 10, Python 3.12.10)

Against `qone-advisor-api` at `main` (`913e9e6`, release 2.0.0), with the steps above:

```text
PS> python -m pytest tests\test_advisor_negative_authz.py -v -o addopts=""
platform win32 -- Python 3.12.10, pytest-8.4.2, pluggy-1.6.0
rootdir: C:\Users\Usuario\Desktop\Sistemas Distribuidos\qampus\qone-advisor-api
configfile: pyproject.toml
collected 3 items

tests/test_advisor_negative_authz.py::test_a_service_token_cannot_open_a_conversation_and_nothing_reaches_openai PASSED [ 33%]
tests/test_advisor_negative_authz.py::test_a_student_cannot_write_in_another_students_conversation_and_nothing_reaches_openai PASSED [ 66%]
tests/test_advisor_negative_authz.py::test_a_professor_conversation_never_runs_propose_enrollment_even_if_the_model_asks PASSED [100%]

============================== 3 passed in 0.94s ==============================
```

`-o addopts=""` only overrides the `-q` of the service's `pyproject.toml`, so the test names are printed.

## Validation of security.yml

Checked with actionlint v1.7.12 (the official playground, https://rhysd.github.io/actionlint/): **"No error
was detected."** Three jobs: `secret-scan`, `dependency-audit`, `authorization-tests`; `env.SERVICE_REPO`
and `env.SERVICE_REF` are valid in `with:` of a step.
