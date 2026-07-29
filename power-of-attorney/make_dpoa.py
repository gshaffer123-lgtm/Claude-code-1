#!/usr/bin/env python3
"""
Generate a Washington State Durable Power of Attorney for Health Care (DPOA-HC),
drafted to track chapter 11.125 RCW (Uniform Power of Attorney Act).

Print-ready: blanks are real ruled lines sized for handwriting.
Optionally pre-fills the principal / agent / alternate names from a JSON file.

Usage:  make_dpoa.py OUT.pdf [values.json]
"""

import io
import json
import sys

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, PageBreak, NextPageTemplate, Flowable,
)

OUT = sys.argv[1] if len(sys.argv) > 1 else "WA-DPOA-HealthCare.pdf"
V = {}
if len(sys.argv) > 2:
    with open(sys.argv[2]) as fh:
        V = json.load(fh)


def v(key):
    """Pre-filled value for a blank, or '' to leave it ruled and empty."""
    return (V.get(key) or "").strip()


PAGE_W, PAGE_H = letter
LM = RM = 0.8 * inch
TM = 0.7 * inch
BM = 0.85 * inch
CONTENT_W = PAGE_W - LM - RM
BOX_PAD = 8
INNER_W = CONTENT_W - 2 * BOX_PAD

# Filled in by the first (probe) build pass:
#   TOTAL_PAGES  - pages in the whole file
#   INSTR_START  - 1-based page number where the instruction sheet begins
TOTAL_PAGES = 0
INSTR_START = 0
MARKS = {}

# ---------------------------------------------------------------- styles


def S(name, **kw):
    base = dict(fontName="Times-Roman", fontSize=10.5, leading=13.8,
                alignment=TA_JUSTIFY, spaceAfter=5.5)
    base.update(kw)
    return ParagraphStyle(name, **base)


TITLE = S("title", fontName="Times-Bold", fontSize=15.5, leading=19,
          alignment=TA_CENTER, spaceAfter=2)
TITLE_SM = S("title_sm", fontName="Times-Bold", fontSize=13.2, leading=16.5,
             alignment=TA_CENTER, spaceAfter=2)
SUBTITLE = S("sub", fontSize=10.5, leading=13.5, alignment=TA_CENTER, spaceAfter=1)
SUBTITLE_I = S("subi", fontName="Times-Italic", fontSize=9.5, leading=12.5,
               alignment=TA_CENTER, spaceAfter=9)
H1 = S("h1", fontName="Times-Bold", fontSize=11, leading=13.6, alignment=0,
       spaceBefore=9.5, spaceAfter=3.5)
H2 = S("h2", fontName="Times-Bold", fontSize=10.5, leading=13, alignment=0,
       spaceBefore=7, spaceAfter=3)
BODY = S("body")
BODY_L = S("bodyl", alignment=0)
BODY_I = S("bodyi", fontName="Times-Italic", fontSize=9.5, leading=12.4)
SUBITEM = S("sub_item", leftIndent=22, bulletIndent=6, spaceAfter=4)
SMALL = S("small", fontSize=9, leading=11.6)
SMALL_L = S("smalll", fontSize=9, leading=11.6, alignment=0)
SMALL_C = S("smallc", fontSize=9, leading=11.6, alignment=TA_CENTER)
NOTE = S("note", fontName="Times-Italic", fontSize=9, leading=11.6)
CAPTION = S("cap", fontName="Helvetica", fontSize=7.2, leading=9, alignment=0,
            textColor=colors.HexColor("#333333"), spaceAfter=0)
FILLED = S("filled", fontName="Times-Bold", fontSize=11, leading=13, alignment=0,
           spaceAfter=0)
BANNER = S("banner", fontName="Times-Bold", fontSize=10.5, leading=13.5,
           alignment=TA_CENTER, spaceAfter=4)

# Slightly compressed styles, used only on the instruction sheet so it fits one page.
IH1 = S("ih1", fontName="Times-Bold", fontSize=10.4, leading=12.6, alignment=0,
        spaceBefore=7, spaceAfter=2.5)
IBODY = S("ibody", fontSize=9.6, leading=11.9, spaceAfter=4)
ISUB = S("isub", fontSize=9.6, leading=11.9, leftIndent=20, bulletIndent=5,
         spaceAfter=3)
IFINE = S("ifine", fontSize=8.6, leading=11)

LINE = colors.HexColor("#111111")
GRAY_BG = colors.HexColor("#f2f2f2")


class Marker(Flowable):
    """Zero-size flowable that records which page it landed on."""

    def __init__(self, name):
        Flowable.__init__(self)
        self.name = name
        self.width = self.height = 0

    def wrap(self, aw, ah):
        return (0, 0)

    def draw(self):
        MARKS[self.name] = self.canv.getPageNumber()


class Rule(Flowable):
    """Full-width horizontal rule."""

    def __init__(self, width=CONTENT_W, thickness=0.7, pad=4):
        Flowable.__init__(self)
        self.width, self.thickness, self.pad = width, thickness, pad
        self.height = thickness + pad

    def draw(self):
        self.canv.setStrokeColor(LINE)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.pad, self.width, self.pad)


def blanks(rows, total_w=CONTENT_W, gap=15, line_h=19, gap_after=7):
    """Ruled fill-in lines with small captions beneath.

    rows: list of rows; each row is a list of (caption, relative_width, key)
    where key is an optional pre-fill key. Any value present in V is typed
    onto the line instead of leaving it blank.
    """
    out = []
    for r in rows:
        cols = [w for _, w, *_ in r]
        total = float(sum(cols))
        gutters = gap * (len(r) - 1)
        scale = (total_w - gutters) / total

        colw, line_row, cap_row = [], [], []
        for i, spec in enumerate(r):
            cap, w = spec[0], spec[1]
            key = spec[2] if len(spec) > 2 else None
            val = v(key) if key else ""
            colw.append(w * scale)
            line_row.append(Paragraph(val, FILLED) if val else "")
            cap_row.append(Paragraph(cap, CAPTION) if cap else "")
            if i < len(r) - 1:
                colw.append(gap)
                line_row.append("")
                cap_row.append("")

        t = Table([line_row, cap_row], colWidths=colw, rowHeights=[line_h, None])
        style = [
            ("VALIGN", (0, 0), (-1, 0), "BOTTOM"),
            ("VALIGN", (0, 1), (-1, 1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
            ("BOTTOMPADDING", (0, 1), (-1, 1), 2),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ]
        ci = 0
        for _ in range(len(r)):
            style.append(("LINEBELOW", (ci, 0), (ci, 0), 0.7, LINE))
            ci += 2
        t.setStyle(TableStyle(style))
        out.append(t)
        out.append(Spacer(1, gap_after))
    return out


def boxed(flowables, pad=BOX_PAD, bg=None, border=0.8, width=CONTENT_W):
    t = Table([[flowables]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), border, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), pad),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
    ] + ([("BACKGROUND", (0, 0), (-1, -1), bg)] if bg else [])))
    return t


def short_rule(width, height=13):
    """A ruled blank whose line sits on the first text baseline of its row."""
    t = Table([[""]], colWidths=[width], rowHeights=[height])
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (0, 0), 0.7, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def initial_line(text, total_w=CONTENT_W):
    """Short initials blank at left, aligned to the first line of the text."""
    bw = 0.6 * inch
    t = Table([[short_rule(bw), Paragraph(text, SMALL)]],
              colWidths=[bw + 10, total_w - bw - 10])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (0, 0), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def inline_blank(width_in):
    """Used inside sentences: returns underscores sized roughly to width."""
    return "&nbsp;" + "_" * int(width_in * 9) + "&nbsp;"


# ---------------------------------------------------------------- page furniture


def _footer(canv, left, right):
    canv.saveState()
    canv.setFont("Times-Italic", 8.2)
    canv.setFillColor(colors.HexColor("#444444"))
    canv.drawString(LM, 0.5 * inch, left)
    canv.drawRightString(PAGE_W - RM, 0.5 * inch, right)
    canv.restoreState()


def on_page_legal(canv, doc):
    """Footer for the legal instrument: its own page numbering plus initials."""
    legal_total = (INSTR_START - 1) if INSTR_START else doc.page
    _footer(canv,
            "Durable Power of Attorney for Health Care — State of Washington "
            "(ch. 11.125 RCW)",
            "Page %d of %d" % (doc.page, legal_total))
    canv.saveState()
    canv.setFont("Times-Roman", 8.2)
    canv.setFillColor(colors.HexColor("#444444"))
    canv.drawCentredString(PAGE_W / 2.0, 0.66 * inch,
                           "Principal's initials: __________")
    canv.restoreState()


def on_page_instr(canv, doc):
    """Footer for the instruction sheet: numbered separately, no initials line."""
    if INSTR_START:
        n, total = doc.page - INSTR_START + 1, TOTAL_PAGES - INSTR_START + 1
        right = "Instruction sheet — page %d of %d" % (n, total)
    else:
        right = "Instruction sheet"
    _footer(canv, "Instructions only — not part of the legal document", right)


# ---------------------------------------------------------------- content


def build_story():
    E = []
    A = E.append

    A(Paragraph("DURABLE POWER OF ATTORNEY FOR HEALTH CARE", TITLE))
    A(Paragraph("State of Washington", SUBTITLE))
    A(Paragraph("Executed under the Uniform Power of Attorney Act, chapter 11.125 RCW",
                SUBTITLE_I))
    A(Rule())
    A(Spacer(1, 5))

    # ---- Article 1
    A(Paragraph("ARTICLE 1. &nbsp;PRINCIPAL", H1))
    A(Paragraph(
        "I am the person identified below. I am at least eighteen years of age, I am of sound "
        "mind, and I am signing this document voluntarily, free of duress and undue influence. I "
        "create this Durable Power of Attorney for Health Care so that the person I name below "
        "may speak for me and make health care decisions for me.", BODY))
    A(Spacer(1, 3))
    for f in blanks([
        [("Print my full legal name (Principal)", 62, "principal_name"),
         ("Date of birth", 38, "principal_dob")],
        [("Street address", 100, "principal_address")],
        [("City", 42, "principal_city"), ("State", 16, "principal_state"),
         ("ZIP", 16, "principal_zip"), ("Telephone", 34, "principal_phone")],
    ]):
        A(f)

    # ---- Article 2
    A(Paragraph("ARTICLE 2. &nbsp;APPOINTMENT OF MY AGENT (ATTORNEY-IN-FACT) FOR HEALTH CARE", H1))
    A(Paragraph(
        "I appoint the following person as my agent (also called my attorney-in-fact) to make "
        "health care decisions for me and to receive my health information, with the authority "
        "described in Article 6 below:", BODY))
    A(Spacer(1, 3))
    for f in blanks([
        [("Agent&rsquo;s full name", 62, "agent_name"),
         ("Relationship to me", 38, "agent_relationship")],
        [("Agent&rsquo;s street address, city, state, ZIP", 100, "agent_address")],
        [("Agent&rsquo;s primary telephone", 50, "agent_phone"),
         ("Alternate telephone or e-mail", 50, "agent_alt_contact")],
    ]):
        A(f)

    # ---- Article 3
    A(Paragraph("ARTICLE 3. &nbsp;ALTERNATE AGENT", H1))
    A(Paragraph(
        "If the agent named in Article 2 is unable, unwilling, or unavailable to act, or resigns, "
        "I appoint the following person to serve as my agent in that person&rsquo;s place, with the "
        "same authority. Only one agent serves at a time. <i>(Optional &mdash; this Article may be "
        "left blank.)</i>", BODY))
    A(Spacer(1, 3))
    for f in blanks([
        [("Alternate agent&rsquo;s full name", 62, "alt_agent_name"),
         ("Relationship to me", 38, "alt_agent_relationship")],
        [("Alternate agent&rsquo;s telephone", 50, "alt_agent_phone"),
         ("Alternate agent&rsquo;s address", 50, "alt_agent_address")],
    ]):
        A(f)

    # ---- Article 4 (the operative durability language)
    A(Paragraph("ARTICLE 4. &nbsp;THIS POWER OF ATTORNEY IS DURABLE", H1))
    A(boxed([Paragraph(
        "<b>This power of attorney shall not be affected by my disability or incapacity.</b> The "
        "authority I grant to my agent shall be exercisable notwithstanding my later disability, "
        "incapacity, or uncertainty as to whether I am alive or dead, and notwithstanding any "
        "lapse of time. This document is intended to be a durable power of attorney under RCW "
        "11.125.040.", BODY)]))

    # ---- Article 5
    A(Paragraph("ARTICLE 5. &nbsp;WHEN THIS DOCUMENT TAKES EFFECT AND HOW LONG IT LASTS", H1))
    A(Paragraph(
        "This power of attorney takes effect immediately when I sign it. It remains in effect "
        "until my death or until I revoke it, whichever occurs first. I may revoke it at any time "
        "while I have capacity, by any means showing my intent to revoke, including by a signed "
        "writing or by destroying this document.", BODY))
    A(Paragraph(
        "For as long as I am able to understand and communicate my own health care decisions, my "
        "own decisions control, and my agent shall act in consultation with me. My agent&rsquo;s "
        "authority to decide for me is intended to be used whenever I am unable to give informed "
        "consent myself &mdash; including while I am sedated, anesthetized, or otherwise unable to "
        "communicate during and after a medical procedure &mdash; and at any other time I ask my "
        "agent to act for me.", BODY))

    # ---- Article 6
    A(Paragraph("ARTICLE 6. &nbsp;AUTHORITY OF MY AGENT", H1))
    A(Paragraph(
        "I grant my agent general authority with respect to health care as described in RCW "
        "11.125.400. Without limiting that general grant, I specifically authorize my agent to:",
        BODY))
    items = [
        ("(a)", "give, withhold, or withdraw informed consent to any health care, treatment, "
                "service, medication, test, or procedure, including without limitation cardiac "
                "catheterization and coronary angiography, angioplasty and stent placement, the "
                "administration of contrast dye, sedation and anesthesia, blood products and "
                "transfusion, and any additional diagnostic or corrective procedure that my "
                "physicians recommend during, or arising out of, such a procedure, including the "
                "treatment of any complication;"),
        ("(b)", "consent to or refuse my admission to, transfer between, or discharge from any "
                "hospital, clinic, surgical center, rehabilitation facility, skilled nursing "
                "facility, hospice, or other health care facility, and to arrange my care after "
                "discharge;"),
        ("(c)", "select, employ, and discharge physicians, surgeons, nurses, therapists, and "
                "other health care providers, and to authorize referrals and second opinions;"),
        ("(d)", "act as my personal representative for all purposes of the Health Insurance "
                "Portability and Accountability Act of 1996 (HIPAA), 42 U.S.C. Sec. 1320d and its "
                "implementing regulations, including 45 C.F.R. Sec. 164.502(g), and to request, "
                "receive, review, obtain copies of, and consent to the disclosure of any of my "
                "individually identifiable health information, medical records, imaging, "
                "laboratory results, billing records, and insurance information;"),
        ("(e)", "speak with, question, and receive full reports from any of my physicians, nurses, "
                "and other providers; to be informed of my diagnosis, prognosis, and treatment "
                "options and their risks and alternatives; and to be physically present with me to "
                "the fullest extent the facility permits, including in pre-operative, procedural, "
                "recovery, and intensive care areas;"),
        ("(f)", "sign on my behalf any consent, informed-consent form, HIPAA authorization, "
                "release, waiver, admission or discharge paperwork, financial-responsibility form, "
                "or other document reasonably necessary to carry out this authority, including a "
                "document containing a release from liability;"),
        ("(g)", "consent to and direct measures for my comfort, including medication for the "
                "relief of pain, even if such measures may hasten my death, and to refuse "
                "treatment my agent reasonably believes I would refuse;"),
        ("(h)", "apply for and pursue insurance, Medicare, Medicaid, and other health benefits on "
                "my behalf, and to file appeals and grievances relating to my care."),
    ]
    for lab, txt in items:
        A(Paragraph(txt, SUBITEM, bulletText=lab))
    A(Paragraph(
        "In exercising this authority my agent shall act in good faith, in accordance with any "
        "wishes I have expressed to my agent, and otherwise in my best interest, after "
        "consultation with my physicians. My agent is not liable to me or my estate for decisions "
        "made in good faith on my behalf.", BODY))

    # ---- Article 7
    A(Paragraph("ARTICLE 7. &nbsp;LIFE-SUSTAINING TREATMENT", H1))
    A(Paragraph(
        "<b>Optional.</b> Place your initials on <b>one</b> line below if you wish to address this "
        "subject. If you initial neither line, the final paragraph of this Article applies.", NOTE))
    A(Spacer(1, 2))
    A(initial_line(
        "<b>My agent MAY decide to withhold or withdraw life-sustaining treatment</b> for me, "
        "including cardiopulmonary resuscitation, mechanical ventilation, dialysis, and "
        "artificially administered nutrition and hydration, if my agent determines that this is "
        "consistent with my wishes and my best interest after consulting my physicians. I "
        "expressly grant my agent that authority."))
    A(initial_line(
        "<b>My agent MAY NOT decide to withhold or withdraw life-sustaining treatment</b> for me. "
        "My agent&rsquo;s authority does not extend to that decision."))
    A(Paragraph(
        "If I have initialed neither line above, my agent shall make decisions about "
        "life-sustaining treatment based on my wishes as my agent understands them and, if my "
        "wishes are unknown, on my best interest, in consultation with my attending physician. Any "
        "health care directive (living will), POLST form, or mental health advance directive I "
        "have signed controls over this Article to the extent it conflicts with it.", BODY))

    # ---- Article 8
    A(Paragraph("ARTICLE 8. &nbsp;LIMITATIONS OR SPECIAL INSTRUCTIONS", H1))
    A(Paragraph(
        "My agent&rsquo;s authority is subject to any limitations or special instructions I write "
        "below. <i>(Optional &mdash; if this space is blank, there are no limitations other than "
        "those stated elsewhere in this document or imposed by law.)</i>", BODY))
    A(Spacer(1, 2))
    for f in blanks([[("", 100)], [("", 100)],
                     [("Limitations or special instructions", 100)]], gap_after=4):
        A(f)

    # ---- Article 9
    A(Paragraph("ARTICLE 9. &nbsp;PRIOR DOCUMENTS; OTHER DIRECTIVES", H1))
    A(Paragraph(
        "This document revokes any prior durable power of attorney for health care I have signed "
        "only to the extent that the prior document is inconsistent with this one. Any health care "
        "directive (living will), POLST form, mental health advance directive, or organ-donation "
        "designation I have signed remains in effect, and my agent shall honor it.", BODY))

    # ---- Article 10
    A(Paragraph("ARTICLE 10. &nbsp;RELIANCE BY THIRD PERSONS; COPIES", H1))
    A(Paragraph(
        "Any physician, nurse, hospital, clinic, laboratory, pharmacy, insurer, or other person or "
        "entity may rely on this document and on my agent&rsquo;s authority, and is released from "
        "liability for acting in good faith reliance on it, as provided in chapter 11.125 RCW. A "
        "photocopy, facsimile, scanned image, or other electronic copy of this signed document has "
        "the same force and effect as the signed original. This document is governed by the law of "
        "the State of Washington.", BODY))

    # ---- Article 11
    A(Paragraph("ARTICLE 11. &nbsp;NOMINATION OF GUARDIAN", H1))
    A(Paragraph(
        "If a court ever considers appointing a guardian or conservator of my person, I nominate "
        "the agent then serving under this document to be appointed, and I ask the court to give "
        "this nomination the effect provided by law.", BODY))

    # ---- Article 12 (kept whole; must not be orphaned from its signature lines)
    sig = [
        Paragraph("ARTICLE 12. &nbsp;SIGNATURE OF PRINCIPAL", H1),
        Paragraph(
            "I have read this document, I understand its contents, and I sign it voluntarily as my "
            "own free act. <b>Do not sign until you are in front of a notary public or two "
            "qualified witnesses &mdash; see Article 13.</b>", BODY),
        Spacer(1, 4),
        Paragraph("Signed at%s, Washington, on%s, 20%s." % (
            inline_blank(2.4), inline_blank(1.9), inline_blank(0.45)), BODY_L),
        Spacer(1, 10),
    ]
    for f in blanks([
        [("Signature of Principal", 58), ("Date signed", 42)],
        [("Print name of Principal", 58, "principal_name"), ("", 42)],
    ]):
        sig.append(f)
    A(KeepTogether(sig))

    # ---- Article 13
    A(Paragraph("ARTICLE 13. &nbsp;EXECUTION &mdash; NOTARY <u>OR</u> TWO WITNESSES", H1))
    A(boxed([
        Paragraph("COMPLETE OPTION A <u>OR</u> OPTION B &mdash; NOT BOTH.", BANNER),
        Paragraph(
            "Under RCW 11.125.050 this document must be signed and dated by the Principal, and the "
            "Principal&rsquo;s signature must either (A) be acknowledged before a notary public, or "
            "(B) be attested by two or more competent witnesses who sign in the Principal&rsquo;s "
            "presence and at the Principal&rsquo;s direction or request. <b>Option A (notary) is the "
            "stronger choice</b> &mdash; a notarized signature is presumed genuine and most "
            "hospitals accept it without question. Use Option B only if no notary is available.",
            SMALL),
        Spacer(1, 4),
        Paragraph(
            "<b>Warning about witnesses:</b> a witness may not be related to the Principal <u>or to "
            "the agent</u> by blood, marriage, or state registered domestic partnership, and may "
            "not be the Principal&rsquo;s home care provider or a care provider at an adult family "
            "home or long-term care facility where the Principal lives. Family members therefore "
            "cannot serve as witnesses. A neighbor, family friend, coworker, or church member can.",
            SMALL),
    ], bg=GRAY_BG))

    # Option A -- notarial acknowledgment (keep the whole certificate together)
    seal = Table([[Paragraph("Affix notary<br/>seal or stamp<br/>here", SMALL_C)]],
                 colWidths=[1.75 * inch], rowHeights=[1.45 * inch],
                 style=TableStyle([
                     ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#777777")),
                     ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                 ]))
    left_col = [
        short_rule(2.9 * inch, 17),
        Paragraph("Signature of Notary Public", CAPTION),
        Spacer(1, 15),
        short_rule(2.9 * inch, 17),
        Paragraph("Print name of Notary Public", CAPTION),
        Spacer(1, 9),
        Paragraph("Title: Notary Public in and for the State of Washington", SMALL_L),
        Paragraph("My commission expires:%s" % inline_blank(1.5), SMALL_L),
    ]
    nt = Table([[left_col, seal]], colWidths=[INNER_W - 1.9 * inch, 1.9 * inch])
    nt.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
    ]))
    A(KeepTogether([
        Paragraph("OPTION A &mdash; NOTARIAL ACKNOWLEDGMENT", H2),
        boxed([
            Paragraph("STATE OF WASHINGTON", SMALL_L),
            Paragraph("COUNTY OF%s" % inline_blank(2.2), SMALL_L),
            Spacer(1, 7),
            Paragraph(
                "This record was acknowledged before me on%s(date) by%s(name of Principal), who "
                "signed it as a voluntary act for the purposes stated in it." % (
                    inline_blank(2.0), inline_blank(3.0)), SMALL_L),
            Spacer(1, 14),
            nt,
        ]),
    ]))

    # Option B -- two witnesses, split into separately boxed blocks so the
    # section can break across a page without leaving a half-empty sheet.
    A(KeepTogether([
        Paragraph("OPTION B &mdash; ATTESTATION BY TWO WITNESSES", H2),
        Paragraph(
            "Each of us signs below in the presence of the Principal and at the Principal&rsquo;s "
            "direction or request. Each of us declares under penalty of perjury under the laws of "
            "the State of Washington that: the Principal signed this document in my presence and "
            "appeared to me to be of sound mind and acting freely, without duress, fraud, or undue "
            "influence; I am at least eighteen years of age and competent; I am not the agent or "
            "alternate agent named in this document; I am not related to the Principal or to the "
            "agent by blood, marriage, or state registered domestic partnership; and I am not the "
            "Principal&rsquo;s home care provider, nor a care provider at an adult family home or "
            "long-term care facility in which the Principal resides.", SMALL),
        Spacer(1, 6),
    ]))
    for label in ("First witness", "Second witness"):
        blk = [Paragraph("<b>%s</b>" % label, SMALL_L), Spacer(1, 3)]
        for f in blanks([
            [("Signature of witness", 58), ("Date", 42)],
            [("Print name of witness", 46), ("Address (city and state)", 54)],
        ], total_w=INNER_W, gap_after=5):
            blk.append(f)
        A(boxed(blk))
        A(Spacer(1, 6))

    # ---- Article 14
    agent_ack = [
        Paragraph("ARTICLE 14. &nbsp;ACCEPTANCE BY AGENT", H1),
        Paragraph(
            "<i>Optional but recommended &mdash; it helps hospital staff confirm who the agent "
            "is.</i> I accept appointment as agent under this document. I understand that I must "
            "act in good faith, within the authority granted, in accordance with the "
            "Principal&rsquo;s reasonable expectations and known wishes and otherwise in the "
            "Principal&rsquo;s best interest, and that I must keep the Principal informed to the "
            "extent the Principal is able to participate.", BODY),
        Spacer(1, 5),
    ]
    for f in blanks([
        [("Signature of Agent", 58), ("Date", 42)],
        [("Print name of Agent", 46, "agent_name"), ("Telephone", 54, "agent_phone")],
    ]):
        agent_ack.append(f)
    A(KeepTogether(agent_ack))

    # ================================================ HIPAA authorization
    A(PageBreak())
    A(Paragraph("HIPAA AUTHORIZATION FOR RELEASE OF HEALTH INFORMATION", TITLE_SM))
    A(Paragraph("Accompanies and supplements the Durable Power of Attorney for Health Care",
                SUBTITLE_I))
    A(Rule())
    A(Spacer(1, 7))
    A(Paragraph(
        "This is a stand-alone authorization under the Health Insurance Portability and "
        "Accountability Act of 1996 (HIPAA), 45 C.F.R. Parts 160 and 164. Hospital staff sometimes "
        "ask for one even when a power of attorney is presented; providing it avoids delay.",
        BODY_I))
    A(Spacer(1, 5))
    for f in blanks([
        [("Print full legal name of Principal (patient)", 62, "principal_name"),
         ("Date of birth", 38, "principal_dob")],
    ]):
        A(f)
    A(Paragraph(
        "I authorize any physician, health care professional, hospital, clinic, surgical center, "
        "laboratory, imaging facility, pharmacy, insurer, health plan, or other covered entity "
        "that has provided health care to me, or that has paid for or is billing for my health "
        "care, to disclose my protected health information to the person or persons named below.",
        BODY))
    A(Spacer(1, 3))
    for f in blanks([
        [("Name of person authorized to receive my health information", 62, "agent_name"),
         ("Relationship", 38, "agent_relationship")],
        [("Telephone", 46, "agent_phone"),
         ("Second person authorized (optional) and relationship", 54, "alt_agent_name")],
    ]):
        A(f)
    A(Paragraph(
        "<b>Information covered.</b> This authorization applies to all of my protected health "
        "information, including my complete medical record, physician and nursing notes, history "
        "and physical, operative and procedure reports, imaging and diagnostic studies and their "
        "interpretations, laboratory results, medication and allergy lists, discharge summaries, "
        "billing and payment records, and information about my care and prognosis given verbally, "
        "in person, or by telephone. I intend this authorization to include information relating "
        "to cardiovascular disease and any procedure to diagnose or treat it.", BODY))
    A(Paragraph(
        "<b>Purpose.</b> So that the person named above may be informed about, discuss, "
        "coordinate, and make decisions about my health care.", BODY))
    A(Paragraph(
        "<b>Duration.</b> This authorization takes effect on the date I sign it and remains in "
        "effect until I revoke it in writing. It does not expire upon my disability or incapacity, "
        "and it survives my death to the extent permitted by law.", BODY))
    A(Paragraph(
        "<b>My rights.</b> I understand that I may revoke this authorization at any time by "
        "written notice to the disclosing provider, except to the extent the provider has already "
        "acted in reliance on it; that treatment, payment, enrollment, and eligibility for "
        "benefits may not be conditioned on my signing it; and that information disclosed under "
        "this authorization may no longer be protected by federal privacy rules once it is "
        "received by the person named above.", BODY))
    A(Spacer(1, 9))
    for f in blanks([
        [("Signature of Principal (patient)", 58), ("Date", 42)],
        [("Print name of Principal", 58, "principal_name"), ("", 42)],
    ]):
        A(f)
    A(Spacer(1, 2))
    A(Paragraph(
        "<i>If this page is signed at the same time and before the same notary or witnesses as the "
        "Durable Power of Attorney for Health Care, no separate notarization of this page is "
        "required.</i>", NOTE))

    # ================================================ instruction sheet
    A(NextPageTemplate("instr"))
    A(PageBreak())
    A(Marker("instr_start"))
    A(Paragraph("HOW TO COMPLETE AND USE THIS DOCUMENT", TITLE_SM))
    A(Paragraph("Instruction sheet &mdash; NOT part of the legal document. Do not sign this page.",
                SUBTITLE_I))
    A(Rule())
    A(Spacer(1, 5))

    A(Paragraph("Step by step", IH1))
    steps = [
        "<b>Print the legal document</b> (every page except this one), single-sided if you can "
        "&mdash; hospital records staff scan these.",
        "<b>Fill in Articles 1 and 2</b>, and Article 3 if you want a backup agent. The patient "
        "(Principal) is your dad; the agent is your sister. Blue or black ink, and print names "
        "exactly as they appear on his photo ID and insurance card.",
        "<b>Article 7 is optional.</b> Your dad initials one line only if he wants to address "
        "life-sustaining treatment. If he leaves both blank the document still works &mdash; his "
        "agent then decides based on his wishes and best interest.",
        "<b>Do not sign anything until the notary or both witnesses are watching.</b> Signing "
        "early is the most common reason these get rejected.",
        "<b>Article 12:</b> your dad fills in the city, then signs and dates. "
        "<b>Article 13:</b> complete Option A <u>or</u> Option B &mdash; never both. "
        "<b>Article 14:</b> your sister signs to accept the role.",
        "<b>HIPAA page:</b> your dad fills it in and signs it, naming your sister as the person "
        "authorized to receive his health information.",
        "<b>Make three copies</b> &mdash; hospital medical records, your sister, your dad&rsquo;s "
        "file. Give the hospital a copy and keep the signed original safe. Photograph every page "
        "with her phone as a backup.",
    ]
    for i, s in enumerate(steps, 1):
        A(Paragraph(s, ISUB, bulletText="%d." % i))

    A(Paragraph("Where to get it notarized on short notice", IH1))
    A(Paragraph(
        "Notaries are usually easy to find same-day: a bank or credit union (often free for "
        "members &mdash; call ahead and ask whether a notary is on duty), a UPS Store or other "
        "shipping and mailbox store (walk-in, roughly $15 per signature), a public library or city "
        "clerk&rsquo;s office. <b>Many hospitals also have a notary on staff</b> &mdash; call "
        "patient relations, social work, case management, or admissions and ask; if they do, your "
        "dad can sign at the hospital before the procedure. Everyone signing must bring unexpired "
        "photo ID.", IBODY))
    A(Paragraph(
        "If no notary is reachable in time, use Option B, and mind the disqualification: nobody "
        "related to your dad <u>or to your sister</u> by blood, marriage, or registered domestic "
        "partnership may witness. Two unrelated adults &mdash; neighbors, coworkers, family "
        "friends, church members, or two hospital employees who are not his care providers &mdash; "
        "can sign.", IBODY))

    A(Paragraph("Worth knowing", IH1))
    A(Paragraph(
        "<b>Washington law already gives your sister standing.</b> Even with no document at all, "
        "RCW 7.70.065 sets the order of people who may give informed consent for a patient who "
        "cannot consent: a court-appointed guardian, then an agent under a durable power of "
        "attorney, then the spouse or state registered domestic partner, then adult children, then "
        "parents, then adult brothers and sisters. So if this document is not finished in time, the "
        "procedure will not be blocked. But the adult children have to agree among themselves, "
        "which can be slow, and that route does not by itself unlock medical records &mdash; the "
        "gaps this document and the HIPAA page close.", IBODY))
    A(Paragraph(
        "<b>Call the hospital first.</b> Ask the pre-procedure or admissions nurse whether they "
        "want the form in advance and where to send it, and whether they have their own advance "
        "directive packet they prefer. Most hospitals will accept this one, but a few minutes on "
        "the phone the day before prevents an argument on the morning of the procedure.", IBODY))
    A(Paragraph(
        "<b>Capacity matters.</b> Your dad must understand what he is signing at the moment he "
        "signs it, so get this done before he is medicated or sedated. If he cannot understand it, "
        "this document cannot be used and the RCW 7.70.065 order above governs instead.", IBODY))
    A(Paragraph(
        "<b>Scope.</b> This is a health care power of attorney only. It grants no authority over "
        "money, banking, property, or taxes, apart from the health-benefit claims in Article 6(h). "
        "A financial power of attorney is a separate document.", IBODY))

    A(Spacer(1, 5))
    A(boxed([Paragraph(
        "<b>Not legal advice.</b> This document was prepared to track the requirements of chapter "
        "11.125 RCW so that it can be signed quickly ahead of an upcoming procedure. It is not a "
        "substitute for advice from a Washington attorney, and no attorney-client relationship "
        "exists. For longer-term planning &mdash; or if the situation involves family "
        "disagreement, existing estate planning documents, a guardianship, real property, or "
        "Medicaid &mdash; have a Washington estate-planning or elder-law attorney review it. The "
        "Washington State Medical Association publishes a free advance directive, and free "
        "plain-language forms and instructions are available at WashingtonLawHelp.org.", IFINE)],
        pad=6, bg=GRAY_BG))
    return E


def make_doc(target):
    d = BaseDocTemplate(
        target, pagesize=letter,
        leftMargin=LM, rightMargin=RM, topMargin=TM, bottomMargin=BM,
        title="Durable Power of Attorney for Health Care (Washington)",
        subject="Durable Power of Attorney for Health Care - chapter 11.125 RCW",
        author="",
    )

    def frame():
        return Frame(LM, BM, CONTENT_W, PAGE_H - TM - BM, id="main",
                     leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    d.addPageTemplates([
        PageTemplate(id="legal", frames=[frame()], onPage=on_page_legal),
        PageTemplate(id="instr", frames=[frame()], onPage=on_page_instr),
    ])
    return d


# Pass 1: discover the page count and where the instruction sheet starts, so
# the two footers can number their sections independently.
probe = make_doc(io.BytesIO())
probe.build(build_story())
TOTAL_PAGES = probe.page
INSTR_START = MARKS.get("instr_start", TOTAL_PAGES)

# Pass 2: real output, now that the footers know the counts.
make_doc(OUT).build(build_story())
print("wrote %s — %d legal pages + %d instruction page(s) = %d total"
      % (OUT, INSTR_START - 1, TOTAL_PAGES - INSTR_START + 1, TOTAL_PAGES))
