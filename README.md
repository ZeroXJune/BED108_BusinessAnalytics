# BED 106 Business Analytics — Mini Capstone: Sales Trend Analysis

Checkpoint 1 (Data Fundamentals & SQL Querying) for a sales-trend study of a
multi-category US retailer, 2020–2025.

**Deliverable:** [`reports/Checkpoint_1_Report.docx`](reports/Checkpoint_1_Report.docx)
— the supplied template filled in end to end.
Markdown source: [`reports/Checkpoint_1_Report.md`](reports/Checkpoint_1_Report.md).

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
| 1 | Growth stopped in 2022. Revenue is 17.6% below peak, but margin (24–27%) and average order value (5,010–5,444) never moved — the company writes **fewer** orders, not worse ones. | Q3 |
| 2 | One sub-category explains most of it: **Printers lost 136,865** between 2023 and 2024 — over half the entire peak-to-2024 gap. All Electronics fell; all Office Supplies grew. | Q5, Q7 |
| 3 | Seasonality is **category-specific**: Electronics peaks in Q2, Furniture and Office Supplies in Q4. The single blended planning curve is wrong for all three. | Q4, Q8 |
| 4 | Geography is not a factor — state revenue spans only 28% across five years. | Q6 |

## Repository layout

```
data/raw/          sales_dataset_raw.csv     the source export, unmodified
data/processed/    one CSV per table         cleaned, normalised output
data/sales_trend.db                          populated SQLite build (generated)
sql/01_schema_mysql.sql                      DDL for MySQL 8 (the deliverable)
sql/01_schema_sqlite.sql                     mirror used for the local run
sql/03_insert_data.sql                       generated INSERT statements
sql/04_queries.sql                           the 8 Task 1.4 queries
scripts/clean_and_load.py                    clean → normalise → load → verify
scripts/run_queries.py                       run all queries, capture results
scripts/make_figures.py                      regenerate the report charts
scripts/build_docx.py                        render the report to .docx
docs/erd.md                                  ERD (Mermaid, renders on GitHub)
docs/figures/                                Figures 1–3
reports/                                     report, query results, QA evidence
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

To build in MySQL instead:

```bash
mysql -u root -p < sql/01_schema_mysql.sql
mysql -u root -p sales_trend < sql/03_insert_data.sql
mysql -u root -p sales_trend < sql/04_queries.sql
```

The queries avoid dialect-specific date functions (calendar parts come from
`dim_date`), so the same `04_queries.sql` runs unchanged on MySQL 8 and SQLite 3.

## Schema

Star schema, 7 tables, grain of one transaction line. Full ERD in
[`docs/erd.md`](docs/erd.md).

```
dim_state ──< dim_city ──< dim_customer ──┐
dim_category ──< dim_sub_category ────────┼──< fact_sales
dim_payment_mode ─────────────────────────┤
dim_date ─────────────────────────────────┘
```

Two decisions worth knowing before reading the SQL:

- **`Order ID` is not a primary key.** 547 distinct values cover 1,194 rows and
  194 of them recur against different dates *and* different customers. It is
  kept as the descriptive column `order_ref`; the fact table is keyed on the
  surrogate `sale_id`.
- **2025 is a partial year** — the file stops on 15 March 2025. Every trend
  query filters on `dim_date.is_complete_year = 1` so the cut-off is never
  misread as a collapse in demand.

## Before you submit

Full checklist in [`docs/rubric_compliance.md`](docs/rubric_compliance.md).
The five things only the group can supply:

1. **Rewrite the business interpretations in your own words** (see the notice
   above) and trim each to the 2–3 sentences the rubric asks for.
2. Fill in the cover page: group name/number, submission date, member names.
3. Confirm the dataset's exact licence on its source page and record it in the
   Task 1.2 table.
4. Take your own screenshots of the schema, populated tables and query results
   in phpMyAdmin or MySQL Workbench — the full result sets are already in the
   report, but the brief asks for screenshots of *your* run.
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
