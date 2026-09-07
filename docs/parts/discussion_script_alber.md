# Sales Trend Analysis — Recording Script

**BED 106 Business Analytics — Mini Capstone Project**
Talibon Polytechnic College

**Alber reads the parts below.** The full running order:

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

*Lines in italics inside brackets are stage directions, and the tables and
charts under them are the exhibits to have on screen at that moment. Do not read
any of it aloud — the spoken lines are the plain paragraphs.*

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

## Exhibit index — for Alber, editing

Every exhibit is reproduced in this script at the point it is referred to, so
you can work from here alone. This table says where each one comes from if you
want the original — and note that the **figure numbers in the reports do not
match the file names**: Checkpoint 1's Figure 1 is the ERD, not the trend chart.

| # | Part | Exhibit | File | In the reports |
| --- | --- | --- | --- | --- |
| 1 | 1 | Annual trend chart | `docs/figures/fig1_annual_trend.png` | CP1 report, **Figure 2** |
| 2 | 2 | Raw file extract | `data/raw/sales_dataset_raw.csv` | CP1 report, Raw dataset preview |
| 3 | 3 | ERD | `docs/figures/erd.png` | CP1 report, **Figure 1** |
| 4 | 3 | Loaded row counts | — | CP1 report, Populated row counts |
| 5 | 3 | Q3 annual trend | `sql/04_queries.sql` | CP1 report, Q3 |
| 6 | 3 | Q7 sub-category change | `sql/04_queries.sql` | CP1 report, Q7 |
| 7 | 3 | Q8 quarter shares | `sql/04_queries.sql` | CP1 report, Q8 |
| 8 | 4 | Workbook, Cleaned Data sheet | `reports/Checkpoint_2_Workbook.xlsx` | — |
| 9 | 4 | A PivotChart | `Checkpoint_2_Workbook.xlsx`, sheets PivotTable 1–3 | — |
| 10 | 4 | Descriptive statistics | Workbook, Descriptive Stats | CP2 report, Task 2.2 |
| 11 | 4 | Amount histogram | `docs/figures/cp2_fig1_histogram.png` | CP2 report, **Figure 1** |
| 12 | 4 | Orders vs revenue scatter | `docs/figures/cp2_fig2_regression.png` | CP2 report, **Figure 3** |
| 13 | 4 | Quantity vs amount scatter | `docs/figures/cp2_fig3_no_correlation.png` | CP2 report, **Figure 2** |
| 14 | 4 | Regression output | Workbook, Regression | CP2 report, Task 2.4 |
| 15 | 4 | Trend and forecast chart | `docs/figures/cp2_fig4_forecast.png` | CP2 report, **Figure 4** |
| 16 | 4 | Seasonal indices, forecast, accuracy | Workbook, Forecast | CP2 report, Task 2.5 |
| 17 | 5 | The correction | — | CP2 report, section 2 |
| 18 | 5 | Findings summary | — | CP1 report, Key Findings |

Exhibits 12 and 13 are the ones most easily swapped: the **regression** scatter
is monthly orders against monthly revenue with a steep fitted line, and the
**no-correlation** scatter is quantity against amount with a flat one. The file
names are the reverse of the report's figure order, so go by the file name.

Assembly is simply Parts 1 to 5 in order. Normalise the audio levels across the
three speakers first, and put a two-second title card at the head of each part
carrying the part number, the topic and the speaker's name.

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

*[The annual trend chart — have this on screen.]*

Caption: Revenue per month by year. Growth to the 2022 peak, then two years of decline.

![](docs/figures/fig1_annual_trend.png)

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

*[The histogram and the statistics — have these on screen.]*

Caption: Descriptive statistics for the three numerical variables, n = 1,194.

| Statistic | Amount | Profit | Quantity |
| --- | --- | --- | --- |
| Mean | 5,178.09 | 1,348.99 | 10.67 |
| Median | 5,152.00 | 1,014.00 | 11.00 |
| Mode | 717 (×6) | 177 (×8) | 14 (×73) |
| Standard deviation | 2,804.92 | 1,117.99 | 5.78 |
| Variance | 7,867,587.17 | 1,249,907.39 | 33.37 |
| Minimum | 508 | 50 | 1 |
| Maximum | 9,992 | 4,930 | 20 |
| Range | 9,484 | 4,880 | 19 |
| Q1 | 2,799.00 | 410.00 | 6.00 |
| Q3 | 7,626.00 | 2,035.00 | 16.00 |
| Interquartile range | 4,827.00 | 1,625.00 | 10.00 |
| Coefficient of variation | 54.2% | 82.9% | 54.1% |

Caption: Frequency distribution of Amount. The flat shape is the finding.

![](docs/figures/cp2_fig1_histogram.png)

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

*[The two scatter plots — have these on screen.]*

Caption: Monthly orders against monthly revenue, with the fitted line.

![](docs/figures/cp2_fig2_regression.png)

Caption: Quantity against Amount at line level. The near-flat trendline is the finding.

![](docs/figures/cp2_fig3_no_correlation.png)

Caption: The two correlation pairs side by side.

| Measure | Orders vs revenue | Quantity vs amount |
| --- | --- | --- |
| Pearson r | **+0.9227** | **+0.0446** |
| r² | 0.8514 | 0.0020 |
| p-value | 1.98 × 10⁻²⁴ | 0.123 |
| n | 57 months | 1,194 lines |
| Strength | **Strong** | **Negligible — not significant at 5%** |

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

*[The regression output — show your own ToolPak run, or this.]*

Caption: Simple linear regression of monthly revenue on monthly order count.

| Statistic | Value |
| --- | --- |
| Sample size n | 57 months |
| Slope (b) | **5,224.25** |
| Intercept (a) | −1,353.65 |
| Correlation r | 0.9227 |
| **R²** | **0.8514** |
| Standard error of estimate | 15,099.14 |
| Standard error of slope | 294.35 |
| **t statistic** | **17.75** |
| Degrees of freedom | 55 |
| **p-value** | **1.98 × 10⁻²⁴** |
| Significant at 5%? | **Yes** |

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

*[The trend chart — have this on screen.]*

Caption: The trend in two regimes. Growth to the late-2022 peak, then a plateau; the forecast and the two holdout months are at the right.

![](docs/figures/cp2_fig4_forecast.png)

Caption: The two regimes, measured on revenue per month.

| Regime | Period | Revenue per month | Change |
| --- | --- | --- | --- |
| **Growth** | 2020 → 2022 | 92,934.44 → 121,647.92 | **+30.9%** |
| **Plateau** | 2022 → 2024 | 121,647.92 → 100,206.50 | **−17.6%**, then flat |

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

*[The seasonal indices and the forecast — have these on screen. The chart is the same one as above.]*

Caption: Seasonal index by calendar month, April 2020 to December 2024.

| Month | Index | Reading | Month | Index | Reading |
| --- | --- | --- | --- | --- | --- |
| January | 0.679 | Weak | July | 0.966 | Average |
| February | 0.889 | Weak | August | 1.006 | Average |
| March | 1.025 | Average | September | 0.793 | Weak |
| April | 1.103 | Peak | October | 1.229 | Peak |
| May | 1.131 | Peak | November | 0.878 | Weak |
| June | 1.028 | Average | December | 1.273 | Peak |

Caption: Six-period forecast, with the two complete holdout months compared.

| Period | Index | Forecast | Actual | Error | Status |
| --- | --- | --- | --- | --- | --- |
| 2025-01 | 0.679 | 68,853 | 112,906 | **−39.0%** | Complete — comparable |
| 2025-02 | 0.889 | 90,064 | 84,712 | **+6.3%** | Complete — comparable |
| 2025-03 | 1.025 | 103,870 | 52,198 | — | Partial month — not comparable |
| 2025-04 | 1.103 | 111,806 | — | — | Future |
| 2025-05 | 1.131 | 114,574 | — | — | Future |
| 2025-06 | 1.028 | 104,156 | — | — | Future |

Caption: Forecast accuracy over the two complete holdout months.

| Model | Jan error | Feb error | Mean absolute error |
| --- | --- | --- | --- |
| Seasonal (level × index) | −39.0% | +6.3% | **22.7%** |
| Flat (level only) | −10.2% | +19.6% | **14.9%** |

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

*[The correction — have this on screen.]*

Caption: Which Checkpoint 1 findings the correction affects.

| Affected | Unaffected |
| --- | --- |
| The 2020→2022 growth figure, 69.9% → 30.9% | The −17.6% peak-to-2024 decline — both are full years |
| March's seasonal index, 0.876 → 1.025 | Printers −136,865; Electronics −40.8% |
| | Category-specific seasonality; the geography finding |

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

*[The findings summary — have this on screen.]*

Caption: What the two checkpoints found.

| # | Finding | From |
| --- | --- | --- |
| 1 | Growth stopped in 2022, but margin and average order value never moved — fewer orders, not worse ones | Q3 |
| 2 | Printers lost 136,865, over half the entire gap; all Electronics fell, all Office Supplies grew | Q5, Q7 |
| 3 | Seasonality is category-specific — Electronics peaks in Q2, the others in Q4 | Q4, Q8 |
| 4 | Geography is not a factor — state revenue spans only 28% | Q6 |
| 5 | Order count drives revenue: r = 0.923, R² = 0.851, p < 0.001 | Regression |
| 6 | Units sold predicts nothing: r = 0.045, p = 0.123 | Correlation |
| 7 | Revenue is a poor proxy for profit — CV 82.9% against 54.2% | Descriptive stats |
| 8 | The trend runs in two regimes; one line across both explains under 1% | Trend test |
| 9 | The four-order gap is worth about 250,000 a year, corroborating Q7's 257,297 | Regression |
| 10 | The seasonal forecast did not beat a flat average | Holdout |

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
is real; it's just piecewise. The trend chart shows it.

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
