#!/usr/bin/env python3
"""ANSA Client Package v3.1 — lean Client_v3 content + v2.2 organogram design."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Flowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUTS = [
    Path(r"c:\Users\victo\Desktop") / "ANSA_Client_Package_v3.1.pdf",
    Path(r"c:\Users\victo\Downloads") / "ANSA_Client_Package_v3.1.pdf",
    Path(r"c:\Users\victo\Documents\Projetos Random\Ultimate_Collector_Limpo")
    / "ANSA_Client_Package_v3.1.pdf",
]

INK = colors.HexColor("#111111")
MUTED = colors.HexColor("#555555")
RULE = colors.HexColor("#111111")
HDR = colors.HexColor("#111111")
ALT = colors.HexColor("#F0F0F0")
LIGHT = colors.HexColor("#F7F7F7")
WHITE = colors.white
ARROW = colors.HexColor("#888888")


def S():
    b = getSampleStyleSheet()
    return {
        "cover_brand": ParagraphStyle(
            "cover_brand",
            parent=b["Normal"],
            fontName="Times-Bold",
            fontSize=22,
            textColor=INK,
            alignment=TA_CENTER,
            spaceAfter=2 * mm,
            leading=26,
        ),
        "cover_title": ParagraphStyle(
            "cover_title",
            parent=b["Normal"],
            fontName="Times-Bold",
            fontSize=16,
            textColor=INK,
            alignment=TA_CENTER,
            spaceAfter=4 * mm,
            leading=20,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub",
            parent=b["Normal"],
            fontName="Times-Italic",
            fontSize=10.5,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=8 * mm,
        ),
        "meta": ParagraphStyle(
            "meta",
            parent=b["Normal"],
            fontName="Times-Bold",
            fontSize=10.5,
            textColor=INK,
            alignment=TA_CENTER,
            leading=14,
            spaceAfter=2 * mm,
        ),
        "meta_n": ParagraphStyle(
            "meta_n",
            parent=b["Normal"],
            fontName="Times-Roman",
            fontSize=10,
            textColor=INK,
            alignment=TA_CENTER,
            leading=13,
            spaceAfter=2 * mm,
        ),
        "note": ParagraphStyle(
            "note",
            parent=b["Normal"],
            fontName="Times-Italic",
            fontSize=9,
            textColor=MUTED,
            alignment=TA_CENTER,
            leading=12,
            spaceBefore=3 * mm,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=b["Normal"],
            fontName="Times-Bold",
            fontSize=13,
            textColor=INK,
            spaceBefore=3 * mm,
            spaceAfter=2.5 * mm,
            leading=16,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=b["Normal"],
            fontName="Times-Bold",
            fontSize=10.5,
            textColor=INK,
            spaceBefore=2.5 * mm,
            spaceAfter=1.5 * mm,
        ),
        "body": ParagraphStyle(
            "body",
            parent=b["Normal"],
            fontName="Times-Roman",
            fontSize=9.5,
            textColor=INK,
            leading=12.5,
            alignment=TA_JUSTIFY,
            spaceAfter=2 * mm,
        ),
        "cell": ParagraphStyle(
            "cell",
            parent=b["Normal"],
            fontName="Times-Roman",
            fontSize=8.5,
            textColor=INK,
            leading=11,
        ),
        "cell_b": ParagraphStyle(
            "cell_b",
            parent=b["Normal"],
            fontName="Times-Bold",
            fontSize=8.5,
            textColor=INK,
            leading=11,
        ),
        "cell_w": ParagraphStyle(
            "cell_w",
            parent=b["Normal"],
            fontName="Times-Bold",
            fontSize=8.5,
            textColor=WHITE,
            leading=11,
            alignment=TA_CENTER,
        ),
        "cell_c": ParagraphStyle(
            "cell_c",
            parent=b["Normal"],
            fontName="Times-Roman",
            fontSize=8,
            textColor=INK,
            leading=10.5,
            alignment=TA_CENTER,
        ),
        "cell_cb": ParagraphStyle(
            "cell_cb",
            parent=b["Normal"],
            fontName="Times-Bold",
            fontSize=8.5,
            textColor=INK,
            leading=11,
            alignment=TA_CENTER,
        ),
        "fig": ParagraphStyle(
            "fig",
            parent=b["Normal"],
            fontName="Times-Bold",
            fontSize=9,
            textColor=INK,
            alignment=TA_LEFT,
            spaceBefore=1 * mm,
            spaceAfter=1.5 * mm,
        ),
        "tiny": ParagraphStyle(
            "tiny",
            parent=b["Normal"],
            fontName="Times-Italic",
            fontSize=8.5,
            textColor=MUTED,
            leading=11,
            spaceAfter=1.5 * mm,
        ),
        "footer": ParagraphStyle(
            "footer",
            parent=b["Normal"],
            fontName="Times-Roman",
            fontSize=8,
            textColor=MUTED,
        ),
    }


def P(t, st):
    return Paragraph(t, st)


class HubBox(Flowable):
    """Rounded-ish filled box used as organogram node."""

    def __init__(self, w, h, title, lines, fill=HDR, text=WHITE, border=RULE):
        Flowable.__init__(self)
        self.w, self.h = w, h
        self.title, self.lines = title, lines
        self.fill, self.text, self.border = fill, text, border

    def wrap(self, *a):
        return self.w, self.h

    def draw(self):
        c = self.canv
        c.setFillColor(self.fill)
        c.setStrokeColor(self.border)
        c.setLineWidth(0.8)
        c.roundRect(0, 0, self.w, self.h, 3, fill=1, stroke=1)
        c.setFillColor(self.text)
        c.setFont("Times-Bold", 9)
        c.drawCentredString(self.w / 2, self.h - 12, self.title)
        c.setFont("Times-Roman", 7.5)
        y = self.h - 24
        for line in self.lines:
            c.drawCentredString(self.w / 2, y, line)
            y -= 10


def tbl(data, widths, header=True):
    cmds = [
        ("FONTNAME", (0, 0), (-1, -1), "Times-Roman"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("TEXTCOLOR", (0, 0), (-1, -1), INK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BOX", (0, 0), (-1, -1), 0.7, RULE),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, RULE),
        ("BACKGROUND", (0, 0), (-1, -1), WHITE),
    ]
    if header:
        cmds += [
            ("BACKGROUND", (0, 0), (-1, 0), HDR),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
        ]
        for i in range(1, len(data)):
            if i % 2 == 0:
                cmds.append(("BACKGROUND", (0, i), (-1, i), ALT))
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    t.setStyle(TableStyle(cmds))
    return t


def callout(text, s, width):
    inner = P(text, s["cell"])
    t = Table([[inner]], colWidths=[width])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), ALT),
                ("BOX", (0, 0), (-1, -1), 0.6, RULE),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return t


def flow_row(cells, widths, s, dark_idx=None):
    """Horizontal organogram row: list of (title, subtitle) or '→'."""
    row = []
    for i, cell in enumerate(cells):
        if cell == "→":
            row.append(P('<font color="#888888" size="12"><b>→</b></font>', s["cell_c"]))
        else:
            title, sub = cell
            dark = dark_idx is not None and i == dark_idx
            st_t = s["cell_w"] if dark else s["cell_cb"]
            st_s = (
                ParagraphStyle(
                    f"subw{i}",
                    parent=s["cell_c"],
                    textColor=WHITE if dark else INK,
                    fontSize=7.5,
                )
            )
            html = f"<b>{title}</b><br/>{sub}"
            row.append(P(html, st_t if dark else s["cell_c"]))
    data = [row]
    t = Table(data, colWidths=widths)
    cmds = [
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    for i, cell in enumerate(cells):
        if cell == "→":
            continue
        dark = dark_idx is not None and i == dark_idx
        cmds.append(("BACKGROUND", (i, 0), (i, 0), HDR if dark else ALT))
        cmds.append(("BOX", (i, 0), (i, 0), 0.7, RULE))
        if dark:
            cmds.append(("TEXTCOLOR", (i, 0), (i, 0), WHITE))
    t.setStyle(TableStyle(cmds))
    return t


def architecture_diagram(s, usable):
    """Figure 1 style organogram."""
    # Top row: Employees | SF | Factorial hub
    top = Table(
        [
            [
                P(
                    "<b>Employees / Managers</b><br/>Requests · approvals · self-service",
                    s["cell_c"],
                ),
                P('<font color="#888888" size="14"><b>→</b></font>', s["cell_c"]),
                P(
                    "<b>SAP SuccessFactors</b><br/>People · org · cost centre · manager<br/><i>System of Record</i>",
                    s["cell_c"],
                ),
                P('<font color="#888888" size="11"><b>↓ events / sync</b></font>', s["cell_c"]),
                P(
                    "<font color='white'><b>Factorial IT</b><br/>ITAM · MDM · Procurement<br/>SaaS · JML · Evidence</font>",
                    s["cell_w"],
                ),
            ]
        ],
        colWidths=[34 * mm, 8 * mm, 48 * mm, 22 * mm, usable - 112 * mm],
    )
    top.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), ALT),
                ("BACKGROUND", (2, 0), (2, 0), WHITE),
                ("BACKGROUND", (4, 0), (4, 0), HDR),
                ("BOX", (0, 0), (0, 0), 0.7, RULE),
                ("BOX", (2, 0), (2, 0), 0.7, RULE),
                ("BOX", (4, 0), (4, 0), 0.8, RULE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )

    bot = Table(
        [
            [
                P("<b>MDM</b><br/>macOS · Win · iOS", s["cell_c"]),
                P("<b>Android</b><br/>BYOD + Corp (QR)", s["cell_c"]),
                P("<b>Vendors</b><br/>Catalogue / PO", s["cell_c"]),
                P("<b>SaaS</b><br/>Licenses", s["cell_c"]),
                P('<font color="#888888" size="12"><b>←</b></font>', s["cell_c"]),
                P(
                    "<b>Microsoft 365</b><br/>SSO · MFA · groups → RBAC",
                    s["cell_c"],
                ),
            ]
        ],
        colWidths=[28 * mm, 32 * mm, 28 * mm, 24 * mm, 8 * mm, usable - 120 * mm],
    )
    bot.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (3, 0), ALT),
                ("BACKGROUND", (5, 0), (5, 0), ALT),
                ("BOX", (0, 0), (0, 0), 0.7, RULE),
                ("BOX", (1, 0), (1, 0), 0.7, RULE),
                ("BOX", (2, 0), (2, 0), 0.7, RULE),
                ("BOX", (3, 0), (3, 0), 0.7, RULE),
                ("BOX", (5, 0), (5, 0), 0.7, RULE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    wrap = Table(
        [[top], [P('<font color="#888888" size="10"><b>↓</b></font>', s["cell_c"])], [bot]],
        colWidths=[usable],
    )
    wrap.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 1.0, RULE),
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("ALIGN", (0, 1), (0, 1), "CENTER"),
            ]
        )
    )
    return wrap


def build():
    s = S()
    story = []
    usable = A4[0] - 32 * mm

    # —— COVER ——
    story.append(Spacer(1, 28 * mm))
    story.append(P("ANSA McAL Group", s["cover_brand"]))
    story.append(P("Factorial IT Implementation Package", s["cover_title"]))
    story.append(Spacer(1, 6 * mm))
    story.append(P("~6,000 employees · 48 operating companies · Caribbean", s["meta"]))
    story.append(P("Systems: Factorial IT · SAP SuccessFactors · Microsoft 365", s["meta_n"]))
    story.append(Spacer(1, 4 * mm))
    story.append(
        callout(
            "<b>Commercial:</b> POC ~500 employees / ~1,000 devices · target ~10,000 devices "
            "by June 2027 · kick-off October 2026 · Professional Services <b>USD 5,000 once</b> "
            "at kick-off · platform billing from January 2027",
            s,
            usable,
        )
    )

    # —— 1 SCOPE ——
    story.append(P("1. Scope", s["h1"]))
    story.append(
        P(
            "Factorial IT will operate ANSA McAL’s IT asset lifecycle: request, approval, "
            "procurement, registration, deployment, transfer, recovery, retirement and disposal. "
            "SAP SuccessFactors remains the system of record for people and organisation data.",
            s["body"],
        )
    )
    scope = [
        [P("In scope", s["cell_w"]), P("Out of scope", s["cell_w"])],
        [
            P(
                "ITAM / inventory; MDM; JML automation; procurement and catalogue; SaaS / licenses; "
                "asset ticketing; remote assistance; approvals; reporting; audit trail.",
                s["cell"],
            ),
            P(
                "Payroll / core HR; ITIL incident &amp; problem management; SLA timers; change "
                "management; CMDB impact modelling; network redesign; non-IT facilities assets; "
                "Android corporate Zero-Touch; native buyback/payment workflow; signature / "
                "acceptable-use capture.",
                s["cell"],
            ),
        ],
    ]
    story.append(tbl(scope, [usable / 2, usable / 2]))
    story.append(Spacer(1, 2 * mm))
    story.append(
        callout(
            "<b>Android:</b> BYOD Work Profile in scope. Company-owned Android uses staged "
            "provisioning (not Zero-Touch).<br/>"
            "<b>Disposal:</b> ANSA nominates local disposal vendors; Factorial IT carries the evidence trail.<br/>"
            "<b>POC:</b> mandatory gate before January 2027 go-live (macOS, Windows, iOS, Android BYOD + company-owned).",
            s,
            usable,
        )
    )

    # —— 2 ARCHITECTURE (organogram) ——
    story.append(P("2. Target Architecture", s["h1"]))
    story.append(
        P(
            "Figure 1 — System context (one-way people data; Factorial IT as asset operations hub)",
            s["fig"],
        )
    )
    story.append(architecture_diagram(s, usable))
    story.append(Spacer(1, 2 * mm))
    story.append(
        P(
            "System of record: SuccessFactors for people data. Operational system of record: "
            "Factorial IT for asset operations.",
            s["tiny"],
        )
    )

    # —— 3 CORE FLOWS ——
    story.append(P("3. Core Flows", s["h1"]))
    story.append(P("Joiner / Mover / Leaver", s["h2"]))
    story.append(
        P(
            "Figure 2 — Corporate devices on macOS / Windows / iOS: automated wipe/lock. "
            "Android: company-owned remote wipe (console) or BYOD disenrollment on termination.",
            s["tiny"],
        )
    )
    jml_cells = [
        ("1. SF event", "Hire · Transfer · Termination"),
        "→",
        ("2. Factorial IT", "Automation rule fires"),
        "→",
        ("3. Action", "Onboard / reassign / recover<br/>+ Android wipe / disenroll"),
        "→",
        ("4. Evidence", "Logged · auditable"),
    ]
    # dark index: Factorial IT is index 2
    story.append(
        flow_row(
            jml_cells,
            [32 * mm, 7 * mm, 36 * mm, 7 * mm, 48 * mm, 7 * mm, usable - 137 * mm],
            s,
            dark_idx=2,
        )
    )

    story.append(P("Device lifecycle", s["h2"]))
    life = [
        ("Request", "Self-service"),
        ("Approval", "Policy thresholds"),
        ("Order", "Catalogue / PO"),
        ("Register", "Serial / model / cost"),
        ("Configure", "MDM baseline"),
        ("Handover", "Onboarding record"),
        ("Transfer / Offboard", "Reassign / wipe / recover"),
        ("Retire / Dispose", "Evidence before closure"),
    ]
    life_row = []
    life_w = []
    cell_w = usable / 8
    for i, (t, sub) in enumerate(life):
        life_row.append(P(f"<b>{t}</b><br/>{sub}", s["cell_c"]))
        life_w.append(cell_w)
    lt = Table([life_row], colWidths=life_w)
    lt.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), ALT),
                ("BOX", (0, 0), (-1, -1), 0.7, RULE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, RULE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("BACKGROUND", (0, 0), (0, 0), HDR),
                ("TEXTCOLOR", (0, 0), (0, 0), WHITE),
                ("BACKGROUND", (-1, 0), (-1, 0), HDR),
                ("TEXTCOLOR", (-1, 0), (-1, 0), WHITE),
            ]
        )
    )
    story.append(lt)

    # —— 4 ROADMAP ——
    story.append(P("4. Delivery Roadmap", s["h1"]))
    phases = [
        [P("Phase", s["cell_w"]), P("Timing", s["cell_w"]), P("Outcome / gate", s["cell_w"])],
        [P("0 · Planning", s["cell_b"]), P("Early Oct 2026", s["cell"]), P("Charter and governance", s["cell"])],
        [P("1 · Discovery", s["cell_b"]), P("Oct 2026", s["cell"]), P("Signed inputs and OS estate split", s["cell"])],
        [
            P("2 · Design + Configure", s["cell_b"]),
            P("Oct–Nov 2026", s["cell"]),
            P("Solution design, RBAC, catalogue, workflows, MDM", s["cell"]),
        ],
        [
            P("3 · Integration + POC", s["cell_b"]),
            P("Nov–Dec 2026", s["cell"]),
            P("SuccessFactors sync + four OS paths validated", s["cell"]),
        ],
        [P("POC Gate", s["cell_b"]), P("Dec 2026", s["cell"]), P("Steering sign-off required", s["cell"])],
        [P("4 · Go-live", s["cell_b"]), P("Jan 2027", s["cell"]), P("~500 employees / ~1,000 devices", s["cell"])],
        [
            P("5 · Rollouts", s["cell_b"]),
            P("Jan–Jun 2027", s["cell"]),
            P("Cohorts expand to ~10,000 devices", s["cell"]),
        ],
        [
            P("6 · Hypercare / BAU", s["cell_b"]),
            P("From Jun 2027", s["cell"]),
            P("Stabilisation and handover", s["cell"]),
        ],
    ]
    story.append(tbl(phases, [42 * mm, 32 * mm, usable - 74 * mm]))

    story.append(P("Rollout sequence", s["h2"]))
    roll = [
        ("POC", "~1k devices<br/>Oct–Dec 2026"),
        "→",
        ("Go-live", "Jan 2027<br/>POC cohort"),
        "→",
        ("Rollout A", "Trinidad<br/>Jan–Feb"),
        "→",
        ("Rollout B", "Barbados + Guyana<br/>Feb–Mar"),
        "→",
        ("Rollouts C–D", "Remaining<br/>Apr–Jun → 10k"),
    ]
    story.append(
        flow_row(
            roll,
            [30 * mm, 6 * mm, 28 * mm, 6 * mm, 28 * mm, 6 * mm, 36 * mm, 6 * mm, usable - 146 * mm],
            s,
            dark_idx=2,
        )
    )

    # —— 5 WORKSHOPS ——
    story.append(P("5. Discovery Workshops", s["h1"]))
    ws = [
        [P("Workshop", s["cell_w"]), P("Output", s["cell_w"])],
        [
            P("Asset Governance", s["cell_b"]),
            P(
                "Lifecycle states, mandatory fields, evidence; ANSA nominates local disposal vendors",
                s["cell"],
            ),
        ],
        [
            P("Procurement &amp; Catalogue", s["cell_b"]),
            P("Equipment Policy, Purchasing Policy, country catalogues", s["cell"]),
        ],
        [P("Joiner / Mover / Leaver", s["cell_b"]), P("Event-to-automation design", s["cell"])],
        [P("Security &amp; Compliance", s["cell_b"]), P("MDM baseline, RBAC, retention", s["cell"])],
        [P("Identity &amp; SSO", s["cell_b"]), P("IdP, SSO, SCIM decisions", s["cell"])],
        [
            P("MDM Operations", s["cell_b"]),
            P("OS enrolment paths; Android Work Profile / staged provisioning", s["cell"]),
        ],
        [
            P("SaaS &amp; Licenses", s["cell_b"]),
            P("Register, approval and reclamation rules", s["cell"]),
        ],
        [P("Reporting", s["cell_b"]), P("KPI / dashboard definitions", s["cell"])],
        [
            P("SuccessFactors Integration", s["cell_b"]),
            P("Field map, event contract, error handling", s["cell"]),
        ],
    ]
    story.append(tbl(ws, [48 * mm, usable - 48 * mm]))

    # —— 6 OUTCOMES ——
    story.append(P("6. Key Capability Outcomes", s["h1"]))
    outc = [
        [P("Area", s["cell_w"]), P("Target state", s["cell_w"])],
        [P("Joiner", s["cell_b"]), P("Hire event opens onboarding and applies equipment entitlement", s["cell"])],
        [
            P("Leaver", s["cell_b"]),
            P("Termination drives access deprovisioning, device action and recovery", s["cell"]),
        ],
        [
            P("Transfer", s["cell_b"]),
            P("Company / cost centre / manager updated with configured approvals", s["cell"]),
        ],
        [
            P("Procurement", s["cell_b"]),
            P("Purchasing Policy controls catalogue spend and approvers", s["cell"]),
        ],
        [P("Disposal", s["cell_b"]), P("Closure requires disposal / wipe evidence", s["cell"])],
        [
            P("MDM", s["cell_b"]),
            P(
                "Unified management for macOS / Windows / iOS; Android BYOD Work Profile in Phase 1",
                s["cell"],
            ),
        ],
        [P("SaaS", s["cell_b"]), P("Central register, approvals and reclamation rules", s["cell"])],
        [P("Audit", s["cell_b"]), P("Single evidence trail across asset events", s["cell"])],
    ]
    story.append(tbl(outc, [28 * mm, usable - 28 * mm]))
    story.append(Spacer(1, 2 * mm))
    story.append(
        callout(
            "<b>Boundaries:</b> Android corporate Zero-Touch is not Phase 1. Signed handover / "
            "acceptable-use acknowledgement remains outside the platform. Staff buyback runs as a "
            "ticket, with valuation and Finance approval outside the platform.",
            s,
            usable,
        )
    )

    # —— 7 COMMERCIALS ——
    story.append(P("7. Commercials", s["h1"]))
    story.append(P("All figures in USD.", s["tiny"]))
    com = [
        [P("Item", s["cell_w"]), P("Terms", s["cell_w"])],
        [P("Platform list price", s["cell"]), P("USD 10 / managed device / month", s["cell"])],
        [
            P("ANSA offer", s["cell"]),
            P("USD 6 / managed device / month for initial 12 billable months", s["cell"]),
        ],
        [
            P("POC / ramp", s["cell"]),
            P("~1,000 devices initially; target ~10,000 by June 2027; quarterly true-up", s["cell"]),
        ],
        [P("Oct–Dec 2026", s["cell"]), P("Platform complimentary", s["cell"])],
        [P("First platform invoice", s["cell"]), P("January 2027", s["cell"])],
        [P("Professional Services", s["cell_b"]), P("USD 5,000 fixed", s["cell_b"])],
        [
            P("PS payment", s["cell_b"]),
            P("USD 5,000 once at kick-off (October 2026)", s["cell_b"]),
        ],
        [
            P("Minimum subscription term", s["cell"]),
            P("12 billable months: Jan–Dec 2027", s["cell"]),
        ],
    ]
    story.append(tbl(com, [52 * mm, usable - 52 * mm]))

    story.append(P("Figure 4 — Commercial timeline (USD · October start)", s["fig"]))
    comm_flow = [
        ("Oct", "Kick-off<br/>Platform $0<br/><b>PS $5,000</b>"),
        "→",
        ("Nov", "Configure + POC<br/>Platform $0<br/>PS —"),
        "→",
        ("Dec", "POC sign-off<br/>Platform $0"),
        "→",
        ("Jan ★", "First platform invoice<br/>$6 × enrolled devices"),
    ]
    story.append(
        flow_row(
            comm_flow,
            [38 * mm, 8 * mm, 40 * mm, 8 * mm, 36 * mm, 8 * mm, usable - 138 * mm],
            s,
            dark_idx=6,
        )
    )
    story.append(Spacer(1, 2 * mm))
    story.append(
        callout(
            "<b>Year-1 snapshot:</b> Platform Jan–Dec 2027 ≈ USD 549,000 under the stated ramp "
            "assumption + USD 5,000 implementation = ≈ USD 554,000 total.",
            s,
            usable,
        )
    )

    # —— 8 INCLUDED ——
    story.append(P("8. Included", s["h1"]))
    incl = [
        [P("Platform", s["cell_w"]), P("Professional Services (USD 5,000)", s["cell_w"])],
        [
            P(
                "• ITAM / CMDB<br/>"
                "• MDM connectors (macOS, Windows, iOS, Android BYOD + company-owned wipe)<br/>"
                "• Asset ticketing &amp; remote assistance<br/>"
                "• JML automations<br/>"
                "• Procurement / catalogue<br/>"
                "• SaaS visibility<br/>"
                "• Approvals &amp; audit trail",
                s["cell"],
            ),
            P(
                "• Phases 0–3 POC delivery<br/>"
                "• 9 discovery workshops<br/>"
                "• SuccessFactors integration design &amp; build support<br/>"
                "• POC validation and go-live readiness<br/>"
                "• Rollout runbooks &amp; training foundation",
                s["cell"],
            ),
        ],
    ]
    story.append(tbl(incl, [usable / 2, usable / 2]))
    story.append(Spacer(1, 3 * mm))
    story.append(
        callout(
            "<b>Final gate:</b> Steering Committee POC sign-off is required before January 2027 "
            "production go-live.",
            s,
            usable,
        )
    )

    primary = OUTS[0]
    doc = SimpleDocTemplate(
        str(primary),
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=14 * mm,
        bottomMargin=14 * mm,
        title="ANSA McAL Factorial IT Implementation Package",
        author="Factorial",
    )
    doc.build(story)

    for dest in OUTS[1:]:
        dest.write_bytes(primary.read_bytes())
        print("copied", dest)
    print("Wrote", primary)
    return primary


if __name__ == "__main__":
    build()
