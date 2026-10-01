#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera PDFs leves de demo Kibanda (handbook, onboarding Tom, contract sample)."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parents[3]
ASSET_DIR = ROOT / "clients" / "glovo-sibasi" / "glovo-sibasiasset"


def _styles():
    base = getSampleStyleSheet()
    title = ParagraphStyle(
        "KibandaTitle",
        parent=base["Heading1"],
        fontSize=16,
        spaceAfter=10,
        textColor="#0b3d5c",
    )
    h2 = ParagraphStyle(
        "KibandaH2",
        parent=base["Heading2"],
        fontSize=12,
        spaceBefore=10,
        spaceAfter=6,
        textColor="#0b3d5c",
    )
    body = ParagraphStyle(
        "KibandaBody",
        parent=base["BodyText"],
        fontSize=10,
        leading=14,
        spaceAfter=6,
    )
    note = ParagraphStyle(
        "KibandaNote",
        parent=base["BodyText"],
        fontSize=8,
        textColor="#666666",
        spaceBefore=12,
    )
    return title, h2, body, note


def _build(path: Path, story_parts: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
    )
    doc.build(story_parts)
    print(f"Wrote {path}")


def handbook() -> Path:
    title, h2, body, note = _styles()
    out = ASSET_DIR / "Kibanda_Employee_Handbook_Demo.pdf"
    parts = [
        Paragraph("Kibanda Employee Handbook", title),
        Paragraph("Nairobi · Four branches + Head Office · Demo document", body),
        Paragraph("Welcome", h2),
        Paragraph(
            "Kibanda started on Moi Avenue in 2019. Today we serve chapati, beans and chai "
            "across CBD, Westlands, Kilimani and Karen. This handbook is a <b>demo sample</b> "
            "for Factorial East Africa presentations — not legal advice.",
            body,
        ),
        Paragraph("Our branches", h2),
        Paragraph(
            "• Kibanda CBD — opens 06:30 for breakfast<br/>"
            "• Kibanda Westlands — lunch meetings and busy weekends<br/>"
            "• Kibanda Kilimani — deliveries and evening crowd<br/>"
            "• Kibanda Karen — family brunch (closed Mondays)<br/>"
            "• Head Office — above Kilimani (HR, accounts, procurement)",
            body,
        ),
        Paragraph("Leave (Kenya demo policy)", h2),
        Paragraph(
            "Annual leave 21 working days · Sick leave 7 full + 7 half · Maternity 3 months · "
            "Paternity 2 weeks · Compassionate 3 working days (Kibanda policy).",
            body,
        ),
        Paragraph("Working time", h2),
        Paragraph(
            "At least one rest day in every seven. Shift templates live in Factorial "
            "(PREP, AM, PM, SPLIT, WKND, OFF). Rotas are published in the app — not WhatsApp.",
            body,
        ),
        Paragraph(
            "Demo only · Prepared for Brenda's Factorial story · September 2026",
            note,
        ),
    ]
    _build(out, parts)
    return out


def onboarding_tom() -> Path:
    title, h2, body, note = _styles()
    out = ASSET_DIR / "Kibanda_Onboarding_Checklist_Tom_Sang.pdf"
    parts = [
        Paragraph("Onboarding checklist — Tom Kiplagat Sang", title),
        Paragraph("Casual Waiter · Kibanda Westlands · Manager: Grace Wanjiku Kamau", body),
        Paragraph("Before day 1", h2),
        Paragraph(
            "☐ Upload ID copy<br/>"
            "☐ KRA PIN<br/>"
            "☐ NSSF number<br/>"
            "☐ SHA number<br/>"
            "☐ Valid food handler medical certificate<br/>"
            "☐ Acknowledge Kibanda handbook",
            body,
        ),
        Paragraph("Week 1", h2),
        Paragraph(
            "☐ Welcome message from Grace<br/>"
            "☐ Shadow AM and PM service once each<br/>"
            "☐ Clock-in practice on Factorial app with Westlands location<br/>"
            "☐ Confirm leave balance visible in app",
            body,
        ),
        Paragraph(
            "Demo workflow sample for Factorial East Africa · Not a live HR form",
            note,
        ),
    ]
    _build(out, parts)
    return out


def contract_sample() -> Path:
    title, h2, body, note = _styles()
    out = ASSET_DIR / "Kibanda_Employment_Contract_Sample_Brian_Wafula.pdf"
    parts = [
        Paragraph("Employment contract (demo sample)", title),
        Paragraph("Employee: Brian Wafula Wekesa · Role: Waiter · Branch: Westlands", body),
        Paragraph("Parties", h2),
        Paragraph(
            "Employer: Kibanda Limited (Nairobi)<br/>"
            "Employee: Brian Wafula Wekesa",
            body,
        ),
        Paragraph("Key terms (demo)", h2),
        Paragraph(
            "• Start date: 15 January 2025<br/>"
            "• Place of work: Kibanda Westlands, Nairobi<br/>"
            "• Pay: basic salary plus 15% housing allowance (demo figures)<br/>"
            "• Hours: as published in Factorial rota; overtime per Kenya wage order demo notes<br/>"
            "• Leave: per Kibanda handbook / Employment Act demo checklist<br/>"
            "• Notice: 28 days (monthly-paid demo)",
            body,
        ),
        Paragraph("E-signature note", h2),
        Paragraph(
            "In the live demo path, Esther sends this style of contract through Factorial "
            "E-Signature so waiters can sign on their phone between shifts.",
            body,
        ),
        Paragraph(
            "FICTIONAL DEMO DOCUMENT · Not a real contract · Not legal advice",
            note,
        ),
        Spacer(1, 12),
        Paragraph("Signature (demo): ______________________  Date: __________", body),
    ]
    _build(out, parts)
    return out


def main() -> int:
    handbook()
    onboarding_tom()
    contract_sample()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
