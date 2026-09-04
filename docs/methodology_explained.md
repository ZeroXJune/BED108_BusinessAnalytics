# Why We Did It That Way — Methodology Defence

**BED 106 — Business Analytics · Mini Capstone · Sales Trend Analysis**

Not *what* the project contains — that is in `project_explained.md`. This is
**how each answer was arrived at, what method produced it, why that method and
not another, and what would change the answer.**

Every decision below is written in the same five parts:

> **What we did** · **What it means** · **Why this method** · **What we
> rejected, and why** · **What would change it**

Where a rejected alternative could be measured, it was measured. The numbers in
the comparison tables are real runs against the same data, not assertions.

**Contents**

1. [Framing the problem](#1-framing-the-problem)
2. [Preparing the data](#2-preparing-the-data)
3. [Designing the database](#3-designing-the-database)
4. [Writing the queries](#4-writing-the-queries)
5. [Choosing the statistics](#5-choosing-the-statistics)
6. [Building the forecast](#6-building-the-forecast)
7. [Building the workbook](#7-building-the-workbook)
8. [How we knew we were right](#8-how-we-knew-we-were-right)
9. [Known weaknesses](#9-known-weaknesses)

---

## 1. Framing the problem

### 1.1 Why "growth stalled" rather than "analyse sales"

**What we did.** Framed the problem as: *the company grew fast, then stopped,
and nobody can say why.*

**What it means.** The project has a falsifiable question with a decision
attached, not a topic.

**Why this method.** A problem statement has to be something the data can
settle and a manager could act on. The deciding observation is that **margin
never moved** — it held between 23.97% and 26.93% across all five years. That
rules out the obvious explanation before the analysis starts: if margin had
collapsed, the answer would be "we are discounting too hard" and no database
would be needed. Because margin held while revenue fell, the change must be in
*what is being sold* — which is a structural question a database can answer and
a single annual revenue figure cannot.

**What we rejected.** "Analyse sales trends" — an activity, not a problem, and
nothing can falsify it. "Which customers are most valuable?" — the data has 807
customers averaging 1.48 lines each, too thin for segmentation. "Forecast next
year's revenue" — we later proved the series has no projectable trend, so that
framing would have led nowhere.

**What would change it.** If margin had moved with revenue, this would be a
pricing investigation instead, and the queries would centre on discount and
cost rather than product mix.

### 1.2 Why these three business questions

**What we did.** Three questions, each mapped to named queries: the trend
(Q3), the drivers (Q5, Q7), the timing (Q4, Q8).

**Why this method.** They decompose the problem along the only three axes the
data supports — **time, product, geography** — and together they exhaust the
possible explanations. If the decline is not in time, not in product mix and
not in geography, there is nothing left in this dataset to blame.

**What we rejected.** Questions requiring data we do not have: pricing
elasticity (no cost or list price), customer churn (no repeat-purchase history
worth the name), campaign effect (no marketing data). Asking them would have
produced speculation.

---

## 2. Preparing the data

### 2.1 Why `Order ID` was replaced rather than repaired

**What we did.** Kept it as a descriptive column `order_ref` and keyed the fact
table on a generated `sale_id`.

**How we found the problem.** Counted distinct values against row count: 547
against 1,194. That alone is normal. The test that mattered was grouping by
`Order ID` and counting distinct dates and customers within each group — **194
of the 547 have more than one of each.**

**Why this method.** A primary key must identify exactly one row. This value
identifies up to three unrelated transactions. A surrogate key is the standard
response when a natural key is not unique, and keeping the original as an
attribute preserves traceability to the source file.

**What we rejected.** *Making a composite key* of (Order ID, Date, Customer,
Sub-Category) — still not unique, 36 combinations repeat. *Deduplicating* to
force uniqueness — would delete 647 real transactions and destroy the totals.
*Renumbering the source file* — that is editing raw data, which breaks
traceability.

**What would change it.** If the source had a genuinely unique order key, no
surrogate would be needed and `sales` would key on it directly.

### 2.2 Why the customer key is (name, city)

**What we did.** Keyed customers on the pair, producing 807 rows from 802
distinct names.

**How we found the problem.** Grouped names and counted distinct cities per
name: five names occur in more than one.

**Why this method.** Keying on name alone silently merges different people,
which would corrupt every per-customer figure. Adding city is the minimum
addition that separates them using only fields we have.

**What we rejected.** *Name alone* — merges five pairs. *Treating every row as
a new customer* — would report 1,194 customers and make revenue-per-customer
meaningless. *Fuzzy matching* to merge near-identical names — invents
relationships the data does not assert, and on synthetic names would be noise.

**What would change it.** A real customer ID in the source would remove the
guesswork entirely. Note the residual risk we cannot remove: two genuinely
different people with the same name in the same city would still merge.

### 2.3 Why the 36 near-duplicates were kept

**What we did.** Kept every row. Deleted nothing.

**What it means.** 36 rows repeat the same (Order ID, Date, Customer,
Sub-Category) combination but differ in amount.

**Why this method.** A customer can legitimately buy two items from the same
sub-category on one order. Nothing in the data distinguishes "a genuine second
line" from "an accidental duplicate", and the amounts differ, so they are not
copies. Deleting rows on suspicion would change every total in the project.

**What we rejected.** Deleting them — 36 lines and their revenue disappear on
an assumption we cannot test.

**What would change it.** A line-number column in the source would settle it
outright.

### 2.4 Why we documented the synthetic data instead of fixing it

**What we did.** Reported five independent signals and left the data untouched.

**How we found it.** Each signal is a check that can be re-run: zero rows with
negative profit; names ending in credential suffixes (22 of 802); payment
methods cross-tabulated against country (UPI and EMI against US cities); the
spread of the payment mix (206–260 across five methods); and the shape of the
Amount histogram, which is flat rather than bell-shaped.

**Why this method.** The brief calls data fabrication grounds for a failing
mark. Adding plausible losses to make the data look real would be exactly that.
Documenting the limitation costs nothing and demonstrates that we examined the
data rather than assuming it.

**What we rejected.** *Injecting returns or losses* — fabrication. *Saying
nothing* — the flat histogram in Checkpoint 2 would expose it anyway, and
finding it ourselves is worth more than being asked about it.

**What would change it.** Nothing about the method. The figures would become
real conclusions rather than a modelling exercise if the data were real.

### 2.5 Why two completeness flags rather than one date filter

**What we did.** Added `is_complete_year` and `is_complete_month` to the
calendar table.

**Why this method.** The two flags answer two different questions, and
collapsing them would lose one. `is_complete_year` protects **year-on-year**
comparisons from the partial 2025. `is_complete_month` protects **monthly
averages** from the ten-day March 2020 and fifteen-day March 2025. Putting them
in the calendar table means the rule is written once and every query inherits
it, instead of each query carrying its own hand-written date range that can
drift.

**What we rejected.** *A single "exclude 2025" filter* — this is what
Checkpoint 1 originally did, and it is exactly why the 2020 error survived
into the submitted report. *Hard-coded date ranges in each query* — twenty
places to update and no guarantee they agree.

**What would change it.** A dataset covering whole years at both ends would
need neither flag.

---

## 3. Designing the database

### 3.1 Why a star schema

**What we did.** One fact table, seven dimensions, 8 tables total.

**Why this method.** Every question in Task 1.1 has the same shape — *a measure,
sliced by a dimension, over time*. That is the shape a star schema is built to
answer, and it does so in a single join hop from the fact table to any
dimension. It also makes the grain explicit, which is what keeps the sums
correct.

**What we rejected.** *One flat table* — "Miami" would be stored on all 66
Miami rows, so a correction has 66 places to go wrong, and Task 1.4 would have
no genuine joins to demonstrate. *Full third normal form* — splitting further
(a separate table for order references, say) adds joins that answer no question
we have. *A snowflake beyond two levels* — the hierarchy is only ever
state→city→customer and category→sub-category, so more levels would be
theoretical.

**What would change it.** More measures at a different grain — order-level
shipping cost, say — would need a second fact table.

### 3.2 Why a `dates` table instead of date functions

**What we did.** Built a 648-row calendar table with year, quarter, month,
month name and the two completeness flags precomputed.

**Why this method.** Three reasons, in order of importance. **First**, the
completeness flags are properties of the calendar and need somewhere to live;
without the table they would be repeated conditions in every query.
**Second**, portability: `YEAR()` is MySQL and `strftime()` is SQLite, so
storing `year_number` as a column lets one query file run unchanged on both —
which is what let us cross-check every result on two engines. **Third**,
`WHERE d.year_number = 2024` can use an index; `WHERE YEAR(f.order_date) = 2024`
generally cannot, because the function has to be evaluated per row.

**What we rejected.** *Calling `YEAR()` and `MONTH()` inline* — ties the
project to one engine and loses the flags. *Storing the raw `Year-Month` text
column* — it duplicates the date, which is the redundancy we removed.

### 3.3 Why the tables are named plainly

**What we did.** `sales`, `customers`, `dates` rather than `fact_sales`,
`dim_customer`, `dim_date`.

**Why this method.** It was a deliberate choice, and the roles are unchanged —
`sales` is still the fact table because its measures are additive at the grain
of one transaction line. The names were tested against MySQL's reserved-word
list before adoption.

**What we rejected.** The `fact_`/`dim_` convention, which is standard in data
warehousing and announces each table's role in its name. Losing that is a real
cost, which is why the reports and the ERD now state the roles explicitly
instead of relying on the prefix to carry them.

---

## 4. Writing the queries

### 4.1 Why margin is `SUM(profit)/SUM(amount)` and never `AVG(margin)`

**What we did.** Computed every margin as the ratio of the two sums.

**Why this method.** Averaging a percentage treats every row as equally
important. A 508-unit sale and a 9,992-unit sale would count the same, so the
"average margin" would describe neither the business nor any actual sale.
Summing first weights each transaction by its size, which is what a business
means by "our margin".

**What we rejected.** `AVG(margin_pct)` — the intuitive-looking version, and
wrong for the reason above. This is the single most likely thing to be asked
about in a defence.

### 4.2 Why conditional aggregation for Q7

**What we did.** Used `SUM(CASE WHEN year = 2023 THEN amount ELSE 0 END)`
alongside the same for 2024, to put both years on one row.

**Why this method.** The question is "how did each sub-category change", which
requires 2023 and 2024 **side by side** so they can be subtracted. Conditional
aggregation pivots rows into columns in a single pass over the data, with no
join and no temporary table, and it works identically on MySQL and SQLite.

**What we rejected.** *A self-join* of the table to itself on sub-category —
more code, an extra pass, and it silently drops sub-categories missing from
either year. *Two separate queries* compared by hand — the comparison then
lives outside the database and cannot be checked. *A pivot function* — not
available in MySQL.

### 4.3 Why a window function for Q8, and why an alternative is supplied

**What we did.** Used `SUM(SUM(amount)) OVER (PARTITION BY category)` to give
each quarter's share of its own category, and shipped a correlated-subquery
version alongside.

**Why this method.** The question needs two levels of aggregation at once — the
quarter's revenue **and** its category's total — while keeping one row per
quarter. That is precisely what a window function does, and it reads as one
idea rather than a query nested in a query.

**What we rejected.** Nothing, exactly — the correlated subquery is *also*
shipped, because window functions need MySQL 8 and a lab machine may be on 5.7.
Both were run and return byte-identical output, so the alternative is a tested
fallback rather than a guess.

### 4.4 Why INNER joins throughout

**What we did.** Plain `JOIN` everywhere.

**Why this method.** Foreign keys guarantee every fact row has a matching
dimension row, so an inner join cannot drop data here — and we verified that
with orphan-row counts, which are zero on both sides.

**What we rejected.** `LEFT JOIN` — it would produce identical results at more
cost, and would misleadingly imply the possibility of unmatched rows. Note the
one case where it *would* be needed: showing categories with **zero** sales in
a period, since those have no fact rows to match.

---

## 5. Choosing the statistics

### 5.1 Why order count was chosen as the predictor

**What we did.** Regressed monthly revenue on monthly order count.

**How we chose it.** By testing the candidates, not by assuming:

| Predictor of monthly revenue | r | R² | p | Verdict |
| --- | --- | --- | --- | --- |
| **Orders per month** | **0.9227** | **0.8514** | 2.0 × 10⁻²⁴ | **Chosen** |
| Units sold per month | 0.8670 | 0.7517 | 2.8 × 10⁻¹⁸ | Weaker, and less actionable |
| Profit per month | 0.9427 | 0.8887 | 6.8 × 10⁻²⁸ | Highest R², but **circular** |
| Time index | 0.0881 | 0.0078 | 0.515 | Not significant |

**Why this method.** Three criteria, applied in order. **Non-circularity
first:** profit has the highest R², and it is disqualified precisely because of
that — profit is derived from revenue, so regressing one on the other tests
arithmetic, not business behaviour. Reporting R² = 0.89 from that model would
be the most impressive-looking and least meaningful result in the project.
**Then strength:** orders beats units (0.85 against 0.75). **Then
actionability:** a business can influence how many orders it wins far more
directly than how many units each contains.

**What would change it.** If units had beaten orders substantially we would
have used units and the recommendation would have been about basket size rather
than order volume.

### 5.2 Why the model is credible beyond its R²

**What we did.** Compared the fitted slope against a quantity computed a
completely different way.

**What it means.** The slope is **5,224.25**. The mean transaction line is
**5,178.09**. They agree to within **0.9%**.

**Why this matters more than R².** A high R² only says the line fits the points.
It cannot tell you the model describes the mechanism rather than a coincidence.
Here the slope has a physical meaning — *revenue added per extra order* — and
it lands on the average order value, which is what must happen if revenue is
order count multiplied by a stable order size. Two independent routes to one
number is corroboration; R² alone is not.

### 5.3 Why a correlation that shows nothing was included

**What we did.** Reported quantity against amount: r = 0.0446, p = 0.123.

**Why this method.** The brief asks for two pairs, and choosing two obvious
positives would demonstrate nothing beyond the ability to run `CORREL`. This
pair tests an assumption a real business would act on — *sell more units, earn
more revenue* — and finds it false. That is a decision-relevant result: it
rules out a units-based sales target.

**Why it is stated as "not significant" and not "no relationship".** At
p = 0.123 we fail to reject the null; we have not proven the correlation is
zero. The distinction matters and is a likely defence question.

### 5.4 Why the coefficient of variation earns its place

**What we did.** Reported SD ÷ mean alongside the raw standard deviations.

**Why this method.** The brief asks for standard deviation, which is not
comparable across variables with different units — 2,805 for Amount and 1,118
for Profit look like Amount varies more. Dividing by the mean makes them
comparable, and reverses the reading: Profit's **82.9%** against Amount's
**54.2%** shows profit is the *less* predictable of the two. That is a finding
the required statistics alone would have hidden.

### 5.5 Why `COUNTIFS` and not `FREQUENCY` for the histogram

**What we did.** Counted each bin with its own `COUNTIFS` formula.

**Why this method.** `FREQUENCY` is an array formula. It returns one block that
must be entered across a range, which makes individual bins non-auditable and —
relevant here — does not survive being written by a library outside Excel. One
independent formula per bin can be clicked on and read, and a total row checks
they sum to `COUNT(Amount)`.

---

## 6. Building the forecast

This is the section where our chosen method **did not win**, and the honest
account is more useful than a tidy one.

### 6.1 Why no trend was projected

**What we did.** Tested for a linear trend, found none, and projected no growth
rate.

**How we tested it.** Regressed revenue on a time index — and, because
"no trend" could be an artifact of the window chosen, repeated it on four
windows:

| Window | Slope per month | p | Verdict |
| --- | --- | --- | --- |
| Last 12 months | −1,840.6 | 0.497 | Flat |
| Last 24 months | +172.1 | 0.857 | Flat |
| Last 36 months | −666.6 | 0.314 | Flat |
| All 57 months | +206.0 | 0.515 | Flat |

**Why this method.** No window shows a significant slope, so "there is no
trend" is a property of the series and not of our choice of window. Projecting
a slope this weak forward would compound a number indistinguishable from noise.

**What we rejected.** *Fitting the trend anyway* — it is the expected thing to
do and would have produced a confident, wrong line through a structural break.
Measured on the holdout it is worse than a flat mean (16.3% against 14.9%), so
rejecting it was correct on the evidence as well as in principle.

### 6.2 Why level × seasonal index — and why that was arguably wrong

**What we did.** Forecast each month as the mean of the last 24 months
multiplied by that month's seasonal index.

**Why we chose it.** The seasonality in the 57-month history is large and
consistent — December sits at 1.273 and January at 0.679, nearly a factor of
two. Ignoring a swing that size seemed indefensible, and with no trend to
project, level × index is the standard construction.

**How it actually performed.** All eight candidate methods, scored on the two
complete holdout months:

| Method | Mean absolute error |
| --- | --- |
| Flat, last 12 months | **14.8%** |
| Flat, last 24 months | 14.9% |
| Flat, all 57 months | 15.3% |
| Linear trend projection | 16.3% |
| 3-month moving average | 16.3% |
| Seasonal × level (12m) | 22.4% |
| **Seasonal × level (24m) — what we used** | **22.7%** |
| Trend × seasonal | 24.6% |

**The honest reading.** Our method placed **fifth of eight**. Every flat model
beat every seasonal one. The cause is identifiable: January 2025 came in at
112,906 against a seasonal prediction of 68,853 — it behaved like an average
month, not like its historical index.

**Why we did not simply switch to the flat model.** Two observations cannot
choose between forecasting methods. Switching to whichever method won on two
data points is *overfitting the holdout* — the exact error the holdout exists to
prevent. The defensible position is the one we take: the seasonal structure is
real in 57 months of history, it failed on the one January we could test, and
two months is not enough to conclude which will hold. That uncertainty is
reported rather than resolved by fiat.

**What would change it.** A full year of holdout. If January 2026 also comes in
near the average, the seasonal pattern has genuinely broken and the flat model
is right.

### 6.3 Why the last 24 months for the level

**What we did.** Averaged the most recent 24 months.

**Why this method.** It has to be long enough to average out noise and short
enough to exclude the 2020–2022 growth phase, which is a different regime. The
trend test above confirms the last 24 months are flat (p = 0.857), which is the
condition under which a mean is the right summary.

**What we rejected.** *All 57 months* — includes the growth phase and would sit
too low. *The last 12* — flat too, and marginally better on the holdout, but
half the data for no principled reason. The choice was made on regime, not on
holdout score.

### 6.4 Why hold anything out at all

**What we did.** Excluded January and February 2025 from every calculation, then
forecast them and compared.

**Why this method.** A forecast checked against the data that built it is not
checked at all. Holding data back is the cheapest honest test available, and it
is what turned "here is a forecast" into "here is a forecast, and here is how it
did."

**What we rejected.** *No validation* — the common approach, and it would have
let us present a forecast with no idea whether it works. *Cross-validation* —
the right tool with more data; with two eligible months there is nothing to
fold.

---

## 7. Building the workbook

### 7.1 Why every computed cell is a formula

**What we did.** No pasted values anywhere — 1,724 live formulas.

**Why this method.** A pasted number is a photograph of a result. It cannot be
checked, it does not update, and nothing reveals it if the source data changes
underneath it. A formula can be clicked on and read, which is also how a marker
verifies the work.

### 7.2 Why named ranges

**What we did.** Named each column of the data sheet.

**Why this method.** `=SUMIF(Category,"Electronics",Amount)` states its own
intent; `=SUMIF('Cleaned Data'!$M$2:$M$1195,"Electronics",'Cleaned Data'!$Q$2:$Q$1195)`
does not, and a mistyped column letter in the second form is invisible.

**The trade-off we accepted.** Named ranges are fixed at rows 2–1195, so rows
added below are invisible to every formula. The documented fix is to re-run the
builder rather than extend by hand.

### 7.3 Why only Excel-2007-era functions

**What we did.** Restricted the workbook to `SUMIFS`, `INDEX`, `VLOOKUP`,
`TDIST` and similar; avoided `XLOOKUP`, `FILTER`, `TEXTJOIN`.

**Why this method.** Newer functions are spilling array formulas. A file written
by a library outside Excel carries no spill metadata, so only the top-left cell
of the range would get a value — and it would fail *silently*, reporting no
error while producing wrong output. Older functions have no such failure mode.

### 7.4 Why both cross-tabs and native PivotTables

**What we did.** Shipped four SUMIFS cross-tabs *and* three PivotTable objects.

**Why this method.** They are good at different things. A cross-tab is
auditable — every cell has a readable formula. A PivotTable is interactive and
is what "pivot table" most likely means to a marker. Building both costs little
and removes the risk of guessing which reading applies.

### 7.5 Why the self-check block exists

**What we did.** Seven formulas on the first sheet, each recomputing a total two
independent ways and comparing.

**Why this method.** The workbook was built in an environment where Excel could
not be opened, so its formulas had **never been calculated** before delivery.
Rather than claim it works, the file tests itself the first time it is opened.
This is the one honest response available to "I cannot verify this myself."

---

## 8. How we knew we were right

### 8.1 Verification against the source, not against notes

**What we did.** Every figure quoted in every report and explainer was
recomputed from the database and compared against the text, mechanically, each
time a document changed.

**Why this method.** Numbers copied between documents drift. Recomputing from
the source catches it; re-reading does not.

### 8.2 Cross-engine agreement

**What we did.** Ran all eight queries on both MySQL and SQLite and compared
row by row.

**What it caught.** Two real defects. A **non-deterministic `ORDER BY`** in Q2 —
three rows tie on both sort keys, so the engines returned them in different
orders, meaning a screenshot could disagree with the report. Fixed with a
tiebreaker. And a **one-cent rounding difference** in one cell, where MySQL
rounds half away from zero and SQLite rounds half to even on a value ending in
exactly .325 — documented rather than papered over.

### 8.3 Where verification failed to catch something

**What we did.** Found the partial-2020 error only in Checkpoint 2.

**What it means.** Every Checkpoint 1 figure was verified against the database
and every one was correct. The error was not arithmetic — it was **comparing
nine months against twelve** and calling the difference growth. Verification
confirms that a number matches the data; it cannot tell you the number answers
the question.

**What caught it in the end.** Building the monthly series forced every month to
be counted individually, which made the short year impossible to miss. The
lesson worth stating in a defence: *changing the unit of analysis is a
diagnostic in itself.*

---

## 9. Known weaknesses

Stated because being asked about a weakness you have already named is a very
different conversation from being caught by one.

| Weakness | Why it stands | What it would take to fix |
| --- | --- | --- |
| The data is synthetic | Fabricating realism is a failing offence | A real dataset |
| The regression assumes months are independent | Sales series are usually autocorrelated, which inflates significance | A Durbin-Watson test, or time-series methods beyond this course |
| One predictor only | Cannot capture mix, seasonality or the Printer problem together | Multiple regression — Checkpoint 4 |
| The forecast lost to a flat mean | Two holdout months cannot settle it | A full year of holdout |
| Printers is a *where*, not a *why* | Supply failure and demand collapse look identical in a sales table | Stock and supplier records |
| Two names in one city would still merge | No customer ID in the source | A real customer key |
| The 2025 rounding difference | Engines round half-values differently | Nothing — it is documented |

**The one that matters most.** Finding 2 says Printers lost 136,865 — more than
half the entire gap. It does **not** say why. A supply failure and a demand
collapse produce an identical signature in a sales table and demand opposite
responses: chase the supplier, or exit the line. The recommendation is
therefore to check stock and supplier records **before** concluding anything
about demand. Knowing what the data cannot tell you is part of the analysis,
not a gap in it.
