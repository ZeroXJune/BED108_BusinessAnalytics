# BED 106 Business Analytics — Mini Capstone: Sales Trend Analysis

A sales-trend study of a multi-category US retailer, 2020–2025.
Checkpoints 1 and 2 of 4 are complete.

| Checkpoint | Phase | Deliverables |
| --- | --- | --- |
| **CP1** — Data Fundamentals & SQL | Preliminary | [Report](reports/Checkpoint_1_Report.docx) · [SQL](sql/) · [ERD](docs/erd.md) · [Explainer](docs/Checkpoint_1_Explained.docx) |
| **CP2** — Spreadsheet & Statistics | Midterm | [Report](reports/Checkpoint_2_Report.docx) · [Workbook](reports/Checkpoint_2_Workbook.xlsx) · [Excel guide](docs/checkpoint2_excel_guide.md) · [Explainer](docs/Checkpoint_2_Explained.docx) |
| CP3 — BI Dashboard | Semi-Final | not started |
| CP4 — Predictive & Defense | Final | not started |

> ### Read before submitting
>
> Section 3.2 of the BED 106 project brief states that **AI-generated analysis
> is not permitted** and that insights must be derived by the students
> themselves. The business interpretations in this report were drafted with AI
> assistance and **must be rewritten by the group in their own words**.
>
> The rest is unaffected: the query results are computed output, and the schema
> and SQL are tooling. What has to be yours is the *reading* of the numbers.
> The rubric also asks for 2–3 sentences per query and the current drafts run
> longer — rewriting them shorter and in your own voice fixes both at once.
> Full detail in [`docs/rubric_compliance.md`](docs/rubric_compliance.md).

**Understanding it:** [`docs/checkpoint1_explained.md`](docs/checkpoint1_explained.md)
(also as `docs/Checkpoint_1_Explained.docx`) explains every part of Checkpoint 1
— the rubric, every file, every design decision, all eight queries line by line,
and likely defense questions. Read it before the checkpoint: Section 1.4 of the
brief lets the instructor ask any member to explain any part of the project.

## Headline findings

| # | Finding | Evidence |
| --- | --- | --- |
| 1 | Growth stopped in 2022. Revenue per month is 17.6% below peak, but margin (24–27%) and average order value (5,008–5,444) never moved — the company writes **fewer** orders, not worse ones. | Q3 |
| 2 | One sub-category explains most of it: **Printers lost 136,865** between 2023 and 2024 — over half the entire peak-to-2024 gap. All Electronics fell; all Office Supplies grew. | Q5, Q7 |
| 3 | Seasonality is **category-specific**: Electronics peaks in Q2, Furniture and Office Supplies in Q4. The single blended planning curve is wrong for all three. | Q4, Q8 |
| 4 | Geography is not a factor — state revenue spans only 28% across five years. | Q6 |
| 5 | **Order count drives revenue**, now proven not inferred: r = 0.923, R² = 0.851, p < 0.001 over 57 months. | CP2 regression |
| 6 | **Units sold predicts nothing** (r = 0.045, p = 0.123). Volume-based targets would not move revenue. | CP2 correlation |
| 7 | **No linear trend exists** to project — time explains under 1% of variation (p = 0.515). The series is growth then plateau. | CP2 trend test |

## Repository layout

```
data/raw/          sales_dataset_raw.csv     the source export, unmodified
data/processed/    one CSV per table         cleaned, normalised output
data/sales_trend.db                          populated SQLite build (generated)
sql/02_mysql_full_import.sql                 ONE-FILE IMPORT: database + tables + data
sql/01_schema_mysql.sql                      DDL for MySQL 8 (the deliverable)
sql/01_schema_sqlite.sql                     mirror used for the local run
sql/03_insert_data.sql                       generated INSERT statements
sql/04_queries.sql                           the 8 Task 1.4 queries
sql/05_screenshot_queries.sql                run-in-order script for screenshots
scripts/clean_and_load.py                    clean → normalise → load → verify
scripts/run_queries.py                       run all queries, capture results
scripts/make_figures.py                      regenerate the report charts
scripts/build_docx.py                        render the report to .docx
docs/erd.md                                  ERD (image + Mermaid source)
docs/figures/erd.png|.svg                    rendered ERD for the report
scripts/make_erd.py                          generates the ERD from the schema
docs/figures/                                Figures 1–3
reports/                                     report, query results, QA evidence
reports/Form_A_Individual_Contribution.docx  printable form, 4 signable copies
docs/project_explained.md                    EVERYTHING explained in one document
docs/methodology_explained.md                WHY each method was chosen, with the alternatives measured
docs/contribution_guide.md                   what each role did, for filling in Form A
scripts/build_form_a.py                      builds the contribution form
```

## Reproducing everything

No third-party packages are needed for the data pipeline — only the figures and
the Word build need `matplotlib` and `python-docx`.

```bash
python3 scripts/clean_and_load.py   # clean, load, verify referential integrity
python3 scripts/run_queries.py      # → reports/query_results.md
python3 scripts/make_figures.py     # → docs/figures/*.png
python3 scripts/build_docx.py       # → reports/Checkpoint_1_Report.docx
```

### Loading it into MySQL

One file creates the database, all 8 tables and all the data:

```bash
mysql -u root -p < sql/02_mysql_full_import.sql
```

In phpMyAdmin: *Import* tab → choose `sql/02_mysql_full_import.sql` → *Go*.
Nothing needs to exist first. The file ends with a verification block whose
last row must read `1194 | 6182639.00 | 547 | 57 | 0 | 0`.

Then run the analysis queries:

```bash
mysql -u root -p sales_trend < sql/04_queries.sql
```

The modular route still works — `01_schema_mysql.sql` then
`03_insert_data.sql` — but the insert file carries no `USE` statement so that
it also runs on SQLite, so name the database on the command line.

**Verified, not assumed:** the import and all sixteen screenshot blocks were
executed against a real MariaDB 10.11 server. The schema creates 8 primary
keys, 7 foreign keys, 6 unique constraints and 4 check constraints, and both
constraint types were confirmed to reject invalid rows.

The queries avoid dialect-specific date functions (calendar parts come from
`dates`), so the same `04_queries.sql` runs unchanged on MySQL 8 and SQLite 3.

## Schema

Star schema, 8 tables (1 fact + 7 dimensions), grain of one transaction line. Full ERD in
[`docs/erd.md`](docs/erd.md).

```
states ──< cities ──< customers ──┐
categories ──< sub_categories ────────┼──< sales
payment_modes ─────────────────────────┤
dates ─────────────────────────────────┘
```

Two decisions worth knowing before reading the SQL:

- **`Order ID` is not a primary key.** 547 distinct values cover 1,194 rows and
  194 of them recur against different dates *and* different customers. It is
  kept as the descriptive column `order_ref`; the fact table is keyed on the
  surrogate `sale_id`.
- **Both ends of the series are partial.** The file runs 22 March 2020 to
  15 March 2025, so 2025 is a part-year, 2020 is a *nine-month* year, and
  March 2020 and March 2025 are part-months. `dates` carries
  `is_complete_year` and `is_complete_month`; the analysis window is the 57
  complete months from April 2020 to December 2024. Q3 also reports
  `revenue_per_month` so the short 2020 cannot be compared unfairly against a
  full year.

## Before you submit

Full checklist in [`docs/rubric_compliance.md`](docs/rubric_compliance.md).
The five things only the group can supply:

1. **Rewrite the business interpretations in your own words** (see the notice
   above) and trim each to the 2–3 sentences the rubric asks for.
2. Fill in the cover page: group name/number, submission date, member names.
3. Confirm the dataset's exact licence on its source page and record it in the
   Task 1.2 table.
4. Take your own screenshots: run `sql/05_screenshot_queries.sql` block by block
   and follow [`docs/screenshot_guide.md`](docs/screenshot_guide.md), which maps
   each block to its report slot and gives the result to expect.
5. Complete and sign `reports/Form_A_Individual_Contribution.md`, one per
   member. This is required with every checkpoint.

The repository folder is named `BED108_BusinessAnalytics`, but the course is
**BED 106** per the project brief. The folder name is cosmetic; every document
and SQL header now says BED 106.

## Limitation

The source file contains no loss-making transactions across five years, profit
never exceeds amount, and the five payment methods split almost evenly. Real
retail data of this size would carry returns and discounts, so this dataset is
very likely synthetic or pre-filtered. The schema, queries and method are sound;
the specific figures should be presented as a modelling exercise, not as a real
company's trading results. This is stated in the report itself.
