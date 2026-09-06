# Sales Trend Analysis — Recording Script

**BED 106 Business Analytics — Mini Capstone Project**
Talibon Polytechnic College

**Alber's part.** Each speaker records their own part straight through, in their own time and
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

## For Alber, as editor

Join the four parts in order: 1, 2, 3, 4. There is nothing to interleave.

**Normalise the audio levels first.** Three people in three rooms will not
match, and a viewer reaching for the volume between speakers is the most
noticeable flaw a stitched recording can have.

**Put a title card between parts** — a plain slide with the part number, the
topic and the speaker's name, held for two seconds. It hides the seam, it tells
the instructor who is talking, and it doubles as your figure numbering.

**Keep the transitions.** The last line of each part sets up the next one. Cut
the dead air and the stumbles; leave those lines alone, because they are what
makes four recordings sound like one explanation.

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
| 3 | Descriptive statistics | The Amount histogram |
| 3 | Correlation | Both scatter plots |
| 3 | Regression | The ToolPak output |
| 3 | Trend and seasonality | Figure 2 with the shading, then the forecast chart |
| 3 | The correction | The correction table from the Checkpoint 2 report |
| 4 | What it means | The findings summary |
| 4 | Close | Cover page again, or the team slide |

---

# Part 1 — Alber

*About 3 minutes. Record straight through.*

# Part 1 — Alber

*About 3 minutes. Record straight through.*

## Opening

*On screen: the cover page*

Say your name, then:

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

# Part 4 — Alber

*About 2.5 minutes. Record straight through.*

## What it means for the business

*On screen: the findings summary*

Pick the thread up — with the correction made, here is what the analysis
actually tells the business. Three recommendations, each tied to a measurement
rather than an opinion:

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

## Close

*On screen: the cover page again, or the team slide*

- Two questions worth answering before you finish. *What would you do
  differently?* Validate the source before building on it, and check the
  completeness of both ends of the date range first — that is exactly what caused
  the one real error, and it would have cost ten minutes to catch at the start.
  *What is next?* Checkpoint 3, the dashboard, built on **order count** as the
  primary KPI rather than revenue because it is the leading indicator and the
  actionable one, and segmented on **margin** rather than revenue, given how
  weakly those two turned out to be related
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
