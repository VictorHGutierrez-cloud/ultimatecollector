#!/usr/bin/env python3
"""Generate ANSA McAL Factorial IT Implementation Package v2.3 PDF."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUT = Path(r"c:\Users\victo\Downloads") / (
    "ANSA McAL Group — Factorial IT Implementation Package v2.3.pdf"
)

INK = colors.HexColor("#111111")
MUTED = colors.HexColor("#333333")
RULE = colors.HexColor("#111111")
HDR_BG = colors.HexColor("#111111")
ALT_BG = colors.HexColor("#F0F0F0")
WHITE = colors.white
LIGHT = colors.HexColor("#FAFAFA")


def styles():
    base = getSampleStyleSheet()
    s = {
        "date": ParagraphStyle(
            "date",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=9.5,
            textColor=MUTED,
            spaceAfter=2 * mm,
        ),
        "title": ParagraphStyle(
            "title",
            parent=base["Normal"],
            fontName="Times-Bold",
            fontSize=17,
            textColor=INK,
            spaceAfter=1 * mm,
            leading=20,
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=base["Normal"],
            fontName="Times-Bold",
            fontSize=12,
            textColor=INK,
            spaceAfter=3 * mm,
            leading=15,
        ),
        "meta": ParagraphStyle(
            "meta",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=9.5,
            textColor=MUTED,
            leading=12.5,
            spaceAfter=1.5 * mm,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Normal"],
            fontName="Times-Bold",
            fontSize=11,
            textColor=INK,
            spaceBefore=4 * mm,
            spaceAfter=2 * mm,
            leading=14,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Normal"],
            fontName="Times-Bold",
            fontSize=10.5,
            textColor=INK,
            spaceBefore=3 * mm,
            spaceAfter=1.5 * mm,
            leading=13,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=9.5,
            textColor=INK,
            leading=12.5,
            alignment=TA_JUSTIFY,
            spaceAfter=2 * mm,
        ),
        "body_left": ParagraphStyle(
            "body_left",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=9.5,
            textColor=INK,
            leading=12.5,
            alignment=TA_LEFT,
            spaceAfter=1.5 * mm,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=9.5,
            textColor=INK,
            leading=12.5,
            leftIndent=4 * mm,
            spaceAfter=1 * mm,
        ),
        "note": ParagraphStyle(
            "note",
            parent=base["Normal"],
            fontName="Times-Italic",
            fontSize=9,
            textColor=MUTED,
            leading=12,
            spaceAfter=2 * mm,
            spaceBefore=1 * mm,
        ),
        "cell": ParagraphStyle(
            "cell",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=8.5,
            textColor=INK,
            leading=11,
        ),
        "cell_b": ParagraphStyle(
            "cell_b",
            parent=base["Normal"],
            fontName="Times-Bold",
            fontSize=8.5,
            textColor=INK,
            leading=11,
        ),
        "cell_w": ParagraphStyle(
            "cell_w",
            parent=base["Normal"],
            fontName="Times-Bold",
            fontSize=8.5,
            textColor=WHITE,
            leading=11,
        ),
        "cell_w_n": ParagraphStyle(
            "cell_w_n",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=8.5,
            textColor=WHITE,
            leading=11,
        ),
        "fig": ParagraphStyle(
            "fig",
            parent=base["Normal"],
            fontName="Times-Bold",
            fontSize=9,
            textColor=INK,
            alignment=TA_CENTER,
            spaceBefore=2 * mm,
            spaceAfter=1 * mm,
        ),
        "footer": ParagraphStyle(
            "footer",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=8,
            textColor=MUTED,
            alignment=TA_CENTER,
        ),
        "box_title": ParagraphStyle(
            "box_title",
            parent=base["Normal"],
            fontName="Times-Bold",
            fontSize=9.5,
            textColor=INK,
            spaceAfter=1 * mm,
        ),
    }
    return s


def P(text, style):
    return Paragraph(text, style)


def table(data, col_widths, header=True, font_size=8.5):
    style_cmds = [
        ("FONTNAME", (0, 0), (-1, -1), "Times-Roman"),
        ("FONTSIZE", (0, 0), (-1, -1), font_size),
        ("TEXTCOLOR", (0, 0), (-1, -1), INK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("GRID", (0, 0), (-1, -1), 0.4, RULE),
        ("BACKGROUND", (0, 0), (-1, -1), WHITE),
    ]
    if header:
        style_cmds += [
            ("BACKGROUND", (0, 0), (-1, 0), HDR_BG),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
        ]
        for i in range(1, len(data)):
            if i % 2 == 0:
                style_cmds.append(("BACKGROUND", (0, i), (-1, i), ALT_BG))
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    t.setStyle(TableStyle(style_cmds))
    return t


def flow_box(rows, col_widths, s):
    """Simple horizontal flow diagram as a table."""
    data = [[P(c, s["cell"]) for c in row] for row in rows]
    t = Table(data, colWidths=col_widths)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), ALT_BG),
                ("BOX", (0, 0), (-1, -1), 0.6, RULE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, RULE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return t


def build():
    s = styles()
    story = []
    usable = A4[0] - 36 * mm

    # Cover / header
    story.append(P("September 2026 · v2.3", s["date"]))
    story.append(P("ANSA McAL Group", s["title"]))
    story.append(P("IT Asset Lifecycle — Factorial IT Implementation", s["subtitle"]))
    story.append(
        P(
            "Client: ANSA McAL Group · ~6,000 employees · 48 operating companies · Caribbean",
            s["meta"],
        )
    )
    story.append(
        P(
            "Platform: Factorial IT · HRIS System of Record: SAP SuccessFactors · Identity: Microsoft 365",
            s["meta"],
        )
    )
    story.append(
        P(
            "Commercial: POC ~500 employees / ~1,000 devices · Ramp to ~10,000 by Jun 2027 · "
            "Kick-off: October 2026 · First invoice: January 2027",
            s["meta"],
        )
    )
    story.append(
        P(
            "POC mandatory (macOS · Windows · iOS · Android BYOD + company-owned) before January 2027 go-live",
            s["meta"],
        )
    )
    story.append(
        P(
            "Professional Services: USD 5,000 fixed — billed once at kick-off (October 2026)",
            s["meta"],
        )
    )

    # 1 PURPOSE
    story.append(P("1. PURPOSE", s["h1"]))
    story.append(
        P(
            "This package defines the delivery approach to migrate IT asset lifecycle operations "
            "(request, approval, procurement, registration, deployment, transfer, recovery, retirement "
            "and disposal) from the current SysAid-centric model onto Factorial IT, with SAP "
            "SuccessFactors remaining the System of Record for people and organisation data.",
            s["body"],
        )
    )
    story.append(
        P(
            "Existing governance intent, mandatory fields, approvals and evidence requirements are "
            "preserved where Factorial IT native capability supports them. Configuration uses native "
            "Factorial IT capability only. Custom development is out of scope. Platform capability "
            "constraints (notably Android corporate Zero-Touch and buyback/acceptance boundaries) are "
            "stated explicitly below so scope matches what can be delivered in 2026–2027.",
            s["body"],
        )
    )

    # 2 SCOPE
    story.append(P("2. SCOPE", s["h1"]))
    scope_rows = [
        [P("Item", s["cell_w"]), P("Detail", s["cell_w"])],
        [
            P("In scope", s["cell_b"]),
            P(
                "ITAM/CMDB, MDM (macOS, Windows, iOS corporate enrolment paths; Android BYOD Work "
                "Profile + company-owned staged provisioning/remote wipe), Joiner/Mover/Leaver (JML) "
                "automation from SuccessFactors, procurement and equipment catalogue, inventory "
                "(including network hardware as accessories), SaaS/license management, asset-related "
                "ticketing, remote assistance, approvals, reporting, audit trail, asset governance.",
                s["cell"],
            ),
        ],
        [
            P("Out of scope", s["cell_b"]),
            P(
                "Payroll; core HR record-keeping; ITIL-process service management (incident/problem "
                "separation, SLA timers and escalation, change management, CMDB impact modelling — "
                "remains in SysAid); network infrastructure redesign; non-IT facility assets; Android "
                "zero-touch automatic enrollment (roadmap item with no committed date); native "
                "employee buyback/staff-offer workflow with Finance approval and payment handling; "
                "signature capture and acceptable-use acknowledgement.",
                s["cell"],
            ),
        ],
        [
            P("In scope (Android)", s["cell_b"]),
            P(
                "Remote lock on all enrolled Android devices; remote wipe on company-owned Android "
                "(console action within offboarding task); BYOD disenrollment removing company data "
                "while leaving personal data untouched. Company-owned handsets enrolled via staged "
                "provisioning flow — not zero-touch.",
                s["cell"],
            ),
        ],
        [P("Sponsor", s["cell_b"]), P("Group CIO", s["cell"])],
        [
            P("Business owner", s["cell_b"]),
            P("Group Head of IT Operations", s["cell"]),
        ],
        [
            P("Duration", s["cell_b"]),
            P(
                "October 2026 kick-off through hypercare exit (POC → Go-live → gradual rollouts → BAU)",
                s["cell"],
            ),
        ],
    ]
    story.append(table(scope_rows, [32 * mm, usable - 32 * mm]))

    story.append(P("2.1 Ticketing", s["h2"]))
    story.append(
        P(
            "ITIL-process service management remains in SysAid. Asset-related requests, approvals and "
            "remediation are worked as tickets in Factorial IT:",
            s["body"],
        )
    )
    story.append(
        P(
            "• Tickets: title, description, priority, due date, assignee, requester (opened on behalf of), tags, child tasks",
            s["bullet"],
        )
    )
    story.append(
        P(
            "• Comments: internal (admins/assignee only) or public",
            s["bullet"],
        )
    )
    story.append(
        P(
            "• Related objects: device, employee, identity, order, shipment or SaaS application",
            s["bullet"],
        )
    )
    story.append(
        P(
            "• Remote assistance: auto-installs on targeted devices; sessions start from the device page "
            "without user codes or passwords; logged for audit",
            s["bullet"],
        )
    )
    story.append(
        P(
            "• Not included: ITIL problem management, SLA timers and escalation ladders, change "
            "management, or CMDB impact modelling.",
            s["bullet"],
        )
    )

    story.append(P("2.2 Out of scope clarifications", s["h2"]))
    clar = [
        [P("Topic", s["cell_w"]), P("Position", s["cell_w"])],
        [
            P("ITIL-process service management", s["cell_b"]),
            P(
                "Incident/problem separation, SLA timers, change management and CMDB impact modelling "
                "remain in SysAid. Factorial IT covers asset-related requests and remediation via tickets "
                "(see §2.1).",
                s["cell"],
            ),
        ],
        [
            P("Network infrastructure redesign", s["cell_b"]),
            P(
                "Permanently excluded. Network hardware may be inventoried as accessories; inventorying "
                "a switch is not designing a network.",
                s["cell"],
            ),
        ],
        [
            P("Non-IT facility assets", s["cell_b"]),
            P(
                "Excluded — no facilities-management semantics (depreciation, space or maintenance management).",
                s["cell"],
            ),
        ],
        [
            P("Android zero-touch enrollment", s["cell_b"]),
            P(
                "Excluded. Company-owned handsets use staged provisioning; zero-touch is a roadmap item "
                "with no committed date.",
                s["cell"],
            ),
        ],
        [
            P("Staff offer / buyback", s["cell_b"]),
            P(
                "No native employee-facing offer, valuation engine, Finance approval chain or payment "
                "handling. Runs as a ticket with tasks; Finance approval outside the platform.",
                s["cell"],
            ),
        ],
        [
            P("Handover acceptance", s["cell_b"]),
            P(
                "No signature capture or acceptable-use acknowledgement. Handover recorded against "
                "onboarding ticket — not a signed acceptance.",
                s["cell"],
            ),
        ],
        [
            P("Disposal / resale geography", s["cell_b"]),
            P(
                "ANSA nominates local disposal vendors; Factorial IT carries the evidence trail.",
                s["cell"],
            ),
        ],
    ]
    story.append(table(clar, [42 * mm, usable - 42 * mm]))

    story.append(P("2.3 Platform capability matrix", s["h2"]))
    story.append(
        P(
            "The current SysAid framework assumes full Zero-Touch and remote wipe across all OS "
            "families, including Android corporate Zero-Touch. This package scopes delivery to what "
            "Factorial IT supports today and through Phase 1.",
            s["body"],
        )
    )
    cap = [
        [
            P("Capability", s["cell_w"]),
            P("macOS", s["cell_w"]),
            P("Windows", s["cell_w"]),
            P("iOS", s["cell_w"]),
            P("Android (Phase 1)", s["cell_w"]),
        ],
        [
            P("Zero-Touch / automatic enrolment", s["cell_b"]),
            P("In scope (Viable / Complete)", s["cell"]),
            P("In scope (Viable / Complete)", s["cell"]),
            P("In scope (Viable / Complete)", s["cell"]),
            P(
                "Out of scope — corporate Zero-Touch (coming soon; no committed date)",
                s["cell"],
            ),
        ],
        [
            P("Android Work Profile (BYOD)", s["cell_b"]),
            P(
                "Not applicable — Work Profile is Android-specific. macOS / Windows / iOS use their own MDM enrolment paths.",
                s["cell"],
            ),
            P("—", s["cell"]),
            P("—", s["cell"]),
            P("In scope — account-driven Work Profile isolation", s["cell"]),
        ],
        [
            P("JML-driven provisioning", s["cell_b"]),
            P("In scope", s["cell"]),
            P("In scope", s["cell"]),
            P("In scope", s["cell"]),
            P(
                "Partial — staged provisioning / Work Profile enrol; zero-touch not relied upon",
                s["cell"],
            ),
        ],
        [
            P("Remote lock / wipe (offboarding)", s["cell_b"]),
            P("In scope", s["cell"]),
            P("In scope", s["cell"]),
            P("In scope", s["cell"]),
            P(
                "Company-owned: full remote wipe in scope (console action). BYOD: disenroll only — no full-device wipe",
                s["cell"],
            ),
        ],
        [
            P("Inventory / visibility", s["cell_b"]),
            P("In scope", s["cell"]),
            P("In scope", s["cell"]),
            P("In scope", s["cell"]),
            P(
                "In scope — Work Profile and company-owned devices visible and managed",
                s["cell"],
            ),
        ],
    ]
    # Merge note for BYOD row visually by spanning - keep simple columns
    story.append(table(cap, [32 * mm, 28 * mm, 28 * mm, 28 * mm, usable - 116 * mm]))
    story.append(
        P(
            "Android corporate provisioning gaps are addressed through BYOD Work Profile enrolment per "
            "Factorial IT's current BYOD capability statement. Corporate Zero-Touch automatic enrollment "
            "is excluded from this programme with no committed delivery date. Company-owned Android remote "
            "wipe is available today as a console action; API-driven wipe automation is not committed in Phase 1.",
            s["body"],
        )
    )

    # 3 AD
    story.append(P("3. ARCHITECTURAL DECISIONS", s["h1"]))
    ads = [
        [P("#", s["cell_w"]), P("Decision", s["cell_w"]), P("Rationale", s["cell_w"])],
        [
            P("AD-01", s["cell_b"]),
            P(
                "SAP SuccessFactors is the sole System of Record for people data.",
                s["cell"],
            ),
            P(
                "No dual maintenance of employee/org data; HR events drive asset actions.",
                s["cell"],
            ),
        ],
        [
            P("AD-02", s["cell_b"]),
            P(
                "Factorial IT is the sole system of record for asset operations.",
                s["cell"],
            ),
            P(
                "One operational surface for ITAM, MDM, procurement, SaaS and evidence.",
                s["cell"],
            ),
        ],
        [
            P("AD-03", s["cell_b"]),
            P(
                "Permissions follow Central / Regional / Local IT, plus HR, Finance and InfoSec.",
                s["cell"],
            ),
            P(
                "Matches ANSA's operating model; least privilege by company and region.",
                s["cell"],
            ),
        ],
        [
            P("AD-04", s["cell_b"]),
            P("Native configuration only — no custom code.", s["cell"]),
            P("Lower TCO and cleaner BAU handover.", s["cell"]),
        ],
        [
            P("AD-05", s["cell_b"]),
            P("Gradual rollout by cohort and geography. No big-bang cutover.", s["cell"]),
            P("Contains risk; allows controlled rollback per cohort.", s["cell"]),
        ],
        [
            P("AD-06", s["cell_b"]),
            P(
                "Two policies: Equipment Policy (entitlement) and Purchasing Policy (spend controls).",
                s["cell"],
            ),
            P(
                'Separates "who gets what" from "who authorises spend".',
                s["cell"],
            ),
        ],
        [
            P("AD-07", s["cell_b"]),
            P(
                "POC on macOS / Windows / iOS / Android BYOD is a hard gate before January 2027 go-live.",
                s["cell"],
            ),
            P(
                "Validates all in-scope MDM paths before scaling beyond the POC cohort.",
                s["cell"],
            ),
        ],
        [
            P("AD-08", s["cell_b"]),
            P(
                "Android Phase 1 = BYOD Work Profile in scope; company-owned remote wipe (console) in "
                "scope; corporate Zero-Touch excluded (no date commitment).",
                s["cell"],
            ),
            P(
                "Scope matches deliverable capability; avoids inventing Android delivery timelines the "
                "platform has not committed.",
                s["cell"],
            ),
        ],
    ]
    story.append(table(ads, [18 * mm, (usable - 18 * mm) * 0.52, (usable - 18 * mm) * 0.48]))

    # 4 Architecture
    story.append(P("4. TARGET ARCHITECTURE", s["h1"]))
    story.append(
        P(
            "Figure 1 — System context (one-way people data; Factorial IT as asset operations hub)",
            s["fig"],
        )
    )
    story.append(
        flow_box(
            [
                [
                    "<b>Employees / Managers</b><br/>Requests · approvals · self-service",
                    "→",
                    "<b>SAP SuccessFactors</b><br/>People · org · cost centre · manager<br/><i>System of Record</i>",
                    "↓ events",
                    "<b>Factorial IT</b><br/>ITAM · MDM · Procurement · SaaS · JML · Evidence",
                ]
            ],
            [34 * mm, 8 * mm, 48 * mm, 16 * mm, usable - 106 * mm],
            s,
        )
    )
    story.append(Spacer(1, 2 * mm))
    story.append(
        flow_box(
            [
                [
                    "<b>MDM</b><br/>macOS · Win · iOS<br/>Android BYOD + Corp (QR)",
                    "<b>Vendors</b><br/>Catalogue / PO",
                    "<b>SaaS</b><br/>Licenses",
                    "←",
                    "<b>Microsoft 365</b><br/>SSO · MFA · groups → RBAC",
                ]
            ],
            [48 * mm, 32 * mm, 28 * mm, 8 * mm, usable - 116 * mm],
            s,
        )
    )
    story.append(
        P(
            "Figure 2 — Joiner / Mover / Leaver flow. Corporate devices on macOS / Windows / iOS receive "
            "automated wipe/lock. Android: remote lock on all enrolled devices; company-owned remote wipe "
            "(console) or BYOD disenrollment on termination.",
            s["note"],
        )
    )
    story.append(
        flow_box(
            [
                [
                    "<b>1. SF event</b><br/>Hire · Transfer · Termination",
                    "→",
                    "<b>2. Factorial IT</b><br/>Automation rule fires",
                    "→",
                    "<b>3. Action</b><br/>Onboard / reassign / recover<br/>+ Android wipe / disenroll",
                    "→",
                    "<b>4. Evidence</b><br/>Logged · auditable",
                ]
            ],
            [32 * mm, 7 * mm, 32 * mm, 7 * mm, 48 * mm, 7 * mm, usable - 133 * mm],
            s,
        )
    )

    # 5 Phases
    story.append(P("5. DELIVERY PHASES", s["h1"]))
    phases = [
        [
            P("Phase", s["cell_w"]),
            P("When", s["cell_w"]),
            P("Objective", s["cell_w"]),
            P("Exit", s["cell_w"]),
        ],
        [
            P("0 — Planning", s["cell_b"]),
            P("Early Oct 2026", s["cell"]),
            P("Charter, Steering, RAID, comms; lock Android BYOD boundary", s["cell"]),
            P("Charter signed", s["cell"]),
        ],
        [
            P("1 — Discovery", s["cell_b"]),
            P("Oct 2026", s["cell"]),
            P(
                "Nine workshops (condensed calendar); signed inputs; OS estate split (corp vs BYOD Android)",
                s["cell"],
            ),
            P("Workshop outputs signed", s["cell"]),
        ],
        [
            P("2 — Design + Configure", s["cell_b"]),
            P("Oct–Nov 2026", s["cell"]),
            P(
                "Solution blueprint; RBAC, catalogue, workflows, MDM paths including Android Work Profile",
                s["cell"],
            ),
            P("Design approved", s["cell"]),
        ],
        [
            P("3 — SF Integration + POC", s["cell_b"]),
            P("Nov–Dec 2026", s["cell"]),
            P(
                "Employee sync + JML events in staging; prove enrolment, JML, evidence on all four OS paths",
                s["cell"],
            ),
            P("POC criteria met", s["cell"]),
        ],
        [
            P("Gate", s["cell_b"]),
            P("Dec 2026", s["cell"]),
            P("Steering POC sign-off", s["cell"]),
            P("Mandatory before go-live", s["cell"]),
        ],
        [
            P("4 — Official Go-live", s["cell_b"]),
            P("Jan 2027", s["cell"]),
            P(
                "Production cutover for POC cohort (~500 employees / ~1,000 devices)",
                s["cell"],
            ),
            P("POC cohort live", s["cell"]),
        ],
        [
            P("5 — Gradual Rollouts", s["cell_b"]),
            P("Jan–Jun 2027", s["cell"]),
            P("Add cohorts by geography until ~10,000 devices", s["cell"]),
            P("Scale target reached", s["cell"]),
        ],
        [
            P("6 — Hypercare & BAU", s["cell_b"]),
            P("From Jun 2027", s["cell"]),
            P(
                "Stabilise; runbook handover; SysAid asset module retirement per cohort",
                s["cell"],
            ),
            P("Operational acceptance", s["cell"]),
        ],
    ]
    story.append(table(phases, [38 * mm, 28 * mm, usable - 90 * mm, 24 * mm]))

    story.append(P("5.1 Discovery workshops", s["h2"]))
    ws = [
        [P("#", s["cell_w"]), P("Workshop", s["cell_w"]), P("Output", s["cell_w"])],
        [
            P("1", s["cell"]),
            P("Asset Governance", s["cell_b"]),
            P(
                "Lifecycle states, mandatory attributes, evidence points; local disposal vendor nomination (Caribbean)",
                s["cell"],
            ),
        ],
        [
            P("2", s["cell"]),
            P("Procurement & Catalogue", s["cell_b"]),
            P("Equipment Policy, Purchasing Policy, country catalogues", s["cell"]),
        ],
        [
            P("3", s["cell"]),
            P("Joiner / Mover / Leaver", s["cell_b"]),
            P("JML design and event-to-automation map", s["cell"]),
        ],
        [
            P("4", s["cell"]),
            P("Security & Compliance", s["cell_b"]),
            P("MDM baseline, RBAC matrix, retention rules", s["cell"]),
        ],
        [
            P("5", s["cell"]),
            P("Identity & SSO", s["cell_b"]),
            P("IdP, SSO and SCIM decisions", s["cell"]),
        ],
        [
            P("6", s["cell"]),
            P("MDM Operations", s["cell_b"]),
            P(
                "Device groups, enrolment paths for macOS / Windows / iOS; Android Enterprise binding "
                "via Microsoft 365; BYOD Work Profile and company-owned QR enrolment",
                s["cell"],
            ),
        ],
        [
            P("7", s["cell"]),
            P("SaaS & Licenses", s["cell_b"]),
            P("SaaS register, approval and reclamation rules", s["cell"]),
        ],
        [
            P("8", s["cell"]),
            P("Reporting", s["cell_b"]),
            P("KPI list and dashboard definitions", s["cell"]),
        ],
        [
            P("9", s["cell"]),
            P("SuccessFactors Integration", s["cell_b"]),
            P("Field map, event contract, error handling", s["cell"]),
        ],
    ]
    story.append(table(ws, [12 * mm, 48 * mm, usable - 60 * mm]))

    # 6 Calendar
    story.append(P("6. CALENDAR ROADMAP (BY QUARTER)", s["h1"]))
    story.append(
        P(
            "Figure 3 — Delivery vs. commercial calendar. No platform subscription until January 2027. "
            "Professional Services billed once at kick-off (USD 5,000). POC sign-off gates go-live.",
            s["note"],
        )
    )
    story.append(
        P(
            "<b>Platform complimentary (Oct–Dec 2026)</b> · <b>PS USD 5,000 once (Oct 2026)</b> · "
            "<b>Subscription billing starts (Jan 2027)</b>",
            s["body_left"],
        )
    )
    cal = [
        [
            P("Quarter", s["cell_w"]),
            P("Month", s["cell_w"]),
            P("Delivery / commercial focus", s["cell_w"]),
        ],
        [
            P("Q4 2026 · COMPLIMENTARY", s["cell_b"]),
            P("October ★", s["cell"]),
            P(
                "Kick-off · Planning + Discovery · <b>PS invoice USD 5,000 (full amount)</b>",
                s["cell"],
            ),
        ],
        [
            P("", s["cell"]),
            P("November", s["cell"]),
            P("Configure + SF integration · POC validation", s["cell"]),
        ],
        [
            P("", s["cell"]),
            P("December", s["cell"]),
            P("POC review · Steering sign-off · Go-live readiness", s["cell"]),
        ],
        [
            P("Q1 2027 · BILLABLE", s["cell_b"]),
            P("January ★", s["cell"]),
            P("First platform invoice · Official go-live · POC cohort live", s["cell"]),
        ],
        [
            P("", s["cell"]),
            P("February", s["cell"]),
            P("Rollout A — Trinidad", s["cell"]),
        ],
        [
            P("", s["cell"]),
            P("March", s["cell"]),
            P("Rollout B — Barbados / Guyana", s["cell"]),
        ],
        [
            P("Q2 2027 · BILLABLE", s["cell_b"]),
            P("April–May", s["cell"]),
            P("Rollouts C–D", s["cell"]),
        ],
        [
            P("", s["cell"]),
            P("June", s["cell"]),
            P("~10,000 devices target · Hypercare start", s["cell"]),
        ],
        [
            P("Q3 2027+ · BILLABLE", s["cell_b"]),
            P("July+", s["cell"]),
            P("BAU steady state · SysAid asset retired per cohort · Quarterly true-up", s["cell"]),
        ],
    ]
    story.append(table(cal, [48 * mm, 28 * mm, usable - 76 * mm]))

    story.append(P("6.1 Rollout sequence", s["h2"]))
    story.append(
        P(
            "Figure 4 — No big-bang. POC Steering sign-off is required before January 2027 go-live. "
            "Each arrow is a Go / No-Go gate.",
            s["note"],
        )
    )
    story.append(
        flow_box(
            [
                [
                    "<b>POC</b><br/>~500 emp · ~1k devices<br/>Oct–Dec 2026<br/>All 4 OS paths",
                    "→",
                    "<b>Go-live</b><br/>Jan 2027<br/>POC cohort",
                    "→",
                    "<b>Rollout A</b><br/>Trinidad<br/>Jan–Feb 2027",
                    "→",
                    "<b>Rollout B</b><br/>Barbados + Guyana<br/>Feb–Mar 2027",
                    "→",
                    "<b>C–D</b><br/>Remaining<br/>Apr–Jun 2027<br/>→ 10k devices",
                ]
            ],
            [34 * mm, 6 * mm, 24 * mm, 6 * mm, 28 * mm, 6 * mm, 34 * mm, 6 * mm, usable - 144 * mm],
            s,
        )
    )
    story.append(Spacer(1, 2 * mm))
    gates = [
        [
            P("Gate", s["cell_w"]),
            P("Entry", s["cell_w"]),
            P("Rollback / boundary", s["cell_w"]),
        ],
        [
            P("POC", s["cell_b"]),
            P(
                "Design approved; sample fleet on macOS / Windows / iOS / Android BYOD",
                s["cell"],
            ),
            P("No go-live without Steering POC sign-off", s["cell"]),
        ],
        [
            P("Go-live", s["cell_b"]),
            P("POC signed; MDM baseline signed; SF sync stable", s["cell"]),
            P("SysAid shadow mode; JML kill-switch", s["cell"]),
        ],
        [
            P("Rollout A", s["cell_b"]),
            P("Go-live exit met", s["cell"]),
            P("Per-company revert to SysAid", s["cell"]),
        ],
        [
            P("Rollouts B–D", s["cell_b"]),
            P("Prior cohort exit", s["cell"]),
            P("Per-cohort Go / No-Go; quarterly true-up aligns cost to devices", s["cell"]),
        ],
    ]
    story.append(table(gates, [28 * mm, (usable - 28 * mm) * 0.5, (usable - 28 * mm) * 0.5]))

    # 7 Security (was 11) — risks table removed
    story.append(P("7. SECURITY & RACI", s["h1"]))
    story.append(
        P(
            "• Admin access via enterprise IdP (Microsoft 365) with MFA; roles scoped by company / region.",
            s["bullet"],
        )
    )
    story.append(
        P(
            "• Internal Audit: read-only. Break-glass accounts: named, MFA-hardened, periodically reviewed.",
            s["bullet"],
        )
    )
    story.append(
        P(
            "• Every status change, approval and evidence upload is logged (actor, timestamp, before/after).",
            s["bullet"],
        )
    )
    story.append(
        P(
            "• MDM baseline for macOS, Windows, iOS and Android BYOD signed by InfoSec before POC sign-off.",
            s["bullet"],
        )
    )
    story.append(
        P(
            "• Steering monthly; Working Group weekly. POC sign-off is a hard gate before January 2027 go-live.",
            s["bullet"],
        )
    )
    story.append(Spacer(1, 2 * mm))
    raci = [
        [
            P("Activity", s["cell_w"]),
            P("A", s["cell_w"]),
            P("R", s["cell_w"]),
            P("C / I", s["cell_w"]),
        ],
        [
            P("Programme approval", s["cell"]),
            P("CIO", s["cell"]),
            P("PMO", s["cell"]),
            P("CISO, Finance, HR, Procurement", s["cell"]),
        ],
        [
            P("SAP SF integration", s["cell"]),
            P("PMO", s["cell"]),
            P("Solution Architect + HR / SF", s["cell"]),
            P("InfoSec, Central IT", s["cell"]),
        ],
        [
            P("MDM baseline", s["cell"]),
            P("CISO", s["cell"]),
            P("Solution Architect + Central IT", s["cell"]),
            P("Regional IT", s["cell"]),
        ],
        [
            P("Rollout execution", s["cell"]),
            P("PMO", s["cell"]),
            P("Central / Regional / Local IT", s["cell"]),
            P("HR, InfoSec, Procurement", s["cell"]),
        ],
        [
            P("BAU operations", s["cell"]),
            P("CIO", s["cell"]),
            P("Central / Regional / Local IT", s["cell"]),
            P("HR, InfoSec, Finance, Procurement", s["cell"]),
        ],
    ]
    story.append(table(raci, [42 * mm, 22 * mm, 55 * mm, usable - 119 * mm]))

    # 8 Deliverables — includes platform / PS inclusion (once, not redundant with §9)
    story.append(P("8. DELIVERABLES", s["h1"]))
    story.append(
        P(
            "Project deliverables below. Platform inclusions and Professional Services inclusions are "
            "listed here once (they are not repeated in §9 Investment).",
            s["body"],
        )
    )
    dels = [
        [
            P("#", s["cell_w"]),
            P("Deliverable", s["cell_w"]),
            P("Phase", s["cell_w"]),
            P("Sign-off", s["cell_w"]),
        ],
        [
            P("D01", s["cell"]),
            P("Statement of Work / this package", s["cell"]),
            P("0", s["cell"]),
            P("CIO", s["cell"]),
        ],
        [
            P("D02", s["cell"]),
            P("Project Charter & Governance", s["cell"]),
            P("0", s["cell"]),
            P("Steering", s["cell"]),
        ],
        [
            P("D03", s["cell"]),
            P("Communication Plan", s["cell"]),
            P("0", s["cell"]),
            P("PMO", s["cell"]),
        ],
        [
            P("D04", s["cell"]),
            P("Discovery workshop outputs", s["cell"]),
            P("1", s["cell"]),
            P("Working Group", s["cell"]),
        ],
        [
            P("D05–D06", s["cell"]),
            P("Equipment Policy · Purchasing Policy", s["cell"]),
            P("1–2", s["cell"]),
            P("CIO / CFO delegate", s["cell"]),
        ],
        [
            P("D07–D09", s["cell"]),
            P("Solution Design · SF Integration · Security Baseline", s["cell"]),
            P("2 / 3", s["cell"]),
            P("Steering / HR / CISO", s["cell"]),
        ],
        [
            P("D10–D11", s["cell"]),
            P("Target Operating Model · Configuration Runbook", s["cell"]),
            P("2–3", s["cell"]),
            P("CIO / Central IT", s["cell"]),
        ],
        [
            P("D12", s["cell"]),
            P("POC Sign-off Pack", s["cell"]),
            P("3", s["cell"]),
            P("Steering", s["cell"]),
        ],
        [
            P("D13–D14", s["cell"]),
            P("Test / Rollout / Hypercare packs", s["cell"]),
            P("4–6", s["cell"]),
            P("Business leads / Steering / CIO", s["cell"]),
        ],
        [
            P("D15", s["cell"]),
            P("Risk Register & RACI (live)", s["cell"]),
            P("0–6", s["cell"]),
            P("Steering", s["cell"]),
        ],
    ]
    story.append(table(dels, [22 * mm, usable - 70 * mm, 22 * mm, 26 * mm]))
    story.append(Spacer(1, 3 * mm))

    # Inclusion boxes side by side
    left_items = [
        "ITAM / CMDB",
        "MDM connectors (macOS, Windows, iOS, Android BYOD + company-owned wipe)",
        "Asset-related ticketing &amp; remote assistance",
        "JML automations",
        "Procurement / catalogue",
        "SaaS visibility",
        "Approvals &amp; audit trail",
    ]
    right_items = [
        "Phases 0–3 delivery (POC scope)",
        "9 Discovery workshops",
        "SF integration design &amp; build support",
        "POC validation and go-live readiness",
        "Rollout runbooks &amp; training foundation",
    ]
    left_html = "<b>Included in platform</b><br/>" + "<br/>".join(f"• {x}" for x in left_items)
    right_html = (
        "<b>Included in Professional Services (USD 5,000)</b><br/>"
        + "<br/>".join(f"• {x}" for x in right_items)
    )
    incl = Table(
        [[P(left_html, s["cell"]), P(right_html, s["cell"])]],
        colWidths=[usable * 0.5, usable * 0.5],
    )
    incl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.6, RULE),
                ("LINEBEFORE", (1, 0), (1, 0), 0.4, RULE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(KeepTogether([incl]))

    # 9 Investment
    story.append(P("9. INVESTMENT", s["h1"]))
    story.append(
        P(
            "Commercial schedule · All figures in USD",
            s["note"],
        )
    )
    story.append(
        P(
            "All commercial figures in this section are in United States dollars (USD). Platform list "
            "price: USD 10 per managed device / month. POC assumption: ~1,000 managed devices, ramping "
            "to ~10,000 by June 2027. Implementation (Professional Services) for this programme: "
            "<b>USD 5,000 fixed</b> (Phases 0–3 POC scope), billed <b>once at kick-off</b>.",
            s["body"],
        )
    )
    story.append(
        P(
            "Kick-off in October 2026. Platform complimentary Oct–Dec 2026 (no subscription charge). "
            "Implementation paid in <b>one instalment of USD 5,000 in October 2026</b>. First platform "
            "invoice January 2027 at USD 6 per managed device per month, with quarterly true-up as devices ramp.",
            s["body"],
        )
    )

    story.append(P("Implementation fee", s["h2"]))
    fee = [
        [P("Item", s["cell_w"]), P("Amount", s["cell_w"])],
        [
            P("Professional Services — Phases 0–3 POC scope (fixed)", s["cell"]),
            P("USD 5,000", s["cell_b"]),
        ],
        [
            P("Payment plan (October 2026 kick-off)", s["cell"]),
            P("1 × USD 5,000 (full amount at once)", s["cell_b"]),
        ],
    ]
    story.append(table(fee, [usable * 0.7, usable * 0.3]))

    story.append(
        P("Figure 5 — Commercial timeline (USD · October start)", s["fig"])
    )
    story.append(
        flow_box(
            [
                [
                    "<b>Oct</b><br/>Kick-off<br/>Platform USD 0<br/><b>PS USD 5,000</b>",
                    "→",
                    "<b>Nov</b><br/>Configure + POC<br/>Platform USD 0<br/>PS —",
                    "→",
                    "<b>Dec</b><br/>POC sign-off<br/>Platform USD 0<br/>PS —",
                    "→",
                    "<b>Jan ★</b><br/>First platform invoice<br/>USD 6 × enrolled devices<br/>ex. USD 6,000 @ 1k",
                ]
            ],
            [40 * mm, 8 * mm, 40 * mm, 8 * mm, 36 * mm, 8 * mm, usable - 140 * mm],
            s,
        )
    )

    story.append(P("Commercial terms", s["h2"]))
    terms = [
        [P("Item", s["cell_w"]), P("List", s["cell_w"]), P("ANSA offer", s["cell_w"])],
        [
            P("Platform — per managed device / month", s["cell"]),
            P("USD 10", s["cell"]),
            P("USD 6 per device for the initial 12 billable months", s["cell"]),
        ],
        [
            P("Device assumption", s["cell"]),
            P("—", s["cell"]),
            P(
                "POC ~1,000 devices; ramp to ~10,000 by Jun 2027 (quarterly true-up)",
                s["cell"],
            ),
        ],
        [
            P("Kick-off target", s["cell"]),
            P("—", s["cell"]),
            P("October 2026 (order form signed on or before 31 Oct 2026)", s["cell"]),
        ],
        [
            P("Complimentary platform", s["cell"]),
            P("—", s["cell"]),
            P("1 Oct – 31 Dec 2026 (3 months). No platform subscription.", s["cell"]),
        ],
        [
            P("First billable platform month", s["cell"]),
            P("—", s["cell"]),
            P(
                "January 2027 → USD 6 × enrolled devices (e.g. ~USD 6,000 at 1,000 devices; true-up as ramp progresses)",
                s["cell"],
            ),
        ],
        [
            P("Minimum subscription term", s["cell"]),
            P("—", s["cell"]),
            P("12 billable months (Jan 2027 – Dec 2027)", s["cell"]),
        ],
        [
            P("Professional Services", s["cell"]),
            P("—", s["cell"]),
            P("<b>USD 5,000 once at kick-off (October 2026)</b>", s["cell"]),
        ],
        [
            P("Year 2+ renewal", s["cell"]),
            P("—", s["cell"]),
            P("Subject to renewal negotiation", s["cell"]),
        ],
    ]
    story.append(table(terms, [52 * mm, 22 * mm, usable - 74 * mm]))

    story.append(P("What ANSA pays when", s["h2"]))
    cash = [
        [
            P("Month", s["cell_w"]),
            P("Platform (ramp)", s["cell_w"]),
            P("Professional Services", s["cell_w"]),
            P("Cash out (that month)", s["cell_w"]),
        ],
        [
            P("Oct 2026", s["cell"]),
            P("USD 0", s["cell"]),
            P("USD 5,000 (full)", s["cell_b"]),
            P("USD 5,000", s["cell_b"]),
        ],
        [
            P("Nov 2026", s["cell"]),
            P("USD 0", s["cell"]),
            P("—", s["cell"]),
            P("USD 0", s["cell"]),
        ],
        [
            P("Dec 2026", s["cell"]),
            P("USD 0", s["cell"]),
            P("—", s["cell"]),
            P("USD 0", s["cell"]),
        ],
        [
            P("Jan 2027", s["cell"]),
            P("~USD 6,000 (ex. 1,000 devices @ USD 6)", s["cell"]),
            P("—", s["cell"]),
            P("~USD 6,000", s["cell"]),
        ],
        [
            P("Feb–Jun 2027", s["cell"]),
            P("USD 6 × enrolled devices (ramp to 10k)", s["cell"]),
            P("—", s["cell"]),
            P("Per true-up schedule", s["cell"]),
        ],
        [
            P("Jul 2027+", s["cell"]),
            P("USD 6 × enrolled devices", s["cell"]),
            P("—", s["cell"]),
            P("Quarterly true-up", s["cell"]),
        ],
    ]
    story.append(table(cash, [28 * mm, 58 * mm, 42 * mm, usable - 128 * mm]))
    story.append(
        P(
            "During Oct–Dec the client has zero platform subscription — only the single implementation "
            "payment (USD 5,000 in October). From January 2027, platform billing applies at USD 6 per "
            "enrolled device, with quarterly true-up as the ramp progresses.",
            s["body"],
        )
    )

    story.append(P("Year-1 snapshot (ramp to 10,000 devices · all USD)", s["h2"]))
    y1 = [
        [P("Line", s["cell_w"]), P("Amount", s["cell_w"])],
        [
            P("Platform Oct–Dec 2026 (complimentary)", s["cell"]),
            P("USD 0", s["cell"]),
        ],
        [
            P("Platform Jan–Dec 2027 @ USD 6 (ramp to 10k)", s["cell"]),
            P("~USD 549,000 (indicative ramp)", s["cell"]),
        ],
        [
            P("Implementation (USD 5,000 once at kick-off)", s["cell"]),
            P("USD 5,000", s["cell"]),
        ],
        [
            P("Total cash Year 1 (platform + PS)", s["cell_b"]),
            P("~USD 554,000", s["cell_b"]),
        ],
    ]
    story.append(table(y1, [usable * 0.7, usable * 0.3]))

    story.append(P("Commercial conditions", s["h2"]))
    story.append(
        P(
            "1. Order form / MSA signed on or before 31 October 2026.",
            s["bullet"],
        )
    )
    story.append(
        P(
            "2. Minimum term of 12 billable months from January 2027.",
            s["bullet"],
        )
    )
    story.append(
        P(
            "3. POC device floor: ~1,000; ramp target ~10,000 by Jun 2027; quarterly true-up to actual enrolled devices.",
            s["bullet"],
        )
    )
    story.append(
        P(
            "4. Oct–Dec complimentary period applies to platform subscription only. The Professional "
            "Services fee (USD 5,000) is due once at kick-off in October 2026.",
            s["bullet"],
        )
    )
    story.append(
        P(
            "5. If the engagement is cancelled before Dec 2026 POC sign-off, the Professional Services "
            "fee remains due for work already delivered; unused complimentary months are not convertible to cash.",
            s["bullet"],
        )
    )

    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont("Times-Roman", 8)
        canvas.setFillColor(MUTED)
        canvas.drawCentredString(
            A4[0] / 2,
            12 * mm,
            f"ANSA McAL Group · Factorial IT Implementation Package v2.3 · Page {doc.page}",
        )
        canvas.restoreState()

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=14 * mm,
        bottomMargin=18 * mm,
        title="ANSA McAL Group — Factorial IT Implementation Package v2.3",
        author="Factorial",
    )
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"Wrote {OUT}")
    return OUT


if __name__ == "__main__":
    build()
