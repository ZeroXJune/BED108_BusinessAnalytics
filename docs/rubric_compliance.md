# Checkpoint 1 — Rubric Compliance Map

Every requirement in the BED 106 project brief for Checkpoint 1, mapped to
where it is satisfied. Items marked **ACTION** need something only the group
can supply.

## Tasks & Deliverables

| Brief requirement | Status | Where |
| --- | --- | --- |
| **1.1** Business domain and specific problem | Done | Report, Task 1.1 — Retail & Sales Analytics |
| **1.1** Why the problem matters (impact) | Done | Report, "Business Impact & Significance" |
| **1.1** Key business questions | Done | Three questions, each mapped to the queries that answer it |
| **1.1** Data type planned and source | Done | Report, "Data Source Overview" |
| **1.2** Dataset name, source URL/file, date accessed, licence | Partial | Table 2 — **ACTION: confirm the exact licence** |
| **1.2** Data dictionary (name, type, description) | Done | Table 3, all 12 columns |
| **1.2** Quality assessment: missing, duplicates, inconsistencies, cleaning | Done | Report §"Preliminary Data Quality Assessment"; evidence in `reports/data_quality_report.md` |
| **1.2** Raw dataset preview, first 10–20 rows | Partial | Table 4 — **ACTION: paste your own screenshot** |
| **1.3** ERD with at least 2 related tables | Exceeded | 7 tables, `docs/erd.md` |
| **1.3** Tables with appropriate types and PK/FK | Done | `sql/01_schema_mysql.sql` |
| **1.3** Import and load cleaned data | Done | `sql/03_insert_data.sql`, 1,194 fact rows |
| **1.3** Screenshots of schema and populated tables | Not done | **ACTION: screenshot your own RDBMS run** |
| **1.4** ≥2 SELECT with WHERE and ORDER BY | Done | Q1, Q2 |
| **1.4** ≥2 GROUP BY with aggregates | Done | Q3, Q4 (COUNT, SUM, AVG) |
| **1.4** ≥2 JOIN queries, 2+ tables | Exceeded | Q5, Q6 — four tables each |
| **1.4** ≥2 business-relevant queries answering the key questions | Done | Q7, Q8 |
| **1.4** For each query: SQL code | Done | `sql/04_queries.sql`, commented |
| **1.4** For each query: output/result screenshot | Partial | Full result sets in `reports/query_results.md` — **ACTION: screenshot your own run** |
| **1.4** For each query: 2–3 sentence business interpretation | See note | Present, but longer than 2–3 sentences — **see the note below** |

## General guidelines (Section 3.1)

| Requirement | Status |
| --- | --- |
| Arial 12pt | Done |
| 1-inch margins | Done |
| 1.5 line spacing | Done |
| Section headings clearly and consistently labelled | Done |
| Figures, tables and charts numbered and captioned | Done — 12 tables, 3 figures |
| Cover page: course code and title, project title, members and roles, submission date, academic year | Done — **ACTION: fill the blanks** |
| Dataset minimum 200 rows | Done — 1,194 rows |

## Submission requirements

| Requirement | Status |
| --- | --- |
| Printed and bound report (Tasks 1.1–1.4) | Ready to print — `reports/Checkpoint_1_Report.docx` |
| SQL script file (.sql) via class portal | Ready — `sql/01_schema_mysql.sql`, `sql/03_insert_data.sql`, `sql/04_queries.sql` |
| Signed Individual Contribution Form | Template at `reports/Form_A_Individual_Contribution.md` — **ACTION: complete and sign, one per member** |
| Deadline: end of Week 4 laboratory session | — |

## Note on the written interpretations

Section 3.2 of the brief states that **AI-generated analysis is not permitted**
and that insights must be derived by the students themselves. The business
interpretations currently in the report were drafted with AI assistance and
**must be rewritten by the group in their own words** before submission.

The underlying material is not affected by this: the query results in
`reports/query_results.md` are computed output, and the schema and SQL are
tooling. What must be your own is the *reading* of those numbers — the
"what this means for the business" prose under each query.

The rubric also asks for 2–3 sentences per query; the current drafts are
longer. Rewriting them shorter and in your own voice satisfies both points at
once. The instructor may ask any member to explain any part of the project, so
the group needs to be able to defend every claim regardless.

---

# Checkpoint 2 — Rubric Compliance Map

Requirements from the BED 106 brief for Checkpoint 2 (Midterm, Weeks 5–9,
100 points), mapped to where each is satisfied. **ACTION** marks what only the
group can supply.

## Task 2.1 — Spreadsheet Analytics Report

| Brief requirement | Status | Where |
| --- | --- | --- |
| Sheet 1 — Cleaned Data | Done | `Cleaned Data`, 1,194 rows × 19 columns |
| Sheet 2 — at least 3 pivot tables | Exceeded | `Pivot Analysis`, four cross-tabs |
| Sheet 3 — at least 3 pivot charts, titled, labelled, annotated | Exceeded | `Pivot Charts`, four charts |
| Sheet 4 — at least 5 Excel functions | Exceeded | `Formulas Showcase`, eight functions |
| Native PivotTable objects | See note | Cross-tabs are formula-driven; `docs/checkpoint2_excel_guide.md` §2 gives the procedure — **ACTION if your instructor wants the objects** |

## Task 2.2 — Descriptive Statistics

| Brief requirement | Status | Where |
| --- | --- | --- |
| At least 3 numerical variables | Done | Amount, Profit, Quantity |
| Mean, median, mode | Done | `Descriptive Stats` |
| Std deviation, variance, range, min, max | Done | `Descriptive Stats`, plus quartiles, IQR and coefficient of variation |
| Frequency distribution table | Done | `Frequency`, ten bins with a total check |
| Histogram for one key variable | Done | `Frequency`, Amount |
| One paragraph narrative per variable | Done | Report, Task 2.2 |

## Task 2.3 — Correlation Analysis

| Brief requirement | Status | Where |
| --- | --- | --- |
| Two pairs of variables | Exceeded | Two required pairs plus a supporting third |
| Pearson r via CORREL | Done | `Correlation` |
| Scatter plot with trendline | Done | Two scatter charts with linear trendlines, R² and equation displayed |
| Interpret direction, strength, business implication | Done | Report, Task 2.3 |

## Task 2.4 — Simple Linear Regression

| Brief requirement | Status | Where |
| --- | --- | --- |
| Regression equation Y = a + bX | Done | Revenue = −1,353.65 + 5,224.25 × Orders |
| Report and interpret R² | Done | 0.8514 |
| Test significance of the slope (p-value) | Done | t = 17.75, df = 55, p = 1.98 × 10⁻²⁴ |
| At least one business forecast | Exceeded | Four order volumes, plus the 250,000/year gap valuation |
| Discuss limitations and conditions | Done | Six numbered limitations |
| Data Analysis ToolPak | Partial | Computed with individual functions, which shows the working. ToolPak procedure and an expected-output table are in the Excel guide §3 — **ACTION: run it and screenshot** |

## Task 2.5 — Trend / Seasonality Analysis

| Brief requirement | Status | Where |
| --- | --- | --- |
| Plot data over time, identify trend pattern | Done | `Forecast` chart and Figure 4 |
| Project the next 3–6 periods | Done | Six periods, Jan–Jun 2025 |
| Discuss reliability and assumptions | Exceeded | Trend test shows no significant slope, so none is projected; forecast validated against two holdout months and honestly reported as *not* beating a flat average |

## General guidelines (Section 3.1)

| Requirement | Status |
| --- | --- |
| Arial 12pt, 1-inch margins, 1.5 spacing | Done |
| Figures and tables numbered and captioned | Done |
| Cover page complete | Done — **ACTION: fill the blanks** |
| Same dataset as Checkpoint 1 | Done — rebuilt from the same database |

## Submission requirements

| Requirement | Status |
| --- | --- |
| Printed report with interpretations and screenshots | Ready — `reports/Checkpoint_2_Report.docx` |
| Excel workbook (.xlsx) submitted digitally | Ready — `reports/Checkpoint_2_Workbook.xlsx` |
| Updated signed Individual Contribution Form | Template updated for CP2 — **ACTION: complete and sign** |
| Deadline: end of Week 9 laboratory session | — |

## Actions for the group

1. **Open the workbook in Excel and confirm all seven Read Me self-checks say
   OK.** It was built on Linux and has never been opened in Excel.
2. **Rewrite the interpretations in your own words** (Section 3.2), as with
   Checkpoint 1.
3. Fill the cover page blanks.
4. Screenshot your own outputs — the ToolPak regression especially.
5. Add native PivotTables if your instructor wants the objects (guide §2).
6. Complete and sign Form A for Checkpoint 2.

## Note on the Checkpoint 1 correction

Checkpoint 2 work surfaced an error in Checkpoint 1: 2020 was treated as a full
year when the file starts on 22 March, overstating 2020→2022 growth as 69.9%
when the like-for-like figure is 30.9%. Checkpoint 1 has been reissued with the
correction, a new `is_complete_month` flag, and a `revenue_per_month` column in
Q3. All other Checkpoint 1 findings are unaffected.

Section 3.4 of the brief allows Checkpoint 1 and 2 outputs to be revised and
resubmitted with Checkpoint 3, capped at 80/100. If Checkpoint 1 has already
been submitted and marked, ask the instructor whether to resubmit the corrected
version or simply note the correction in the Checkpoint 2 report — the
correction is already documented there either way.
