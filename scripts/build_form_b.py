"""
Builds the printable Peer Evaluation Form (Form B).

Required by Checkpoint 4 only: each member individually rates all other group
members, and the completed forms go to the instructor in a sealed envelope on
defense day. The document holds one ready-to-sign page per member.

Layout follows Section 5 of the brief exactly — the four rating columns are
Effort, Quality, Collaboration and Communication, each out of 5, with a
comments column.

Formatted to the Section 3.1 standard: Arial 12pt, 1-inch margins.

Run:  python3 scripts/build_form_b.py
"""

import os

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reports", "Form_B_Peer_Evaluation.docx")

FONT = "Arial"
INK = RGBColor(0x1F, 0x29, 0x33)
MUTED = RGBColor(0x5A, 0x66, 0x72)

MEMBERS = 3                      # one page per member of the group
COLUMNS = ["Member Name", "Effort", "Quality", "Collab.", "Commun.", "Comments"]
WIDTHS = [1.75, 0.62, 0.62, 0.62, 0.72, 2.17]


def rule(paragraph):
    """Draw a writing line as a bottom border."""
    pPr = paragraph._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "7B8794")
    borders.append(bottom)
    pPr.append(borders)


def styled(par, text, size=11, bold=False, italic=False, color=INK):
    run = par.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.name = FONT
    run.font.size = Pt(size)
    run.font.color.rgb = color
    return run


def heading(doc, text, size, after=6):
    par = doc.add_paragraph()
    par.paragraph_format.space_after = Pt(after)
    styled(par, text, size, bold=True)
    return par


def field(doc, label, width_hint=None, space_after=14):
    par = doc.add_paragraph()
    par.paragraph_format.space_after = Pt(space_after)
    styled(par, label + "  ", bold=True)
    styled(par, " " * (width_hint or 48))
    rule(par)
    return par


def page(doc):
    heading(doc, "Peer Evaluation Form — Final Capstone Defense", 15)
    heading(doc, "BED 106 — Business Analytics · Mini Capstone Project", 11,
            after=2)
    par = doc.add_paragraph()
    par.paragraph_format.space_after = Pt(16)
    styled(par, "Talibon Polytechnic College · A.Y. 2026–2027, 1st Semester · "
                "Instructor: Jessie A. Melendres", 9, italic=True, color=MUTED)

    table = doc.add_table(rows=1, cols=2)
    table.autofit = False
    for i, (label, width) in enumerate((("Evaluator's Name:", 4.0),
                                        ("Group:", 2.5))):
        cell = table.rows[0].cells[i]
        cell.width = Inches(width)
        par = cell.paragraphs[0]
        styled(par, label + "  ", bold=True)
        styled(par, " " * 26)
        rule(par)

    par = doc.add_paragraph()
    par.paragraph_format.space_before = Pt(18)
    par.paragraph_format.space_after = Pt(8)
    styled(par, "Rate each member below (1 = Poor, 5 = Excellent) and add "
                "comments:", 10.5)

    grid = doc.add_table(rows=1 + MEMBERS, cols=len(COLUMNS))
    grid.style = "Table Grid"
    grid.alignment = WD_TABLE_ALIGNMENT.CENTER
    grid.autofit = False

    for i, name in enumerate(COLUMNS):
        cell = grid.rows[0].cells[i]
        cell.width = Inches(WIDTHS[i])
        par = cell.paragraphs[0]
        par.alignment = (WD_ALIGN_PARAGRAPH.CENTER if i else
                         WD_ALIGN_PARAGRAPH.LEFT)
        styled(par, name, 10, bold=True)

    for r in range(MEMBERS):
        row = grid.rows[r + 1]
        row.height = Inches(0.62)
        for i in range(len(COLUMNS)):
            cell = row.cells[i]
            cell.width = Inches(WIDTHS[i])
            par = cell.paragraphs[0]
            if i == 0:
                styled(par, "Member %d:" % (r + 1), 10, color=MUTED)
            elif i < 5:
                par.alignment = WD_ALIGN_PARAGRAPH.CENTER
                styled(par, "/5", 10, color=MUTED)

    par = doc.add_paragraph()
    par.paragraph_format.space_before = Pt(14)
    par.paragraph_format.space_after = Pt(22)
    styled(par, "Rate every other member of your group. Do not rate "
                "yourself — leave that row blank or strike it through.",
           9, italic=True, color=MUTED)

    table = doc.add_table(rows=1, cols=2)
    table.autofit = False
    for i, (label, width) in enumerate((("Evaluator's Signature:", 4.0),
                                        ("Date:", 2.5))):
        cell = table.rows[0].cells[i]
        cell.width = Inches(width)
        par = cell.paragraphs[0]
        styled(par, label + "  ", bold=True)
        styled(par, " " * 22)
        rule(par)

    par = doc.add_paragraph()
    par.paragraph_format.space_before = Pt(26)
    styled(par, "Submit to the instructor in a sealed envelope on defense "
                "day. One completed form per member.", 9, italic=True,
           color=MUTED)


def main():
    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(11)
    normal.font.color.rgb = INK
    normal.paragraph_format.space_after = Pt(6)

    for section in doc.sections:
        section.left_margin = section.right_margin = Inches(1.0)
        section.top_margin = section.bottom_margin = Inches(1.0)

    for i in range(MEMBERS):
        if i:
            doc.add_page_break()
        page(doc)

    doc.save(OUT)
    print("wrote %s" % OUT)
    print("  %d copies, one per member" % MEMBERS)


if __name__ == "__main__":
    main()
