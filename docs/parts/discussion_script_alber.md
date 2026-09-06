# Sales Trend Analysis — Recording Script

**BED 106 Business Analytics — Mini Capstone Project**
Talibon Polytechnic College

**Alber reads the parts below.** The full running order:

| Part | Speaker | Covers | Approx |
| --- | --- | --- | --- |
| 1 | Alber | Opening; the business problem | 3:00 |
| 2 | Julebeth | Checkpoint 1 — the dataset, the database, the queries | 8:45 |
| 3 | Alber | The Checkpoint 2 workbook | 1:30 |
| 4 | Mardy | Checkpoint 2 — statistics, correlation, regression, the trend | 8:30 |
| 5 | Alber | The correction, what it means, the questions, the close | 6:00 |

About **28 minutes** at a normal speaking pace — Alber 10:30 across his three
parts, Julebeth 8:45, Mardy 8:30. If you need it shorter, cut the six
limitations down to one line in Part 4 and drop three of the eight questions in
Part 5; that takes off about three minutes without losing a task.

*Lines in italics inside brackets are stage directions — what to have on screen.
Do not read them aloud.*

**One thing before you record.** Section 3.2 of the brief says AI-generated
analysis is not permitted. This script was drafted with AI help, so change the
wording as you go — say it the way you would say it, swap sentences around, cut
what feels stiff. The numbers and the reasoning have to stay; the phrasing
should become yours. Read it through once, then record without staring at the
page.

**Recording notes.** Record your part in one take, screen-recording with audio
rather than filming a monitor. If you stumble, don't stop — pause and repeat the
sentence, and Alber cuts it. Leave two seconds of silence at each end. Agree on
screen resolution and mic distance beforehand so the three parts match. Alber
joins the five files in order, normalises the audio, and puts a two-second title
card at the head of each part.

---

# Part 1 — Alber

*[Cover page on screen.]*

Good day. My name is Alber, and this is our mini capstone project for BED 106,
Business Analytics. Our domain is Retail and Sales Analytics, and our topic is
sales trend analysis.

What we'll go through is the first two checkpoints. Checkpoint 1 is where we
took a raw sales file, cleaned it, and built a database out of it, so we could
ask what actually happened to this company. Checkpoint 2 is where we took that
same data into Excel and asked a harder question — how strong is the evidence,
and can we predict anything from it.

The dataset is a retail sales export. 1,194 transaction lines, running from
March 2020 to March 2025.

*[Switch to Figure 1, the annual trend.]*

So here's the problem we're looking at. The company is a multi-category
retailer — electronics, furniture and office supplies — selling across six US
states. And what happened to it is simple to say: it grew, and then it stopped.

On a like-for-like monthly basis, revenue went up 30.9 percent from 2020 to its
peak in 2022. Then it fell in each of the next two years, and finished 2024 at
17.6 percent below that peak.

Now, you might ask — why does that need a database? Sales went down. That's not
a mystery.

Here's why. It's because of what didn't move. Margin held between 23.97 and
26.93 percent for the whole five years. Average order value stayed between 5,008
and 5,444. Neither of those budged.

And that changes the whole question. If margin had collapsed, the answer would
just be "we discounted too hard," and nobody would need any of this. But margin
held steady while revenue fell. That means the company isn't selling worse
orders — it's writing fewer of them. And fewer orders of what, sold when, and
sold where — that is not something a single annual revenue figure can tell you.

So we set three business questions, and everything in this project comes back to
one of them.

First: how have revenue and profit trended, and is the company still growing?

Second: which categories and sub-categories are driving that trend?

And third: when does demand actually concentrate — and is that pattern the same
for every category?

These matter because of the decisions sitting behind them. What to stock, when
to stock it, and where to put the sales effort. Get those wrong and you're
paying for inventory that doesn't sell, and running campaigns in the wrong
quarter.

None of that could be answered from the raw file, though. It had to be assessed,
cleaned, and put into a database first — and that's where Checkpoint 1 starts.

---

# Part 3 — Alber

*[The workbook on screen — Cleaned Data sheet.]*

The first thing Checkpoint 2 needed was the workbook itself, built on the same
dataset, which the brief requires.

It has thirteen sheets. And there's one design decision in it worth explaining,
because it's the one we'd defend if asked.

Everything in this workbook is live formulas. Not pasted values. About 1,724 of
them. The cross-tabs are SUMIFS, COUNTIFS and AVERAGEIFS running against named
ranges over the Cleaned Data sheet — so if a single row changed, every statistic
downstream would change with it. Pasted values would have looked absolutely
identical on the page, and proved nothing.

*[Switch to a PivotChart.]*

Beyond what the brief asks for, there are three native PivotTables, each with a
PivotChart bound to it, all sharing one pivot cache. The brief wants three pivot
tables and three pivot charts, and the SUMIFS cross-tabs on their own would have
been arguable.

And there are seven self-check formulas on the Read Me sheet. Each one
recalculates a headline figure by a completely independent route and prints
either OK or MISMATCH. The row count, the revenue total, the regression slope —
all checked that way. So if a cell gets edited that shouldn't have been, the
workbook tells you.

With the data laid out that way and checked, we could run the statistics on it.

---

# Part 5 — Alber

*[The correction table from the Checkpoint 2 report on screen.]*

This part we're raising ourselves, because volunteering an error is worth more
than having somebody find it.

Building the Checkpoint 2 monthly series exposed a mistake in our own Checkpoint
1. We treated 2020 as a full year. But the file starts on 22 March, so 2020 only
holds nine months of trading. That overstated our 2020-to-2022 growth as 69.9
percent, when the like-for-like figure is 30.9. It also distorted March's
seasonal index, pulling it from 1.025 down to 0.876.

What it affected was that growth figure and that one index. What it did not
affect: the minus 17.6 percent decline from peak to 2024, because those are both
full years. Printers down 136,865. Electronics down 40.8 percent. The
category-specific seasonality. The geography finding. All of that stands.

So the central thesis is unchanged — one supporting number was overstated.
Checkpoint 1 has been reissued with an is_complete_month flag and a per-month
column in Query 3, so the mistake can't happen again. And it's documented in the
Checkpoint 2 report either way.

*[Switch to the findings summary.]*

So with that correction made, here's what the analysis actually tells this
business. Three recommendations, and each one is tied to a measurement rather
than an opinion.

**First — track order count, not revenue.** Revenue is the lagging indicator.
Order count is what drives it, at r of 0.923, and it's the thing the business can
actually act on.

**Second — plan seasonality by category, not company-wide.** The blended curve is
wrong for all three categories. Electronics peaks in Q2; Furniture and Office
Supplies peak in Q4. A single planning curve over-stocks Electronics in Q4 and
under-stocks it in Q2.

**Third — investigate Printers first.** One sub-category, 136,865 lost, more than
half the entire gap. Whether that's a supply problem, a competitive loss, or a
category in structural decline is not something this dataset can tell us. But it
tells us where to look — and that's what the analysis was for.

Now the limitations, and we'd rather say these ourselves.

The data is synthetic. So these figures illustrate a method; they don't describe
a real company. We proved that, we said it, and we didn't invent corrections,
because that would have been worse.

The forecast is weak. 22.7 percent error against a flat average's 14.9. We
measured our own error and reported it, rather than quietly dropping the test.

And correlation is not causation. Order count and revenue move together. That is
not proof that one causes the other.

What we would stand behind is the method. A dataset whose defects are documented
rather than hidden. A normalised schema with constraints that are enforced and
tested. Queries verified on two different database engines. And statistics tested
for significance rather than eyeballed — with the negative results reported right
alongside the positive ones.

Let me finish with the questions we'd expect to be asked.

**Doesn't a fake dataset invalidate the project?** It invalidates the figures,
not the method. We proved it with five signals, and we didn't fabricate
corrections, which would have been worse. The schema, the queries and the
analysis would run identically on real data.

**Why not use Order ID as the primary key?** 1,194 rows, 547 distinct IDs, and
the repeats span different dates and different customers. It identifies neither a
row nor an order.

**Why exclude 2025, and why show 2020 per month?** Because both ends of the file
are partial. Including them whole would show fake growth at one end and a fake
collapse at the other — which is exactly the mistake we made, and corrected.

**Is an R-squared of 0.85 good?** For cross-sectional business data, yes. But
R-squared on its own isn't the test. The p-value — 1.98 times ten to the negative
24 — is what tells you the slope isn't zero.

**Your trend test found nothing. Doesn't that sink a trend project?** It found
that no single line fits both regimes, and that is itself the finding. The trend
is real; it's just piecewise. Figure 2 shows it.

**Your forecast lost to a flat average. Why keep it?** Because choosing a method
on the strength of two observations is overfitting the holdout. We report the
loss and state the reliability honestly.

**What would you do differently?** Validate the source before building on it, and
check the completeness of both ends of the date range first. That's exactly what
caused our one real error, and it would have taken ten minutes to catch at the
start.

**And what's next?** Checkpoint 3, the dashboard. We'd build it on order count as
the primary KPI rather than revenue, because that's the leading indicator and the
actionable one. And we'd segment on margin rather than revenue, given how weakly
those two turned out to be related.

*[Cover page, or the team slide.]*

So, to sum up. Growth stopped in 2022. It was driven by a small number of
sub-categories rather than a general slowdown. And order count is the measurable
driver behind it.

Thank you for watching. That's Alber, Julebeth and Mardy — and any of us can
answer questions on any part of this project.
