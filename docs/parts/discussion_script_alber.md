# Sales Trend Analysis — Group Discussion Script

**BED 106 Business Analytics — Mini Capstone Project**
Talibon Polytechnic College

**Alber's part.** A recording script for three speakers who record **separately**, in their own
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
