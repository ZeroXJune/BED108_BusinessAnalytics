# Sales Trend Analysis — Group Discussion Script

**BED 106 Business Analytics — Mini Capstone Project**
Talibon Polytechnic College

A three-speaker script for presenting and discussing the project. The running
order follows the project brief: Task 1.1 through 1.4 for Checkpoint 1, then
Task 2.1 through 2.5 for Checkpoint 2, then the limitations, then Q&A.

Running time is roughly **15 minutes** for the script itself, plus Q&A.

---

## Before you use this

**Read this part first. It affects your marks.**

Section 3.2 of the brief states that AI-generated analysis is not permitted and
that insights must be derived by the students themselves. This script was
drafted with AI assistance, so **do not read it out as written**. Use it the way
you would use a lecture outline: it tells you *what to cover, in what order, and
which number belongs where*. The sentences that come out of your mouth have to
be yours.

Practically, that means: read a segment, close the script, and say the same
thing in your own words. If you cannot say it without looking, you do not
understand it yet — and Section 1.4 lets the instructor ask **any member** to
explain **any part** of the project.

Every figure quoted here has been checked against the database. If you are
asked where a number comes from, the answer is always a specific query or a
specific worksheet cell, and those are named in the margin notes.

### The speakers

| Label | Role from the brief | Covers |
| --- | --- | --- |
| **LEAD** | Project Lead / Analyst | The business problem, the findings, what the business should do |
| **DATA** | Data Engineer | The dataset, its quality, the ERD, the database, the workbook build |
| **STATS** | Statistician / Modeler | The queries, descriptive statistics, correlation, regression, forecasting |

If your group has four members, the **BI Developer / Visualizer** takes the
figures and charts: split segment 4 (the queries) and segment 9 (the forecast
chart) so that the visualiser presents each chart and STATS presents the number
behind it.

### What to have on screen

| Segment | Show |
| --- | --- |
| 1 | Cover page, or Figure 1 (annual trend) |
| 2 | The raw CSV preview, first 10–20 rows |
| 3 | `docs/figures/erd.png`, then the `SHOW TABLES` screenshot |
| 4 | Query screenshots Q3, Q5, Q8 |
| 5 | The workbook — Cleaned Data, then a PivotChart |
| 6 | The Amount histogram |
| 7 | The two scatter plots |
| 8 | The ToolPak regression output |
| 9 | Figure 2 with the regime shading, then the forecast chart |
| 10 | The correction table from the Checkpoint 2 report |

---

## Segment 1 — The business problem (Task 1.1)

*About 2 minutes. LEAD opens.*

**LEAD.** Our domain is Retail and Sales Analytics, and our topic is sales
trend analysis. The subject is a multi-category retailer — electronics,
furniture and office supplies — trading across six US states between 2020 and
2025.

The problem is simple to state and not simple to answer: **the company grew,
then stopped**. On a like-for-like monthly basis, revenue rose 30.9% from 2020
to the 2022 peak, then fell in each of the next two years and finished 2024 at
17.6% below that peak.

**DATA.** Why is that an analytical problem? Falling sales is not exactly a
mystery.

**LEAD.** Because of what *didn't* move. Margin held between 23.97% and 26.93%
for the whole five years, and average order value stayed between 5,008 and
5,444. If margin had collapsed, the answer would be "we discounted too hard"
and nobody would need a database to find that. Margin held steady while revenue
fell, which means the company is writing **fewer orders**, not worse ones. And
"fewer orders of what, when, and where" is a question a single annual revenue
figure cannot answer.

**STATS.** So the business questions.

**LEAD.** Three of them, and every deliverable in this project maps back to
one:

| # | Question | Answered by |
| --- | --- | --- |
| 1 | How have revenue and profit trended, and is the company still growing? | Query 3, and the Checkpoint 2 regression |
| 2 | Which categories and sub-categories drive the trend? | Queries 5 and 7 |
| 3 | When does demand concentrate, and is the pattern the same for every category? | Queries 4 and 8 |

Why it matters: the decisions hanging off these answers are what to stock, when
to stock it, and where to put the sales effort. Getting them wrong costs
inventory that does not sell and campaigns that land in the wrong quarter.

---

## Segment 2 — The dataset and what was wrong with it (Task 1.2)

*About 2.5 minutes. DATA leads.*

**DATA.** The dataset is a retail sales export, 1,194 transaction lines and 12
columns, covering 22 March 2020 to 15 March 2025. The brief asks for at least
200 rows. The grain — and this is the word to remember — is **one row per
product line on an order**, not one row per order.

We ran a quality assessment before touching anything, and found five problems.
I will take them in order of how much trouble they caused.

**One. `Order ID` is not a primary key.** There are 1,194 rows but only 547
distinct order IDs, and the repeats are not duplicate rows — the same ID
appears on different dates, for different customers. So it does not identify an
order either. We kept it as a plain attribute and issued our own surrogate key,
`sale_id`.

**LEAD.** Why not repair it instead?

**DATA.** Because repairing it means deciding which of two rows with the same
ID is the "real" one, and we have no evidence for that decision. Inventing that
evidence is data fabrication, which the brief says is grounds for a failing
mark. Documenting the defect costs us nothing analytically — no question we ask
needs order identity.

**Two. Customer name is not an identifier either.** 807 customers resolve from
802 distinct names, because five names appear in more than one city. Our
customer key is the pair (name, city).

**Three.** The `Year-Month` column is redundant — it is derivable from the
date, so it does not belong in a normalised schema. We rebuilt it in the
`dates` table.

**Four. Both ends of the file are partial.** It starts 22 March 2020 and stops
15 March 2025. That matters more than it sounds, and it is where our one
significant error came from. I will come back to it.

**Five, and the one to be upfront about: the dataset is synthetic.** It is not
real trading data. We have five machine-checked signals:

- Not one loss-making line in five years — no real retailer has that
- 22 of the 802 names end in credential suffixes like "MD" or "DDS", which is a Faker library artefact
- US cities paired with UPI and EMI payment methods, which are Indian payment rails
- The payment mix is near-uniform, 206 to 260 across every method
- The Amount histogram is flat, not normal — real transaction values are right-skewed

**STATS.** And we did not fix any of it.

**DATA.** We did not. Fixing it would mean inventing numbers. What we did
instead was state it, prove it, and carry the limitation into every conclusion.
The method is unaffected — every query and every statistic in this project
would run identically against a real export.

---

## Segment 3 — The database (Task 1.3)

*About 2 minutes. DATA continues, with the ERD on screen.*

**DATA.** We normalised the flat file into a **star schema**: one fact table
surrounded by seven dimensions, eight tables in total.

`sales` is the fact table, one row per transaction line. Around it:
`customers`, `cities`, `states`, `categories`, `sub_categories`,
`payment_modes` and `dates`.

**LEAD.** Why a star, and not just the one table we started with?

**DATA.** Three reasons.

First, **consistency**. In the flat file, a category name is repeated on every
row that uses it, so a typo in one row creates a category that does not exist.
In the star, the name lives once in `categories` and the fact table carries an
integer key. A typo becomes impossible rather than merely unlikely.

Second, **the brief asks for it** — Task 1.3 requires at least two related
tables with proper primary and foreign keys. We have eight tables, eight
primary keys, seven foreign keys, six unique constraints and four check
constraints, and we tested that the constraints actually reject bad rows rather
than assuming they would.

Third, **it is what the queries need**. The category trend question needs
category and date on the same row as the amount; a star gives you that in one
join.

**STATS.** Say something about the `dates` table, because that is the one that
looks like overkill.

**DATA.** It looks like overkill until you try to write the queries. Two
reasons it earns its place. One, it keeps the SQL portable — we never call
`YEAR()` or `strftime()`, so the same query file runs unchanged on MySQL and on
SQLite, and we verified that. Two, it carries two flags the raw dates cannot:
`is_complete_month` and `is_complete_year`. Those flags are the fix for problem
four, the partial ends of the file, and they are what stops anyone
accidentally comparing a nine-month 2020 against a full 2021.

One trap worth flagging because it cost us real time: `year_month` is a
**reserved word in MySQL**. `CREATE TABLE dates` failed outright with a syntax
error until we backticked it. We only found that because we installed a real
MySQL server and ran the import rather than assuming the file was fine.

The whole thing loads from one file — `02_mysql_full_import.sql` creates the
database, all eight tables and all the data, and ends with a verification block
whose last row must read 1,194 rows, 6,182,639.00 in revenue, 547 order IDs and
57 complete months, with zero orphans.

---

## Segment 4 — The eight queries (Task 1.4)

*About 3 minutes. STATS leads. Have the Q3, Q5 and Q8 screenshots ready.*

**STATS.** Eight queries in four groups: two basic retrievals with `WHERE` and
`ORDER BY`, two aggregates with `GROUP BY`, two multi-table joins — ours join
four tables each — and two business-insight queries. I will skip the mechanics
and go to what they found, which is four things.

**Finding one — growth stopped in 2022, and it stopped in a specific way.**
Query 3 aggregates by year, but on a **per-month** basis so the partial years
cannot distort it. Revenue per month went from 92,934 in 2020, up to 121,648 at
the 2022 peak, then down to 100,207 in 2024. Meanwhile margin never left the
24-to-27% band and average order value never left the 5,008-to-5,444 band. That
combination is the whole diagnosis: fewer orders, not cheaper or less
profitable ones.

**LEAD.** Which is actionable in a way that "revenue fell" is not. It points at
demand generation, not at pricing.

**STATS.** **Finding two — one sub-category explains most of the gap.** Query 5
and Query 7 break the trend down by category and sub-category. Printers lost
136,865 between 2023 and 2024, a 71.0% collapse — that single line item is over
half of the entire peak-to-2024 gap. Every Electronics sub-category fell, and
the category as a whole is down 40.8%. Every Office Supplies sub-category grew;
Paper is up 85,689, or 149.4%.

**DATA.** So it is not a general slowdown.

**STATS.** It is not. Two opposite trends are running at once, and the
company-wide figure is their average, which describes neither. That is the
single most useful thing Checkpoint 1 produced.

**Finding three — seasonality is category-specific.** Query 4 and Query 8. The
blended figure says Q4 is the peak quarter. Split it out and Electronics
actually peaks in **Q2**, at 30.79% of its annual revenue, while Furniture
peaks in Q4 at 30.84% and Office Supplies in Q4 at 32.16%. So a single blended
planning curve is wrong for all three categories — it over-stocks Electronics
in Q4 and under-stocks it in Q2.

**Finding four — geography is not a factor.** Query 6. Across five years, state
revenue spans only 28% between the highest and the lowest, with no state
trending against the others. Not every finding has to be a discovery; this one
tells the business where *not* to spend its analytical effort.

---

## Segment 5 — The workbook (Task 2.1)

*About 1.5 minutes. DATA leads, workbook on screen.*

**DATA.** Checkpoint 2 takes the same dataset — the brief requires the same
dataset — out of the database and into Excel. The workbook has thirteen sheets.

The one design decision to be able to defend: **everything is live formulas,
not pasted values.** Around 1,724 of them. The cross-tabs are `SUMIFS`,
`COUNTIFS` and `AVERAGEIFS` against named ranges over the Cleaned Data sheet,
so if a row changed, every statistic downstream would change with it. Pasted
values would have looked identical and proved nothing.

Beyond the brief's minimum we added three native PivotTables, each with a bound
PivotChart, sharing one pivot cache — the brief asks for three pivot tables and
three pivot charts, and the SUMIFS cross-tabs alone would have been arguable.

There are also seven **self-check** formulas on the Read Me sheet. Each one
recomputes a headline figure by an independent route and prints OK or MISMATCH.
The row count, the revenue total and the regression slope are all checked that
way. If someone edits a cell they should not have, the workbook says so.

---

## Segment 6 — Descriptive statistics (Task 2.2)

*About 1.5 minutes. STATS.*

**STATS.** Three numerical variables: Amount, Profit and Quantity. Mean,
median, mode, standard deviation, variance, range, quartiles, IQR and
coefficient of variation for each, plus a frequency distribution and a
histogram.

Two things in there are worth your attention; the rest is table-filling.

**One — Profit is far less predictable than revenue.** Amount has a coefficient
of variation of 54.2%. Profit has 82.9%, and a skew of +0.94. So profit is both
more variable *and* asymmetric — a long right tail of a few very profitable
lines. Practically: a revenue target does not manage profit, because the two do
not move together tightly enough for one to stand in for the other.

**LEAD.** That is the point that changes what we recommend for the dashboard.

**STATS.** It is. **Two — the histogram is the real finding.** Amount is
distributed almost flat across its range. Real transaction values are
right-skewed: many small sales, few large ones. A flat distribution is what a
random number generator produces. So our own descriptive statistics
independently confirm the synthetic-data conclusion from Checkpoint 1, and we
report it as evidence rather than hiding it.

---

## Segment 7 — Correlation (Task 2.3)

*About 1.5 minutes. STATS, scatter plots on screen.*

**STATS.** Two required pairs plus a third for support. Pearson's r, with
scatter plots and fitted trendlines.

**Pair one — monthly order count against monthly revenue: r = 0.9227.** Strong
positive. Order count explains about 85% of the variation in monthly revenue.
Checkpoint 1 *inferred* that fewer orders were the mechanism; this measures it.

**Pair two — line quantity against line amount: r = 0.0446, p = 0.123.** No
relationship, and not statistically significant, so we cannot reject the null
hypothesis that the true correlation is zero. This is a **negative result and
we are keeping it**, because it kills an obvious strategy: a "sell more units"
target would not move revenue in this business. Price per line varies far more
than units per line.

**Supporting pair — amount against profit: r = 0.6753**, so about 46% of profit
variation tracks revenue. Moderate, not strong. Same conclusion as the CV
figures from the previous segment, reached a different way.

**DATA.** And the caveat.

**STATS.** Correlation is not causation, and we say so explicitly. Order count
and revenue could both be driven by something else — market conditions, a
campaign we cannot see in this data. What we can say is that the association is
strong and consistent over 57 months, not that one causes the other.

---

## Segment 8 — Regression (Task 2.4)

*About 2 minutes. STATS, ToolPak output on screen.*

**STATS.** We regressed monthly revenue on monthly order count over the 57
complete months. The equation:

**Revenue = −1,353.65 + 5,224.25 × Orders**

Reading it properly:

- **The slope, 5,224.25.** One additional order in a month is associated with
  about 5,224 more revenue in that month. Here is the check that makes this
  convincing: the mean order value in the data is 5,178.09. The slope lands
  within 0.9% of it — the regression rediscovered the average order value
  without being told it.
- **R² = 0.8514.** Order count explains 85% of the month-to-month variation in
  revenue.
- **Significance: t = 17.75, 55 degrees of freedom, p = 1.98 × 10⁻²⁴.** The
  slope is not zero. That is not a marginal result.
- **The intercept, −1,353.65, is not meaningful.** Zero orders cannot produce
  negative revenue. It is where the fitted line crosses the axis, extrapolated
  outside the range of the data, and we do not interpret it.

**LEAD.** And the forecast the brief asks for.

**STATS.** The company is running about four orders per month below its 2022
level. At 5,224 per order, closing that gap is worth roughly **250,000 a
year**. Checkpoint 1 arrived at 257,297 by an entirely different route —
summing the actual category shortfalls. Two independent methods landing within
3% of each other is the strongest single piece of evidence in this project.

We list six limitations, and I will name the three that matter most: it is a
single-predictor model, so it says nothing about *why* orders fell; it is
fitted on 57 monthly points, which is not many; and it should not be
extrapolated beyond the observed range of order counts.

---

## Segment 9 — Trend and seasonality (Task 2.5)

*About 2.5 minutes. STATS and LEAD share this. Figure 2 on screen, then the forecast chart.*

**STATS.** This is the segment that carries our topic, so I want to be precise
about what we did and did not find.

The trend is real and it is the finding: **the series runs in two regimes.**
Growth from 2020 to 2022 — 92,934 up to 121,648 per month, +30.9%. Then a
plateau from 2022 to 2024 — down to 100,207, −17.6%. You can see both on
Figure 2; the shading marks where one ends and the other begins.

**LEAD.** Then why is there no growth rate in the forecast?

**STATS.** Because we tested for one and there isn't a single one. We fitted a
straight line across all 57 months and it explains **under 1% of the variation
— R² = 0.0078, p = 0.515.** We ran it on four different windows and got the
same answer each time.

That result is not "no trend". It is "**no single straight line fits both
regimes**", which is exactly what you would expect from a series that rises and
then flattens: the up-slope and the flat cancel out, and the average of the two
is nearly horizontal. Reporting that honestly, and refusing to project a growth
rate we cannot demonstrate, is the correct handling — projecting one anyway
would be inventing a number.

So the forecast is built from **level and seasonality** instead of from a trend
line. We computed monthly seasonal indices — January runs at 0.679 of an
average month, October at 1.229, December at 1.273 — and applied them to the
recent level to project the six months from January to June 2025.

**DATA.** And you tested whether that actually worked.

**STATS.** We did, and it is the part of this project I would most want the
instructor to see. We held out the two months we could check and compared the
seasonal forecast against a naive flat average. **The seasonal forecast lost.**
Mean absolute error 22.7% against the flat average's 14.9%. It ranks fifth of
the eight methods we tested.

The reason is visible: January 2025 came in at 112,906 against our prediction of
68,853. January's seasonal index says January is the weakest month of the year,
and this January was not.

**LEAD.** So why keep the seasonal method?

**STATS.** Because switching methods on the strength of two observations is
overfitting the holdout — you would be choosing the model that happened to win
on a two-month sample, which is not evidence. We report the result, we keep the
method, and we say plainly that our forecast reliability over this horizon is
weak. The reliability discussion the brief asks for is not a formality here; we
have measured our own error and it is 22.7%.

---

## Segment 10 — The correction, and what we would tell the business

*About 2 minutes. LEAD closes, with DATA on the correction.*

**DATA.** Before the conclusion, one thing we have to put on the record
ourselves. Building the Checkpoint 2 monthly series exposed an **error in our
own Checkpoint 1**.

We treated 2020 as a full year. The file starts 22 March, so 2020 holds nine
months. That overstated 2020-to-2022 growth as **69.9%** when the like-for-like
figure is **30.9%**. It also distorted March's seasonal index, from 1.025 down
to 0.876.

| Affected | Unaffected |
| --- | --- |
| The 2020→2022 growth figure | The −17.6% peak-to-2024 decline — both are full years |
| March's seasonal index | Printers −136,865; Electronics −40.8% |
| | Category-specific seasonality; the geography finding |

The central thesis is unchanged; one supporting number was overstated. We
reissued Checkpoint 1 with an `is_complete_month` flag and a per-month column
in Query 3 so the mistake cannot recur, and it is documented in the Checkpoint
2 report either way.

**LEAD.** Three recommendations come out of this, and each one is tied to a
measurement rather than an opinion.

**One — track order count, not revenue.** Revenue is the lagging indicator;
order count is what drives it, r = 0.923, and it is the thing the business can
actually act on.

**Two — plan seasonality by category, not company-wide.** The blended curve is
wrong for all three categories. Electronics peaks in Q2; the other two peak in
Q4.

**Three — investigate Printers first.** One sub-category, 136,865, over half
the gap. Whether that is a supply problem, a competitive loss, or a category in
structural decline is not something this dataset can tell us — but it tells us
where to look, and that is what the analysis was for.

**STATS.** And the honest summary of the limitations.

**LEAD.** Three. The data is synthetic, so the *figures* illustrate the method
rather than describe a real company. The forecast is weak — 22.7% error against
a flat average's 14.9%, and we say so rather than quietly dropping the test.
And correlation is not causation: we have shown that order count and revenue
move together, not that one causes the other.

What we would stand behind is the method: a defect-documented dataset, a
normalised schema with enforced constraints, queries verified on two database
engines, and statistics tested for significance rather than eyeballed — with
the negative results reported alongside the positive ones.

---

## Q&A — likely questions and who takes them

*Answer in your own words. Whoever owns the area takes the question; the others
should be able to take it too.*

| Question | Who | The short answer |
| --- | --- | --- |
| Your dataset looks fake — doesn't that invalidate the project? | DATA | It invalidates the figures, not the method. We proved it with five signals and did not fabricate corrections, which would be worse. |
| Why didn't you use `Order ID` as the primary key? | DATA | 1,194 rows, 547 distinct IDs, and the repeats span different dates and customers. It identifies neither a row nor an order. |
| Why eight tables instead of one? | DATA | Consistency, enforced constraints, and because the queries need category and date on the same row as the amount. |
| Why a `dates` table? | DATA | Portability — no `YEAR()` or `strftime()`, so the same SQL runs on MySQL and SQLite — plus the two completeness flags. |
| Why exclude 2025 and show 2020 per month? | DATA | Both ends are partial. Including them whole would show a fake collapse and fake growth. This is exactly the mistake we made and corrected. |
| Is R² = 0.85 good? | STATS | For cross-sectional business data, yes — but R² alone is not the test. The p-value of 1.98 × 10⁻²⁴ is what says the slope is not zero. |
| Your trend test found nothing. Doesn't that sink a *trend* project? | STATS | It found that no single line fits both regimes, which is itself the finding. The trend is real; it is just piecewise, and Figure 2 shows it. |
| Why not project a growth rate anyway? | STATS | Because we cannot demonstrate one. Projecting a number we tested for and did not find would be inventing it. |
| Your forecast lost to a flat average. Why keep it? | STATS | Choosing a method on two observations is overfitting the holdout. We report the loss and state the reliability honestly. |
| Correlation or causation? | STATS | Association only. Strong and consistent over 57 months; not proof of a mechanism. |
| What does the intercept mean? | STATS | Nothing usable. Zero orders cannot produce negative revenue — it is an extrapolation outside the data. |
| Why is the workbook all formulas? | DATA | So the analysis is reproducible and auditable. Pasted values would look identical and prove nothing; the seven self-checks would not work. |
| What would you do differently? | LEAD | Validate the source before building on it, and check the completeness of both ends of the date range first — that is what caused our one real error. |
| What is next? | LEAD | Checkpoint 3: a dashboard built on order count as the primary KPI and margin as the segmentation, because revenue is a poor proxy for profit here. |

---

## Rehearsal checklist

- Every number you say out loud, you can point to — a query, a figure, or a cell
- Each speaker can answer at least one question from another speaker's segment
- Someone owns the screen and knows the order the exhibits appear in
- You have said the synthetic-data limitation out loud before anyone asks
- You have said the Checkpoint 1 correction out loud before anyone finds it
- Total run time under the limit, with Q&A time left over
