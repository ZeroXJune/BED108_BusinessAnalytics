# Sales Trend Analysis — Group Discussion Script

**BED 106 Business Analytics — Mini Capstone Project**
Talibon Polytechnic College

**Mardy's part.** A recording script for three speakers who record **separately**, in their own
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
