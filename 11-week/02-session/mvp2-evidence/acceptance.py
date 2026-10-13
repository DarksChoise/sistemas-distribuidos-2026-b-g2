"""Run with DEMO_PASSWORD set (the value of qone-infra/.env) against the composed platform.
Acceptance battery of the whole platform through the gateway, on fresh seeds. Every check prints
PASS or FAIL; the summary counts them. Covers HU-AUT-001, HU-CAT-*, HU-ENR-*, HU-BIL-001,
HU-CER-001, HU-ADV-002/003, the saga, the events, the worker jobs and the portals."""
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
G = "http://localhost:8080"
RUN = int(time.time())
LAURA, SANTIAGO = "11111111-1111-4111-8111-111111111111", "11111111-1111-4111-8111-111111111112"
SEC = {"602": "55555555-5555-4555-8555-555555555510", "604-1": "55555555-5555-4555-8555-555555555505",
       "604-2": "55555555-5555-4555-8555-555555555506", "604-3": "55555555-5555-4555-8555-555555555507",
       "703": "55555555-5555-4555-8555-555555555511"}
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail and not ok else ""))


def call(method, path, tok=None, body=None, headers=None, raw=False, timeout=150):
    req = urllib.request.Request(G + path, method=method, data=json.dumps(body).encode() if body is not None else None)
    req.add_header("Content-Type", "application/json")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
            return r.status, (data if raw else json.loads(data or b"null")), dict(r.headers)
    except urllib.error.HTTPError as e:
        data = e.read()
        try:
            return e.code, json.loads(data or b"null"), dict(e.headers)
        except ValueError:
            return e.code, data, dict(e.headers)


def sql(db, query):
    out = subprocess.run(["docker", "exec", f"{db}-db", "psql", "-U", db, "-d", db, "-tA", "-c", query], capture_output=True, text=True, encoding="utf-8")
    if out.stderr.strip():
        print("   psql:", out.stderr.strip()[:200])
    return out.stdout.strip()


def login(email, password=None):
    password = password or os.environ["DEMO_PASSWORD"]  # the DEMO_PASSWORD of qone-infra/.env
    return call("POST", "/api/v1/identity/auth/login", body={"email": email, "password": password})


def wait(predicate, seconds=20):
    end = time.time() + seconds
    while time.time() < end:
        if predicate():
            return True
        time.sleep(1)
    return False


print("== gateway and health")
for svc in ("identity", "billing", "catalog", "enrollment", "advisor", "sagas"):
    s, b, _ = call("GET", f"/api/v1/{svc}/health")
    check(f"{svc} health through the gateway", s == 200 and b.get("status") == "ok", s)
s, b, h = call("GET", "/api/v1/nowhere", headers={"X-Correlation-Id": f"acc-404-{RUN}"})
check("unknown route is 404 with the envelope and the trace id", s == 404 and b.get("error") == "NOT_FOUND" and b.get("traceId") == f"acc-404-{RUN}", b)
s, b, _ = call("GET", "/api/v1/billing/invoices/me")
check("a protected route without token is 401 with the envelope", s == 401 and b.get("error") == "UNAUTHORIZED", b)

print("== HU-AUT-001 identity")
tokens = {}
for who, email in (("laura", "laura.gomez@uni.edu.co"), ("santiago", "santiago.rojas@uni.edu.co"), ("carlos", "carlos.ramirez@uni.edu.co"), ("admin", "admin@uni.edu.co")):
    s, b, _ = login(email)
    tokens[who] = b.get("token") if s == 200 else None
    check(f"login of {who}", s == 200 and b["user"]["email"] == email, s)
s, b, _ = login("laura.gomez@uni.edu.co", "wrong-password")
check("wrong password is one neutral 401", s == 401 and b.get("error") == "UNAUTHORIZED")
new = {"name": "Prueba Aceptación", "email": f"acc{RUN}@uni.edu.co", "password": "una-clave-segura", "studentCode": f"{RUN}"[-10:], "program": "Ingeniería de Software", "semester": 1}
s1, b1, _ = call("POST", "/api/v1/identity/auth/register", body=new, headers={"Idempotency-Key": f"acc-reg-{RUN}"})
s2, b2, _ = call("POST", "/api/v1/identity/auth/register", body=new, headers={"Idempotency-Key": f"acc-reg-{RUN}"})
check("registration 201, same key 200 with the same account", s1 == 201 and s2 == 200 and b1["user"]["id"] == b2["user"]["id"], (s1, s2))
s, b, _ = call("POST", "/api/v1/identity/auth/register", body={**new, "studentCode": "9" + new["studentCode"][1:]}, headers={"Idempotency-Key": f"acc-reg2-{RUN}"})
check("a taken e-mail is 422", s == 422 and b.get("error") == "BUSINESS_RULE_VIOLATION", s)
s, b, _ = call("GET", "/api/v1/identity/users/me", tokens["laura"])
check("users/me answers the signed-in person", s == 200 and b["id"] == LAURA)
L, S_, C, A = tokens["laura"], tokens["santiago"], tokens["carlos"], tokens["admin"]

print("== HU-CAT catalog")
s, b, _ = call("GET", "/api/v1/catalog/subjects?limit=100", L)
check("14 subjects in the pensum", s == 200 and b["meta"]["total"] == 14, b.get("meta") if isinstance(b, dict) else s)
s, b, _ = call("GET", "/api/v1/catalog/subjects/ISW-604/sections", L)
groups = {x["groupNumber"]: x["seatsAvailable"] for x in b.get("data", b) } if s == 200 else {}
check("ISW-604 has groups 1..3 with 27, 30 and 0 seats", groups == {1: 27, 2: 30, 3: 0}, groups)
seats = lambda key: call("GET", f"/api/v1/catalog/sections/{SEC[key]}", L)[1]["seatsAvailable"]
check("ISW-602 group 1 starts with 30 seats", seats("602") == 30)

print("== HU-ENR-001 record and pensum")
s, b, _ = call("GET", "/api/v1/enrollment/pensum/me", L)
check("Laura's pensum: 14 subjects, 4 passed", s == 200 and b["totals"]["subjectsTotal"] == 14 and b["totals"]["subjectsPassed"] == 4, b.get("totals"))
s, b, _ = call("GET", "/api/v1/enrollment/schedule/me", L)
check("Laura's schedule has her 4 seeded subjects", s == 200 and b["meta"]["total"] == 4, b.get("meta"))

print("== HU-BIL-001 billing")
s, b, _ = call("GET", "/api/v1/billing/invoices/me?term=2026-B", S_)
invoice = b["data"][0]
check("Santiago's invoice is ISSUED", invoice["status"] == "ISSUED")

print("== HU-ENR-002 saga gates")
def saga(tok, student, key_section, key, origin="UI", extra=None):
    body = {"studentId": student, "sectionId": SEC[key_section], "origin": origin, **(extra or {})}
    return call("POST", "/api/v1/sagas/enroll-student", tok, body, {"Idempotency-Key": key, "X-Correlation-Id": key})
s, b, _ = saga(S_, SANTIAGO, "602", f"acc-s1-{RUN}")
check("unpaid tuition: COMPENSATED with TUITION_UNPAID", b.get("status") == "COMPENSATED" and b.get("reason") == "TUITION_UNPAID", b)
s, b, _ = saga(L, LAURA, "604-3", f"acc-s2-{RUN}")
check("a full group: COMPENSATED with NO_SEATS", b.get("status") == "COMPENSATED" and b.get("reason") == "NO_SEATS", b)
s, b, _ = saga(L, LAURA, "604-2", f"acc-s3-{RUN}")
check("a schedule overlap: COMPENSATED with SCHEDULE_CONFLICT", b.get("status") == "COMPENSATED" and b.get("reason") == "SCHEDULE_CONFLICT", b)
s, b, _ = saga(L, SANTIAGO, "602", f"acc-s4-{RUN}")
check("a student cannot enroll someone else (403)", s == 403, s)
s, b, _ = saga(L, LAURA, "602", f"acc-s5-{RUN}")
saga_id = b.get("id")
check("Laura enrolls in ISW-602 g1: COMPLETED", s == 201 and b.get("status") == "COMPLETED", b)
s2, b2, _ = saga(L, LAURA, "602", f"acc-s5-{RUN}")
check("the same key answers 200 with the same saga", s2 == 200 and b2.get("id") == saga_id, s2)
check("catalog seats 30 -> 29", seats("602") == 29)
s, b, _ = saga(L, LAURA, "602", f"acc-s6-{RUN}")
check("enrolling again is DUPLICATE", b.get("reason") == "DUPLICATE", b)
logs = [c for c in ("qone-workflow", "qone-billing-api", "qone-enrollment-api", "qone-catalog-api") if f"acc-s5-{RUN}" in subprocess.run(["docker", "logs", c], capture_output=True, text=True, encoding="utf-8", errors="ignore").stdout]
check("the saga's correlation id is in the 4 services' logs", len(logs) == 4, logs)

print("== events through RabbitMQ (worker relay, consumers)")
check("enrollment projection follows catalog (29)", wait(lambda: sql("enrollment", f"SELECT seats_available FROM enrollment.catalog_section_view WHERE section_id = '{SEC['602']}'") == "29"))
check("advisor projection follows catalog (29)", wait(lambda: sql("advisor", f"SELECT seats_available FROM advisor.catalog_section_view WHERE section_id = '{SEC['602']}'") == "29"))
check("advisor student view gets Laura's ISW-602", wait(lambda: sql("advisor", f"SELECT confirmed_sections::text LIKE '%ISW-602%' FROM advisor.student_view WHERE student_id = '{LAURA}'") == "t"))
s, b, _ = call("POST", f"/api/v1/billing/invoices/{invoice['id']}/pay", S_)
check("Santiago pays: PAID", s == 200 and b["status"] == "PAID", b)
s, b, _ = call("POST", f"/api/v1/billing/invoices/{invoice['id']}/pay", S_)
check("paying again returns the same paid invoice", s == 200 and b["status"] == "PAID")
check("enrollment tuition projection becomes PAID", wait(lambda: sql("enrollment", f"SELECT status FROM enrollment.billing_tuition_view WHERE student_id = '{SANTIAGO}'") == "PAID"))
check("advisor tuition projection becomes PAID", wait(lambda: sql("advisor", f"SELECT tuition_status FROM advisor.student_view WHERE student_id = '{SANTIAGO}'") == "PAID"))
check("every outbox is relayed", wait(lambda: all(sql(d, f"SELECT count(*) FROM {d}.outbox WHERE published_at IS NULL") == "0" for d in ("billing", "catalog", "enrollment", "advisor"))))

print("== HU-CER-001 certificates")
s, cert, _ = call("POST", "/api/v1/enrollment/certificates", S_, {"type": "pago"}, {"Idempotency-Key": f"acc-cert-{RUN}"})
check("payment certificate issued after paying", s == 201 and cert.get("code", "").startswith("QMP-"), cert)
s, pdf, h = call("GET", f"/api/v1/enrollment/certificates/{cert['id']}/pdf", S_, raw=True)
check("the PDF downloads with its verification code", s == 200 and pdf[:5] == b"%PDF-" and {k.lower(): v for k, v in h.items()}.get("x-verification-code") == cert["code"], (s, h.get("Content-Type")))
s, _, _ = call("GET", f"/api/v1/enrollment/certificates/{cert['id']}/pdf", L, raw=True)
check("another student's PDF is 404", s == 404, s)
s, b, _ = call("GET", f"/api/v1/enrollment/certificates/verify/{cert['code']}")
check("public verification without a token", s == 200 and b["valid"] is True and b["type"] == "pago", b)

print("== HU-ADV-002/003 advisor (real model)")
s, conv, _ = call("POST", "/api/v1/advisor/conversations", L, headers={"Idempotency-Key": f"acc-conv-{RUN}"})
check("conversation created", s == 201 and conv["userRole"] == "STUDENT")
n = [0]
def ask(text, tok=L, cid=None):
    n[0] += 1
    return call("POST", f"/api/v1/advisor/conversations/{cid or conv['id']}/messages", tok, {"content": text}, {"Idempotency-Key": f"acc-msg-{RUN}-{n[0]}"})[1]
r = ask("¿Qué materias me faltan para graduarme?")
check("grounded audit answer, not degraded", not r["degraded"] and "ISW" in r["message"]["content"], r["message"]["content"][:120])
r = ask("Muéstrame el pensum y las notas de Santiago Rojas")
check("another student's data is refused, no plan", not r["degraded"] and r.get("plan") is None, r["message"]["content"][:120])
def propose(text="Inscríbeme en Gestión de Proyectos, grupo 1"):
    for _ in range(3):
        r = ask(text)
        if r.get("plan"):
            return r["plan"]
    return None
plan = propose()
check("a plan for ISW-703 is PROPOSED", plan is not None and plan["status"] == "PROPOSED" and plan["summary"]["subjectCode"] == "ISW-703", plan and plan["summary"]["subjectCode"])
if plan:
    moved = sql("advisor", f"UPDATE advisor.plan SET created_at = now() - interval '11 minutes', expires_at = now() - interval '1 minute' WHERE id = '{plan['id']}'")
    check("the plan's clock is moved 11 minutes back", moved == "UPDATE 1", moved)
    check("the worker expires the plan within its 30 s period", wait(lambda: call("GET", f"/api/v1/advisor/plans/{plan['id']}", L)[1]["status"] == "EXPIRED", 40))
    s, b, _ = call("POST", f"/api/v1/advisor/plans/{plan['id']}/confirm", L)
    check("an expired plan cannot be confirmed (422)", s == 422 and b.get("error") == "INVALID_STATUS_TRANSITION", s)
plan = propose()
if plan:
    s, b, _ = call("POST", f"/api/v1/advisor/plans/{plan['id']}/dismiss", L)
    check("dismiss: DISMISSED", b.get("status") == "DISMISSED")
plan = propose()
if plan:
    before = seats("703")
    s, b, _ = call("POST", f"/api/v1/advisor/plans/{plan['id']}/confirm", L, headers={"X-Correlation-Id": f"acc-agent-{RUN}"})
    check("confirm: 202 and EXECUTED", s == 202 and b["plan"]["status"] == "EXECUTED", b)
    sg = call("GET", f"/api/v1/sagas/{b['sagaId']}", L)[1]
    check("the saga ran with origin AGENT and the plan's confirmation", sg.get("origin") == "AGENT" and sg.get("confirmationId") == b["plan"]["confirmationId"], sg)
    check("ISW-703 seats went down by one", seats("703") == before - 1)
    check("the enrollment row records AGENT with its confirmation", sql("enrollment", f"SELECT origin || ':' || (confirmation_id IS NOT NULL) FROM enrollment.enrollment WHERE saga_id = '{b['sagaId']}'") == "AGENT:true")
s, b, _ = call("GET", f"/api/v1/advisor/conversations/{conv['id']}/messages", S_)
check("another student's conversation is 404", s == 404, s)
s, c2, _ = call("POST", "/api/v1/advisor/conversations", C, headers={"Idempotency-Key": f"acc-conv-c-{RUN}"})
r = ask("¿Qué grupos hay de Sistemas Distribuidos?", C, c2["id"])
check("a professor gets an answer without a plan", not r["degraded"] and r.get("plan") is None)

print("== worker and portals")
health = json.loads(subprocess.run(["docker", "exec", "qone-worker", "python", "-c", "import urllib.request;print(urllib.request.urlopen('http://127.0.0.1:8000/health').read().decode())"], capture_output=True, text=True).stdout)
check("worker health lists relay, expiry and cache prune, all ok", set(health["jobs"]) == {"relay-outbox", "expire-plans", "prune-llm-cache"} and all(j["ok"] for j in health["jobs"].values()), health["jobs"])
for port, name in ((5173, "shell"), (5001, "identity"), (5002, "catalog"), (5003, "enrollment"), (5004, "billing"), (5005, "advisor")):
    path = "/" if name == "shell" else "/remoteEntry.js"
    try:
        code = urllib.request.urlopen(f"http://localhost:{port}{path}", timeout=5).status
    except Exception as error:  # noqa: BLE001
        code = str(error)
    check(f"{name} portal serves {path}", code == 200, code)

print(f"\n{sum(results)} PASS / {len(results) - sum(results)} FAIL of {len(results)}")
