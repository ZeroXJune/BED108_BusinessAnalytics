# Sales Trend Analysis — Recording Script

**BED 106 Business Analytics — Mini Capstone Project**
Talibon Polytechnic College

| Part | Speaker | Covers | Approx |
| --- | --- | --- | --- |
| 1 | Alber | Opening; the business problem | 3:00 |
| 2 | Julebeth | Checkpoint 1 — the dataset and its five problems | 3:30 |
| 3 | Mardy | Checkpoint 1 — the database, and the eight queries | 5:30 |
| 4 | Alber | Checkpoint 2 — the workbook, statistics, regression, the trend | 10:00 |
| 5 | Alber | The correction, what it means, the questions, the close | 6:00 |

About **28 minutes** at a normal speaking pace. Alber carries Checkpoint 2 and
the framing — 19 minutes across three files — while Julebeth and Mardy split
Checkpoint 1 between them. Alber's Part 4 is the long one, so record it in two
sittings if you need to; there is a natural break after the regression.

If you need it shorter, cut the six limitations in Part 4 down to one line and
drop three of the eight questions in Part 5; that takes off about three minutes
without losing a task.

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

# Part 2 — Julebeth

*[The raw CSV on screen, first 15–20 rows.]*

I'm Julebeth, and I'll take it from the raw file.

This is the export we started with — 1,194 transaction lines, 12 columns,
running from 22 March 2020 to 15 March 2025. The brief asks for at least 200
rows, so we're well past that.

One thing to be clear about first: the grain. Each row here is one product line
on an order, not one order. Three products on an order means three rows.
Everything we do later depends on that.

We ran a quality assessment before touching anything, and we found five
problems.

**First, the Order ID column is not a primary key.** 1,194 rows, but only 547
distinct order IDs — and these aren't duplicate rows. The same ID shows up on
different dates, for different customers. So it identifies neither a row nor an
order.

Why not just repair it? Because repairing it means deciding which of two rows
sharing an ID is the real one, and we have no evidence for that decision. Making
that evidence up is data fabrication, and the brief says that's grounds for a
failing mark. So we kept it as a plain attribute and issued our own key, called
sale_id. It costs us nothing, because no question we ask needs order identity.

**Second, the customer name isn't an identifier either.** 807 customers resolve
from 802 distinct names, because five names appear in more than one city. So our
customer key is the pair — name and city together.

**Third, the Year-Month column is redundant.** You can derive it from the date,
so it doesn't belong in a normalised schema. We rebuilt it in a dates table.

**Fourth, both ends of the file are partial.** It starts on 22 March 2020 and
stops on 15 March 2025. That sounds minor. It isn't — it's where the one real
error in this project came from, and we'll come back to it.

**And fifth, the dataset is synthetic.** It's not real trading data, and we're
saying that up front rather than burying it. We have five pieces of evidence.

There isn't one loss-making line in five years — no real retailer has that. 22
of the 802 names end in credential suffixes like MD or DDS, which is what the
Faker library produces. There are US cities paired with UPI and EMI payment
methods, and those are Indian payment rails. The payment mix is almost perfectly
uniform — 206 to 260 across every single method. And the Amount histogram comes
out flat instead of right-skewed, which is what a random number generator looks
like.

And we didn't fix any of it. Fixing it would mean inventing numbers. So we
stated it, we proved it, and we carried it through as a limitation. The method
isn't affected — every query and every statistic in this project would run
exactly the same way on real data.

That is the state of the raw data we started from. What we built out of it
next was a proper database.

---

# Part 3 — Mardy

*[The ERD on screen.]*

I'm Mardy, and I'll take the database and the queries.

So we normalised that flat file into a star schema. One fact table, seven
dimension tables around it — eight in total. The fact table is sales, one row per
transaction line, and around it we have customers, cities, states, categories,
sub_categories, payment_modes and dates.

Why a star, instead of the one table we started with? Three reasons.

Consistency — in the flat file a category name is repeated on every row that
uses it, so one typo creates a category that doesn't exist. In the star that
name lives in one place and the fact table just carries an integer key. A typo
goes from unlikely to impossible.

The brief — Task 1.3 wants at least two related tables with proper primary and
foreign keys. What we built has eight tables, eight primary keys, seven foreign
keys, six unique constraints and four check constraints. And we tested that
those constraints actually reject bad rows; we didn't just assume it.

And the queries — the category trend question needs category and date sitting on
the same row as the amount, and a star gives you that in one join.

The dates table looks like overkill until you try to write the queries. It's
there for two reasons. We never call YEAR or strftime anywhere, so the same
query file runs unchanged on MySQL and on SQLite — we verified that. And it
carries two flags the raw dates can't: is_complete_month and is_complete_year.
Those are the fix for problem four, and they're what stops anyone from comparing
a nine-month 2020 against a full 2021.

One thing that cost us real time — year_month is a reserved word in MySQL. Our
CREATE TABLE statement failed outright with a syntax error until we put
backticks around it. And we only found that because we installed an actual MySQL
server and ran the import, instead of assuming the file was fine.

*[Switch to the SHOW TABLES screenshot.]*

The whole thing loads from one file — the database, all eight tables, all the
data. And it ends with a verification block whose last row has to read 1,194
rows, 6,182,639 in revenue, 547 order IDs, 57 complete months, and zero orphaned
rows.

*[Switch to the query screenshots — Q3 first.]*

So with the database built, we could ask the questions. There are eight queries
in four groups: two basic retrievals using WHERE and ORDER BY, two aggregates
using GROUP BY, two multi-table joins — ours each join four tables — and two
business-insight queries. Here's what they found.

**First, growth stopped in 2022, and it stopped in a specific way.** Query 3
aggregates by year, but on a per-month basis, so the partial years can't distort
it. Revenue per month went from 92,934 in 2020, up to 121,648 at the 2022 peak,
then down to 100,207 in 2024. But margin never left that 24-to-27 percent band,
and average order value never left 5,008 to 5,444. Put those together and you
have the diagnosis — fewer orders, not cheaper ones and not less profitable
ones. Which points at demand generation, not at pricing.

*[Switch to Q5.]*

**Second, one sub-category explains most of the gap.** Printers lost 136,865
between 2023 and 2024 — a 71 percent collapse, and on its own that's more than
half the entire gap between the 2022 peak and 2024. Every Electronics
sub-category fell, and the category as a whole is down 40.8 percent. But every
Office Supplies sub-category grew — Paper is up 85,689, which is 149.4 percent.

And that's the point: this is not a general slowdown. Two opposite trends are
running at the same time, and the company-wide figure is just their average,
which describes neither of them. That's the most useful thing Checkpoint 1
produced.

*[Switch to Q8.]*

**Third, seasonality is category-specific.** The blended figure tells you Q4 is
the peak quarter. But split it out, and Electronics actually peaks in Q2, at
30.79 percent of its annual revenue. Furniture peaks in Q4 at 30.84, and Office
Supplies in Q4 at 32.16. So one blended planning curve is wrong for all three —
it over-stocks Electronics in Q4 and under-stocks it in Q2.

**And fourth, geography isn't a factor.** State revenue spans only 28 percent
across five years, and no state trends against the others. Not every finding has
to be a discovery — this one tells the business where not to spend its effort.

So that was Checkpoint 1 — what happened. Checkpoint 2 takes the same data into
Excel and asks how strong the evidence actually is, and what we can predict.

---

# Part 4 — Alber

*[The workbook on screen — Cleaned Data sheet.]*

So, Checkpoint 2. The first thing it needed was the workbook itself, built
on the same dataset, which the brief requires.

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

*[Switch to the Amount histogram.]*

So the first thing we asked of that data was simply what it looks like. Three
numerical variables — Amount, Profit and Quantity — and for each one we have the
mean, median and mode, standard deviation, variance, range, quartiles, the
interquartile range and the coefficient of variation, plus a frequency
distribution and a histogram.

Two things in there are worth your attention. The rest is table-filling.

**The first is that profit is far less predictable than revenue.** Amount has a
coefficient of variation of 54.2 percent. Profit has 82.9, and a skew of plus
0.94 — so it's both more variable and asymmetric, with a long right tail of a few
very profitable lines. What that means in practice is that a revenue target does
not manage profit. The two don't move together tightly enough for one to stand in
for the other.

**The second is that the histogram itself is a finding.** Amount is spread
almost perfectly flat across its range. Real transaction values are
right-skewed — lots of small sales, a few big ones. Flat is what a random number
generator produces. So our own descriptive statistics independently confirm what
Checkpoint 1 said about this data being synthetic, and we report that as
evidence rather than hide it.

*[Switch to the scatter plots.]*

Next, whether the variables actually move together. Pearson's r on two required
pairs plus a third for support, with scatter plots and fitted trendlines.

**The first pair is monthly order count against monthly revenue, and r is
0.9227.** Strongly positive — order count explains about 85 percent of the
variation in monthly revenue. And notice what that does: Checkpoint 1 inferred
that fewer orders were the mechanism. This measures it.

**The second pair is line quantity against line amount, and r is 0.0446, with a
p-value of 0.123.** No relationship, and not statistically significant — we
cannot reject the null hypothesis that the true correlation is zero. That's a
negative result and we're keeping it, because it kills an obvious strategy: a
"sell more units" target would not move revenue in this business. Price per line
varies far more than units per line.

**And the supporting pair, amount against profit, gives r of 0.6753** — about 46
percent of profit variation tracks revenue. Moderate, not strong. Which is the
same conclusion as those coefficients of variation, reached a different way.

One caveat we have to state: correlation is not causation. Order count and
revenue could both be driven by something we can't see in this data. What we can
say is that the association is strong and consistent across 57 months — not that
one causes the other.

*[Switch to the ToolPak regression output.]*

So then we regressed monthly revenue on monthly order count, over those 57
complete months. The equation is:

Revenue equals negative 1,353.65, plus 5,224.25 times orders.

There are four things to read in that.

**The slope is 5,224.25** — one additional order in a month is associated with
about 5,224 more revenue that month. And here's the check that makes it
convincing: the mean order value in our data is 5,178.09. The slope lands within
0.9 percent of it. The regression rediscovered the average order value without
ever being told what it was.

**R-squared is 0.8514** — order count explains 85 percent of the month-to-month
variation in revenue.

**For significance, t is 17.75 on 55 degrees of freedom, and p is 1.98 times ten
to the negative 24.** So the slope is not zero, and that's not a marginal result.

**And the intercept, negative 1,353.65, isn't meaningful** — zero orders can't
produce negative revenue. It's where the fitted line crosses the axis,
extrapolated outside our data, so we don't interpret it.

Then the forecast. The company is running about four orders per month below its
2022 level. At 5,224 per order, closing that gap is worth roughly 250,000 a
year. And Checkpoint 1 arrived at 257,297 by a completely different route —
just summing the actual category shortfalls. Two independent methods landing
within 3 percent of each other. That's the strongest single piece of evidence in
this project.

We list six limitations. The three that matter most: it's a single predictor, so
it says nothing about why orders fell; it's fitted on 57 monthly points, which
isn't many; and it shouldn't be extrapolated beyond the range of order counts we
actually observed.

*[Switch to Figure 2, with the regime shading.]*

Last, the trend itself — which is what our topic is named after, so I want to be
precise about what we found and what we didn't.

The trend is real, and this is the finding: the series runs in two regimes.
Growth from 2020 to 2022 — 92,934 up to 121,648 per month, so plus 30.9 percent.
Then a plateau from 2022 to 2024, down to 100,207, which is minus 17.6 percent.
You can see both here; the shading marks where one ends and the other begins.

So the obvious question is, why isn't there a growth rate in our forecast?

Because we tested for one, and there isn't a single one. We fitted a straight
line across all 57 months and it explains under 1 percent of the variation —
R-squared of 0.0078, p-value of 0.515. We ran it on four different windows and
got the same answer every time.

Here's the interpretation, and this is the part that matters. That result is not
"there's no trend." It's "no single straight line fits both regimes" — which is
exactly what you'd expect from a series that rises and then flattens. The
up-slope and the flat part cancel each other out, and the average comes out
nearly horizontal. Reporting that honestly, and refusing to project a growth
rate we can't demonstrate, is the correct handling. Projecting one anyway would
be inventing a number.

*[Switch to the forecast chart.]*

So the forecast is built on level and seasonality instead. We computed monthly
seasonal indices — January comes out at 0.679, October at 1.229, December at
1.273 — and applied them to the recent level to project six months forward,
January to June 2025.

And then we checked it, which is the part I'd most want you to see. We held out
the two months we could actually verify and compared our seasonal forecast
against a naive flat average. The seasonal forecast lost. Mean absolute error of
22.7 percent, against the flat average's 14.9. It ranks fifth out of the eight
methods we tested.

You can see why. January 2025 came in at 112,906, against our prediction of
68,853. Our index says January is the weakest month of the year — and this
January wasn't.

So why keep the method? Because switching on the strength of two observations is
overfitting the holdout. You'd be picking whichever model happened to win on a
two-month sample, and that isn't evidence. So we report the result, we keep the
method, and we say plainly that our forecast reliability over this horizon is
weak. The reliability discussion the brief asks for isn't a formality here — we
measured our own error, and it's 22.7 percent.

Building that monthly series also turned up something nobody expected. And it
was a mistake of our own.

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
