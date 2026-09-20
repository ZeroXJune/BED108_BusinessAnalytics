"""
Builds the printable Individual Contribution Form (Form A).

Checkpoint 4 requires signed forms for all four checkpoints, one per member,
so the document holds a ready-to-sign page for every member-checkpoint pair -
twelve for a group of three - followed by a reminder page of what was actually
done in each checkpoint.

Member name and role are left blank to write in: the brief asks for both, and
who held which role is the group's to state.

Formatted to the Section 3.1 standard: Arial 12pt, 1-inch margins.

Run:  python3 scripts/build_form_a.py
"""

import os

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reports", "Form_A_Individual_Contribution.docx")

FONT = "Arial"
INK = RGBColor(0x1F, 0x29, 0x33)
ACCENT = RGBColor(0x2F, 0x6F, 0x9F)
MUTED = RGBColor(0x5A, 0x66, 0x72)

MEMBERS = 3          # copies per checkpoint, one for each member
CHECKPOINTS = [
    (1, "Data Fundamentals & SQL Querying"),
    (2, "Spreadsheet & Statistical Analysis"),
    (3, "BI Dashboard Development"),
    (4, "Capstone Analytics Project & Final Defense"),
]

PROMPTS = {
    "Checkpoint 1 — Data Fundamentals & SQL Querying": [
        ("Project Lead / Analyst",
         "Business problem framing, the three key business questions, business "
         "interpretations of the query results, report assembly."),
        ("Data Engineer",
         "Dataset sourcing and documentation, data quality assessment, "
         "cleaning steps, ERD, schema creation, data load."),
        ("Statistician / Modeler",
         "Aggregate and trend queries, year-on-year and seasonality "
         "calculations, verification that reported figures match the data."),
        ("BI Developer / Visualizer",
         "Charts and figures, table formatting, report layout and "
         "presentation of results."),
    ],
    "Checkpoint 2 — Spreadsheet & Statistical Analysis": [
        ("Project Lead / Analyst",
         "Choice of variables for correlation and regression, written "
         "interpretations, report assembly, the Checkpoint 1 correction."),
        ("Data Engineer",
         "Export of the cleaned dataset into the workbook, named ranges, "
         "pivot cross-tabs and formula showcase, workbook self-checks."),
        ("Statistician / Modeler",
         "Descriptive statistics, frequency distribution, correlation "
         "coefficients, the regression and its significance test, the trend "
         "and seasonality analysis and its holdout check."),
        ("BI Developer / Visualizer",
         "Pivot charts, histogram, scatter plots with trendlines, forecast "
         "chart, workbook formatting and layout."),
    ],
    "Checkpoint 3 — BI Dashboard Development": [
        ("Project Lead / Analyst",
         "Dashboard blueprint and page purposes, the choice of order count as "
         "the primary KPI, the written discussion of insights, presentation "
         "narrative."),
        ("Data Engineer",
         "The five dashboard views, the exported datasets and their "
         "verification against the published figures, the Power BI data model "
         "and relationships."),
        ("Statistician / Modeler",
         "The clustering: feature choice, selecting k by silhouette, naming "
         "the segments from the cluster centres, and the segment profile "
         "figures."),
        ("BI Developer / Visualizer",
         "Building the three dashboard pages, slicers and drill-through, "
         "chart formatting, titles and labels, the exported PDF."),
    ],
    "Checkpoint 4 — Capstone Analytics Project & Final Defense": [
        ("Project Lead / Analyst",
         "Executive summary, integration of all four checkpoints into the "
         "final report, the conclusions and recommendations, defense "
         "coordination."),
        ("Data Engineer",
         "Data governance section, the compiled digital submission folder, "
         "references and appendix."),
        ("Statistician / Modeler",
         "The multiple regression, multicollinearity and residual "
         "diagnostics, holdout evaluation, model assumptions and "
         "limitations."),
        ("BI Developer / Visualizer",
         "Slide deck, dashboard screenshots and annotation, figure and table "
         "numbering across the integrated report."),
    ],
}


def rule(paragraph):
    """Draw a writing line as a bottom border, so there is room to write."""
    pPr = paragraph._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "7B8794")
    borders.append(bottom)
    pPr.append(borders)


def field(doc, label, space_after=14):
    """A labelled write-in line."""
    par = doc.add_paragraph()
    par.paragraph_format.space_after = Pt(space_after)
    par.paragraph_format.space_before = Pt(2)
    run = par.add_run(label)
    run.bold = True
    run.font.name = FONT
    run.font.size = Pt(11)
    run.font.color.rgb = INK
    par.add_run("  ").font.size = Pt(11)
    rule(par)
    return par


def blank_line(doc, prefix=""):
    par = doc.add_paragraph()
    par.paragraph_format.space_after = Pt(16)
    if prefix:
        run = par.add_run(prefix)
        run.font.name = FONT
        run.font.size = Pt(11)
        run.font.color.rgb = INK
    rule(par)
    return par


def heading(doc, text, size=15, color=ACCENT, after=6):
    par = doc.add_paragraph()
    par.paragraph_format.space_after = Pt(after)
    run = par.add_run(text)
    run.bold = True
    run.font.name = FONT
    run.font.size = Pt(size)
    run.font.color.rgb = color
    return par


def small(doc, text, italic=True, after=10):
    par = doc.add_paragraph()
    par.paragraph_format.space_after = Pt(after)
    run = par.add_run(text)
    run.italic = italic
    run.font.name = FONT
    run.font.size = Pt(9)
    run.font.color.rgb = MUTED
    return par


def prefilled(doc, label, value, space_after=18):
    """A labelled line with the value already filled in."""
    par = doc.add_paragraph()
    par.paragraph_format.space_after = Pt(space_after)
    run = par.add_run(label + "  ")
    run.bold = True
    run.font.name = FONT
    run.font.size = Pt(11)
    run.font.color.rgb = INK
    run = par.add_run(value)
    run.font.name = FONT
    run.font.size = Pt(11)
    run.font.color.rgb = ACCENT
    rule(par)
    return par


def form_page(doc, number, title):
    heading(doc, "Individual Contribution Form", 16)
    heading(doc, "BED 106 — Business Analytics · Mini Capstone Project",
            11, INK, after=2)
    small(doc, "Talibon Polytechnic College · A.Y. 2026–2027, 1st Semester · "
               "Instructor: Jessie A. Melendres", after=16)

    field(doc, "Group Name / Number:")
    prefilled(doc, "Checkpoint No.:", "%d — %s" % (number, title))
    field(doc, "Member Name:")
    field(doc, "Role:")

    heading(doc, "Specific Contributions This Checkpoint", 12, INK, after=4)
    small(doc, "Write these in your own words. Be specific about what you "
               "personally did.", after=12)
    for n in (1, 2, 3):
        blank_line(doc, f"{n}.  ")
        blank_line(doc)

    par = doc.add_paragraph()
    par.paragraph_format.space_before = Pt(12)
    par.paragraph_format.space_after = Pt(26)
    run = par.add_run("I certify that the contributions listed above are "
                      "accurate and reflect my actual participation.")
    run.font.name = FONT
    run.font.size = Pt(10.5)
    run.font.color.rgb = INK

    table = doc.add_table(rows=1, cols=2)
    table.autofit = False
    for i, (label, width) in enumerate((("Signature:", 3.9), ("Date:", 2.4))):
        cell = table.rows[0].cells[i]
        cell.width = Inches(width)
        par = cell.paragraphs[0]
        run = par.add_run(label)
        run.bold = True
        run.font.name = FONT
        run.font.size = Pt(11)
        run.font.color.rgb = INK
        rule(par)


def prompts_page(doc):
    heading(doc, "What each role did", 15)
    small(doc, "Reminders only. Section 3.2 of the brief requires the work to "
               "be described in your own words, so use these to jog your "
               "memory rather than copying them.", after=14)

    for checkpoint, rows in PROMPTS.items():
        heading(doc, checkpoint, 12, INK, after=6)
        table = doc.add_table(rows=1, cols=2)
        table.style = "Light Grid Accent 1"
        hdr = table.rows[0].cells
        for i, text in enumerate(("Role", "Work in this checkpoint")):
            hdr[i].text = ""
            run = hdr[i].paragraphs[0].add_run(text)
            run.bold = True
            run.font.name = FONT
            run.font.size = Pt(10)
        for role, work in rows:
            cells = table.add_row().cells
            for i, text in enumerate((role, work)):
                cells[i].text = ""
                run = cells[i].paragraphs[0].add_run(text)
                run.font.name = FONT
                run.font.size = Pt(9.5)
                if i == 0:
                    run.bold = True
        table.columns[0].width = Inches(1.9)
        table.columns[1].width = Inches(4.6)
        doc.add_paragraph().paragraph_format.space_after = Pt(10)


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

    first = True
    for number, title in CHECKPOINTS:
        for _ in range(MEMBERS):
            if not first:
                doc.add_page_break()
            first = False
            form_page(doc, number, title)

    doc.add_page_break()
    prompts_page(doc)

    doc.save(OUT)
    pages = len(CHECKPOINTS) * MEMBERS
    print(f"wrote {OUT}")
    print(f"  {pages} signable copies — {MEMBERS} members x "
          f"{len(CHECKPOINTS)} checkpoints — plus a prompts page")


if __name__ == "__main__":
    main()
