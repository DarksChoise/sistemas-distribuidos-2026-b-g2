"""Screens of Qampus v2.0.0 for the MVP 2 evidence: the composed platform (qone-infra) at
http://localhost:5173, signed in through the identity portal like a person, 1440x900, Chrome.
Usage: capture_v2.py <output folder>"""
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
BASE = "http://localhost:5173"
PASSWORD = os.environ["DEMO_PASSWORD"]  # the DEMO_PASSWORD of qone-infra/.env, never versioned
shots = []


def snap(page, name, wait_text=None, full=False):
    if wait_text:
        page.get_by_text(wait_text, exact=False).first.wait_for(timeout=150_000)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(600)
    page.screenshot(path=str(OUT / f"{name}.png"), full_page=full)
    shots.append(name)
    print("captured", name)


def sign_in(context, email):
    page = context.new_page()
    page.goto(f"{BASE}/login")
    page.get_by_label("E-mail").wait_for()
    page.get_by_label("E-mail").fill(email)
    page.get_by_label("Password", exact=True).fill(PASSWORD)
    page.get_by_role("button", name="Sign in", exact=True).first.click()
    page.wait_for_url(f"{BASE}/")
    return page


with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome")
    new = lambda: browser.new_context(viewport={"width": 1440, "height": 900})  # noqa: E731

    ctx = new()
    page = ctx.new_page()
    page.goto(f"{BASE}/login")
    snap(page, "public-sign-in", "Create your account")
    page.goto(f"{BASE}/login/register")
    snap(page, "public-register", "Student code")
    ctx.close()

    ctx = new()
    page = sign_in(ctx, "laura.gomez@uni.edu.co")
    snap(page, "student-home")
    page.goto(f"{BASE}/catalog")
    snap(page, "student-catalog-subjects", "ISW-604")
    page.goto(f"{BASE}/catalog/ISW-604")
    snap(page, "student-catalog-subject-sections", "Group")
    page.goto(f"{BASE}/enrollment/pensum")
    snap(page, "student-pensum", "My pensum", full=True)
    page.goto(f"{BASE}/enrollment/schedule")
    snap(page, "student-schedule", "Schedule")
    page.goto(f"{BASE}/enrollment/enrollments")
    snap(page, "student-enrollments", "ISW")
    page.goto(f"{BASE}/billing/invoice")
    snap(page, "student-invoice-paid", "Paid")
    ctx.close()

    ctx = new()
    page = sign_in(ctx, "santiago.rojas@uni.edu.co")
    page.goto(f"{BASE}/enrollment/certificates")
    snap(page, "student-certificates", "Download PDF")
    ctx.close()

    ctx = new()
    page = sign_in(ctx, "maria.cabrera@uni.edu.co")
    page.goto(f"{BASE}/advisor")
    page.get_by_role("button", name="New conversation").click()
    page.get_by_label("Your question").fill("¿Qué materias me faltan para graduarme?")
    page.get_by_role("button", name="Send").click()
    page.get_by_role("button", name="Send").wait_for(timeout=150_000)
    page.get_by_label("Your question").fill("Inscríbeme en Teoría de la Computación")
    page.get_by_role("button", name="Send").click()
    snap(page, "student-advisor-plan-card", "Confirm enrollment", full=True)
    ctx.close()

    ctx = new()
    page = sign_in(ctx, "carlos.ramirez@uni.edu.co")
    page.goto(f"{BASE}/catalog/professor/sections")
    snap(page, "professor-sections", "ISW")
    ctx.close()

    ctx = new()
    page = sign_in(ctx, "admin@uni.edu.co")
    page.goto(f"{BASE}/catalog/admin/subjects/new")
    snap(page, "admin-new-subject", "Prerequisites")
    page.goto(f"{BASE}/catalog/admin/sections/new")
    snap(page, "admin-open-section", "Professor")
    page.goto(f"{BASE}/billing/admin/invoices/new")
    snap(page, "admin-issue-invoice", "Amount")
    ctx.close()
    browser.close()

print(len(shots), "screens")
