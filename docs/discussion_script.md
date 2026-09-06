# Sales Trend Analysis — Recording Script

**BED 106 Business Analytics — Mini Capstone Project**
Talibon Polytechnic College

Each speaker records their own part straight through, in their own time and
place. Nobody waits for a cue, nobody answers anybody, and nobody states a role
— each part simply continues the explanation where the last one stopped. Alber
joins them in order afterwards.

| Part | Speaker | Covers | Approx |
| --- | --- | --- | --- |
| 1 | Alber | Opening; the business problem and the three questions | 3:00 |
| 2 | Julebeth | Checkpoint 1 — the dataset, the database, the eight queries and what they found | 6:40 |
| 3 | Alber | The Checkpoint 2 workbook | 1:30 |
| 4 | Mardy | Checkpoint 2 — descriptive statistics, correlation, regression, the trend and the forecast | 6:25 |
| 5 | Alber | The correction, what it means for the business, the questions, the close | 6:00 |

Roughly **23 minutes** assembled — about **10:30** of it Alber, and **6:30**
each for Julebeth and Mardy. Alber records three separate files; Julebeth and
Mardy record one each.

If you were given a time limit shorter than that, the two places to cut are the
descriptive statistics and the correlation in Part 4 — each survives as two
sentences. Do not cut a whole task; the brief's tasks are what is being marked.

---

## Before you record

**Read this part first. It affects your marks.**

Section 3.2 of the brief states that AI-generated analysis is not permitted and
that insights must be derived by the students themselves. This script was
drafted with AI assistance, so **do not read it out as written**. Use it the way
you would use a lecture outline: it tells you *what to cover, in what order, and
which number belongs where*. The sentences that come out of your mouth have to
be yours.

The practical test: read a section's beats, close the script, and say the same
thing in your own words. If you cannot say it without looking, you do not
understand it yet — and Section 1.4 lets the instructor ask **any member** to
explain **any part** of the project, recording or no recording.

Every figure quoted here has been checked against the database. If you are asked
where a number comes from, the answer is always a specific query or a specific
worksheet cell, and those are named beside each section.

---

## How to record your part

**Say your name once, at the start of your first part** — your instructor is
matching a voice to a name for a mark under Section 1.4, and the video may not
show your face. Alber records three parts and only needs to do this in Part 1;
the later two just continue.

**Say nothing about who did what.** Your name, then straight into the material.
Nobody claims a task, a role, or a contribution — the recording discusses the
project, not the group. Everything you say is about Checkpoint 1 and Checkpoint
2 and how the work progressed.

**Record straight through.** Your part is one continuous explanation. If you
stumble, do not stop the recording: pause, take a breath, and repeat that
sentence from the beginning. Alber cuts the repeat out. Restarting from the top
every time you fluff a word is how a twenty-minute job becomes an evening.

**Leave two seconds of silence at the start and the end.** Press record, wait,
then speak. At the end, stop talking and let it run for two seconds before you
stop recording. Cuts made against silence are clean; cuts made against a breath
are not.

**Screen-record with audio; do not film a monitor.** Every exhibit in this
project is on a screen — the ERD, the query output, the workbook, the figures.
Filmed off a monitor the numbers are unreadable, and unreadable evidence is the
same as no evidence.

**Have your exhibits open before you press record**, in the order the script
lists them, so you are not hunting for a window mid-sentence.

**Agree three settings before anyone records:** screen resolution (1920 × 1080
is the safe choice), video format, and roughly how close you sit to the mic.
Three parts recorded at three different volumes is the one problem that is
genuinely annoying to fix afterwards.

**Do a thirty-second test first.** Record, play it back, and check three things:
your voice is audible, the on-screen text is legible at that resolution, and no
fan or echo is drowning you. Finding this out after you have recorded everything
is the most common way groups lose an evening.

**Name your file by part number** — `Part2_Julebeth.mp4` — and send Alber the
take you want used, not every take you shot.

---

## For Alber, as editor

Join the five parts in order: 1, 2, 3, 4, 5. There is nothing to interleave.

**Normalise the audio levels first.** Three people in three rooms will not
match, and a viewer reaching for the volume between speakers is the most
noticeable flaw a stitched recording can have.

**Put a title card at the head of every part** — a plain slide with the part
number, the topic and the speaker's name, held for two seconds. It hides the
seam, it backs up the spoken name for Section 1.4, and it doubles as your figure
numbering.

**Keep the transitions.** The last line of each part sets up the next one. Cut
the dead air and the stumbles; leave those lines alone, because they are what
makes five recordings sound like one explanation.

If a part comes back unusable and re-recording is impossible, cover it yourself
rather than leaving a gap — a missing task is a missing mark.

### What to have on screen

| Part | Section | Show |
| --- | --- | --- |
| 1 | Opening | Cover page |
| 1 | The business problem | Figure 1, the annual trend |
| 2 | The dataset | The raw CSV, first 15–20 rows |
| 2 | The database | `docs/figures/erd.png`, then the `SHOW TABLES` screenshot |
| 2 | The queries | Query screenshots Q3, Q5, Q8 |
| 3 | The workbook | Cleaned Data, then a PivotChart |
| 4 | Descriptive statistics | The Amount histogram |
| 4 | Correlation | Both scatter plots |
| 4 | Regression | The ToolPak output |
| 4 | Trend and seasonality | Figure 2 with the shading, then the forecast chart |
| 5 | The correction | The correction table from the Checkpoint 2 report |
| 5 | What it means | The findings summary |
| 5 | Close | Cover page again, or the team slide |

---

# Part 1 — Alber

*About 3 minutes. Record straight through.*

## Opening

*On screen: the cover page*

Say your name, then go straight into the project:

- This is our BED 106 Business Analytics mini capstone. Our domain is Retail and
  Sales Analytics, and our topic is **sales trend analysis**
- What the recording covers: **Checkpoint 1**, where we built a database and
  asked what happened, and **Checkpoint 2**, where we took the same data into
  Excel and asked how strong the evidence is and what can be predicted
- One sentence on the dataset: 1,194 transaction lines, March 2020 to March 2025
- Then straight into the problem — no need to announce that you are about to
  start

## The business problem

*Task 1.1 · on screen: Figure 1*

- The subject is a multi-category retailer — electronics, furniture, office
  supplies — trading across six US states between 2020 and 2025
- The problem: **the company grew, then stopped.** On a like-for-like monthly
  basis revenue rose **30.9%** from 2020 to the 2022 peak, then fell two years
  running to finish 2024 **17.6% below** that peak
- Now the part that makes this an analytical problem rather than an obvious one.
  Ask it out loud and answer it: *why does a falling sales figure need a database
  at all?* Because of what **didn't** move. Margin held between **23.97% and
  26.93%** for the whole five years, and average order value stayed between
  **5,008 and 5,444**
- Had margin collapsed, the answer would be "we discounted too hard" and none of
  this would be needed. Margin held steady while revenue fell, which means the
  company is writing **fewer orders**, not worse ones — and "fewer orders of
  what, when, and where" is a question a single annual revenue figure cannot
  answer
- The three business questions, which every deliverable maps back to:

| # | Question | Answered by |
| --- | --- | --- |
| 1 | How have revenue and profit trended, and is the company still growing? | Query 3, and the Checkpoint 2 regression |
| 2 | Which categories and sub-categories drive the trend? | Queries 5 and 7 |
| 3 | When does demand concentrate, and is the pattern the same for every category? | Queries 4 and 8 |

- Why they matter: the decisions hanging off them are what to stock, when to
  stock it, and where to put the sales effort. Getting them wrong costs
  inventory that does not sell and campaigns that land in the wrong quarter

**End the part on this line:** none of those questions could be answered until
the raw file had been assessed, cleaned and put into a database — which is where
Checkpoint 1 starts.

---

# Part 2 — Julebeth

*About 6.5 minutes. Record straight through — the three sections below run on
from each other, so treat them as one talk with three topics.*

## The dataset and what was wrong with it

*Task 1.2 · on screen: the raw CSV, first 15–20 rows*

Say your name, then pick the thread up on the file itself: here is the raw
export, and here is what was wrong with it.

- The dataset is a retail sales export, **1,194 transaction lines and 12
  columns**, covering **22 March 2020 to 15 March 2025**. The brief asks for at
  least 200 rows
- The word to stress: the **grain** is one row per *product line on an order*,
  not one row per order. Everything downstream depends on that
- A quality assessment was run before anything was touched, and it found **five
  problems**, in order of how much trouble they caused

**One — `Order ID` is not a primary key.** 1,194 rows, only **547 distinct
order IDs**, and the repeats are not duplicate rows: the same ID appears on
different dates, for different customers. So it does not identify an order
either. It was kept as a plain attribute and a surrogate key, `sale_id`, was
issued instead.

Then answer the obvious objection before it is asked — *why not repair it?*
Because repairing it means deciding which of two rows sharing an ID is the real
one, and there is no evidence for that decision. Inventing that evidence is data
fabrication, which the brief says is grounds for a failing mark. Documenting the
defect costs nothing analytically, because no question in this project needs
order identity.

**Two — customer name is not an identifier either.** **807 customers** resolve
from **802 distinct names**, because five names appear in more than one city.
The customer key is the pair (name, city).

**Three — `Year-Month` is redundant.** It is derivable from the date, so it does
not belong in a normalised schema. It was rebuilt in the `dates` table.

**Four — both ends of the file are partial.** It starts 22 March 2020 and stops
15 March 2025. Say that this matters more than it sounds and that it comes back
later — it is where the project's one significant error came from.

**Five — the dataset is synthetic.** Say this plainly and do not bury it. Five
machine-checked signals:

- Not one loss-making line in five years — no real retailer has that
- 22 of the 802 names end in credential suffixes like "MD" or "DDS", which is a
  Faker library artefact
- US cities paired with UPI and EMI payment methods, which are Indian payment rails
- The payment mix is near-uniform, 206 to 260 across every method
- The Amount histogram is flat, not normal — real transaction values are right-skewed

Then the point that matters: **none of it was fixed.** Fixing it would mean
inventing numbers. It was stated, proved, and carried into every conclusion as a
limitation. The method is unaffected — every query and every statistic in this
project would run identically against a real export.

*Move straight on:* with the defects documented, the next step was turning that
flat file into a proper database.

## The database

*Task 1.3 · on screen: the ERD, then `SHOW TABLES`*

- The flat file was normalised into a **star schema**: one fact table surrounded
  by seven dimensions, **eight tables** in total
- `sales` is the fact table, one row per transaction line. Around it:
  `customers`, `cities`, `states`, `categories`, `sub_categories`,
  `payment_modes` and `dates`
- Ask it out loud — *why a star, and not the one table we started with?* Three
  reasons:

**Consistency.** In the flat file a category name is repeated on every row that
uses it, so a typo in one row creates a category that does not exist. In the
star the name lives once in `categories` and the fact table carries an integer
key. A typo becomes impossible rather than merely unlikely.

**The brief asks for it.** Task 1.3 requires at least two related tables with
proper primary and foreign keys. There are **eight tables, eight primary keys,
seven foreign keys, six unique constraints and four check constraints** — and
the constraints were tested to confirm they actually reject bad rows, rather
than assumed to.

**The queries need it.** The category trend question needs category and date on
the same row as the amount, and a star gives you that in one join.

Then the `dates` table, which looks like overkill until you try to write the
queries. Two reasons it earns its place:

- **Portability.** `YEAR()` and `strftime()` are never called, so the same query
  file runs unchanged on MySQL and on SQLite, and that was verified
- **The completeness flags.** It carries `is_complete_month` and
  `is_complete_year`, which raw dates cannot. Those flags are the fix for
  problem four, and they are what stops anyone comparing a nine-month 2020
  against a full 2021

One trap worth telling them about, because it cost real time: **`year_month` is
a reserved word in MySQL.** `CREATE TABLE dates` failed outright with a syntax
error until it was backticked — and that only surfaced because a real MySQL
server was installed and the import actually run, rather than the file being
assumed correct.

Finish the section on the loader: the whole thing loads from **one file**,
`02_mysql_full_import.sql`, which creates the database, all eight tables and all
the data, and ends with a verification block whose last row must read 1,194
rows, 6,182,639.00 in revenue, 547 order IDs and 57 complete months, with zero
orphaned rows.

*Move straight on:* with the database built, the questions could finally be
asked.

## The eight queries

*Task 1.4 · on screen: Q3, Q5 and Q8 screenshots*

- Eight queries in four groups: two basic retrievals with `WHERE` and
  `ORDER BY`, two aggregates with `GROUP BY`, two multi-table joins — each
  joining four tables — and two business-insight queries
- Skip the mechanics; go to what they found, which is four things

**Finding one — growth stopped in 2022, and in a specific way.** Query 3
aggregates by year, but on a **per-month** basis so the partial years cannot
distort it. Revenue per month went **92,934 in 2020 → 121,648 at the 2022 peak →
100,207 in 2024**. Meanwhile margin never left the 24-to-27% band and average
order value never left the 5,008-to-5,444 band. That combination is the whole
diagnosis: fewer orders, not cheaper or less profitable ones — which points at
demand generation rather than at pricing.

**Finding two — one sub-category explains most of the gap.** Queries 5 and 7
break the trend down. **Printers lost 136,865 between 2023 and 2024, a 71.0%
collapse** — that single line item is over half the entire peak-to-2024 gap.
Every Electronics sub-category fell, and the category as a whole is down
**40.8%**. Every Office Supplies sub-category grew; **Paper is up 85,689, or
149.4%**.

Say why that matters: it is not a general slowdown. Two opposite trends are
running at once, and the company-wide figure is their average, which describes
neither. That is the single most useful thing Checkpoint 1 produced.

**Finding three — seasonality is category-specific.** Queries 4 and 8. The
blended figure says Q4 is the peak quarter. Split it out and Electronics
actually peaks in **Q2, at 30.79%** of its annual revenue, while Furniture peaks
in Q4 at **30.84%** and Office Supplies in Q4 at **32.16%**. So a single blended
planning curve is wrong for all three categories — it over-stocks Electronics in
Q4 and under-stocks it in Q2.

**Finding four — geography is not a factor.** Query 6. Across five years, state
revenue spans only **28%** between highest and lowest, with no state trending
against the others. Not every finding has to be a discovery — this one tells the
business where *not* to spend its analytical effort.

**End the part on this line:** that was Checkpoint 1 — what happened. Checkpoint
2 takes the same data into Excel and asks how strong the evidence is, and what
can be predicted.

---

# Part 3 — Alber

*About 1.5 minutes. A short bridge between the two checkpoints — no need to say
your name again.*

## The workbook

*Task 2.1 · on screen: Cleaned Data, then a PivotChart*

Pick the thread up: the first thing Checkpoint 2 needed was the workbook itself,
built on the same dataset the brief requires.

- The workbook has **thirteen sheets**
- The one design decision worth defending: **everything is live formulas, not
  pasted values** — around **1,724** of them. The cross-tabs are `SUMIFS`,
  `COUNTIFS` and `AVERAGEIFS` against named ranges over the Cleaned Data sheet,
  so if a row changed, every statistic downstream would change with it. Pasted
  values would have looked identical and proved nothing
- Beyond the brief's minimum there are **three native PivotTables**, each with a
  bound PivotChart, sharing one pivot cache. The brief asks for three pivot
  tables and three pivot charts, and the SUMIFS cross-tabs alone would have been
  arguable
- **Seven self-check formulas** on the Read Me sheet. Each recomputes a headline
  figure by an independent route and prints OK or MISMATCH — the row count, the
  revenue total and the regression slope are all checked that way. If a cell is
  edited that should not have been, the workbook says so

**End the part on this line:** with the data laid out that way and checked, the
statistics could be run on it.

---

# Part 4 — Mardy

*About 6.5 minutes. Record straight through — four topics, one continuous talk.*

## Descriptive statistics

*Task 2.2 · on screen: the Amount histogram*

Say your name, then pick the thread up: the first thing asked of that data was
what it looks like.

- Three numerical variables — Amount, Profit and Quantity — with mean, median,
  mode, standard deviation, variance, range, quartiles, IQR and coefficient of
  variation for each, plus a frequency distribution and a histogram
- Say that two things in there are worth attention and the rest is table-filling

**One — profit is far less predictable than revenue.** Amount has a coefficient
of variation of **54.2%**. Profit has **82.9%**, and a skew of **+0.94** — more
variable *and* asymmetric, with a long right tail of a few very profitable
lines. Practically: a revenue target does not manage profit, because the two do
not move together tightly enough for one to stand in for the other. That is the
finding that shapes what the dashboard should be built on.

**Two — the histogram is the real finding.** Amount is distributed almost flat
across its range. Real transaction values are right-skewed: many small sales,
few large ones. A flat distribution is what a random number generator produces.
So the descriptive statistics independently confirm the synthetic-data
conclusion from Checkpoint 1 — reported as evidence rather than hidden.

## Correlation

*Task 2.3 · on screen: both scatter plots*

- Two required pairs plus a third for support — Pearson's r, with scatter plots
  and fitted trendlines

**Pair one — monthly order count against monthly revenue: r = 0.9227.** Strong
positive. Order count explains about **85%** of the variation in monthly
revenue. Checkpoint 1 *inferred* that fewer orders were the mechanism; this
measures it.

**Pair two — line quantity against line amount: r = 0.0446, p = 0.123.** No
relationship, and not statistically significant, so the null hypothesis that the
true correlation is zero cannot be rejected. Stress that this is a **negative
result being kept**, because it kills an obvious strategy: a "sell more units"
target would not move revenue in this business. Price per line varies far more
than units per line.

**Supporting pair — amount against profit: r = 0.6753**, so about **46%** of
profit variation tracks revenue. Moderate, not strong — the same conclusion as
the coefficients of variation a moment ago, reached a different way.

Then the caveat, said explicitly: **correlation is not causation.** Order count
and revenue could both be driven by something else — market conditions, a
campaign not visible in this data. What can be said is that the association is
strong and consistent over 57 months, not that one causes the other.

## Regression

*Task 2.4 · on screen: the ToolPak output*

- Monthly revenue regressed on monthly order count, over the 57 complete months

State the equation clearly, and slowly enough to be heard:

**Revenue = −1,353.65 + 5,224.25 × Orders**

Then read it properly, four parts:

- **The slope, 5,224.25.** One additional order in a month is associated with
  about 5,224 more revenue that month. Here is the check that makes it
  convincing: the mean order value in the data is **5,178.09**. The slope lands
  within **0.9%** of it — the regression rediscovered the average order value
  without being told it
- **R² = 0.8514.** Order count explains 85% of the month-to-month variation in
  revenue
- **Significance: t = 17.75, 55 degrees of freedom, p = 1.98 × 10⁻²⁴.** The
  slope is not zero, and that is not a marginal result
- **The intercept, −1,353.65, is not meaningful.** Zero orders cannot produce
  negative revenue. It is where the fitted line crosses the axis, extrapolated
  outside the range of the data, and it is not interpreted

Then the forecast the brief asks for: the company is running about **four orders
per month** below its 2022 level. At 5,224 per order, closing that gap is worth
roughly **250,000 a year**. Checkpoint 1 arrived at **257,297** by an entirely
different route — summing the actual category shortfalls. Two independent
methods landing within 3% of each other is the strongest single piece of
evidence in this project. Say that sentence deliberately; it is the high point
of the whole recording.

Close the section with limitations — six are listed; name the three that matter:
single predictor, so it says nothing about *why* orders fell; fitted on 57
monthly points, which is not many; and it should not be extrapolated beyond the
observed range of order counts.

## Trend and seasonality

*Task 2.5 · on screen: Figure 2 with the shading, then the forecast chart*

This is the section the topic is named after. Be precise about what was and was
not found, and do not rush the middle of it.

- **The trend is real, and it is the finding: the series runs in two regimes.**
  Growth from 2020 to 2022 — **92,934 up to 121,648** per month, **+30.9%**.
  Then a plateau from 2022 to 2024 — down to **100,207**, **−17.6%**. Both are
  visible on Figure 2; the shading marks where one ends and the other begins
- Then raise the obvious question and answer it: *so why is there no growth rate
  in the forecast?* Because one was tested for and there is not a single one. A
  straight line fitted across all 57 months explains **under 1% of the variation
  — R² = 0.0078, p = 0.515.** It was run on four different windows and gave the
  same answer each time
- Now the interpretation, which is the part that matters: that result is **not**
  "no trend". It is "**no single straight line fits both regimes**", which is
  exactly what you would expect from a series that rises and then flattens — the
  up-slope and the flat cancel out, and the average of the two is nearly
  horizontal. Reporting that honestly, and refusing to project a growth rate
  that cannot be demonstrated, is the correct handling. Projecting one anyway
  would be inventing a number
- So the forecast is built from **level and seasonality** instead. Monthly
  seasonal indices were computed — **January 0.679, October 1.229, December
  1.273** — and applied to the recent level to project the six months from
  January to June 2025

Then the honest check, which is the part most worth having on the recording:

- The two months that could be checked were held out, and the seasonal forecast
  was compared against a naive flat average. **The seasonal forecast lost.**
  Mean absolute error **22.7%** against the flat average's **14.9%**. It ranks
  fifth of the eight methods tested
- The reason is visible: **January 2025 came in at 112,906 against a prediction
  of 68,853.** January's index says January is the weakest month of the year,
  and this January was not
- Answer *why keep the method, then?* Because switching on the strength of two
  observations is overfitting the holdout — you would be choosing the model that
  happened to win on a two-month sample, which is not evidence. The result is
  reported, the method is kept, and the forecast's reliability over this horizon
  is stated plainly as weak. The reliability discussion the brief asks for is not
  a formality here: the error was measured, and it is 22.7%

**End the part on this line:** building that monthly series also turned up
something nobody expected — and it was a mistake of our own.

---

# Part 5 — Alber

*About 6 minutes. Record straight through — no need to say your name again.*

## The correction

*On screen: the correction table from the Checkpoint 2 report*

This section exists because volunteering an error is worth more than having it
found. Do not soften it.

- Building the Checkpoint 2 monthly series exposed an **error in our own
  Checkpoint 1**
- 2020 was treated as a full year. The file starts 22 March, so 2020 holds only
  **nine months**. That overstated 2020-to-2022 growth as **69.9%** when the
  like-for-like figure is **30.9%**. It also distorted March's seasonal index,
  from 1.025 down to 0.876
- What it did and did not touch:

| Affected | Unaffected |
| --- | --- |
| The 2020→2022 growth figure | The −17.6% peak-to-2024 decline — both are full years |
| March's seasonal index | Printers −136,865; Electronics −40.8% |
| | Category-specific seasonality; the geography finding |

- The central thesis is unchanged; one supporting number was overstated
- Checkpoint 1 was reissued with an `is_complete_month` flag and a per-month
  column in Query 3, so the mistake cannot recur, and it is documented in the
  Checkpoint 2 report either way

## What it means for the business

*On screen: the findings summary*

With that correction made, here is what the analysis actually tells the
business. Three recommendations, each tied to a measurement rather than an
opinion:

- **Track order count, not revenue.** Revenue is the lagging indicator; order
  count is what drives it, r = 0.923, and it is the thing the business can act on
- **Plan seasonality by category, not company-wide.** The blended curve is wrong
  for all three categories — Electronics peaks in Q2, Furniture and Office
  Supplies in Q4. A single planning curve over-stocks Electronics in Q4 and
  under-stocks it in Q2
- **Investigate Printers first.** One sub-category, **136,865** lost, over half
  the entire gap. Whether that is supply, competition, or a category in
  structural decline is not something this dataset can answer — but it tells us
  where to look, and that is what the analysis was for

## The limitations

Three, stated plainly and in your own voice:

- **The data is synthetic.** The figures illustrate the method rather than
  describe a real company. It was proved, it was stated, and no corrections were
  invented, because that would have been worse
- **The forecast is weak.** 22.7% mean absolute error against a flat average's
  14.9%. Our own error was measured and reported rather than the test quietly
  dropped
- **Correlation is not causation.** Order count and revenue move together; that
  is not proof that one causes the other

Then what the group *would* stand behind: the method. A defect-documented
dataset, a normalised schema with enforced constraints, queries verified on two
database engines, and statistics tested for significance rather than eyeballed —
with the negative results reported alongside the positive ones.

## The questions we would expect

Still speaking continuously, raise these and answer them in your own words. This
is the part that stands in for a live defense, so take it slowly.

**Does a fake dataset invalidate the project?** It invalidates the *figures*,
not the *method*. It was proved with five signals and no corrections were
fabricated, which would have been worse. The schema, the queries and the
analysis would run identically on real data.

**Why not use `Order ID` as the primary key?** 1,194 rows, 547 distinct IDs, and
the repeats span different dates and different customers. It identifies neither
a row nor an order.

**Why exclude 2025, and why show 2020 per month?** Both ends of the file are
partial. Including them whole would show fake growth at one end and a fake
collapse at the other — which is exactly the mistake we made and corrected.

**Is R² = 0.85 good?** For cross-sectional business data, yes — but R² alone is
not the test. The p-value of 1.98 × 10⁻²⁴ is what says the slope is not zero.

**The trend test found nothing — doesn't that sink a *trend* project?** It found
that no single line fits both regimes, which is itself the finding. The trend is
real, it is just piecewise, and Figure 2 shows it.

**The forecast lost to a flat average — why keep it?** Choosing a method on two
observations is overfitting the holdout. The loss is reported and the
reliability stated honestly.

**What would you do differently?** Validate the source before building on it,
and check the completeness of both ends of the date range first — that is
exactly what caused the one real error, and it would have cost ten minutes to
catch at the start.

**What is next?** Checkpoint 3, the dashboard, built on **order count** as the
primary KPI rather than revenue because it is the leading indicator and the
actionable one, and segmented on **margin** rather than revenue, given how
weakly those two turned out to be related.

## Close

*On screen: the cover page again, or the team slide*

- One sentence on what the project found: growth stopped in 2022, it was driven
  by a small number of sub-categories rather than a general slowdown, and order
  count is the measurable driver
- Thank the instructor, name the three of you, and state that any member can
  answer questions on any part of the project — which is what Section 1.4 asks
  for, and which is true if you have rehearsed

---

## Checklist

Each of you, before you record:

- Every number you say out loud, you can point to — a query, a figure, or a cell
- You can say your section's beats with the script closed
- You can answer a question about any section, not only the one you recorded —
  Section 1.4 lets the instructor ask any member about any part
- Your exhibits are open and on the right screen before you press record
- You have done the thirty-second test

Alber, before you submit:

- All five parts present and in order, no task missing
- Audio levels normalised across all three speakers
- Each speaker names themselves once, and nobody claims a task or a role
- The synthetic data, the Checkpoint 1 correction and the forecast that lost are
  all audibly in the recording
- Played back end to end — the file opens, the audio does not cut out, the
  on-screen numbers are legible, and the length fits any limit you were given
- File named with your group and the checkpoint
