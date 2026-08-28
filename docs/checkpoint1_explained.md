# Checkpoint 1, Explained End to End

**BED 106 — Business Analytics · Mini Capstone · Sales Trend Analysis**

This document explains everything in Checkpoint 1: what each requirement asked
for, what we built, why each decision was made, and what every SQL query does
line by line.

Read it before the checkpoint. Section 1.4 of the project brief says *"the
instructor reserves the right to ask any member to explain any part of the
project"* — so every member needs to be able to answer from any section here,
not just their own role.

**Contents**

1. [What Checkpoint 1 is](#1-what-checkpoint-1-is)
2. [The files, and what each one does](#2-the-files-and-what-each-one-does)
3. [Task 1.1 — the business problem](#3-task-11--the-business-problem)
4. [Task 1.2 — the dataset](#4-task-12--the-dataset)
5. [Task 1.3 — the database design](#5-task-13--the-database-design)
6. [Task 1.4 — the eight queries, line by line](#6-task-14--the-eight-queries-line-by-line)
7. [SQL concepts used](#7-sql-concepts-used)
8. [The four findings and how we got them](#8-the-four-findings-and-how-we-got-them)
9. [Likely defense questions](#9-likely-defense-questions)
10. [Glossary](#10-glossary)

---

## 1. What Checkpoint 1 is

Checkpoint 1 is the **Preliminary** phase, Weeks 1–4, worth **100 of the 400**
capstone points. It assesses **CILO 1**: *apply data fundamentals, data quality
concepts, and SQL to extract, organize, and prepare business data for analysis.*

The idea is that you act as a junior data analyst who has been handed a raw
business dataset and must turn it into something a company could actually query.
That means four things, in order: decide what business question you are
answering, document and clean the data, put it in a properly designed database,
and then query it to produce insight.

### How the 100 points are split

| Criterion | Points | What the examiner looks for |
| --- | --- | --- |
| SQL Query Accuracy | **35** | All 8+ queries run without errors. SELECT, GROUP BY, JOIN and aggregates all present. Queries are relevant to the business problem. |
| Data Preparation | **25** | ERD with 2+ related tables, proper keys and data types. Database populated with clean data. Quality issues found *and resolved*. |
| Problem & Data Understanding | **20** | Business problem clearly defined with specific questions. Complete data dictionary and quality assessment. Scope appropriate. |
| Documentation | **20** | Organised, professional formatting. Screenshots labelled. SQL readable and commented. Interpretations insightful and accurate. |

Note where the marks actually are: **SQL accuracy and data preparation together
are 60% of the grade.** The writing is 40%. A common mistake is to spend all the
effort on prose and submit four queries that barely run.

### What must be submitted

- One printed and bound report covering Tasks 1.1–1.4.
- The SQL script file(s) via the class portal.
- A signed Individual Contribution Form **per member**.
- Deadline: end of the Week 4 laboratory session.

---

## 2. The files, and what each one does

```
data/raw/sales_dataset_raw.csv     The original file, never edited.
data/processed/*.csv               One cleaned CSV per database table.
data/sales_trend.db                A working SQLite copy (rebuilt, not committed).

sql/01_schema_mysql.sql            CREATE TABLE statements — the deliverable.
sql/01_schema_sqlite.sql           Same schema, SQLite syntax, for local testing.
sql/03_insert_data.sql             Generated INSERT statements to populate it.
sql/04_queries.sql                 The eight Task 1.4 queries.

scripts/clean_and_load.py          Cleans the raw file, builds the tables, loads them.
scripts/run_queries.py             Runs all 8 queries, writes the real results out.
scripts/make_figures.py            Draws the three charts.
scripts/build_docx.py              Renders the report into Word format.

docs/erd.md                        The Entity-Relationship Diagram.
docs/rubric_compliance.md          Every rubric line mapped to where it is met.
docs/figures/                      Figures 1–3.

reports/Checkpoint_1_Report.docx   The submission document.
reports/query_results.md           The actual output of all 8 queries.
reports/data_quality_report.md     Evidence for the Task 1.2 quality claims.
reports/Form_A_...md               Individual Contribution Form.
```

### Why there are scripts at all

We could have cleaned the data by hand in Excel. We didn't, for three reasons
worth being able to say out loud:

1. **Repeatability.** Anyone can run `python3 scripts/clean_and_load.py` and get
   byte-identical tables. Hand-editing cannot be checked or repeated.
2. **The raw file is never touched.** `data/raw/` is the evidence. Every
   transformation is a line of code you can point at.
3. **No typing errors in the report.** `run_queries.py` writes the result tables
   directly from the database, so a number in the report cannot drift from the
   number the query actually returned.

### The order things run in

```
sales_dataset_raw.csv
        │
        ▼  clean_and_load.py  ── cleans, splits into 7 tables, checks foreign keys
   sales_trend.db  +  data/processed/*.csv  +  sql/03_insert_data.sql
        │
        ▼  run_queries.py     ── executes sql/04_queries.sql
   reports/query_results.md
        │
        ▼  make_figures.py + build_docx.py
   the report
```

---

## 3. Task 1.1 — the business problem

### What was asked

A one-page problem statement giving the domain and specific problem, why it
matters, the key business questions, and the data source.

### The domain

**Retail & Sales Analytics** — an approved domain in Section 1.3 of the brief,
which lists "sales trends" as an example topic. A multi-category retailer
(electronics, furniture, office supplies) across six US states.

### The problem, and why it is framed this way

A weak problem statement says *"we want to analyse sales."* That is not a
problem, it is an activity. A strong one names something that is actually wrong
and that the data can settle.

Ours: **the company grew fast, then stopped, and nobody can say why.**

- Revenue rose **69.9%** from 2020 to 2022 (859,401 → 1,459,775).
- It then fell two years running, ending 2024 at **1,202,478** — **17.6% below
  the peak**.
- Margin never moved (23.97%–26.93% the whole time).

That last point is what makes it a real analytical problem rather than an
obvious one. If margin had collapsed, the answer would be "we are discounting
too hard" and you would not need a database. Because margin is *flat* while
revenue fell, something structural changed in what is being sold — and a single
company-wide revenue figure per year cannot tell you what.

### The three key business questions

Each one is answered by named queries. This matters: the rubric wants queries
"relevant to the business problem", so every question is traceable to SQL.

| # | Question | Answered by |
| --- | --- | --- |
| 1 | How have revenue and profit trended 2020–2024, and is the company still growing? | Q3, Figure 1 |
| 2 | Which categories and sub-categories drive the trend, and which reversed most recently? | Q5, Q7, Figure 3 |
| 3 | When does demand concentrate, and is the pattern the same for every category? | Q4, Q8, Figure 2 |

### Why the impact section uses numbers

"This will help the business decide better" is worth nothing. Every impact claim
in the report is quantified:

- The gap between the 2022 peak and 2024 is **257,297 per year**.
- October and December alone carry **21.7%** of annual revenue; January carries
  **4.72%**. Stocking to a flat monthly average therefore guarantees both
  stockouts and dead stock.

---

## 4. Task 1.2 — the dataset

### What was asked

A Data Source Report (name, source, date accessed, licence), a data dictionary,
a preliminary quality assessment, and a raw preview of 10–20 rows.

### The dataset

1,194 rows × 12 columns, one row per **product line on an order**, covering
**22 March 2020 to 15 March 2025**. The brief requires a minimum of 200 rows;
this clears it comfortably.

### The five quality problems we found

This is the section that earns Data Preparation marks, because the rubric asks
for issues *identified and resolved* — not just listed.

#### Problem 1 — `Order ID` is not unique, and cannot be a key

547 distinct Order ID values spread over 1,194 rows. That alone is normal: one
order can have several product lines. What is *not* normal is that **194 of
those IDs appear against more than one order date and a different customer**.

The first three rows of the raw file are the proof, and we put them in the
report deliberately:

| Order ID | Order Date | CustomerName | City |
| --- | --- | --- | --- |
| B-26776 | 2023-06-27 | David Padilla | Miami |
| B-26776 | 2024-12-27 | Connor Morgan | Chicago |
| B-26776 | 2021-07-25 | Robert Stone | Buffalo |

One "order", three dates, three customers, three states. It is not an order
identifier at all.

**Resolution.** We kept the value as a descriptive column called `order_ref` and
gave the fact table a **surrogate primary key**, `sale_id` — a simple counter
that is guaranteed unique. Explained further in §5.

#### Problem 2 — `CustomerName` is not an identifier either

802 distinct names, but **5 of them appear in more than one city**. If you key
customers on name alone you silently merge two different people.

**Resolution.** The customer business key is **(name, city)**. That is why
`dim_customer` has **807 rows** against 802 distinct names — the 5 extra rows
are those duplicated names correctly separated.

#### Problem 3 — `Year-Month` is redundant

The column holds `2023-06` where `Order Date` already holds `2023-06-27`. We
checked all 1,194 rows: **zero mismatches**. It is derivable, so storing it is
duplication — and duplicated data is where update anomalies come from.

**Resolution.** Dropped it; the calendar parts are recomputed in `dim_date`.

#### Problem 4 — 2025 is a partial year

The file stops on **15 March 2025**, giving only 44 rows for that year. Charted
naively, that looks like an 80% collapse in demand. It is a file cut-off.

**Resolution.** `dim_date` carries a flag, `is_complete_year`, set to 1 for
2020–2024 and 0 for 2025. Every trend query filters on it. This is the single
most important guard in the whole project — without it, every conclusion about
the trend would be wrong.

#### Problem 5 — the data is almost certainly synthetic

Worth stating because the rubric rewards honest assessment, and because it feeds
the Checkpoint 4 ethics section.

- **Zero loss-making transactions in five years.** Real retail always has
  returns, write-offs and discounted clearance.
- Profit never exceeds amount, and quantity is never zero or negative — too
  clean.
- The five payment methods split almost evenly (206–260 lines each). Real
  payment mix is never uniform.
- **22 of the 802 distinct customer names end in a credential suffix** (MD,
  DDS, PhD, Jr) — 10 of them "MD". That is the signature of the Python `Faker`
  library generating names like "Jason Smith MD", not a real customer list.
- US cities (Miami, Chicago, Buffalo) paired with **UPI and EMI** payment
  methods, which are Indian payment systems.

**Resolution.** We did not change the data — inventing "realistic" losses would
be data fabrication, which the brief calls grounds for a failing mark. Instead
the limitation is stated plainly in the report: the method is sound, the figures
should be presented as a modelling exercise.

> **This is also the answer to the customer-name privacy question.** The names
> are generated, so there is no data subject and no personal data. The reason is
> *"these names are synthetic"*, **not** *"it was public on Kaggle"* — public
> availability is not consent, and RA 10173 applies to personal data regardless
> of where you obtained it. Keep that distinction for Task 4.2.

### What "no missing values" means

All 12 columns are complete across all 1,194 rows. Say this explicitly rather
than skipping it — the rubric asks you to *identify* missing values, and
"we checked and there are none" is a finding.

---

## 5. Task 1.3 — the database design

### What was asked

An ERD with at least 2 related tables, correct data types and primary/foreign
keys, the cleaned data loaded, and screenshots.

We built **7 tables**. The minimum was 2.

### The shape: a star schema

```
dim_state ──< dim_city ──< dim_customer ──┐
                                          │
dim_category ──< dim_sub_category ────────┼──< fact_sales
                                          │
dim_payment_mode ─────────────────────────┤
                                          │
dim_date ─────────────────────────────────┘
```

One **fact table** in the middle holding the numbers, surrounded by **dimension
tables** holding the descriptive labels you slice those numbers by.

**Why this shape.** Look at the three business questions — each is "a *measure*,
broken down by a *dimension*, over *time*". Revenue by category by year. Revenue
by month. That is precisely the question shape a star schema is built for, and
each one is answered in a single join hop.

### Grain — the most important concept here

The **grain** is what exactly one row of the fact table represents. Ours:

> One row of `fact_sales` = one product line on one order.

Fix the grain before anything else, because every measure has to be additive at
that grain. `quantity`, `amount` and `profit` all are: summing them across any
group gives a meaningful total. If you mixed grains — some rows per order, some
per line — every SUM would be wrong.

### The seven tables

| Table | Rows | Primary key | Holds |
| --- | --- | --- | --- |
| `dim_state` | 6 | `state_id` | State names |
| `dim_city` | 18 | `city_id` | City, with FK to state |
| `dim_customer` | 807 | `customer_id` | Customer, with FK to city |
| `dim_category` | 3 | `category_id` | Electronics, Furniture, Office Supplies |
| `dim_sub_category` | 12 | `sub_category_id` | 12 sub-categories, FK to category |
| `dim_payment_mode` | 5 | `payment_mode_id` | COD, Credit Card, Debit Card, EMI, UPI |
| `dim_date` | 648 | `order_date` | One row per date, with year/quarter/month parts |
| `fact_sales` | 1,194 | `sale_id` | The transactions |

`fact_sales` has exactly the 1,194 rows of the raw file. **No transaction was
lost or invented in normalisation** — that is a checkable claim, and a good one
to state in the defense.

### Surrogate keys, and why we used one

A **natural key** is a key made of real data (Order ID). A **surrogate key** is
a meaningless number generated purely to identify the row (`sale_id` = 1, 2,
3…).

We used a surrogate because the natural key was broken (Problem 1). Being able
to explain *why* — "the natural key was not unique, so we introduced a
surrogate and kept the original as a descriptive attribute" — is exactly the
kind of thing the Data Preparation criterion rewards.

### Why geography and product are separate tables

We could have put `state` straight into `dim_customer` as text. Splitting into
`dim_state → dim_city → dim_customer` instead means:

- "Miami" is stored **once**, not on all 66 Miami transactions. If it is
  misspelled, you fix one row. This is what **normalisation** is for — removing
  the redundancy that causes update anomalies.
- It creates genuine multi-table joins for Task 1.4, which the rubric requires.

Same reasoning for `dim_category → dim_sub_category`.

### Why `dim_date` exists

We could read the year straight off `order_date` with MySQL's `YEAR()`
function. We built a date table instead because:

1. **`is_complete_year` needs somewhere to live.** The partial-2025 guard is a
   property of the calendar, so it belongs in the calendar table.
2. **Portability.** `YEAR()` is MySQL; SQLite uses `strftime()`. By storing
   `year_number` as a column, the same query file runs on both unchanged.
3. **Readability.** `WHERE d.year_number = 2024` reads better than
   `WHERE YEAR(f.order_date) = 2024`, and it can use an index.

### The constraints in the schema

The DDL is not just `CREATE TABLE`. It carries:

- `PRIMARY KEY` on every table — no duplicate rows possible.
- `FOREIGN KEY` on every relationship — you cannot insert a sale pointing at a
  customer who does not exist.
- `UNIQUE (city_name, state_id)` — a city name is only unique *within* a state.
- `CHECK (quantity > 0)`, `CHECK (amount >= 0)` — the database itself refuses
  impossible values.
- Indexes on `order_date`, `sub_category_id`, `customer_id`, `payment_mode_id`
  — the columns the queries filter and group by.

And after loading, the build runs a referential-integrity check and **fails**
if any foreign key is violated. Data quality is enforced, not hoped for.

---

## 6. Task 1.4 — the eight queries, line by line

### What was asked

Minimum 8 queries: ≥2 with `SELECT`/`WHERE`/`ORDER BY`, ≥2 with `GROUP BY` and
aggregates, ≥2 joining 2+ tables, ≥2 answering the key business questions. For
each: the SQL, the result, and a 2–3 sentence business interpretation.

> **Reminder.** The interpretations currently in the report were AI-drafted and
> must be rewritten in your own words before submission — Section 3.2 of the
> brief. This document explains what each query *does* and what the numbers
> *say*; the reading of them has to be yours.

---

### Group 1 — Basic Data Retrieval

#### Q1 — biggest transaction lines of 2024

```sql
SELECT sale_id, order_ref, order_date, quantity, amount, profit
FROM fact_sales
WHERE order_date >= '2024-01-01'
  AND order_date <= '2024-12-31'
ORDER BY amount DESC
LIMIT 15;
```

- `SELECT …` — the six columns we want back.
- `FROM fact_sales` — one table only; this is deliberately the simplest query.
- `WHERE … AND …` — restricts to the 2024 calendar year. Two conditions joined
  with `AND`, so both must be true.
- `ORDER BY amount DESC` — sorts biggest first. `DESC` = descending.
- `LIMIT 15` — return only the first 15 rows after sorting.

**What the result says.** The top 15 sit between **9,380 and 9,914**, against a
dataset-wide maximum of 9,992 — a hard ceiling near 10,000, not a long tail. So
no single large lost account could explain the revenue decline. Profit on those
near-identical revenues ranges from **414 to 4,339**, so revenue rank is a poor
guide to which orders are actually valuable.

#### Q2 — bulk orders sold at thin margins

```sql
SELECT sale_id, order_date, quantity, amount, profit,
       ROUND(100.0 * profit / amount, 2) AS margin_pct
FROM fact_sales
WHERE quantity >= 15
  AND profit < 0.15 * amount
ORDER BY margin_pct ASC, amount DESC
LIMIT 15;
```

- `ROUND(100.0 * profit / amount, 2) AS margin_pct` — a **calculated column**.
  Margin isn't stored; we compute it. `AS margin_pct` names the result.
- **Why `100.0` and not `100`?** With integers, SQL may do integer division and
  throw away the decimals. Writing `100.0` forces floating-point arithmetic.
  This is a classic exam question.
- `WHERE quantity >= 15 AND profit < 0.15 * amount` — bulk *and* thin margin.
  Note you can compare a column against an expression on other columns.
- `ORDER BY margin_pct ASC, amount DESC` — sort by margin ascending (worst
  first); **ties** broken by larger amount first.

**What the result says.** The worst line shipped 19 units for 7,702 revenue and
**60 profit — a 0.78% margin**. All 15 return under 3.7%. They appear in every
year from 2020 to 2024, so this is a standing pricing issue, *not* a cause of
the trend break.

---

### Group 2 — Aggregate Analysis

#### Q3 — annual sales trend (the headline query)

```sql
SELECT d.year_number AS year,
       COUNT(*)      AS transaction_lines,
       SUM(f.quantity) AS units_sold,
       ROUND(SUM(f.amount), 2) AS revenue,
       ROUND(SUM(f.profit), 2) AS profit,
       ROUND(AVG(f.amount), 2) AS avg_line_value,
       ROUND(100.0 * SUM(f.profit) / SUM(f.amount), 2) AS margin_pct
FROM fact_sales AS f
JOIN dim_date AS d ON d.order_date = f.order_date
WHERE d.is_complete_year = 1
GROUP BY d.year_number
ORDER BY d.year_number;
```

- `AS f`, `AS d` — **table aliases**, so you write `f.amount` not
  `fact_sales.amount`.
- `JOIN dim_date AS d ON d.order_date = f.order_date` — matches each sale to
  its calendar row. The `ON` clause is the matching rule.
- `WHERE d.is_complete_year = 1` — **the partial-2025 guard**. Without this line
  the chart shows a fake collapse.
- `GROUP BY d.year_number` — collapses all rows of a year into one output row.
- The aggregates: `COUNT(*)` counts rows, `SUM()` totals, `AVG()` averages.

**Rule to remember:** every column in the `SELECT` must either be inside an
aggregate function or listed in the `GROUP BY`.

**Note the margin calculation.** It is `SUM(profit) / SUM(amount)` — *not*
`AVG(margin_pct)`. Averaging percentages weights a 500-unit sale the same as a
5-unit one. Summing first is the correct weighting. Expect to be asked this.

**Result:**

| year | lines | units | revenue | profit | avg_line_value | margin_pct |
| --- | --- | --- | --- | --- | --- | --- |
| 2020 | 171 | 1,695 | 859,401 | 224,103 | 5,025.74 | 26.08 |
| 2021 | 217 | 2,358 | 1,181,446 | 283,231 | 5,444.45 | 23.97 |
| 2022 | 288 | 3,234 | 1,459,775 | 393,113 | 5,068.66 | 26.93 |
| 2023 | 234 | 2,497 | 1,229,723 | 321,671 | 5,255.23 | 26.16 |
| 2024 | 240 | 2,523 | 1,202,478 | 308,336 | 5,010.32 | 25.64 |

**What it says.** Growth stopped in 2022. The decisive detail is in the last two
columns: **average line value barely moved** (5,010–5,444, a 9% spread) while
**line count moved a lot** (171 → 288 → 240). The company is writing *fewer*
orders, not smaller or cheaper ones. That points the investigation at demand and
availability rather than pricing — and margin holding at 24–27% confirms
profitability per sale was never the issue.

#### Q4 — monthly seasonality

```sql
SELECT d.month_number AS month_no, d.month_name AS month,
       COUNT(*) AS transaction_lines,
       ROUND(SUM(f.amount), 2) AS revenue,
       ROUND(AVG(f.amount), 2) AS avg_line_value,
       ROUND(100.0 * SUM(f.amount) / (
           SELECT SUM(f2.amount) FROM fact_sales AS f2
           JOIN dim_date AS d2 ON d2.order_date = f2.order_date
           WHERE d2.is_complete_year = 1
       ), 2) AS pct_of_total_revenue
FROM fact_sales AS f
JOIN dim_date AS d ON d.order_date = f.order_date
WHERE d.is_complete_year = 1
GROUP BY d.month_number, d.month_name
ORDER BY d.month_number;
```

The new idea is the **scalar subquery** — the `SELECT` in brackets. It computes
one single number (total revenue across all complete years), and every row
divides by it to get its share. It needs its own aliases (`f2`, `d2`) and its
own `WHERE` filter so the denominator covers the same years as the numerator.

`GROUP BY d.month_number, d.month_name` groups on both because `month_name` is
in the `SELECT` and isn't aggregated.

**What it says.** December is **11.05%** of annual revenue and October
**10.66%** — together **21.7%**. January is the trough at **4.72%**, under 43%
of a December. But the peak is driven by **order count, not basket size**:
December has the most lines (133) at an average line value of 4,928, *below*
the annual averages in Q3. So Q4 is a throughput problem — more orders to pick
and ship — which means staffing and warehouse capacity, not premium stock.

---

### Group 3 — Multi-Table Joins

Both queries here join **four** tables; the requirement was two.

#### Q5 — revenue by category per year

```sql
FROM fact_sales AS f
JOIN dim_date         AS d ON d.order_date      = f.order_date
JOIN dim_sub_category AS s ON s.sub_category_id = f.sub_category_id
JOIN dim_category     AS c ON c.category_id     = s.category_id
WHERE d.is_complete_year = 1
GROUP BY c.category_name, d.year_number
```

Note the **chain**: `fact_sales` has no direct link to `dim_category`. It knows
its sub-category, and the sub-category knows its category. So you hop
`fact_sales → dim_sub_category → dim_category`. Being able to trace that path
is the point of the exercise.

**Result:**

| category | 2020 | 2021 | 2022 | 2023 | 2024 |
| --- | --- | --- | --- | --- | --- |
| Electronics | 233,178 | 387,757 | 478,451 | 538,319 | **318,630** |
| Furniture | 299,708 | 391,342 | 496,353 | 385,893 | 415,878 |
| Office Supplies | 326,515 | 402,347 | 484,971 | 305,511 | 467,970 |

**What it says.** The flat company total hides three different stories.
Electronics kept growing a year longer, peaking in 2023, then fell **40.8%**.
Office Supplies did the opposite — dropped in 2023, rebounded **53%** in 2024.
So the "plateau" is really an Electronics collapse nearly cancelled out by an
Office Supplies recovery. Managing to the aggregate number would have missed
both.

#### Q6 — top cities by revenue and revenue per customer

```sql
FROM fact_sales   AS f
JOIN dim_customer AS cu ON cu.customer_id = f.customer_id
JOIN dim_city     AS ci ON ci.city_id     = cu.city_id
JOIN dim_state    AS st ON st.state_id    = ci.state_id
GROUP BY st.state_name, ci.city_name
ORDER BY revenue DESC
LIMIT 10;
```

The other four-table chain, this time through geography. New idea:
`COUNT(DISTINCT cu.customer_id)` — counts *unique* customers, not rows. Without
`DISTINCT` a customer with three purchases would count three times, and
`revenue_per_customer` would be nonsense.

**What it says.** Geography is **not** the problem. Across six states revenue
spans only 884,768 (Ohio) to 1,130,048 (New York) — a 28% spread over five
years, which is remarkably even. The useful signal is per-customer value:
Orlando returns **9,829 per customer**, Buffalo only **7,216** from 26% more
customers. Buffalo's revenue costs more relationships to service. This
confirms the problem is national and product-driven — which is what makes Q7
the decisive query.

---

### Group 4 — Business-Relevant Insights

#### Q7 — which sub-categories caused the plateau (Question 2)

```sql
SUM(CASE WHEN d.year_number = 2023 THEN f.amount ELSE 0 END) AS revenue_2023,
SUM(CASE WHEN d.year_number = 2024 THEN f.amount ELSE 0 END) AS revenue_2024,
...
ROUND(100.0 * (SUM(CASE WHEN d.year_number = 2024 THEN f.amount ELSE 0 END)
             - SUM(CASE WHEN d.year_number = 2023 THEN f.amount ELSE 0 END))
     / NULLIF(SUM(CASE WHEN d.year_number = 2023 THEN f.amount ELSE 0 END), 0), 1)
```

The technique is **conditional aggregation** — the most useful trick in this
whole checkpoint.

`CASE WHEN … THEN … ELSE … END` is SQL's if-statement. Inside a `SUM()`, it adds
`f.amount` only when the year matches and adds `0` otherwise. Two of them side
by side turn *rows* (one per year) into *columns* (2023 and 2024 next to each
other) so you can subtract them on one line. This is called **pivoting**.

`NULLIF(x, 0)` returns `NULL` if `x` is zero, otherwise `x`. It is **division-by-zero
protection**: a sub-category with no 2023 revenue would crash the percentage
calculation; instead it returns `NULL` (shown as `—`).

**Result — the headline finding:**

| category | sub_category | 2023 | 2024 | change | % |
| --- | --- | --- | --- | --- | --- |
| Electronics | **Printers** | 192,817 | 55,952 | **−136,865** | **−71.0** |
| Electronics | Electronic Games | 144,484 | 88,017 | −56,467 | −39.1 |
| Electronics | Phones | 115,909 | 99,526 | −16,383 | −14.1 |
| Furniture | Bookcases | 86,730 | 74,875 | −11,855 | −13.7 |
| Electronics | Laptops | 85,109 | 75,135 | −9,974 | −11.7 |
| Furniture | Chairs | 87,711 | 86,185 | −1,526 | −1.7 |
| Furniture | Sofas | 92,052 | 98,984 | +6,932 | +7.5 |
| Office Supplies | Markers | 100,742 | 120,002 | +19,260 | +19.1 |
| Office Supplies | Binders | 64,442 | 88,011 | +23,569 | +36.6 |
| Office Supplies | Pens | 82,959 | 116,900 | +33,941 | +40.9 |
| Furniture | Tables | 119,400 | 155,834 | +36,434 | +30.5 |
| Office Supplies | **Paper** | 57,368 | 143,057 | **+85,689** | **+149.4** |

**What it says.** The plateau is not broad weakness — it is **concentrated in
one sub-category**. Printers alone lost **136,865**, more than half the entire
257,297 peak-to-2024 gap, and more than the next two decliners combined. All
four Electronics lines fell; all four Office Supplies lines grew.

The pattern suggests consumables growing while durable hardware falls away.
**The honest next step is to check 2024 Printer stock and supplier status before
concluding anything about demand** — a supply failure and a demand collapse look
identical in a sales table but need opposite responses. Saying this is a
strength, not a hedge: it shows you know what the data cannot tell you.

#### Q8 — is the Q4 peak universal? (Question 3)

```sql
ROUND(100.0 * SUM(f.amount) / SUM(SUM(f.amount)) OVER (
          PARTITION BY c.category_name), 2) AS pct_of_category_revenue
```

This uses a **window function** — the `OVER (…)` clause. A normal aggregate
collapses rows into one; a window function computes across a set of rows *while
keeping every row*. `PARTITION BY c.category_name` defines the window as "all
rows for this category".

So `SUM(SUM(f.amount)) OVER (PARTITION BY category)` is the category's total
across all quarters, available on each quarter's row — letting each quarter
express itself as a share of its **own** category rather than of the company.
The nested `SUM(SUM(...))` looks odd but is correct: the inner `SUM` is the
group aggregate, the outer one sums those group results across the window.

**Result:**

| category | Q1 | Q2 | Q3 | Q4 |
| --- | --- | --- | --- | --- |
| Electronics | 20.76% | **30.61%** | 23.55% | 25.09% |
| Furniture | 16.96% | 29.46% | 22.74% | **30.84%** |
| Office Supplies | 17.47% | 24.86% | 25.68% | **31.98%** |

**What it says.** The company-wide Q4 peak is **not universal**. Furniture and
Office Supplies peak in Q4 (30.8%, 32.0%). **Electronics does not** — it peaks
in **Q2** at 30.61%, and Q4 is only its second-best quarter. Planning
Electronics stock against the blended company curve therefore over-stocks it in
Q4 and under-stocks it in Q2, every single year. The recommendation is
per-category seasonal curves. Q1 is weakest for all three (17–21%), so it is the
natural clearance window.

---

## 7. SQL concepts used

Quick reference for anything you might be asked to define.

| Concept | What it does | Where |
| --- | --- | --- |
| `SELECT` | Chooses which columns to return | All |
| `WHERE` | Filters **rows**, before grouping | Q1–Q7 |
| `ORDER BY` | Sorts the result. `ASC` / `DESC` | Q1, Q2, Q6 |
| `LIMIT` | Caps the number of rows returned | Q1, Q2, Q6 |
| `JOIN … ON` | Combines tables on a matching rule | Q3–Q8 |
| `GROUP BY` | Collapses rows into one per group | Q3–Q8 |
| `COUNT(*)` | Counts rows in each group | Q3–Q8 |
| `COUNT(DISTINCT x)` | Counts *unique* values | Q6 |
| `SUM` / `AVG` | Totals / averages a column | Q3–Q8 |
| `ROUND(x, 2)` | Rounds to 2 decimal places | Most |
| Table alias (`AS f`) | Short name for a table | Q3–Q8 |
| Calculated column | A value computed, not stored | Q2 |
| Scalar subquery | An inner query returning one value | Q4 |
| `CASE WHEN` | SQL's if-statement | Q7 |
| Conditional aggregation | `SUM(CASE WHEN …)` to pivot rows into columns | Q7 |
| `NULLIF(x, 0)` | Division-by-zero guard | Q7 |
| Window function `OVER (PARTITION BY …)` | Aggregates across rows without collapsing them | Q8 |

### Three things people get wrong

1. **`WHERE` vs `HAVING`.** `WHERE` filters rows *before* grouping; `HAVING`
   filters groups *after*. We only needed `WHERE`.
2. **Integer division.** `100 * profit / amount` can truncate to whole numbers.
   Always write `100.0`.
3. **Averaging percentages.** `SUM(profit)/SUM(amount)` is right;
   `AVG(margin_pct)` is wrong because it ignores the size of each sale.

### Join types (you may be asked)

- **INNER JOIN** (what plain `JOIN` means) — keeps only rows that match on both
  sides. All ours are inner joins, which is safe here because foreign keys
  guarantee every fact row has a matching dimension row.
- **LEFT JOIN** — keeps every row from the left table even without a match,
  filling the right side with `NULL`. You would need this if, say, you wanted
  categories with zero sales in a period to still appear.

---

## 8. The four findings and how we got them

| # | Finding | How we know |
| --- | --- | --- |
| 1 | **Growth stopped in 2022.** 2024 is 17.6% below peak, but margin and average order value never moved — fewer orders, not worse ones. | Q3: revenue by year alongside `AVG(amount)` and margin. The flatness of the last two columns is the evidence. |
| 2 | **One sub-category explains most of it.** Printers lost 136,865, over half the whole gap. | Q7: conditional aggregation comparing 2023 with 2024 for all 12 sub-categories, ranked by change. |
| 3 | **Seasonality is category-specific.** Electronics peaks Q2; Furniture and Office Supplies peak Q4. | Q8: window function giving each quarter's share of its own category, which exposes what the company-wide average in Q4 hides. |
| 4 | **Geography is not a factor.** State revenue spans only 28% over five years. | Q6: revenue by city and state; the narrow spread is the finding. |

Notice that findings 1 and 3 both come from **comparing a breakdown against an
average**. That is the core analytical move in this project: an aggregate hides
variation, and the insight is in the variation.

### The recommended next step

Verify the Printer supply hypothesis against stock and supplier records, then
model monthly revenue with per-category seasonal terms rather than one blended
index. That carries directly into Checkpoint 2's regression and forecasting work.

---

## 9. Likely defense questions

**Why a star schema and not one flat table?**
The business questions are all "a measure by a dimension over time", which a
star answers in one join. A flat table repeats "Miami" on all 66 Miami rows —
redundancy that causes update anomalies. Splitting stores each label once.

**Why is `Order ID` not your primary key?**
Because it isn't unique in a usable way: 194 of the 547 values appear against
different dates *and* different customers. The first three rows of the raw file
show one ID across three dates, three customers and three states. We kept it as
`order_ref` and used a surrogate `sale_id`.

**Why does `dim_customer` have 807 rows when there are 802 names?**
Five names appear in more than one city. Keying on name alone would merge two
different people, so the key is (name, city), which correctly splits those five.

**Why exclude 2025?**
The file stops on 15 March 2025 — 44 rows. Including it shows a fake ~80%
collapse. `dim_date.is_complete_year` fences it off so a file cut-off is never
read as a business event.

**Your dataset looks fake. Doesn't that invalidate the project?**
It invalidates the *figures*, not the *method*. We state it plainly: zero
loss-making lines in five years, a near-uniform payment split, and 22 names
ending in a credential suffix, which is a `Faker` artifact. We did not fabricate corrections,
because that would be worse. The schema, queries and analysis method are all
valid and would run identically on real data.

**What is the difference between `WHERE` and `HAVING`?**
`WHERE` filters individual rows before grouping. `HAVING` filters whole groups
after grouping. To keep only years above 1,000,000 in revenue you would need
`HAVING SUM(amount) > 1000000`, because the sum doesn't exist yet at `WHERE` time.

**Why `SUM(profit)/SUM(amount)` instead of `AVG(margin)`?**
Averaging percentages treats a 20-unit sale and a 1-unit sale as equally
important. Summing first weights each sale by its actual size.

**How do you know Printers is the cause and not just correlated?**
We don't — and we say so. Q7 establishes *where* the revenue went, not *why*.
Both a supply failure and a demand collapse produce this exact signature, so the
report recommends checking stock and supplier records before concluding.

**What would you do differently with more time?**
Get a dataset with returns and loss-making orders so margin analysis is
meaningful, and obtain inventory data so the Printer question could actually be
settled rather than flagged.

---

## 10. Glossary

**Aggregate function** — a function that turns many rows into one value:
`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`.

**Cardinality** — how many rows on one side of a relationship relate to the
other. Ours are all one-to-many.

**Conditional aggregation** — `SUM(CASE WHEN … THEN … END)`, used to turn rows
into columns (pivoting).

**Data dictionary** — the table listing every column with its type and meaning.

**Dimension table** — a table of descriptive attributes you slice measures by
(customer, product, date).

**ERD** — Entity-Relationship Diagram; the picture of tables and their links.

**Fact table** — the central table holding the numeric measures.

**Foreign key (FK)** — a column pointing at another table's primary key. Stops
you inserting a sale for a customer who doesn't exist.

**Grain** — what one row of the fact table represents. Ours: one product line
on one order.

**Join** — combining tables on a matching rule.

**Natural key** — a key made from real data (Order ID). **Surrogate key** — a
meaningless generated number (`sale_id`).

**Normalisation** — removing redundancy by splitting data into related tables so
each fact is stored once.

**Primary key (PK)** — the column uniquely identifying each row.

**Referential integrity** — the guarantee that every foreign key points at a row
that actually exists.

**Star schema** — one fact table surrounded by dimension tables.

**Window function** — an aggregate computed across a set of rows *without*
collapsing them, written with `OVER (PARTITION BY …)`.
