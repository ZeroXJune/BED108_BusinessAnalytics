# Checkpoint 2, Explained End to End

**BED 106 — Business Analytics · Mini Capstone · Sales Trend Analysis**

Everything in Checkpoint 2: what was asked, what the workbook contains sheet by
sheet, what every statistic means, and how each finding was reached.

Read it before the checkpoint. Section 1.4 of the brief lets the instructor ask
any member to explain any part of the project — and Checkpoint 2 is the one
where that is most likely to mean *"what does this number mean?"*

**Contents**

1. [What Checkpoint 2 is](#1-what-checkpoint-2-is)
2. [The workbook, sheet by sheet](#2-the-workbook-sheet-by-sheet)
3. [Task 2.1 — the spreadsheet](#3-task-21--the-spreadsheet)
4. [Task 2.2 — descriptive statistics](#4-task-22--descriptive-statistics)
5. [Task 2.3 — correlation](#5-task-23--correlation)
6. [Task 2.4 — regression](#6-task-24--regression)
7. [Task 2.5 — trend and seasonality](#7-task-25--trend-and-seasonality)
8. [Statistics reference](#8-statistics-reference)
9. [The six findings](#9-the-six-findings)
10. [Likely defense questions](#10-likely-defense-questions)
11. [Glossary](#11-glossary)

---

## 1. What Checkpoint 2 is

The **Midterm** phase, Weeks 5–9, worth **100 of the 400** capstone points. It
assesses **CILO 2**: *apply spreadsheet and statistical techniques (descriptive
statistics, correlation, regression) to analyze business data and support
decision-making.*

Checkpoint 1 built a database and asked *what happened*. Checkpoint 2 takes the
same data into a spreadsheet and asks *how strong is the evidence, and what can
we predict*. The brief requires the **same dataset** — you cannot switch.

### How the 100 points split

| Criterion | Points | What the examiner looks for |
| --- | --- | --- |
| Statistical Accuracy | **30** | Descriptive stats correct and complete. Correlation and regression outputs accurate. Calculations match the data. |
| Interpretation of Results | **30** | Narratives show genuine business insight. R², p-value and the equation interpreted correctly. Findings tied back to the original questions. |
| Spreadsheet Report Quality | **25** | Organised workbook, labelled sheets. Pivot tables and charts correct and relevant. Formulas appropriate. |
| Documentation | **15** | Neat structure, titled charts, workbook submitted with the report. |

**Where the marks really are:** accuracy and interpretation together are **60%**.
Getting the numbers right is only half — you must also say what they *mean* for
the business. A correct R² with no interpretation scores badly.

### What must be submitted

- Printed report with all written interpretations and printed outputs.
- The Excel workbook (`.xlsx`) via the class portal.
- Updated signed Individual Contribution Form.
- Deadline: end of the Week 9 laboratory session.

---

## 2. The workbook, sheet by sheet

`reports/Checkpoint_2_Workbook.xlsx` — ten sheets, 1,724 formula cells.

| Sheet | Task | What it holds |
| --- | --- | --- |
| **Read Me** | — | Sheet guide and seven self-checks |
| **Cleaned Data** | 2.1 (1) | 1,194 transaction lines × 19 columns |
| **Pivot Analysis** | 2.1 (2) | Four cross-tabs |
| **Pivot Charts** | 2.1 (3) | Four charts |
| **Formulas Showcase** | 2.1 (4) | Eight Excel functions |
| **Descriptive Stats** | 2.2 | 13 statistics × 3 variables |
| **Frequency** | 2.2 | Distribution table + histogram |
| **Correlation** | 2.3 | Two pairs + a supporting third |
| **Regression** | 2.4 | Equation, R², t, p, forecasts, limits |
| **Forecast** | 2.5 | Trend test, seasonal index, forecast, holdout check |

### Two design decisions to be able to defend

**Every computed cell is a live formula, not a pasted number.** Change a value
in Cleaned Data and every statistic, chart and forecast updates. If the
statistics were typed in as constants, the workbook would be a picture of an
analysis rather than an analysis. It also means nothing can silently drift out
of step with the data.

**Formulas use named ranges.** `Amount`, `Profit`, `Quantity`, `Category`,
`State`, `Yr`, `YearMonth`, `SubCategory` and `PaymentMode` each name a column
of Cleaned Data. So the workbook says

```
=SUMIF(Category,"Electronics",Amount)
```

rather than `=SUMIF('Cleaned Data'!$M$2:$M$1195,"Electronics",'Cleaned Data'!$Q$2:$Q$1195)`.
Same result, but you can read it aloud and it means something.

### The self-checks

The Read Me sheet ends with seven rows that each recompute a total **two
independent ways** and compare — for example, Pivot 1's grand total against
`SUM(Amount)`. All seven must read **OK**.

They exist because the workbook was built on Linux, where formulas are written
but never calculated. Excel calculates them the moment the file opens, and
these rows are what proves it worked. **Check them before you submit.**

---

## 3. Task 2.1 — the spreadsheet

### What was asked

A workbook with four sheets: cleaned data, at least 3 pivot tables, at least 3
pivot charts, and at least 5 Excel functions.

### Sheet 1 — Cleaned Data

The 1,194 transaction lines from the Checkpoint 1 database, with calendar
columns (Year, Quarter, MonthNo, MonthName, YearMonth) and the product
hierarchy joined on. `MarginPct` is a formula — `=Profit/Amount` — not a stored
value, because a margin is derived and should never be able to disagree with
the two numbers it comes from.

### Sheet 2 — Pivot Analysis (four cross-tabs)

| # | Cross-tab | Functions | Answers |
| --- | --- | --- | --- |
| 1 | Revenue by Category × Year | `SUMIFS` | Which category is growing? |
| 2 | Orders, revenue, AOV and margin by State | `COUNTIFS`, `SUMIFS`, `AVERAGEIFS` | Is any region different? |
| 3 | Orders, revenue, units by month | `COUNTIFS`, `SUMIFS` | The series everything else uses |
| 4 | Sub-category revenue, 2023 vs 2024 | `SUMIFS` with two criteria | Reproduces the CP1 Printers finding |

**On "pivot tables".** These are **formula-driven cross-tabs**, not PivotTable
objects. They compute exactly what a PivotTable computes, they recalculate
live, and every cell is auditable — you can click it and read the logic, which
you cannot do inside a PivotTable. If your instructor wants the objects
themselves, `docs/checkpoint2_excel_guide.md` §2 has the two-minute procedure
per table. Be ready to explain the difference either way.

### Sheet 3 — Pivot Charts

Four charts, each titled, axis-labelled and annotated with the business point:
category × year, average order value by state, monthly revenue over time, and
the 2023→2024 sub-category change.

### Sheet 4 — Formulas Showcase

Eight functions, each answering a real question rather than demonstrating
syntax: `SUMIF`, `COUNTIF`, `SUMIFS`, `AVERAGEIF`, `VLOOKUP`, `IF`, `TEXT`,
`MAX`/`MIN`.

---

## 4. Task 2.2 — descriptive statistics

### What was asked

For at least 3 numerical variables: mean, median, mode; standard deviation,
variance, range, min, max; a frequency table and histogram for one; and a
written paragraph per variable.

We report **13** statistics for **Amount**, **Profit** and **Quantity**
(n = 1,194), adding quartiles, IQR and the coefficient of variation.

| Statistic | Amount | Profit | Quantity |
| --- | --- | --- | --- |
| Mean | 5,178.09 | 1,348.99 | 10.67 |
| Median | 5,152.00 | 1,014.00 | 11.00 |
| Mode | 717 | 177 | 14 |
| Std deviation | 2,804.92 | 1,117.99 | 5.78 |
| Variance | 7,867,587.17 | 1,249,907.39 | 33.37 |
| Min / Max | 508 / 9,992 | 50 / 4,930 | 1 / 20 |
| Range | 9,484 | 4,880 | 19 |
| Q1 / Q3 | 2,799 / 7,626 | 410 / 2,035 | 6 / 16 |
| IQR | 4,827 | 1,625 | 10 |
| Coefficient of variation | **54.2%** | **82.9%** | 54.1% |

### What each statistic is actually for

**Mean vs median — the skew test.** If they are close, the distribution is
symmetric. If the mean is well above the median, a few large values are pulling
it up (right skew).

- Amount: mean 5,178 ≈ median 5,152 → **symmetric**
- Profit: mean 1,349 ≫ median 1,014 → **right-skewed**

That single comparison is the most useful thing on the sheet, and it is why
the report says the *median* is the honest figure to quote for a typical
order's profit.

**Mode** is the most frequent value. Useful for Quantity (mode 14 out of 20
possible values) and close to meaningless for a continuous variable like
Amount, where the "mode" of 717 appears just 6 times in 1,194 rows. Say that
rather than reporting it as if it mattered — knowing when a statistic does not
apply is worth marks.

**Standard deviation vs variance.** Variance is the standard deviation squared.
Same information, but variance is in *squared* units (currency²), which is
meaningless to a business reader. Quote the standard deviation; report the
variance because the brief asks for it.

**Coefficient of variation** is standard deviation ÷ mean, expressed as a
percentage. It lets you compare spread across variables with different units.
This is the one that produces a real finding: Profit's **82.9%** against
Amount's **54.2%** says profit is far less predictable than revenue — two
orders of the same value can return very different profits.

**Quartiles and IQR.** Q1 is the value 25% of rows fall below, Q3 is 75%. The
IQR is the middle half, and unlike the range it ignores extremes.

### The histogram is the real finding

The **Frequency** sheet bins Amount into ten bands of 1,000 and counts each
with `COUNTIFS` (not the `FREQUENCY` array function, so each cell is
independent and auditable).

The shape is **flat, not bell-shaped**. A normal distribution peaks in the
middle and thins at both ends. This one is roughly level from 508 to 9,992 —
which is what a random number generator produces, and further evidence the
dataset is synthetic, consistent with the four signals documented in
Checkpoint 1.

The business reading: **there is no "typical" order size** to design around,
and no premium segment to separate out.

---

## 5. Task 2.3 — correlation

### What was asked

Two pairs of variables. For each: the Pearson coefficient, a scatter plot with
a trendline, and an interpretation of direction, strength and business meaning.

### What r actually means

Pearson's **r** runs from −1 to +1:

- **Sign** is direction. Positive = they rise together; negative = one rises as
  the other falls.
- **Size** is strength. Conventional bands: 0.7+ strong, 0.4–0.7 moderate,
  below 0.4 weak.
- **r²** is the share of variation in one variable that moves with the other.
  r = 0.9227 gives r² = 0.8514, so about **85%**.
- The **p-value** answers a different question: could a correlation this large
  have arisen by chance if the true correlation were zero? Below 0.05 means no,
  probably not.

### Pair 1 — monthly orders vs monthly revenue

**r = +0.9227, r² = 0.8514, p = 1.98 × 10⁻²⁴, n = 57 months. Strong positive.**

Months with more orders have proportionally more revenue, and order count alone
tracks about 85% of the variation in monthly revenue.

This is the statistical form of the Checkpoint 1 finding. CP1 *observed* that
revenue fell while average order value stayed flat and *inferred* that order
count was doing the work. This tests the inference and confirms it.

### Pair 2 — line quantity vs line amount

**r = +0.0446, r² = 0.0020, p = 0.123, n = 1,194. Negligible — not significant.**

Essentially no relationship. Units sold explains **0.2%** of the variation in
order value, and at p = 0.123 we **cannot reject** the hypothesis that the true
correlation is zero.

**A negative result is still a result, and this one is the more useful of the
two.** The intuitive assumption — sell more units, earn more revenue — is false
here, because unit price varies so widely across the twelve sub-categories that
volume carries no information about value. Practically: an incentive scheme
based on units shifted would not raise revenue, and "units sold" should not be
used as a performance measure.

### Supporting check — amount vs profit

**r = +0.6753, r² = 0.4560, p < 0.001.** Moderate-to-strong, but notably *not*
near 1.0: only **46%** of profit variation tracks revenue. The other 54% is
margin differences between products — which is the same story the coefficient
of variation told in Task 2.2, arrived at a different way.

### The caveat you must state

**Correlation is not causation.** A strong r says two things move together. It
does not say one causes the other, and it cannot rule out a third factor
driving both. Say this about Pair 1 explicitly: more orders and more revenue
move together, but that does not prove that pushing order count up would
mechanically raise revenue — if the extra orders were won by discounting, the
average order value would fall and the relationship would not hold.

---

## 6. Task 2.4 — regression

### What was asked

One dependent variable (Y) and one predictor (X); the equation, R², a
significance test on the slope, at least one forecast, and a discussion of
limitations.

### The variables, and why

- **Y (dependent):** monthly revenue
- **X (predictor):** number of orders in that month

Three reasons: it tests the central Checkpoint 1 claim rather than asserting it;
it had by far the strongest correlation of any pair examined; and it is
**actionable** — a business can influence how many orders it wins far more
readily than how large each one is.

### The output

| Statistic | Value | What it is |
| --- | --- | --- |
| n | 57 | Months in the sample |
| **Slope (b)** | **5,224.25** | Revenue added per extra order |
| Intercept (a) | −1,353.65 | Predicted revenue at zero orders |
| r | 0.9227 | Correlation |
| **R²** | **0.8514** | Share of revenue variation explained |
| Std error of estimate | 15,099.14 | Typical prediction error |
| Std error of slope | 294.35 | Uncertainty in the slope |
| **t statistic** | **17.75** | Slope ÷ its standard error |
| Degrees of freedom | 55 | n − 2 |
| **p-value** | **1.98 × 10⁻²⁴** | Chance of this slope if the truth were zero |

### The equation

> **Monthly Revenue = −1,353.65 + 5,224.25 × (Orders in month)**

### Reading it properly

**The slope** says each additional order in a month is associated with about
**5,224** more revenue.

Now the detail worth leading with in a defense: the average transaction line in
this dataset is worth **5,178**. The slope and the average order value agree to
within **1%**. That is exactly what should happen if revenue is simply order
count multiplied by a stable average order size — so the model is *consistent
with* the data, not merely fitted to it. Two independent routes to the same
number is the strongest evidence in the whole checkpoint.

**R² = 0.8514** means order count explains **85.1%** of the month-to-month
variation in revenue. The remaining 14.9% is product mix, seasonality and
noise.

**The t statistic and p-value.** The **null hypothesis** is that the true slope
is zero — that order count tells you nothing about revenue. The t statistic is
the slope divided by its own uncertainty: 5,224.25 ÷ 294.35 = **17.75**. A t of
about 2 is the usual threshold for significance, so 17.75 is enormous. The
p-value converts that to a probability: **1.98 × 10⁻²⁴**, far below 0.05, so we
**reject the null hypothesis**.

**The intercept is meaningless here, and you should say so.** −1,353.65 is the
predicted revenue at zero orders — both impossible and far outside the observed
range (no month had fewer than 9 orders). It is a mathematical artefact of
fitting a line, not a business quantity. Volunteering this shows you understand
the model rather than just reporting its output.

### The forecast, and what it is worth

| Orders in month | Predicted revenue |
| --- | --- |
| 15 | 77,010 |
| 20 | 103,131 |
| 25 | 129,253 |
| 30 | 155,374 |

2024 ran at **20.0** orders per month against **24.0** in 2022. The model puts
the value of closing that four-order gap at roughly **20,900 per month, or
250,000 a year** — which is very close to the **257,297** annual shortfall
measured directly in Checkpoint 1 by a completely different method. Two
independent methods agreeing is a good sign the number is sound.

### The six limitations

1. **Linearity** — assumed to be a straight line; the scatter supports it over
   the observed range.
2. **Independence** — each month assumed independent of the last. **This is the
   weakest assumption.** Monthly sales series are usually autocorrelated, and
   that inflates apparent significance. With t = 17.75 the conclusion survives
   comfortably, but read the p-value as "clearly significant" rather than as a
   precise probability.
3. **Range of validity** — X was observed between 9 and 45 orders. Anything
   outside that, the intercept included, is extrapolation.
4. **Correlation is not causation** — see above.
5. **One predictor only** — cannot capture seasonality, product mix, or the
   Printer supply problem. Multiple regression in Checkpoint 4 is the extension.
6. **Synthetic data** — the coefficients describe this file, not a real market.

---

## 7. Task 2.5 — trend and seasonality

### What was asked

Plot the data over time, identify the trend, project 3–6 periods, and discuss
reliability and assumptions.

### The analysis window: 57 months

The file runs **22 March 2020 to 15 March 2025**, so both ends are partial.
Three windows are excluded:

- **March 2020** — 10 days of trading only
- **March 2025** — 15 days only
- **All of 2025** for year-on-year work

leaving **April 2020 to December 2024 = 57 whole months**. January and February
2025 are complete months in a partial year, so they are **held back** and used
only to check the forecast.

This matters: leaving the 10-day March 2020 in a monthly average pulled March's
seasonal index from 1.025 down to 0.876 — a 15% distortion that would have made
an average month look weak.

### Step 1 — is there a trend to project?

Regressing revenue on a simple time index t = 1, 2, 3…:

| Statistic | Value |
| --- | --- |
| Slope | +206.0 per month |
| **R²** | **0.0078** |
| **p-value** | **0.515** |

Time explains **less than 1%** of the variation, and at p = 0.515 the apparent
upward slope is indistinguishable from noise.

**This is a finding, not a failure.** The series is not a trend — it is a
**growth phase followed by a plateau**. Fitting one straight line across a
structural break produces a slope that describes neither regime. So **no growth
rate is projected**. Forecasting a slope the data does not support is the
easiest way to be badly wrong, and saying so is worth more than producing a
confident-looking number.

### Step 2 — the seasonal index

Each calendar month's average revenue divided by the overall average month.
1.00 = an average month.

| Month | Index | | Month | Index |
| --- | --- | --- | --- | --- |
| January | **0.679** | | July | 0.966 |
| February | 0.889 | | August | 1.006 |
| March | 1.025 | | September | 0.793 |
| April | 1.103 | | October | **1.229** |
| May | 1.131 | | November | 0.878 |
| June | 1.028 | | December | **1.273** |

December and October are the strongest; January is the weakest at barely half a
December.

### Step 3 — the forecast

With no reliable trend, the forecast is **recent level × seasonal index**, where
the level is the mean of the last 24 months (**101,342**).

| Period | Index | Forecast | Actual | Error |
| --- | --- | --- | --- | --- |
| 2025-01 | 0.679 | 68,853 | 112,906 | **−39.0%** |
| 2025-02 | 0.889 | 90,064 | 84,712 | **+6.3%** |
| 2025-03 | 1.025 | 103,870 | *(partial month)* | — |
| 2025-04 | 1.103 | 111,806 | — | — |
| 2025-05 | 1.131 | 114,574 | — | — |
| 2025-06 | 1.028 | 104,156 | — | — |

### Step 4 — the honest check

Compared against a naive alternative that ignores seasonality and predicts the
recent average every month:

| Model | Jan | Feb | Mean absolute error |
| --- | --- | --- | --- |
| Seasonal | −39.0% | +6.3% | **22.7%** |
| Flat | −10.2% | +19.6% | **14.9%** |

**The seasonal model did not win.** Better in February, much worse in January,
and on average the simpler flat forecast was more accurate over these two
months.

The cause is identifiable: January is historically the weakest month at index
0.679, but **January 2025 came in at 112,906 — above the recent average level,
not 32% below it.** Either the seasonal pattern has broken, or January 2025 was
unusual. Two observations cannot tell those apart.

**The conclusion to state: with two comparable months, no forecasting method
can be validated here.** This is reported as a sanity check, not as evidence the
model works. What it does establish is that the seasonal adjustment is not
obviously earning its complexity — worth knowing before anyone plans inventory
on it.

Reporting a check that your own model failed is a strength. The alternative —
presenting a forecast with no validation at all — is what most submissions do,
and it is weaker.

---

## 8. Statistics reference

| Term | Meaning | Where |
| --- | --- | --- |
| Mean | Arithmetic average | 2.2 |
| Median | Middle value; robust to outliers | 2.2 |
| Mode | Most frequent value | 2.2 |
| Standard deviation | Typical distance from the mean | 2.2 |
| Variance | Standard deviation squared | 2.2 |
| Range | Max − min | 2.2 |
| Quartile / IQR | 25th and 75th percentile; the middle half | 2.2 |
| Coefficient of variation | SD ÷ mean; compares spread across units | 2.2 |
| Skewness | Asymmetry; mean > median means right-skewed | 2.2 |
| Pearson r | Linear correlation, −1 to +1 | 2.3 |
| r² | Share of variation shared | 2.3, 2.4 |
| p-value | Chance of the result if the null were true | 2.3, 2.4 |
| Slope / intercept | The `b` and `a` in Y = a + bX | 2.4 |
| Standard error | Uncertainty in an estimate | 2.4 |
| t statistic | Estimate ÷ its standard error | 2.4 |
| Degrees of freedom | n − 2 for simple regression | 2.4 |
| Null hypothesis | "There is no relationship" | 2.4 |
| Seasonal index | Month's average ÷ overall average | 2.5 |
| Mean absolute error | Average error size, ignoring sign | 2.5 |
| Holdout | Data withheld to test a model | 2.5 |

### Excel functions used

`AVERAGE` `MEDIAN` `MODE` `STDEV` `VAR` `MIN` `MAX` `QUARTILE` `COUNT`
`SUMIF` `SUMIFS` `COUNTIF` `COUNTIFS` `AVERAGEIF` `AVERAGEIFS`
`CORREL` `SLOPE` `INTERCEPT` `RSQ` `STEYX` `DEVSQ` `TDIST`
`VLOOKUP` `IF` `TEXT` `ROUND` `ABS` `SQRT`

All are Excel-2007-era functions, chosen deliberately so the workbook opens
correctly in any Excel version and in Google Sheets. Newer functions such as
`XLOOKUP`, `FILTER` and `TEXTJOIN` are avoided.

### Three things people get wrong

1. **r vs r².** r = 0.92 does not mean "92% explained". r² does — 85%.
2. **A high p-value does not prove there is no relationship.** It means the data
   does not provide enough evidence to conclude there is one. Pair 2 shows "not
   significant", not "proven unrelated".
3. **Significance is not importance.** With a big enough sample, a trivial
   relationship can be statistically significant. Always read the effect size
   (the slope, r²) alongside the p-value.

---

## 9. The six findings

| # | Finding | How we know |
| --- | --- | --- |
| 1 | **Order count drives revenue** — proven, not inferred | Regression: r = 0.923, R² = 0.851, p < 0.001 over 57 months (2.3, 2.4) |
| 2 | **Units sold predicts nothing** | r = 0.045, p = 0.123 — not significant (2.3) |
| 3 | **Revenue is a poor proxy for profit** | Profit skew +0.94, CV 82.9% vs 54.2%; only 46% of profit variation tracks revenue (2.2, 2.3) |
| 4 | **No linear trend exists to project** | Time explains under 1%, p = 0.515 (2.5) |
| 5 | **The four-order gap is worth ~250,000 a year** | Slope × 4 × 12, corroborating CP1's 257,297 (2.4) |
| 6 | **The seasonal forecast did not beat a flat average** | MAE 22.7% vs 14.9% over two holdout months (2.5) |

Findings 1 and 5 both **confirm Checkpoint 1 by a different route**, which is
the strongest thing this checkpoint does. Findings 2, 4 and 6 are all *negative*
results — things that turned out not to be true — and they are the ones that
demonstrate actual analysis rather than confirmation.

### Where this points for Checkpoint 3

Build the dashboard around **order count** as the primary KPI rather than
revenue, since it is the leading indicator and the actionable one. Segment on
**margin** rather than revenue, given how weakly the two are related.

---

## 10. Likely defense questions

**What does R² = 0.85 actually mean?**
That 85% of the month-to-month variation in revenue moves together with order
count. The remaining 15% is product mix, seasonality and noise. It is *not* a
statement that order count causes 85% of revenue.

**Your p-value is 1.98 × 10⁻²⁴. What is the hypothesis being tested?**
The null hypothesis that the true slope is zero — that order count tells us
nothing about revenue. With t = 17.75 on 55 degrees of freedom, the probability
of seeing a slope this large if the null were true is about 2 in 10²⁴, so we
reject the null.

**Why is your intercept negative? Revenue cannot be negative.**
Correct, and that is why the intercept is not a business quantity. It is where
the fitted line crosses zero orders, which is far outside the observed range of
9 to 45 orders per month. It is a mathematical artefact of fitting a line.

**How do you know the regression is not just curve-fitting?**
The slope came out at 5,224 and the average order value in the data is 5,178 —
within 1%. Those are two independent routes to the same number, which is what
should happen if revenue really is order count times a stable order size.

**Pair 2 has r = 0.045. Why include a correlation that shows nothing?**
Because "nothing" is the finding. The intuitive assumption is that selling more
units earns more revenue. Here it is false — unit prices vary so much across the
twelve sub-categories that volume carries no information about value. That
directly rules out a units-based sales target.

**Why did you not project a trend line for the forecast?**
Because the trend test does not support one: R² = 0.008 and p = 0.515, so the
apparent slope is indistinguishable from noise. The series is growth followed by
a plateau, and a single straight line describes neither. Projecting it would be
the easiest way to be badly wrong.

**Your forecast lost to a naive average. Is that not a failure?**
It is an honest result. Over the only two complete holdout months, the seasonal
model had a mean absolute error of 22.7% against the flat model's 14.9% —
mostly because January 2025 came in far above its historical index. Two months
cannot validate or invalidate a method, which is exactly what we say. Reporting
a check the model failed is more useful than presenting an unvalidated forecast.

**Why 57 months rather than all 61?**
Both ends of the file are partial. March 2020 has 10 days and March 2025 has 15,
and a part-month is not a valid monthly observation — leaving March 2020 in
pulled that month's seasonal index down 15%. January and February 2025 are
complete months but sit in a partial year, so they are held back as the forecast
check.

**Are these real PivotTables?**
No — they are formula-driven cross-tabs using SUMIFS, COUNTIFS and AVERAGEIFS.
They compute exactly what a PivotTable computes and recalculate live, and every
cell is auditable, which a PivotTable's internals are not. Native PivotTables
can be added in about two minutes each if required.

**Why does the histogram matter?**
Because its shape is flat rather than bell-shaped. A normal distribution peaks
in the middle; this one is roughly level across the whole range, which is what
a random number generator produces. It is a fourth piece of evidence that the
dataset is synthetic, and it means there is no typical order size to design
around.

---

## 11. Glossary

**Coefficient of variation** — standard deviation as a percentage of the mean,
so spread can be compared across variables with different units.

**Correlation** — how strongly two variables move together, measured by r.

**Degrees of freedom** — n − 2 in simple regression, because two parameters
(slope and intercept) are estimated from the data.

**Dependent variable (Y)** — the thing being predicted. **Predictor (X)** — the
thing predicting it.

**Holdout** — data deliberately withheld from the analysis so it can be used to
test the model on values it has never seen.

**Mean absolute error (MAE)** — average size of the forecast errors, ignoring
whether they are over or under.

**Null hypothesis** — the default assumption that there is no relationship. A
significance test asks whether the data gives enough evidence to reject it.

**p-value** — the probability of seeing a result at least this extreme if the
null hypothesis were true. Below 0.05 is conventionally "significant".

**Pearson r** — the linear correlation coefficient, from −1 to +1.

**R²** — the share of variation in Y explained by X. The square of r.

**Regression** — fitting a line Y = a + bX to describe how Y moves with X.

**Seasonal index** — a month's average value divided by the overall average
month. 1.00 is average; 1.27 means 27% above.

**Skewness** — asymmetry of a distribution. Positive means a tail to the right,
and the mean sits above the median.

**Standard error** — the uncertainty attached to an estimate.

**t statistic** — an estimate divided by its own standard error. Roughly 2 or
more is conventionally significant.
