# Sales Trend Analysis — Group Discussion Script

**BED 106 Business Analytics — Mini Capstone Project**
Talibon Polytechnic College

**Julebeth's part.** A recording script for three speakers who record **separately**, in their own
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
