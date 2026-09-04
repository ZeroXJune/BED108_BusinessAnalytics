# Sales Trend Analysis — The Project Explained

**BED 106 — Business Analytics · Mini Capstone**
**Talibon Polytechnic College · A.Y. 2026–2027, 1st Semester**

Everything in Checkpoints 1 and 2 in one document: what was asked, what was
built, what every number means, and how to defend it.

Section 1.4 of the brief lets the instructor ask **any member** to explain
**any part** of the project. This is written so that any member can.

**Contents**

- [Part 0 — The project at a glance](#part-0--the-project-at-a-glance)
- [Part 1 — Checkpoint 1: Data Fundamentals & SQL](#part-1--checkpoint-1-data-fundamentals--sql)
- [Part 2 — Checkpoint 2: Spreadsheet & Statistics](#part-2--checkpoint-2-spreadsheet--statistics)
- [Part 3 — Reference](#part-3--reference)
- [Part 4 — Everything we found](#part-4--everything-we-found)
- [Part 5 — Defense questions](#part-5--defense-questions)
- [Part 6 — Glossary](#part-6--glossary)

---

# Part 0 — The project at a glance

## The business

A multi-category retailer — electronics, furniture, office supplies — trading
across six US states. **Retail & Sales Analytics** is an approved domain in
Section 1.3 of the brief, and "sales trends" is listed under it.

## The dataset

1,194 transaction lines, one row per product line on an order, covering
**22 March 2020 to 15 March 2025**. The brief requires a minimum of 200 rows.

## The problem being investigated

The company grew, then stopped. On a like-for-like monthly basis revenue rose
**30.9%** from 2020 to the 2022 peak, then fell two years running to finish
2024 **17.6% below** that peak.

What makes this a real analytical problem rather than an obvious one:
**margin never moved.** It held between 23.97% and 26.93% throughout. Had
margin collapsed, the answer would be "we are discounting too hard" and no
database would be needed. Because margin held steady while revenue fell,
something structural changed in *what was being sold* — and a single
company-wide revenue figure per year cannot tell you what.

## The three key business questions

| # | Question | Answered by |
| --- | --- | --- |
| 1 | How have revenue and profit trended, and is the company still growing? | Q3, and the CP2 regression |
| 2 | Which categories and sub-categories drive the trend? | Q5, Q7 |
| 3 | When does demand concentrate, and is the pattern the same for every category? | Q4, Q8 |

## How the two checkpoints fit together

**Checkpoint 1** built a database and asked *what happened*. **Checkpoint 2**
took the same data into Excel and asked *how strong is the evidence, and what
can we predict*. The brief requires the same dataset for both.

Two Checkpoint 2 results confirm Checkpoint 1 by a completely different route,
and one of them **corrected** it — see [Part 4](#part-4--everything-we-found).

---

# Part 1 — Checkpoint 1: Data Fundamentals & SQL

## What it is

The **Preliminary** phase, Weeks 1–4, **100 points**, assessing **CILO 1**:
*apply data fundamentals, data quality concepts, and SQL to extract, organize
and prepare business data for analysis.*

| Criterion | Points |
| --- | --- |
| SQL Query Accuracy | **35** |
| Data Preparation | **25** |
| Problem & Data Understanding | **20** |
| Documentation | **20** |

**Where the marks actually are:** SQL accuracy and data preparation together
are **60%**. The writing is 40%. A common mistake is to polish the prose and
submit queries that barely run.

## The files

```
data/raw/sales_dataset_raw.csv     the original file, never edited
sql/02_mysql_full_import.sql       ONE FILE: database + tables + data
sql/01_schema_mysql.sql            the schema on its own
sql/04_queries.sql                 the eight queries
sql/05_screenshot_queries.sql      run-in-order script for screenshots
scripts/clean_and_load.py          cleans, normalises, loads, verifies
docs/figures/erd.png               the ERD
reports/Checkpoint_1_Report.docx   the submission
```

**Why the pipeline is scripted rather than hand-edited.** Three reasons worth
being able to say: anyone can re-run it and get identical tables; the raw file
is never touched, so every transformation is a line of code you can point at;
and the report's numbers are written straight from the database, so they cannot
drift from what the queries return.

## Task 1.1 — the business problem

Covered in [Part 0](#part-0--the-project-at-a-glance). The impact section is
quantified rather than asserted: the gap between the 2022 peak and 2024 is
**257,297 per year**, and October plus December carry **21.8%** of annual
revenue against the 16.7% two average months would give.

## Task 1.2 — the dataset and its five problems

This is where the Data Preparation marks sit, because the rubric asks for
issues **identified and resolved**.

### Problem 1 — `Order ID` cannot be a primary key

547 distinct values over 1,194 rows. That alone is normal — one order can have
several lines. What is not normal is that **194 of those IDs appear against
more than one order date and a different customer.**

The first three rows of the raw file are the proof:

| Order ID | Order Date | CustomerName | City |
| --- | --- | --- | --- |
| B-26776 | 2023-06-27 | David Padilla | Miami |
| B-26776 | 2024-12-27 | Connor Morgan | Chicago |
| B-26776 | 2021-07-25 | Robert Stone | Buffalo |

One "order", three dates, three customers, three states.

**Resolved:** kept as the descriptive column `order_ref`; the fact table is
keyed on a **surrogate key**, `sale_id`.

### Problem 2 — `CustomerName` is not an identifier either

802 distinct names, but **5 appear in more than one city**. Keying on name
alone would silently merge two different people.

**Resolved:** the customer key is **(name, city)**. That is why `customers` has
**807 rows** against 802 names — the 5 extra are those duplicates correctly
separated.

### Problem 3 — `Year-Month` is redundant

It holds `2023-06` where `Order Date` already holds `2023-06-27`. Checked
across all 1,194 rows: **zero mismatches**. Storing it twice is duplication,
and duplicated data is where update anomalies come from.

**Resolved:** dropped; the calendar parts are recomputed in `dates`.

### Problem 4 — both ends of the file are partial

The file runs 22 March 2020 to 15 March 2025. **Three separate traps:**

1. **2025 is a partial year** — 44 rows. Charted naively it looks like an 80%
   collapse in demand. It is a file cut-off.
2. **2020 is a nine-month year.** Comparing its part-year total against a full
   2021 overstates growth: raw totals suggest **69.9%**, the like-for-like
   figure is **30.9%**.
3. **March 2020 and March 2025 are part-months.** March 2020 holds ten days.
   Dropping a ten-day month into a monthly average pulls March's seasonal index
   from 1.025 to 0.876 — a 15% distortion.

**Resolved:** `dates` carries two flags, `is_complete_year` and
`is_complete_month`. The analysis window is the **57 whole months, April 2020
to December 2024**. Q3 also reports `months_covered` and `revenue_per_month` so
the short year is visible in the table rather than hidden in a total.

> Trap 2 was found *during Checkpoint 2* and is a correction to Checkpoint 1.
> See [Part 4](#part-4--everything-we-found).

### Problem 5 — the dataset is synthetic

Four machine-checked signals:

1. **Zero loss-making lines** across 1,194 rows and five years. Real retail
   carries returns, write-offs and clearance.
2. **22 of the 802 distinct customer names end in a credential suffix**
   (MD, DDS, PhD, Jr) — the signature of the `Faker` name generator, not a real
   customer list.
3. **US cities paired with UPI and EMI** payment methods — Indian payment
   systems a Miami retailer would not offer.
4. **Near-uniform payment mix** — 206 to 260 lines across five methods. Real
   payment mix is never that even.

A fifth signal turns up in Checkpoint 2: the histogram of Amount is flat rather
than bell-shaped.

**Resolved:** documented, not "corrected". Inventing realistic losses would be
data fabrication, which the brief calls grounds for a failing mark. The method
is sound; the figures should be presented as a modelling exercise.

> **This also settles the privacy question.** The names are generated, so there
> is no data subject and no personal data, and R.A. 10173 is not engaged. The
> reason is that the names are **synthetic** — *not* that the file was publicly
> downloadable. Public availability is not consent. Keep that distinction for
> Checkpoint 4.

### On missing values

There are none — all 12 columns complete across all 1,194 rows. Say so
explicitly. The rubric asks you to *identify* missing values, and "we checked
and there are none" is a finding.

## Task 1.3 — the database

### The shape: a star schema, 8 tables

```
states ──< cities ──< customers ──┐
categories ──< sub_categories ────┼──< sales
payment_modes ────────────────────┤
dates ────────────────────────────┘
```

One **fact table** holding the numbers, seven **dimension tables** holding the
labels you slice them by.

| Table | Rows | Primary key | Holds |
| --- | --- | --- | --- |
| `states` | 6 | `state_id` | State names |
| `cities` | 18 | `city_id` | City, FK to state |
| `customers` | 807 | `customer_id` | Customer, FK to city |
| `categories` | 3 | `category_id` | Electronics, Furniture, Office Supplies |
| `sub_categories` | 12 | `sub_category_id` | 12 sub-categories, FK to category |
| `payment_modes` | 5 | `payment_mode_id` | COD, Credit Card, Debit Card, EMI, UPI |
| `dates` | 648 | `order_date` | One row per date, calendar parts precomputed |
| `sales` | 1,194 | `sale_id` | The transactions |

The tables are named plainly rather than with `fact_`/`dim_` prefixes, but the
roles are unchanged:

| Role | Which | The test |
| --- | --- | --- |
| **Fact** | `sales` | Its numbers add up meaningfully — `SUM(amount)` is total revenue |
| **Dimension** | the other seven | They describe and label — summing `customer_id` is nonsense |

### Grain — the most important concept here

> One row of `sales` = one product line on one order.

Fix the grain before anything else, because every measure must be additive at
that grain. `quantity`, `amount` and `profit` all are. Mixing grains — some
rows per order, some per line — would make every `SUM` wrong.

### Why the design is the way it is

**Why a star schema.** Every business question has the shape "a measure, by a
dimension, over time" — revenue by category by year, revenue by month. That is
precisely what a star answers in a single join hop.

**Why a surrogate key.** A *natural* key is made of real data (`Order ID`); a
*surrogate* key is a meaningless generated number (`sale_id`). We used a
surrogate because the natural key was broken. Being able to say "the natural key
was not unique, so we introduced a surrogate and kept the original as a
descriptive attribute" is exactly what the Data Preparation criterion rewards.

**Why geography and product are separate tables.** "Miami" is stored once
rather than on all 66 Miami transactions. That is what **normalisation** is for
— removing the redundancy that causes update anomalies. It also creates genuine
multi-table joins for Task 1.4.

**Why `dates` exists.** Three reasons: the completeness flags are properties of
the calendar so they belong there; storing `year_number` as a column keeps the
queries free of dialect-specific functions like `YEAR()` or `strftime()`, so the
same file runs on MySQL and SQLite; and `WHERE d.year_number = 2024` reads
better than `WHERE YEAR(f.order_date) = 2024` and can use an index.

### The constraints

Not just `CREATE TABLE` — **8 primary keys, 7 foreign keys, 6 unique
constraints and 4 check constraints**, plus four indexes on the columns the
queries filter and group by. All verified on a live MySQL-compatible server,
and both foreign keys and check constraints were confirmed to *reject* invalid
rows rather than merely existing.

After loading, the build runs a referential-integrity check and **fails** if any
foreign key is violated. Data quality is enforced, not hoped for.

### One SQL trap worth knowing

`year_month` is a **reserved word** in MySQL and MariaDB — it is the unit in
`INTERVAL 1 YEAR_MONTH`. So:

```sql
SELECT year_month FROM dates;           -- syntax error
SELECT dates.year_month FROM dates;     -- fine, qualified
SELECT `year_month` FROM dates;         -- fine, backticked
```

Every query in the project qualifies or backticks it. It only bites if you type
a quick query of your own — and it is a good thing to be able to explain if
asked why the schema has backticks in it.

## Task 1.4 — the eight queries

> The interpretations in the report were AI-drafted and **must be rewritten in
> your own words** before submission — Section 3.2. This explains what each
> query *does* and what the numbers *say*; the reading of them has to be yours.

### Group 1 — Basic retrieval

**Q1 — the 15 largest transaction lines of 2024.** `SELECT` / `WHERE` /
`ORDER BY` / `LIMIT` on one table.

*What it says:* they sit in a tight band from **9,380 to 9,914** against a
dataset maximum of 9,992 — a hard ceiling near 10,000, not a long tail. So no
single lost account can explain the decline. Profit on those near-identical
revenues ranges from **414 to 4,339**, so revenue rank is a poor guide to which
orders are actually valuable.

**Q2 — bulk orders at thin margins.** Adds a **calculated column**:
`ROUND(100.0 * profit / amount, 2) AS margin_pct`.

> **Why `100.0` and not `100`?** With integers, SQL may do integer division and
> throw away the decimals. Writing `100.0` forces floating-point arithmetic.
> Classic exam question.

*What it says:* the worst line shipped 19 units for 7,702 revenue and **60
profit — a 0.78% margin**. All 15 return under 3.7%, and they appear in every
year from 2020 to 2024, so this is a standing pricing issue, *not* a cause of
the trend break.

### Group 2 — Aggregates

**Q3 — the annual trend.** The headline table. `GROUP BY` with `COUNT`, `SUM`,
`AVG`.

| year | months | lines | revenue | profit | revenue_per_month | avg_line_value | margin_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2020 | 9 | 167 | 836,410 | 217,911 | 92,934.44 | 5,008.44 | 26.05 |
| 2021 | 12 | 217 | 1,181,446 | 283,231 | 98,453.83 | 5,444.45 | 23.97 |
| 2022 | 12 | 288 | 1,459,775 | 393,113 | 121,647.92 | 5,068.66 | 26.93 |
| 2023 | 12 | 234 | 1,229,723 | 321,671 | 102,476.92 | 5,255.23 | 26.16 |
| 2024 | 12 | 240 | 1,202,478 | 308,336 | 100,206.50 | 5,010.32 | 25.64 |

**Rule to remember:** every column in the `SELECT` must either sit inside an
aggregate or be listed in the `GROUP BY`.

> **Note the margin calculation.** It is `SUM(profit)/SUM(amount)` — **not**
> `AVG(margin_pct)`. Averaging percentages weights a 500-unit sale the same as
> a 5-unit one. Expect to be asked this.

*What it says:* watch the `months` column first — 2020 has only nine, so the
comparison must use `revenue_per_month`. On that basis growth was 30.9% to the
2022 peak, then −15.8% and −2.2%. The decisive detail is that **average line
value barely moved** (5,008–5,444, a 9% spread) while **orders per month moved
a lot** (18.6 → 24.0 → 20.0). The company writes *fewer* orders, not smaller
ones — which points at demand and availability, not pricing.

**Q4 — monthly seasonality.** Introduces a **scalar subquery**: an inner
`SELECT` returning one number (total revenue), which every row divides by to
get its share. It needs its own aliases and its own `WHERE`, so the denominator
covers the same months as the numerator.

*What it says:* December is **11.09%** of annual revenue and October
**10.70%** — together **21.8%**. January is the trough at **4.73%**. But the
peak is driven by **order count, not basket size**: December has the most lines
(133) at an average line value of 4,928, *below* the annual averages. So Q4 is
a throughput problem — staffing and warehouse capacity, not premium stock.

### Group 3 — Multi-table joins

Both join **four** tables; the requirement was two.

**Q5 — revenue by category per year.** Note the **chain**: `sales` has no
direct link to `categories`. It knows its sub-category, and the sub-category
knows its category — so you hop `sales → sub_categories → categories`.

| category | 2020 | 2021 | 2022 | 2023 | 2024 |
| --- | --- | --- | --- | --- | --- |
| Electronics | 233,178 | 387,757 | 478,451 | 538,319 | **318,630** |
| Furniture | 299,708 | 391,342 | 496,353 | 385,893 | 415,878 |
| Office Supplies | 326,515 | 402,347 | 484,971 | 305,511 | 467,970 |

*What it says:* the flat company total hides three different stories.
Electronics kept growing a year longer, peaking in 2023, then fell **40.8%**.
Office Supplies did the opposite — dropped in 2023, rebounded **53%**. So the
"plateau" is an Electronics collapse nearly cancelled by an Office Supplies
recovery. Managing to the aggregate would have missed both.

**Q6 — top cities.** The other four-table chain, through geography. New idea:
`COUNT(DISTINCT cu.customer_id)` — without `DISTINCT`, a customer with three
purchases counts three times and revenue-per-customer becomes nonsense.

*What it says:* geography is **not** the problem. Across six states revenue
spans only 884,768 to 1,130,048 — a 28% spread over five years. The useful
signal is per-customer value: Orlando returns **9,829 per customer**, Buffalo
only **7,216** from 26% more customers.

### Group 4 — Business insights

**Q7 — what caused the plateau.** Uses **conditional aggregation**, the most
useful trick in the checkpoint. `CASE WHEN … THEN … ELSE … END` is SQL's
if-statement; inside `SUM()` it adds `amount` only when the year matches. Two
of them side by side turn *rows* into *columns* so you can subtract them — this
is **pivoting**. `NULLIF(x, 0)` is division-by-zero protection.

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

*What it says — the headline finding.* The plateau is **concentrated in one
sub-category**. Printers alone lost **136,865**, more than half the entire
257,297 gap and more than the next two decliners combined. All four Electronics
lines fell; all four Office Supplies lines grew.

The pattern suggests consumables growing while durable hardware falls away.
**The honest next step is to check 2024 Printer stock and supplier status
before concluding anything about demand** — a supply failure and a demand
collapse look identical in a sales table but need opposite responses. Saying
this is a strength: it shows you know what the data cannot tell you.

**Q8 — is the Q4 peak universal?** Uses a **window function**. A normal
aggregate collapses rows into one; a window function computes across a set of
rows *while keeping every row*. `PARTITION BY category` makes the window "all
rows for this category", so each quarter can express itself as a share of its
**own** category.

| category | Q1 | Q2 | Q3 | Q4 |
| --- | --- | --- | --- | --- |
| Electronics | 20.28% | **30.79%** | 23.69% | 25.24% |
| Furniture | 16.96% | 29.46% | 22.74% | **30.84%** |
| Office Supplies | 17.01% | 25.00% | 25.83% | **32.16%** |

*What it says:* the company-wide Q4 peak is **not universal**. Furniture and
Office Supplies peak in Q4; **Electronics does not** — it peaks in **Q2**.
Planning Electronics stock against the blended curve over-stocks it in Q4 and
under-stocks it in Q2, every year. Q1 is weakest for all three, so it is the
natural clearance window.

> Q8 needs **MySQL 8**. On 5.7 use **Q8-ALT** at the end of the screenshot
> script — a correlated subquery that returns byte-identical output.

---

# Part 2 — Checkpoint 2: Spreadsheet & Statistics

## What it is

The **Midterm** phase, Weeks 5–9, **100 points**, assessing **CILO 2**: *apply
spreadsheet and statistical techniques to analyze business data and support
decision-making.*

| Criterion | Points |
| --- | --- |
| Statistical Accuracy | **30** |
| Interpretation of Results | **30** |
| Spreadsheet Report Quality | **25** |
| Documentation | **15** |

**Where the marks are:** accuracy and interpretation together are **60%**.
Getting the numbers right is only half — a correct R² with no interpretation
scores badly.

## The workbook, sheet by sheet

`reports/Checkpoint_2_Workbook.xlsx` — **13 sheets, 1,724 formula cells,
11 charts.**

| Sheet | Task | What it holds |
| --- | --- | --- |
| **Read Me** | — | Sheet guide and seven self-checks |
| **Cleaned Data** | 2.1 (1) | 1,194 lines × 19 columns |
| **Pivot Analysis** | 2.1 (2) | Four SUMIFS cross-tabs |
| **Pivot Charts** | 2.1 (3) | Four charts from those |
| **Formulas Showcase** | 2.1 (4) | Eight Excel functions |
| **Descriptive Stats** | 2.2 | 13 statistics × 3 variables |
| **Frequency** | 2.2 | Distribution table and histogram |
| **Correlation** | 2.3 | Two pairs plus a supporting third |
| **Regression** | 2.4 | Equation, R², t, p, forecasts, limits |
| **Forecast** | 2.5 | Trend test, seasonal index, forecast, holdout check |
| **PivotTable 1–3** | 2.1 (2, 3) | Three native PivotTables, each with a PivotChart |

### Three design decisions to be able to defend

**Every computed cell is a live formula, never a pasted number.** Change a value
in Cleaned Data and every statistic, chart and forecast updates. Typed-in
constants would make the workbook a *picture* of an analysis rather than an
analysis, and nothing could silently drift out of step with the data.

**Formulas use named ranges.** `Amount`, `Profit`, `Quantity`, `Category`,
`State`, `Yr`, `YearMonth`, `SubCategory` and `PaymentMode` each name a column,
so the workbook says

```
=SUMIF(Category,"Electronics",Amount)
```

rather than `=SUMIF('Cleaned Data'!$M$2:$M$1195,"Electronics",'Cleaned Data'!$Q$2:$Q$1195)`.
Same result, but you can read it aloud.

**Both kinds of pivot are present.** *Pivot Analysis* holds four
**formula-driven cross-tabs** — they compute exactly what a PivotTable computes,
recalculate live, and every cell is auditable, which a PivotTable's internals
are not. *PivotTable 1–3* are **native PivotTable objects** with the Fields pane
and drag-and-drop:

| Sheet | Rows | Columns | Values | PivotChart |
| --- | --- | --- | --- | --- |
| PivotTable 1 | Category | Year | Sum of Amount | Clustered column |
| PivotTable 2 | State | — | Average of Amount | Column |
| PivotTable 3 | YearMonth | — | Count of SaleID | Line |

All three read `Cleaned Data!A1:S1195` through **one shared pivot cache** —
what Excel does itself when several PivotTables come from one range, so the data
is cached once and one refresh updates all three.

### The self-checks

The Read Me sheet ends with seven rows that each recompute a total **two
independent ways** and compare — Pivot 1's grand total against `SUM(Amount)`,
and so on. All seven must read **OK**.

They exist because the workbook was built outside Excel, where formulas are
written but never calculated. Excel calculates them on open, and these rows are
what prove it worked.

## Task 2.2 — descriptive statistics

Three variables, n = 1,194.

| Statistic | Amount | Profit | Quantity |
| --- | --- | --- | --- |
| Mean | 5,178.09 | 1,348.99 | 10.67 |
| Median | 5,152.00 | 1,014.00 | 11.00 |
| Mode | 717 | 177 | 14 |
| Standard deviation | 2,804.92 | 1,117.99 | 5.78 |
| Variance | 7,867,587.17 | 1,249,907.39 | 33.37 |
| Min / Max | 508 / 9,992 | 50 / 4,930 | 1 / 20 |
| Range | 9,484 | 4,880 | 19 |
| Q1 / Q3 | 2,799 / 7,626 | 410 / 2,035 | 6 / 16 |
| IQR | 4,827 | 1,625 | 10 |
| Coefficient of variation | **54.2%** | **82.9%** | 54.1% |

### What each statistic is for

**Mean vs median — the skew test.** Close together means symmetric; mean well
above median means a few large values are pulling it up.

- Amount: 5,178 ≈ 5,152 → **symmetric**
- Profit: 1,349 ≫ 1,014 → **right-skewed** (skewness +0.94)

That single comparison is the most useful thing on the sheet, and it is why the
**median** is the honest figure to quote for a typical order's profit.

**Mode** is the most frequent value — useful for Quantity, close to meaningless
for a continuous variable like Amount where the "mode" of 717 appears just 6
times in 1,194 rows. Saying so is worth marks: knowing when a statistic does
not apply is part of using it.

**Standard deviation vs variance.** Variance is the SD squared — same
information, but in *squared* units, which means nothing to a business reader.
Quote the SD; report the variance because the brief asks for it.

**Coefficient of variation** is SD ÷ mean, so spread can be compared across
different units. This is the one that produces a finding: Profit's **82.9%**
against Amount's **54.2%** says profit is far less predictable than revenue —
two orders of the same value can return very different profits.

**Quartiles and IQR.** Q1 is the value 25% fall below, Q3 the value 75% fall
below. The IQR is the middle half, and unlike the range it ignores extremes.

### The histogram is the real finding

Amount binned into ten bands of 1,000, counted with `COUNTIFS` rather than the
`FREQUENCY` array function so each cell is independent and auditable.

The shape is **flat, not bell-shaped**. A normal distribution peaks in the
middle and thins at both ends; this one is roughly level across the whole
range — what a random number generator produces, and the fifth piece of
evidence that the dataset is synthetic.

*Business reading:* there is **no "typical" order size** to design around, and
no premium segment to separate out.

## Task 2.3 — correlation

### What r means

Pearson's **r** runs from −1 to +1. **Sign** is direction, **size** is strength
(0.7+ strong, 0.4–0.7 moderate, below 0.4 weak), **r²** is the share of
variation the two share, and the **p-value** answers a different question: could
a correlation this large have arisen by chance if the true one were zero?

### Pair 1 — monthly orders vs monthly revenue

**r = +0.9227, r² = 0.8514, p = 1.98 × 10⁻²⁴, n = 57. Strong positive.**

Months with more orders have proportionally more revenue; order count alone
tracks about **85%** of the variation. This is the statistical form of the
Checkpoint 1 finding — CP1 *observed* that revenue fell while average order
value stayed flat and *inferred* order count was doing the work. This tests the
inference and confirms it.

### Pair 2 — line quantity vs line amount

**r = +0.0446, r² = 0.0020, p = 0.123, n = 1,194. Negligible — not
significant.**

Units sold explains **0.2%** of the variation in order value, and at p = 0.123
we **cannot reject** the hypothesis that the true correlation is zero.

**A negative result is still a result, and this is the more useful of the two.**
The intuitive assumption — sell more units, earn more revenue — is false here,
because unit price varies so widely across the twelve sub-categories that volume
carries no information about value. So an incentive built on units shifted would
not raise revenue, and "units sold" should not be a performance measure.

### Supporting check — amount vs profit

**r = +0.6753, r² = 0.4560, p < 0.001.** Moderate-to-strong, but notably *not*
near 1.0: only **46%** of profit variation tracks revenue. The rest is margin
differences between products — the same story the coefficient of variation told,
reached a different way.

### The caveat you must state

**Correlation is not causation.** A strong r says two things move together. It
does not say one causes the other. Say it explicitly about Pair 1: it does not
prove that pushing order count up would mechanically raise revenue — if the
extra orders were won by discounting, average order value would fall and the
relationship would not hold.

## Task 2.4 — regression

- **Y (dependent):** monthly revenue
- **X (predictor):** number of orders that month

Chosen because it tests the CP1 claim rather than asserting it, it had by far
the strongest correlation, and it is **actionable** — a business can influence
how many orders it wins far more readily than how large each is.

| Statistic | Value | What it is |
| --- | --- | --- |
| n | 57 | Months in the sample |
| **Slope (b)** | **5,224.25** | Revenue added per extra order |
| Intercept (a) | −1,353.65 | Predicted revenue at zero orders |
| r | 0.9227 | Correlation |
| **R²** | **0.8514** | Share of variation explained |
| Std error of estimate | 15,099.14 | Typical prediction error |
| Std error of slope | 294.35 | Uncertainty in the slope |
| **t statistic** | **17.75** | Slope ÷ its standard error |
| Degrees of freedom | 55 | n − 2 |
| **p-value** | **1.98 × 10⁻²⁴** | Chance of this slope if the truth were zero |

> **Monthly Revenue = −1,353.65 + 5,224.25 × Orders**

### Reading it properly

**The slope.** Each additional order is associated with about **5,224** more
revenue. Now the detail worth leading with: the average transaction line is
worth **5,178**. The slope and the average order value agree to within **1%** —
exactly what should happen if revenue is order count times a stable order size.
**The model is *consistent with* the data, not merely fitted to it.** Two
independent routes to the same number is the strongest evidence in the project.

**R² = 0.8514** — order count explains **85.1%** of month-to-month variation.
The other 14.9% is product mix, seasonality and noise.

**The t statistic and p-value.** The **null hypothesis** is that the true slope
is zero. The t statistic is the slope divided by its own uncertainty:
5,224.25 ÷ 294.35 = **17.75**. About 2 is the usual threshold, so 17.75 is
enormous, and the p-value converts it to **1.98 × 10⁻²⁴** — far below 0.05, so
we **reject the null**.

**The intercept is meaningless here, and say so.** −1,353.65 is revenue at zero
orders — impossible, and far outside the observed range of 9 to 45 orders per
month. It is an artefact of fitting a line, not a business quantity.
Volunteering this shows you understand the model rather than just reporting it.

### The forecast

| Orders in month | Predicted revenue |
| --- | --- |
| 15 | 77,010 |
| 20 | 103,131 |
| 25 | 129,253 |
| 30 | 155,374 |

2024 ran at **20.0** orders per month against **24.0** in 2022. The model puts
that four-order gap at roughly **250,000 a year** — very close to the **257,297**
shortfall measured directly in Checkpoint 1 by a completely different method.

### Six limitations

1. **Linearity** — assumed straight-line; the scatter supports it over the
   observed range.
2. **Independence** — **the weakest assumption.** Monthly sales series are
   usually autocorrelated, which inflates apparent significance. With t = 17.75
   the conclusion survives, but read the p-value as "clearly significant" rather
   than as a precise probability.
3. **Range of validity** — 9 to 45 orders. Outside that, including the
   intercept, is extrapolation.
4. **Correlation is not causation.**
5. **One predictor only** — cannot capture seasonality, mix, or the Printer
   problem. Multiple regression in Checkpoint 4 is the extension.
6. **Synthetic data** — the coefficients describe this file, not a market.

## Task 2.5 — trend and seasonality

### The 57-month window

Both ends of the file are partial, so **March 2020**, **March 2025** and **all
of 2025** are excluded, leaving **April 2020 to December 2024**. January and
February 2025 are complete months in a partial year, so they are **held back**
and used only to check the forecast.

### Step 1 — is there a trend to project?

| Statistic | Value |
| --- | --- |
| Slope | +206.0 per month |
| **R²** | **0.0078** |
| **p-value** | **0.515** |

Time explains **less than 1%** of the variation, and at p = 0.515 the apparent
slope is indistinguishable from noise.

**This is a finding, not a failure.** The series is not a trend — it is a
**growth phase followed by a plateau**, and one straight line across a
structural break describes neither regime. So **no growth rate is projected**.
Forecasting a slope the data does not support is the easiest way to be badly
wrong, and saying so is worth more than a confident-looking number.

### Step 2 — the seasonal index

Each month's average revenue ÷ the overall average month. 1.00 = average.

| Month | Index | | Month | Index |
| --- | --- | --- | --- | --- |
| January | **0.679** | | July | 0.966 |
| February | 0.889 | | August | 1.006 |
| March | 1.025 | | September | 0.793 |
| April | 1.103 | | October | **1.229** |
| May | 1.131 | | November | 0.878 |
| June | 1.028 | | December | **1.273** |

### Step 3 — the forecast

Because the recent regime is flat rather than sloping, the forecast is
**recent level × seasonal index** — the standard construction for a series
stable in level but strongly seasonal. The level is the mean of the last 24
months (**101,342**), a window confirmed flat (p = 0.857).

| Period | Index | Forecast | Actual | Error |
| --- | --- | --- | --- | --- |
| 2025-01 | 0.679 | 68,853 | 112,906 | **−39.0%** |
| 2025-02 | 0.889 | 90,064 | 84,712 | **+6.3%** |
| 2025-03 | 1.025 | 103,870 | *(partial)* | — |
| 2025-04 | 1.103 | 111,806 | — | — |
| 2025-05 | 1.131 | 114,574 | — | — |
| 2025-06 | 1.028 | 104,156 | — | — |

### Step 4 — the honest check

| Model | Jan | Feb | Mean absolute error |
| --- | --- | --- | --- |
| Seasonal | −39.0% | +6.3% | **22.7%** |
| Flat | −10.2% | +19.6% | **14.9%** |

**The seasonal model did not win.** Better in February, much worse in January,
and on average the simpler flat forecast was more accurate.

The cause is identifiable: January is historically the weakest month at 0.679,
but **January 2025 came in at 112,906 — above the recent average, not 32%
below it.** Either the seasonal pattern has broken, or January 2025 was
unusual. Two observations cannot tell those apart.

**State the conclusion: with two comparable months, no forecasting method can
be validated here.** This is a sanity check, not evidence the model works.
Reporting a check your own model failed is a strength — the alternative,
presenting an unvalidated forecast, is what most submissions do.

---

# Part 3 — Reference

## SQL

| Concept | What it does | Where |
| --- | --- | --- |
| `WHERE` | Filters **rows**, before grouping | Q1–Q7 |
| `HAVING` | Filters **groups**, after grouping | not needed here |
| `ORDER BY` | Sorts. `ASC` / `DESC` | Q1, Q2, Q6 |
| `JOIN … ON` | Combines tables on a matching rule | Q3–Q8 |
| `GROUP BY` | Collapses rows into one per group | Q3–Q8 |
| `COUNT(DISTINCT x)` | Counts *unique* values | Q6 |
| Scalar subquery | Inner query returning one value | Q4 |
| `CASE WHEN` | SQL's if-statement | Q7 |
| Conditional aggregation | `SUM(CASE WHEN …)` to pivot rows into columns | Q7 |
| `NULLIF(x, 0)` | Division-by-zero guard | Q7 |
| Window function | Aggregates across rows without collapsing them | Q8 |

**Join types.** All ours are **INNER** joins (plain `JOIN`), which keep only
matching rows — safe here because foreign keys guarantee every fact row has a
matching dimension row. A **LEFT JOIN** keeps every row from the left table even
without a match; you would need it to show categories with zero sales.

## Statistics

| Term | Meaning |
| --- | --- |
| Mean / median / mode | Average / middle value / most frequent |
| Standard deviation | Typical distance from the mean |
| Variance | SD squared |
| Coefficient of variation | SD ÷ mean; compares spread across units |
| Skewness | Asymmetry; mean > median means right-skewed |
| Quartile / IQR | 25th and 75th percentile; the middle half |
| Pearson r | Linear correlation, −1 to +1 |
| r² | Share of variation shared |
| p-value | Chance of the result if the null were true |
| Slope / intercept | The `b` and `a` in Y = a + bX |
| Standard error | Uncertainty in an estimate |
| t statistic | Estimate ÷ its standard error |
| Degrees of freedom | n − 2 for simple regression |
| Null hypothesis | "There is no relationship" |
| Seasonal index | Month's average ÷ overall average |
| Mean absolute error | Average error size, ignoring sign |
| Holdout | Data withheld to test a model |

## Excel functions used

`AVERAGE` `MEDIAN` `MODE` `STDEV` `VAR` `MIN` `MAX` `QUARTILE` `COUNT`
`SUMIF` `SUMIFS` `COUNTIF` `COUNTIFS` `AVERAGEIF` `AVERAGEIFS`
`CORREL` `SLOPE` `INTERCEPT` `RSQ` `STEYX` `DEVSQ` `TDIST`
`VLOOKUP` `IF` `TEXT` `ROUND` `ABS` `SQRT`

All are Excel-2007-era, chosen deliberately so the workbook opens correctly in
any Excel version and in Google Sheets. Newer functions such as `XLOOKUP`,
`FILTER` and `TEXTJOIN` are avoided.

## Six things people get wrong

1. **`WHERE` vs `HAVING`.** `WHERE` filters rows before grouping; `HAVING`
   filters groups after. To keep only years above 1,000,000 in revenue you need
   `HAVING SUM(amount) > 1000000`, because the sum does not exist yet at
   `WHERE` time.
2. **Integer division.** `100 * profit / amount` can truncate. Write `100.0`.
3. **Averaging percentages.** `SUM(profit)/SUM(amount)` is right;
   `AVG(margin_pct)` is wrong because it ignores the size of each sale.
4. **r vs r².** r = 0.92 does not mean "92% explained". r² does — 85%.
5. **A high p-value is not proof of no relationship.** It means insufficient
   evidence. Pair 2 shows "not significant", not "proven unrelated".
6. **Significance is not importance.** With a big enough sample a trivial
   relationship can be significant. Read the effect size alongside the p-value.

---

# Part 4 — Everything we found

| # | Finding | From |
| --- | --- | --- |
| 1 | **Growth stopped in 2022.** Revenue per month is 17.6% below peak, but margin and average order value never moved — the company writes *fewer* orders, not worse ones. | Q3 |
| 2 | **One sub-category explains most of it.** Printers lost 136,865, over half the entire gap. All Electronics fell; all Office Supplies grew. | Q5, Q7 |
| 3 | **Seasonality is category-specific.** Electronics peaks in Q2, the others in Q4. The blended planning curve is wrong for all three. | Q4, Q8 |
| 4 | **Geography is not a factor.** State revenue spans only 28% over five years. | Q6 |
| 5 | **Order count drives revenue** — now proven, not inferred. r = 0.923, R² = 0.851, p < 0.001. | CP2 regression |
| 6 | **Units sold predicts nothing.** r = 0.045, p = 0.123. Volume-based targets would not move revenue. | CP2 correlation |
| 7 | **Revenue is a poor proxy for profit.** Profit skew +0.94, CV 82.9% vs 54.2%; only 46% of profit variation tracks revenue. | CP2 |
| 8 | **The trend runs in two regimes — growth to 2022, then plateau.** A single line across both explains under 1% (p = 0.515), so the forecast uses level and seasonality instead of a growth rate. | CP2 trend test |
| 9 | **The four-order gap is worth ~250,000 a year**, corroborating CP1's 257,297 independently. | CP2 regression |
| 10 | **The seasonal forecast did not beat a flat average** over the two holdout months. | CP2 forecast |

Findings 5 and 9 **confirm Checkpoint 1 by a different route**, which is the
strongest thing Checkpoint 2 does. Findings 6, 8 and 10 are *negative* results —
things that turned out not to be true — and they are what demonstrate analysis
rather than confirmation.

## The correction

Building the Checkpoint 2 monthly series exposed an error in Checkpoint 1.
**2020 was treated as a full year when the file starts on 22 March**, so it
holds only nine months. That overstated 2020→2022 growth as **69.9%** when the
like-for-like figure is **30.9%**.

| Affected | Unaffected |
| --- | --- |
| The 2020→2022 growth figure | The −17.6% peak-to-2024 decline (both full years) |
| March's seasonal index (0.876 → 1.025) | Printers −136,865; Electronics −40.8% |
| | Category-specific seasonality; geography |

The central thesis stands; one supporting number was overstated. Checkpoint 1
was reissued with `is_complete_month` added and `revenue_per_month` in Q3.

Section 3.4 of the brief allows CP1 and CP2 to be revised and resubmitted with
CP3, capped at 80/100. If CP1 is already marked, ask the instructor whether to
resubmit or simply cite the correction — it is documented in the CP2 report
either way.

## Where this points for Checkpoint 3

Build the dashboard around **order count** as the primary KPI rather than
revenue, since it is the leading indicator and the actionable one. Segment on
**margin** rather than revenue, given how weakly the two are related.

---

# Part 5 — Defense questions

## On the data

**Your dataset looks fake. Doesn't that invalidate the project?**
It invalidates the *figures*, not the *method*. We state it plainly with five
pieces of evidence, and we did not fabricate corrections because that would be
worse. The schema, queries and analysis would run identically on real data.

**Why exclude 2025, and why is 2020 shown per month?**
The file stops 15 March 2025, so including 2025 shows a fake collapse. It also
*starts* 22 March 2020, so 2020 holds nine complete months — comparing its
part-year total against a full 2021 would suggest 69.9% growth when the
like-for-like figure is 30.9%.

**What is the difference between the two date flags?**
`is_complete_year` excludes 2025 entirely. `is_complete_month` excludes just
the two part-months at the ends. Together they define the 57-month window.

## On the database

**Which is the fact table, and how do you know?**
`sales`. Two tests: the grain — one row is one product line on one order — and
the measures are additive at that grain. The other seven describe and label;
summing a `customer_id` is meaningless.

**Why is `Order ID` not your primary key?**
194 of its 547 values appear against different dates *and* different customers.
The first three rows of the raw file show one ID across three dates, three
customers and three states.

**Why does `customers` have 807 rows when there are 802 names?**
Five names appear in more than one city. Keying on name alone would merge two
different people.

**Why a star schema and not one flat table?**
The business questions are all "a measure by a dimension over time", which a
star answers in one join. A flat table repeats "Miami" on all 66 Miami rows —
redundancy that causes update anomalies.

**Why does the schema have backticks around `year_month`?**
`YEAR_MONTH` is a reserved word in MySQL — the unit in `INTERVAL 1 YEAR_MONTH`.
Unqualified and unquoted it is a syntax error.

## On the statistics

**What does R² = 0.85 actually mean?**
That 85% of the month-to-month variation in revenue moves together with order
count. It is *not* a statement that order count causes 85% of revenue.

**What hypothesis is the p-value testing?**
The null hypothesis that the true slope is zero. With t = 17.75 on 55 degrees
of freedom, the probability of a slope this large if the null were true is
about 2 in 10²⁴, so we reject it.

**Why is your intercept negative? Revenue cannot be negative.**
Correct — which is why it is not a business quantity. It is where the fitted
line crosses zero orders, far outside the observed 9-to-45 range.

**How do you know the regression is not just curve-fitting?**
The slope came out at 5,224 and the average order value is 5,178 — within 1%.
Two independent routes to the same number.

**Pair 2 has r = 0.045. Why include a correlation that shows nothing?**
Because "nothing" is the finding. It rules out a units-based sales target.

**Did you actually analyse the sales trend?**
Yes, in five ways: year-on-year (Q3), monthly seasonality (Q4), category
trajectory (Q5), sub-category change (Q7), quarterly pattern (Q8), plus a
57-month series and a six-month forecast in Task 2.5. The trend itself is
**two regimes — growth to 2022, then plateau** — which is a more useful answer
than one growth percentage.

**Why did you not project a trend line?**
Because the series has a structural break. A line fitted across both regimes
gives R² = 0.008, p = 0.515 — it describes neither. We forecast on level and
seasonality instead, which is the correct construction for a flat, seasonal
series, and it still produced six months of projections.

**Your forecast lost to a naive average. Is that not a failure?**
It is an honest result over the only two complete holdout months, driven by
January 2025 breaking its historical index. Two months cannot validate a
method, which is exactly what we say.

**Why `SUM(profit)/SUM(amount)` instead of `AVG(margin)`?**
Averaging percentages treats a 20-unit sale and a 1-unit sale as equally
important. Summing first weights each sale by its actual size.

## On the workbook

**Are these real PivotTables?**
Both kinds are present. *Pivot Analysis* holds SUMIFS cross-tabs, auditable cell
by cell; *PivotTable 1–3* are native PivotTable objects sharing one pivot cache,
each with a PivotChart.

**Why share a cache between the three PivotTables?**
They read the same range. A shared cache stores the data once instead of three
times, and one refresh updates all three. It is what Excel does by default.

**How do you know Printers is the cause and not just correlated?**
We don't — and we say so. Q7 establishes *where* the revenue went, not *why*.
A supply failure and a demand collapse produce the same signature, so the report
recommends checking stock and supplier records first.

**What would you do differently with more time?**
Get a dataset with returns and loss-making orders so margin analysis is
meaningful, and obtain inventory data so the Printer question could be settled
rather than flagged.

---

# Part 6 — Glossary

**Aggregate function** — turns many rows into one value: `COUNT`, `SUM`, `AVG`.

**Cardinality** — how many rows on one side of a relationship relate to the
other. Ours are all one-to-many.

**Coefficient of variation** — SD as a percentage of the mean, so spread can be
compared across variables with different units.

**Conditional aggregation** — `SUM(CASE WHEN … THEN … END)`, used to turn rows
into columns (pivoting).

**Correlation** — how strongly two variables move together, measured by r.

**Data dictionary** — the table listing every column with its type and meaning.

**Degrees of freedom** — n − 2 in simple regression, because two parameters are
estimated from the data.

**Dimension table** — descriptive attributes you slice measures by.
**Fact table** — the central table holding the numeric measures.

**ERD** — Entity-Relationship Diagram; the picture of tables and their links.

**Foreign key (FK)** — a column pointing at another table's primary key.
**Primary key (PK)** — the column uniquely identifying each row.

**Grain** — what one row of the fact table represents.

**Holdout** — data withheld so a model can be tested on values it never saw.

**Mean absolute error** — average error size, ignoring direction.

**Natural key** — a key made from real data. **Surrogate key** — a meaningless
generated number.

**Normalisation** — removing redundancy by splitting data into related tables
so each fact is stored once.

**Null hypothesis** — the default assumption that there is no relationship.

**p-value** — probability of a result at least this extreme if the null were
true. Below 0.05 is conventionally "significant".

**Pearson r** — the linear correlation coefficient, −1 to +1.

**R²** — share of variation in Y explained by X. The square of r.

**Referential integrity** — the guarantee that every foreign key points at a row
that exists.

**Regression** — fitting Y = a + bX to describe how Y moves with X.

**Seasonal index** — a month's average divided by the overall average month.

**Skewness** — asymmetry. Positive means a tail to the right.

**Standard error** — the uncertainty attached to an estimate.

**Star schema** — one fact table surrounded by dimension tables.

**t statistic** — an estimate divided by its own standard error.

**Window function** — an aggregate computed across a set of rows *without*
collapsing them, written `OVER (PARTITION BY …)`.
