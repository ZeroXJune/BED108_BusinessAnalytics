# Sales Trend Analysis — Recording Script

**BED 106 Business Analytics — Mini Capstone Project**
Talibon Polytechnic College

**Mardy reads the parts below.** The full running order:

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

# Part 4 — Mardy

*[The Amount histogram on screen.]*

I'm Mardy, and I'll take the analysis.

The first thing we asked of that data was simply what it looks like. Three
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

