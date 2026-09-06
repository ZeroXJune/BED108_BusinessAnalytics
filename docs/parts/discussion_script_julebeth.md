# Sales Trend Analysis — Recording Script

**BED 106 Business Analytics — Mini Capstone Project**
Talibon Polytechnic College

**Julebeth's part.** Each speaker records their own part straight through, in their own time and
place. Nobody waits for a cue, nobody answers anybody, and nobody states a role
— each part simply continues the explanation where the last one stopped. Alber
joins them in order afterwards.

| Part | Speaker | Covers | Approx |
| --- | --- | --- | --- |
| 1 | Alber | Opening; the business problem and the three questions | 3:00 |
| 2 | Julebeth | Checkpoint 1 — the dataset, the database, the eight queries and what they found | 7:30 |
| 3 | Mardy | Checkpoint 2 — the workbook, statistics, regression, the forecast, and the correction | 10:00 |
| 4 | Alber | What it means for the business, the limitations, and the close | 2:30 |

Roughly **23 minutes** assembled. If you were given a time limit shorter than
that, the two places to cut are the descriptive statistics and the correlation
in Part 3 — each survives as two sentences. Do not cut a whole task; the brief's
tasks are what is being marked.

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

**Say your name once, at the very start of your part.** Just the name — your
instructor is matching a voice to a name for a mark under Section 1.4, and the
video may not show your face. Then go straight into the material.

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

# Part 2 — Julebeth

*About 7.5 minutes. Record straight through — the three sections below run on
from each other, so treat them as one talk with three topics.*

## The dataset and what was wrong with it

*Task 1.2 · on screen: the raw CSV, first 15–20 rows*

Say your name, then pick the thread up: here is the raw file, and here is what
was wrong with it.

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

## Questions worth answering here

Still speaking continuously, close your part by raising three questions this
work invites and answering them:

**Does a fake dataset invalidate the project?** It invalidates the *figures*,
not the *method*. It was proved with five signals and no corrections were
fabricated, which would have been worse. The schema, the queries and the
analysis would run identically on real data.

**Why not use `Order ID` as the primary key?** 1,194 rows, 547 distinct IDs, and
the repeats span different dates and different customers. It identifies neither
a row nor an order.

**Why exclude 2025, and why show 2020 per month?** Both ends of the file are
partial. Including them whole would show fake growth at one end and a fake
collapse at the other.

**End the part on this line:** that was Checkpoint 1 — what happened. Checkpoint
2 takes the same data into Excel and asks how strong the evidence is, and what
can be predicted.

---

## Checklist

Each of you, before you record:

- Every number you say out loud, you can point to — a query, a figure, or a cell
- You can say your section's beats with the script closed
- You can answer a question about someone else's part, because Section 1.4 does
  not care who recorded which section
- Your exhibits are open and on the right screen before you press record
- You have done the thirty-second test

Alber, before you submit:

- All four parts present and in order, no task missing
- Audio levels normalised across all three speakers
- Each speaker names themselves once
- The synthetic data, the Checkpoint 1 correction and the forecast that lost are
  all audibly in the recording
- Played back end to end — the file opens, the audio does not cut out, the
  on-screen numbers are legible, and the length fits any limit you were given
- File named with your group and the checkpoint
