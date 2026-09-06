# Sales Trend Analysis — Recording Script

**BED 106 Business Analytics — Mini Capstone Project**
Talibon Polytechnic College

**Mardy's part.** Each speaker records their own part straight through, in their own time and
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

**Say your name once, at the start of your first part.** Just the name — your
instructor is matching a voice to a name for a mark under Section 1.4, and the
video may not show your face. Alber records three parts and only needs to do
this in Part 1; the later two just continue.

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

## Checklist

Each of you, before you record:

- Every number you say out loud, you can point to — a query, a figure, or a cell
- You can say your section's beats with the script closed
- You can answer a question about someone else's part, because Section 1.4 does
  not care who recorded which section
- Your exhibits are open and on the right screen before you press record
- You have done the thirty-second test

Alber, before you submit:

- All five parts present and in order, no task missing
- Audio levels normalised across all three speakers
- Each speaker names themselves once
- The synthetic data, the Checkpoint 1 correction and the forecast that lost are
  all audibly in the recording
- Played back end to end — the file opens, the audio does not cut out, the
  on-screen numbers are legible, and the length fits any limit you were given
- File named with your group and the checkpoint
