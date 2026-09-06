# Sales Trend Analysis — Group Discussion Script

**BED 106 Business Analytics — Mini Capstone Project**
Talibon Polytechnic College

A recording script for three speakers who record **separately**, in their own
time and place, with the leader editing the clips together afterwards.

| Speaker | Role from the brief | Records |
| --- | --- | --- |
| **Alber** | Project Lead / Analyst | Clips A1–A5 — opening, the business problem, recommendations, closing |
| **Julebeth** | Data Engineer | Clips B1–B5 — the dataset, the database, the workbook, the correction |
| **Mardy** | Statistician / Modeler | Clips C1–C6 — the queries, statistics, regression, forecasting |

Total runtime is roughly **17 minutes** assembled.

---

## Before you record

**Read this part first. It affects your marks.**

Section 3.2 of the brief states that AI-generated analysis is not permitted and
that insights must be derived by the students themselves. This script was
drafted with AI assistance, so **do not read it out as written**. Use it the way
you would use a lecture outline: it tells you *what to cover, in what order, and
which number belongs where*. The sentences that come out of your mouth have to
be yours.

The practical test: read a clip's beats, close the script, and say the same
thing in your own words. If you cannot say it without looking, you do not
understand it yet — and Section 1.4 lets the instructor ask **any member** to
explain **any part** of the project, recording or no recording.

Every figure quoted here has been checked against the database. If you are asked
where a number comes from, the answer is always a specific query or a specific
worksheet cell, and those are named beside each clip.

---

## How this works when you record separately

Because nobody is in the room with you, there is no back-and-forth to react to.
Every clip below is therefore **self-contained**: you never wait for a cue, and
you never answer a question someone else has to have asked first.

What holds the recording together instead is the **handoff**. Each clip ends by
naming what comes next and who takes it, and the next clip opens by picking that
thread up. Say those lines even though they feel odd alone in a room — they are
what turns five separate recordings into one discussion instead of five
disconnected reports. They are the single most important thing on the page.

### Rules for every clip

**Name yourself in your first clip.** "I'm Julebeth, I handled the data and the
database." Your instructor is matching a voice to a name for a mark under
Section 1.4. Do not make them guess, and do not assume the video shows your face.

**Say the clip ID before you start speaking.** "Clip B2, take 1." Alber cuts
that off in the edit, but without it he is identifying twenty files by ear.

**Leave two seconds of silence at the start and end of every clip.** Speak the
ID, pause, then begin. At the end, stop talking and let it run for two seconds
before you stop recording. Cuts made against silence are clean; cuts made
against a breath are not.

**Record each clip as its own file.** Do not record all of yours in one long
take. A re-take should cost you ninety seconds, not the whole afternoon.

**Screen-record with audio; do not film a monitor.** Every exhibit in this
project is on a screen — the ERD, the query output, the workbook, the figures.
Filmed off a monitor the numbers are unreadable, and unreadable evidence is the
same as no evidence.

**Name your files by clip ID:** `B2_database_take2.mp4`. Send Alber the takes
you want used, not every take you shot.

**Agree three settings before anyone records:** screen resolution (1920 × 1080
is the safe choice), video format, and roughly how close you sit to the mic.
Three clips recorded at three different volumes is the one problem that is
genuinely annoying to fix in the edit.

**Do a thirty-second test first.** Record, play it back, and check three things:
your voice is audible, the on-screen text is legible at that resolution, and no
fan or echo is drowning you. Fixing this after you have recorded everything is
the most common way groups lose an evening.

### If a clip mentions something you did not do

Each speaker's clips cover that speaker's own work, so this should not arise.
Where a clip refers to another person's area, it does so in one sentence as a
handoff — "the statistics side is Mardy's, and he takes it next" — which is true
and which you can say honestly.

---

## For Alber, as editor

Assemble in this order. Clip IDs are grouped by speaker for recording; this
table is the playback order.

| # | Clip | Speaker | Covers | Brief task | Approx |
| --- | --- | --- | --- | --- | --- |
| 1 | A1 | Alber | Opening and roadmap | — | 0:45 |
| 2 | A2 | Alber | The business problem and three questions | 1.1 | 2:00 |
| 3 | B1 | Julebeth | The dataset and its five defects | 1.2 | 2:30 |
| 4 | B2 | Julebeth | The database and the ERD | 1.3 | 2:00 |
| 5 | C1 | Mardy | The eight queries and four findings | 1.4 | 3:00 |
| 6 | B3 | Julebeth | The workbook | 2.1 | 1:30 |
| 7 | C2 | Mardy | Descriptive statistics | 2.2 | 1:30 |
| 8 | C3 | Mardy | Correlation | 2.3 | 1:30 |
| 9 | C4 | Mardy | Regression | 2.4 | 2:00 |
| 10 | C5 | Mardy | Trend and seasonality | 2.5 | 2:30 |
| 11 | B4 | Julebeth | The Checkpoint 1 correction | — | 1:15 |
| 12 | A3 | Alber | Recommendations and limitations | — | 2:00 |
| 13 | B5 · C6 · A4 | all | Q&A answers, in that order | 1.4 | 2:30 |
| 14 | A5 | Alber | Closing | — | 0:30 |

**Three things to do in the edit**

**Normalise the audio levels** before anything else. Three people in three rooms
will not match, and a viewer reaching for the volume between speakers is the
most noticeable flaw a stitched recording can have.

**Put a title card between speakers** — a plain slide with the segment name and
the speaker's name, held for two seconds. It hides the seam, it tells the
instructor who is talking, and it doubles as your figure numbering.

**Do not trim the handoff lines.** They are what make the cut sound intentional
rather than accidental. Cut the clip-ID slate and the dead air; keep everything
after it.

If a clip comes back unusable and re-recording is not possible, the fallback is
to cover it yourself in the Q&A block and say whose area it was. Do not leave a
gap in the task order — the brief's tasks are what is being marked, and a
missing task is a missing mark.

### What to have on screen, clip by clip

| Clip | Show |
| --- | --- |
| A1 | Cover page |
| A2 | Figure 1, the annual trend |
| B1 | The raw CSV, first 15–20 rows |
| B2 | `docs/figures/erd.png`, then the `SHOW TABLES` screenshot |
| C1 | Query screenshots Q3, Q5, Q8 |
| B3 | The workbook — Cleaned Data, then a PivotChart |
| C2 | The Amount histogram |
| C3 | Both scatter plots |
| C4 | The ToolPak regression output |
| C5 | Figure 2 with the regime shading, then the forecast chart |
| B4 | The correction table from the Checkpoint 2 report |
| A3 | The findings summary |
| A5 | Cover page again, or the team slide |

---

# Part A — Alber

Project Lead / Analyst. Five clips: the opening, the business problem, the
recommendations, one Q&A block, and the close. You bookend the recording, so
your first and last clips set how the whole thing lands.

## Clip A1 — Opening

*About 45 seconds · on screen: the cover page*

**Open with:** your name, your role, the group, and the subject.

Beats:

- This is our BED 106 Business Analytics mini capstone. Our domain is Retail and
  Sales Analytics, and our topic is **sales trend analysis**
- Introduce all three of you by name and role, so a viewer knows who is coming:
  you on the business problem and the findings, Julebeth on the data and the
  database, Mardy on the statistics and the forecast
- Say what the recording covers: **Checkpoint 1**, where we built a database and
  asked what happened, and **Checkpoint 2**, where we took the same data into
  Excel and asked how strong the evidence is and what can be predicted
- One sentence on the dataset: 1,194 transaction lines, March 2020 to March 2025

**Hand off with:** "I'll start with the business problem itself."

## Clip A2 — The business problem

*Task 1.1 · about 2 minutes · on screen: Figure 1*

**Open with:** the problem in one sentence.

Beats:

- The subject is a multi-category retailer — electronics, furniture, office
  supplies — trading across six US states between 2020 and 2025
- The problem: **the company grew, then stopped.** On a like-for-like monthly
  basis revenue rose **30.9%** from 2020 to the 2022 peak, then fell two years
  running to finish 2024 **17.6% below** that peak
- Now the part that makes it an analytical problem rather than an obvious one.
  Pose it as a question and answer it: *why does this need a database at all?*
  Because of what **didn't** move. Margin held between **23.97% and 26.93%**
  for the whole five years, and average order value stayed between **5,008 and
  5,444**
- So if margin had collapsed, the answer would be "we discounted too hard" and
  nobody would need any of this. Margin held steady while revenue fell, which
  means the company is writing **fewer orders**, not worse ones — and "fewer
  orders of what, when, and where" is a question a single annual revenue figure
  cannot answer
- The three business questions, which every deliverable maps back to:

| # | Question | Answered by |
| --- | --- | --- |
| 1 | How have revenue and profit trended, and is the company still growing? | Query 3, and the Checkpoint 2 regression |
| 2 | Which categories and sub-categories drive the trend? | Queries 5 and 7 |
| 3 | When does demand concentrate, and is the pattern the same for every category? | Queries 4 and 8 |

- Why they matter: the decisions hanging off them are what to stock, when to
  stock it, and where to put the sales effort. Getting them wrong costs
  inventory that does not sell and campaigns that land in the wrong quarter

**Hand off with:** "Before any of that could be answered, the data had to be
cleaned and put into a database — that was Julebeth's part, and she takes it
from here."

## Clip A3 — Recommendations and limitations

*About 2 minutes · on screen: the findings summary*

**Open with:** picking up the correction Julebeth has just described — "so with
that correction made, here is what the analysis actually tells the business."

Beats — three recommendations, each tied to a measurement rather than an opinion:

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

Then the limitations, stated plainly and in your own voice — three of them:

- **The data is synthetic.** The figures illustrate the method rather than
  describe a real company. We proved it, we said so, and we did not invent
  corrections, because that would have been worse
- **The forecast is weak.** 22.7% mean absolute error against a flat average's
  14.9%. We measured our own error and we are reporting it rather than quietly
  dropping the test
- **Correlation is not causation.** We showed that order count and revenue move
  together, not that one causes the other

Close the substance with what you *would* stand behind: the method. A
defect-documented dataset, a normalised schema with enforced constraints,
queries verified on two database engines, and statistics tested for significance
rather than eyeballed — with the negative results reported alongside the
positive ones.

**Hand off with:** "Last, each of us will answer a few of the questions we would
expect to be asked."

## Clip A4 — Q&A answers

*About 50 seconds · record after B5 and C6 in the playback order*

Answer these two in your own words, unhurried:

**"What would you do differently?"** — Validate the source before building on
it, and check the completeness of both ends of the date range first. That is
exactly what caused our one real error, and it would have cost ten minutes to
catch at the start.

**"What is next?"** — Checkpoint 3, the dashboard, built on **order count** as
the primary KPI rather than revenue because it is the leading indicator and the
actionable one, and segmented on **margin** rather than revenue, given how
weakly those two turned out to be related.

**Hand off with:** nothing — go straight into the close.

## Clip A5 — Closing

*About 30 seconds · on screen: cover page or team slide*

Beats:

- One sentence on what the project found: growth stopped in 2022, it was driven
  by a small number of sub-categories rather than a general slowdown, and order
  count is the measurable driver
- Thank the instructor, name the three of you again
- State that each member can answer questions on any part of the project — which
  is what Section 1.4 asks for, and which is true if you have rehearsed

---

# Part B — Julebeth

Data Engineer. Five clips: the dataset, the database, the workbook, the
Checkpoint 1 correction, and one Q&A block. Yours are the clips with the most
screen work, so leave yourself time to get the exhibits open before you start.

## Clip B1 — The dataset and what was wrong with it

*Task 1.2 · about 2.5 minutes · on screen: the raw CSV, first 15–20 rows*

**Open with:** your name and role — "I'm Julebeth, I handled the data and the
database" — then pick up Alber's thread: before any of those questions could be
answered, the raw file had to be assessed and cleaned.

Beats:

- The dataset is a retail sales export, **1,194 transaction lines and 12
  columns**, covering **22 March 2020 to 15 March 2025**. The brief asks for at
  least 200 rows
- The word to stress: the **grain** is one row per *product line on an order*,
  not one row per order. Everything downstream depends on that
- We ran a quality assessment before touching anything and found **five
  problems**. Take them in order of how much trouble they caused

**One — `Order ID` is not a primary key.** 1,194 rows, only **547 distinct
order IDs**, and the repeats are not duplicate rows: the same ID appears on
different dates, for different customers. So it does not identify an order
either. We kept it as a plain attribute and issued our own surrogate key,
`sale_id`.

Answer the obvious objection yourself — *why not repair it?* Because repairing
it means deciding which of two rows with the same ID is the real one, and we
have no evidence for that decision. Inventing that evidence is data
fabrication, which the brief says is grounds for a failing mark. Documenting the
defect costs us nothing analytically, because no question we ask needs order
identity.

**Two — customer name is not an identifier either.** **807 customers** resolve
from **802 distinct names**, because five names appear in more than one city.
Our customer key is the pair (name, city).

**Three — `Year-Month` is redundant.** It is derivable from the date, so it does
not belong in a normalised schema. We rebuilt it in the `dates` table.

**Four — both ends of the file are partial.** It starts 22 March 2020 and stops
15 March 2025. Flag that this matters more than it sounds and that you will come
back to it — it is where our one significant error came from.

**Five — the dataset is synthetic.** Say this plainly; do not bury it. Five
machine-checked signals:

- Not one loss-making line in five years — no real retailer has that
- 22 of the 802 names end in credential suffixes like "MD" or "DDS", which is a
  Faker library artefact
- US cities paired with UPI and EMI payment methods, which are Indian payment rails
- The payment mix is near-uniform, 206 to 260 across every method
- The Amount histogram is flat, not normal — real transaction values are right-skewed

Then the point that matters: **we did not fix any of it.** Fixing it would mean
inventing numbers. We stated it, proved it, and carried the limitation into every
conclusion. The method is unaffected — every query and every statistic in this
project would run identically against a real export.

**Hand off with:** "With the defects documented, the next step was turning that
flat file into a proper database."

## Clip B2 — The database

*Task 1.3 · about 2 minutes · on screen: the ERD, then `SHOW TABLES`*

**Open with:** the shape, in one sentence.

Beats:

- We normalised the flat file into a **star schema**: one fact table surrounded
  by seven dimensions, **eight tables** in total
- `sales` is the fact table, one row per transaction line. Around it:
  `customers`, `cities`, `states`, `categories`, `sub_categories`,
  `payment_modes` and `dates`
- Pose the question yourself — *why a star, and not the one table we started
  with?* Three reasons:

**Consistency.** In the flat file a category name is repeated on every row that
uses it, so a typo in one row creates a category that does not exist. In the
star the name lives once in `categories` and the fact table carries an integer
key. A typo becomes impossible rather than merely unlikely.

**The brief asks for it.** Task 1.3 requires at least two related tables with
proper primary and foreign keys. We have **eight tables, eight primary keys,
seven foreign keys, six unique constraints and four check constraints** — and we
tested that the constraints actually reject bad rows rather than assuming they
would.

**The queries need it.** The category trend question needs category and date on
the same row as the amount, and a star gives you that in one join.

Then the `dates` table, which is the one that looks like overkill until you try
to write the queries. Two reasons it earns its place:

- **Portability.** We never call `YEAR()` or `strftime()`, so the same query
  file runs unchanged on MySQL and on SQLite, and we verified that
- **The completeness flags.** It carries `is_complete_month` and
  `is_complete_year`, which the raw dates cannot. Those flags are the fix for
  problem four, and they are what stops anyone comparing a nine-month 2020
  against a full 2021

One trap worth telling them about, because it cost real time: **`year_month` is
a reserved word in MySQL.** `CREATE TABLE dates` failed outright with a syntax
error until we backticked it — and we only found that because we installed a
real MySQL server and ran the import rather than assuming the file was fine.

Finish on the loader: the whole thing loads from **one file**,
`02_mysql_full_import.sql`, which creates the database, all eight tables and all
the data, and ends with a verification block whose last row must read 1,194
rows, 6,182,639.00 in revenue, 547 order IDs and 57 complete months, with zero
orphaned rows.

**Hand off with:** "With the database built, the questions could finally be
asked — and Mardy wrote the queries."

## Clip B3 — The workbook

*Task 2.1 · about 1.5 minutes · on screen: the workbook, Cleaned Data then a PivotChart*

**Open with:** what Checkpoint 2 is — the same dataset, which the brief
requires, taken out of the database and into Excel.

Beats:

- The workbook has **thirteen sheets**
- The one design decision to defend: **everything is live formulas, not pasted
  values** — around **1,724** of them. The cross-tabs are `SUMIFS`, `COUNTIFS`
  and `AVERAGEIFS` against named ranges over the Cleaned Data sheet, so if a row
  changed, every statistic downstream would change with it. Pasted values would
  have looked identical and proved nothing
- Beyond the brief's minimum we added **three native PivotTables**, each with a
  bound PivotChart, sharing one pivot cache. The brief asks for three pivot
  tables and three pivot charts, and the SUMIFS cross-tabs alone would have been
  arguable
- **Seven self-check formulas** on the Read Me sheet. Each recomputes a headline
  figure by an independent route and prints OK or MISMATCH — the row count, the
  revenue total and the regression slope are all checked that way. If someone
  edits a cell they should not have, the workbook says so

**Hand off with:** "The statistics built on top of that are Mardy's, starting
with the descriptive figures."

## Clip B4 — The Checkpoint 1 correction

*About 1.25 minutes · on screen: the correction table from the Checkpoint 2 report*

This clip exists because volunteering your own error is worth more than having
it found. Record it as its own clip and do not soften it.

**Open with:** "Before the conclusions, there is one thing we have to put on the
record ourselves."

Beats:

- Building the Checkpoint 2 monthly series exposed an **error in our own
  Checkpoint 1**
- We treated 2020 as a full year. The file starts 22 March, so 2020 holds only
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
- We reissued Checkpoint 1 with an `is_complete_month` flag and a per-month
  column in Query 3, so the mistake cannot recur, and it is documented in the
  Checkpoint 2 report either way

**Hand off with:** "With that correction made, Alber takes what the analysis
tells the business."

## Clip B5 — Q&A answers

*About 50 seconds · first of the three Q&A clips*

**Open with:** "A few questions we would expect on the data side."

Answer three, in your own words:

**"Your dataset looks fake — doesn't that invalidate the project?"** — It
invalidates the *figures*, not the *method*. We proved it with five signals and
did not fabricate corrections, which would have been worse. The schema, the
queries and the analysis would run identically on real data.

**"Why didn't you use `Order ID` as the primary key?"** — 1,194 rows, 547
distinct IDs, and the repeats span different dates and different customers. It
identifies neither a row nor an order.

**"Why exclude 2025 and show 2020 per month?"** — Both ends of the file are
partial. Including them whole would show fake growth at one end and a fake
collapse at the other. That is precisely the mistake we made and corrected.

**Hand off with:** "Mardy has the questions on the statistics."

---

# Part C — Mardy

Statistician / Modeler. Six clips: the queries, then one clip per Checkpoint 2
task, then a Q&A block. Yours is the largest share, and clips C4 and C5 are the
two that carry the topic — give those the most rehearsal.

## Clip C1 — The eight queries

*Task 1.4 · about 3 minutes · on screen: Q3, Q5 and Q8 screenshots*

**Open with:** your name and role — "I'm Mardy, I wrote the queries and did the
statistical work" — then pick up Julebeth's thread: with the database built,
here is what we asked it.

Beats:

- Eight queries in four groups: two basic retrievals with `WHERE` and
  `ORDER BY`, two aggregates with `GROUP BY`, two multi-table joins — ours join
  four tables each — and two business-insight queries
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
planning curve is wrong for all three categories.

**Finding four — geography is not a factor.** Query 6. Across five years, state
revenue spans only **28%** between highest and lowest, with no state trending
against the others. Not every finding has to be a discovery — this one tells the
business where *not* to spend its analytical effort.

**Hand off with:** "That was what happened. Checkpoint 2 asks how strong the
evidence is — and it starts with the workbook Julebeth built."

## Clip C2 — Descriptive statistics

*Task 2.2 · about 1.5 minutes · on screen: the Amount histogram*

**Open with:** what was measured — three numerical variables: Amount, Profit and
Quantity, with mean, median, mode, standard deviation, variance, range,
quartiles, IQR and coefficient of variation for each, plus a frequency
distribution and a histogram.

Then say that two things in there are worth attention and the rest is
table-filling.

**One — profit is far less predictable than revenue.** Amount has a coefficient
of variation of **54.2%**. Profit has **82.9%**, and a skew of **+0.94** — more
variable *and* asymmetric, with a long right tail of a few very profitable
lines. Practically: a revenue target does not manage profit, because the two do
not move together tightly enough for one to stand in for the other. That is the
finding that changes what we recommend for the dashboard.

**Two — the histogram is the real finding.** Amount is distributed almost flat
across its range. Real transaction values are right-skewed: many small sales,
few large ones. A flat distribution is what a random number generator produces.
So our own descriptive statistics independently confirm the synthetic-data
conclusion from Checkpoint 1 — and we report that as evidence rather than hiding
it.

**Hand off with:** "Next, whether the variables actually move together."

## Clip C3 — Correlation

*Task 2.3 · about 1.5 minutes · on screen: both scatter plots*

**Open with:** two required pairs plus a third for support — Pearson's r, with
scatter plots and fitted trendlines.

Beats:

**Pair one — monthly order count against monthly revenue: r = 0.9227.** Strong
positive. Order count explains about **85%** of the variation in monthly
revenue. Checkpoint 1 *inferred* that fewer orders were the mechanism; this
measures it.

**Pair two — line quantity against line amount: r = 0.0446, p = 0.123.** No
relationship, and not statistically significant, so we cannot reject the null
hypothesis that the true correlation is zero. Stress that this is a **negative
result we are keeping**, because it kills an obvious strategy: a "sell more
units" target would not move revenue in this business. Price per line varies far
more than units per line.

**Supporting pair — amount against profit: r = 0.6753**, so about **46%** of
profit variation tracks revenue. Moderate, not strong — the same conclusion as
the CV figures a moment ago, reached a different way.

Then the caveat, said explicitly: **correlation is not causation.** Order count
and revenue could both be driven by something else — market conditions, a
campaign we cannot see in this data. What we can say is that the association is
strong and consistent over 57 months, not that one causes the other.

**Hand off with:** "The regression puts a number on that relationship."

## Clip C4 — Regression

*Task 2.4 · about 2 minutes · on screen: the ToolPak output*

**Open with:** what was regressed — monthly revenue on monthly order count, over
the 57 complete months.

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
  outside the range of the data, and we do not interpret it

Then the forecast the brief asks for: the company is running about **four orders
per month** below its 2022 level. At 5,224 per order, closing that gap is worth
roughly **250,000 a year**. Checkpoint 1 arrived at **257,297** by an entirely
different route — summing the actual category shortfalls. Two independent
methods landing within 3% of each other is the strongest single piece of
evidence in this project. Say that sentence deliberately; it is the high point.

Close with limitations — we list six; name the three that matter: single
predictor, so it says nothing about *why* orders fell; fitted on 57 monthly
points, which is not many; and it should not be extrapolated beyond the observed
range of order counts.

**Hand off with:** "Last on the analysis: the trend itself, which is what our
topic is actually about."

## Clip C5 — Trend and seasonality

*Task 2.5 · about 2.5 minutes · on screen: Figure 2 with the shading, then the forecast chart*

This is the clip that carries the topic. Be precise about what you did and did
not find, and do not rush the middle of it.

**Open with:** "This is the part our topic is named after, so I want to be exact
about it."

Beats:

- **The trend is real, and it is the finding: the series runs in two regimes.**
  Growth from 2020 to 2022 — **92,934 up to 121,648** per month, **+30.9%**.
  Then a plateau from 2022 to 2024 — down to **100,207**, **−17.6%**. Both are
  visible on Figure 2; the shading marks where one ends and the other begins
- Then answer the obvious question yourself: *so why is there no growth rate in
  the forecast?* Because we tested for one and there is not a single one. We
  fitted a straight line across all 57 months and it explains **under 1% of the
  variation — R² = 0.0078, p = 0.515.** We ran it on four different windows and
  got the same answer each time
- Now the interpretation, which is the part that matters: that result is **not**
  "no trend". It is "**no single straight line fits both regimes**", which is
  exactly what you would expect from a series that rises and then flattens — the
  up-slope and the flat cancel out, and the average of the two is nearly
  horizontal. Reporting that honestly, and refusing to project a growth rate we
  cannot demonstrate, is the correct handling. Projecting one anyway would be
  inventing a number
- So the forecast is built from **level and seasonality** instead. We computed
  monthly seasonal indices — **January 0.679, October 1.229, December 1.273** —
  and applied them to the recent level to project the six months from January to
  June 2025

Then the honest check, which is the part most worth having on the recording:

- We held out the two months we could check and compared the seasonal forecast
  against a naive flat average. **The seasonal forecast lost.** Mean absolute
  error **22.7%** against the flat average's **14.9%**. It ranks fifth of the
  eight methods we tested
- The reason is visible: **January 2025 came in at 112,906 against our
  prediction of 68,853.** January's index says January is the weakest month of
  the year, and this January was not
- Answer *why keep the method, then?* Because switching on the strength of two
  observations is overfitting the holdout — you would be choosing the model that
  happened to win on a two-month sample, which is not evidence. We report the
  result, we keep the method, and we say plainly that our forecast reliability
  over this horizon is weak. The reliability discussion the brief asks for is not
  a formality here: we measured our own error and it is 22.7%

**Hand off with:** "There is one more thing we found, and it was a mistake of
our own — Julebeth has it."

## Clip C6 — Q&A answers

*About 50 seconds · second of the three Q&A clips*

**Open with:** "And the questions we would expect on the statistics."

Answer three, in your own words:

**"Is R² = 0.85 good?"** — For cross-sectional business data, yes, but R² alone
is not the test. The p-value of 1.98 × 10⁻²⁴ is what says the slope is not zero.

**"Your trend test found nothing — doesn't that sink a *trend* project?"** — It
found that no single line fits both regimes, which is itself the finding. The
trend is real, it is just piecewise, and Figure 2 shows it.

**"Your forecast lost to a flat average. Why keep it?"** — Choosing a method on
two observations is overfitting the holdout. We report the loss and state the
reliability honestly.

**Hand off with:** "Alber has the last of them."

---

## Rehearsal checklist

Each of you, before you record:

- Every number you say out loud, you can point to — a query, a figure, or a cell
- You can say your clip's beats with the script closed
- You can answer at least one question from someone else's area, because
  Section 1.4 does not care who recorded which clip
- Your exhibits are open and on the right screen before you press record
- You have said your handoff line, even though it feels strange alone in a room

Alber, before you submit:

- All fourteen clips present, in the assembly order above, no task missing
- Audio levels normalised across all three speakers
- Every speaker names themselves at least once
- The synthetic data, the Checkpoint 1 correction and the forecast that lost are
  all audibly in the recording
- Playback checked end to end — the file opens, the audio does not cut out, the
  on-screen numbers are legible, and the length fits any limit you were given
- File named with your group and the checkpoint
