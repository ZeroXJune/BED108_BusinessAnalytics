# Contribution Guide

**BED 106 — Business Analytics · Mini Capstone · Sales Trend Analysis**

What the work on Checkpoints 1 and 2 actually consisted of, organised by role,
so each member can identify their part, write it up on Form A, and answer for
it if asked.

**One thing this document does not do.** Form A certifies *"my actual
participation"*. This describes what the work contained — who did which part is
yours to state truthfully, and it should be what actually happened rather than
what the table below suggests. Section 3.2 of the brief also requires the
description to be in your own words, so adapt rather than copy.

**Contents**

1. [How the work divided](#1-how-the-work-divided)
2. [Project Lead / Analyst](#2-project-lead--analyst)
3. [Data Engineer](#3-data-engineer)
4. [Statistician / Modeler](#4-statistician--modeler)
5. [BI Developer / Visualizer](#5-bi-developer--visualizer)
6. [Work everyone shares](#6-work-everyone-shares)
7. [Filling in Form A](#7-filling-in-form-a)

---

## 1. How the work divided

| Role | Checkpoint 1 | Checkpoint 2 |
| --- | --- | --- |
| **Project Lead / Analyst** | Framed the business problem and the three key questions; wrote the interpretations; assembled the report | Chose the regression and correlation variables; wrote the interpretations; handled the CP1 correction |
| **Data Engineer** | Sourced and documented the dataset; ran the quality assessment; designed the ERD and schema; loaded the data | Exported the cleaned data into the workbook; built the named ranges, cross-tabs, formula showcase and self-checks |
| **Statistician / Modeler** | Wrote the aggregate and trend queries; verified every reported figure against the data | Descriptive statistics, correlation, regression and significance test, trend and seasonality, holdout check |
| **BI Developer / Visualizer** | Charts and figures; ERD rendering; table formatting; report layout | Pivot charts, histogram, scatter plots, forecast chart; workbook formatting |

The two checkpoints feed each other: Checkpoint 1 established *what happened*,
Checkpoint 2 tested *how strong the evidence is*. Several Checkpoint 2 findings
confirm Checkpoint 1 by a different route, and one of them corrected it.

---

## 2. Project Lead / Analyst

### Checkpoint 1

**Framing the business problem.** The starting point was deciding what question
the project would actually answer. "We want to analyse sales" is an activity,
not a problem. The framing chosen was: *the company grew fast, then stopped,
and nobody can say why.* What makes that a real analytical problem rather than
an obvious one is that **margin never moved** — if margin had collapsed, the
answer would be "we are discounting too hard" and no database would be needed.
Because margin held at 24–27% while revenue fell, something structural changed
in what was being sold.

**The three key business questions.** Each is tied to specific queries, because
the rubric wants queries relevant to the business problem:

1. How have revenue and profit trended, and is the company still growing? *(Q3)*
2. Which categories and sub-categories drive the trend? *(Q5, Q7)*
3. When does demand concentrate, and is the pattern the same for every
   category? *(Q4, Q8)*

**The interpretations.** For each of the eight queries, the 2–3 sentences
saying what the result means for the business — the part the rubric weights
most heavily after SQL accuracy.

**Report assembly.** Pulling Tasks 1.1–1.4 into one document, deciding what
went in the body versus the appendix, and stating the dataset's limitations
honestly rather than hiding them.

### Checkpoint 2

**Choosing the variables.** The single most consequential decision in
Checkpoint 2. The regression uses **monthly order count → monthly revenue**,
chosen for three reasons: it tests the Checkpoint 1 claim instead of asserting
it; it had the strongest correlation of any pair examined; and it is actionable,
because a business can influence how many orders it wins far more easily than
how large each one is.

The second correlation pair — **quantity vs amount** — was chosen deliberately
*because* it was expected to show nothing. A near-zero result rules out a
units-based sales target, which is more useful than a third obvious positive.

**The Checkpoint 1 correction.** Building the monthly series exposed an error:
2020 was treated as a full year when the file starts on 22 March, so it holds
only nine months. That overstated 2020→2022 growth as 69.9% when the
like-for-like figure is **30.9%**. Deciding to correct it, reissue Checkpoint 1,
and document the correction in the Checkpoint 2 report is a judgement call that
belongs to this role.

**Should be able to explain:** why this problem and not another; why margin
holding steady makes it interesting; why order count was the predictor; why a
negative correlation result was worth including; what the CP1 correction
changed and what it did not.

---

## 3. Data Engineer

### Checkpoint 1

**Dataset documentation.** Name, source, date accessed, licence, and a data
dictionary covering all 12 raw columns with type and description.

**The quality assessment — five problems, each with a resolution.** This is
where most of the Data Preparation marks sit, because the rubric asks for
issues *identified and resolved*:

| Problem | Resolution |
| --- | --- |
| `Order ID` is not unique — 547 values over 1,194 rows, and 194 recur against different dates *and* customers | Kept as descriptive `order_ref`; added surrogate key `sale_id` |
| `CustomerName` is not an identifier — 5 names appear in more than one city | Keyed customers on (name, city), giving 807 rows from 802 names |
| `Year-Month` duplicates `Order Date` — 0 mismatches in 1,194 rows | Dropped; calendar parts rebuilt in `dates` |
| Both ends of the file are partial — runs 22 Mar 2020 to 15 Mar 2025 | Two flags, `is_complete_year` and `is_complete_month` |
| The data is synthetic — four machine-checked signals | Documented rather than "corrected", since fabricating data is a failing offence |

**Schema design.** Eight tables — one fact, seven dimensions — with primary
keys, seven foreign keys, six unique constraints and four check constraints.
Choices worth owning: the star schema shape (every business question is "a
measure, by a dimension, over time"); the grain (one row = one product line on
one order); keeping geography and product snowflaked so each label is stored
once; and building a `dates` table so the completeness flags have somewhere to
live and the queries need no dialect-specific date functions.

**Loading and verifying.** A single import file that creates the database, all
eight tables and all the data, ending with a verification block whose last two
columns are orphan-row counts — zeros are the proof of referential integrity.

### Checkpoint 2

**The workbook's data layer.** Exporting the 1,194 cleaned rows with calendar
and hierarchy columns joined on, and defining **named ranges** so formulas read
as `=SUMIF(Category,"Electronics",Amount)` rather than
`=SUMIF('Cleaned Data'!$M$2:$M$1195,...)`.

**The cross-tabs and formula showcase.** Four cross-tabs built with `SUMIFS`,
`COUNTIFS` and `AVERAGEIFS`, and eight Excel functions each answering a real
question rather than demonstrating syntax.

**The self-checks.** Seven rows on the Read Me sheet that each recompute a
total two independent ways and compare. They exist because a workbook built
outside Excel has never had its formulas calculated — these are what prove it
worked on first open.

**Should be able to explain:** why `Order ID` cannot be a primary key, and be
able to point at the three rows that prove it; why `customers` has 807 rows for
802 names; what the two date flags do and why both are needed; what makes
`sales` the fact table; why everything is a live formula rather than a pasted
number.

---

## 4. Statistician / Modeler

### Checkpoint 1

**The aggregate and trend queries.** Q3 (annual trend), Q4 (monthly
seasonality), and the conditional-aggregation work in Q7 that pivots rows into
columns to compare 2023 against 2024 in a single row per sub-category.

**Verification.** Checking that every figure quoted in the report matches what
the queries actually return — the discipline that later caught the partial-year
error.

**A methodological point worth owning:** margin is computed as
`SUM(profit)/SUM(amount)`, **not** `AVG(margin_pct)`. Averaging percentages
weights a 20-unit sale the same as a 1-unit sale. Expect to be asked this.

### Checkpoint 2

This is the role's checkpoint — most of the 30 marks for Statistical Accuracy
sit here.

**Descriptive statistics.** Thirteen statistics across Amount, Profit and
Quantity. The finding that matters is not any single number but a comparison:
Profit's coefficient of variation is **82.9%** against Amount's **54.2%**, so
profit is far less predictable than revenue. Mean-vs-median identifies Profit
as right-skewed (+0.94) while Amount is symmetric.

**Frequency distribution.** Ten bins counted with `COUNTIFS` rather than the
`FREQUENCY` array function, so each cell is independent and auditable. The
histogram's flat shape is itself evidence the data is synthetic.

**Correlation.** Three pairs: monthly orders ↔ revenue (**r = 0.923**), quantity
↔ amount (**r = 0.045, p = 0.123 — not significant**), and amount ↔ profit
(r = 0.675, so only 46% of profit variation tracks revenue).

**Regression and significance test.**
`Revenue = −1,353.65 + 5,224.25 × Orders`, **R² = 0.851**, t = 17.75 on 55
degrees of freedom, **p ≈ 2 × 10⁻²⁴**.

The strongest single point in the whole project belongs here: the slope of
**5,224** lands within 1% of the average order value of **5,178**. Two
independent routes to the same number is what should happen if revenue is order
count times a stable order size — so the model is *consistent with* the data,
not merely fitted to it.

**Trend and seasonality.** The trend test returns R² = 0.008, p = 0.515 — no
significant trend. Deciding **not** to project a slope on that basis, and
saying why, is a real analytical judgement: the series is a growth phase
followed by a plateau, and one straight line describes neither.

**The holdout check.** Holding back January and February 2025, forecasting
them, and reporting that the seasonal model **lost** to a flat average (22.7%
vs 14.9% mean absolute error) because January 2025 broke its historical index.
Reporting a check your own model failed is a strength.

**Should be able to explain:** what R² means and how it differs from r; what
the null hypothesis in the regression is; why the negative intercept is
meaningless; why a p-value of 0.123 means "not enough evidence" rather than
"proven unrelated"; why no trend was projected; why two holdout months cannot
validate a method.

---

## 5. BI Developer / Visualizer

### Checkpoint 1

**The figures.** Three charts — annual revenue and profit per month, monthly
seasonality, and category trend — each titled with the finding rather than a
label, so the chart states its own conclusion.

**The ERD.** Rendered as an image with every table's columns, PK and FK
markers, crow's-foot notation for cardinality, the fact table distinguished
from the dimensions, and a legend explaining the notation.

**Report presentation.** Applying the Section 3.1 standard — Arial 12pt,
1-inch margins, 1.5 line spacing — and numbering and captioning every figure
and table, which is where Documentation marks are commonly lost.

### Checkpoint 2

**The workbook's visual layer.** Four pivot charts, the histogram, two scatter
plots with linear trendlines showing R² and the equation, and the forecast
chart with the holdout months marked.

**A presentation decision worth owning:** the forecast chart shows the actual
2025 values *next to* the forecast, so the January miss is visible rather than
hidden. Charts that show where a model failed are more credible than charts
that only show where it succeeded.

**Should be able to explain:** why each chart type suits its data (line for a
time series, column for categories, scatter for a relationship); what a
trendline on a scatter plot represents; why the flat histogram shape matters;
why the forecast chart shows the misses.

---

## 6. Work everyone shares

Some things are not one person's job, and the brief is explicit that any member
can be asked about any part:

- **The dataset is synthetic.** Four machine-checked signals: zero loss-making
  lines in five years; 22 of the 802 distinct customer names ending in a
  credential suffix, which is a name-generator artefact; US cities paired with
  UPI and EMI, which are Indian payment systems; and a near-uniform payment
  mix. Everyone should be able to say this and explain that it makes the
  *figures* a modelling exercise while leaving the *method* valid.
- **The privacy position.** The customer names are generated, so there is no
  data subject and R.A. 10173 is not engaged. The reason is that the names are
  synthetic — **not** that the file was publicly downloadable. Public
  availability is not consent. This matters again in Checkpoint 4.
- **The partial-data traps.** Both ends of the file are incomplete, 2020 is a
  nine-month year, and that caused a real error which was found and corrected.
- **The interpretations must be the group's own words**, per Section 3.2.

---

## 7. Filling in Form A

`reports/Form_A_Individual_Contribution.docx` holds four signable copies, one
per role. Write **1** or **2** in the Checkpoint No. field for the checkpoint
being submitted.

**Three entries per member.** Make each one specific — what you did, not what
the role covers in general.

| Weaker | Stronger |
| --- | --- |
| "Did the statistics" | "Computed the descriptive statistics for Amount, Profit and Quantity, and identified that Profit's coefficient of variation of 82.9% makes it far less predictable than revenue" |
| "Made the charts" | "Built the scatter plot of monthly orders against revenue with a linear trendline, and the forecast chart showing the two holdout months against the prediction" |
| "Helped with the database" | "Found that Order ID recurs against different dates and customers, and replaced it with a surrogate key while keeping the original as order_ref" |

The stronger versions name a specific artefact and a specific finding. They are
also what lets you answer if the instructor asks you to explain it.

If your group has fewer than four members, the roles were combined — say so on
the form and describe everything you covered, rather than leaving a role's work
unclaimed.
