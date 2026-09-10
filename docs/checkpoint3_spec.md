# Checkpoint 3 — BI Dashboard: data layer and specification

**BED 106 Business Analytics — Mini Capstone Project**

This document covers the part of Checkpoint 3 that is the same whichever BI
tool the dashboard is built in: the data the dashboard reads, the exact
definition of every measure on it, and the layout that answers the three
business questions. Building the visuals in Power BI, Tableau or Looker Studio
is the step after this one.

> **Assumption stated up front.** The project brief's Checkpoint 3 task list is
> not in this repository — only Checkpoints 1 and 2 were transcribed into
> `docs/rubric_compliance.md`. This specification is built from what
> Checkpoints 1 and 2 established, and from the brief's stated shape for
> Checkpoint 3 (a BI dashboard, Semi-Final phase). Check it against the brief's
> actual Task 3.x list before building, and tell me what differs.

---

## 1. The data layer

Five SQL views in `sql/06_dashboard_views.sql`, exported to CSV in
`data/dashboard/` by `scripts/build_dashboard_data.py`. Connect a BI tool to
MySQL and use the views, or load the CSVs — they are the same rows.

| View / file | Grain | Rows | For |
| --- | --- | --- | --- |
| `v_sales_detail` · `sales_detail.csv` | One transaction line, fully labelled | 1,194 | Anything the aggregates do not cover |
| `v_monthly` · `monthly.csv` | One complete calendar month | 59 | Every trend visual |
| `v_category_month` · `category_month.csv` | Month × sub-category | 562 | The mix visuals |
| `v_geography` · `geography.csv` | State × city | 18 | The map, and the "not a factor" check |
| `v_annual` · `annual.csv` | One year in the analysis window | 5 | The year-on-year summary |

**Two things in the data layer are deliberate and worth being able to defend.**

**`v_monthly` returns 59 rows, and 57 of them are the analysis window.**
`is_complete_month` admits January and February 2025 — whole months that sit
outside the window the Checkpoint 2 regression was fitted on. They are the two
holdout months the forecast was tested against. The `in_analysis_window` column
marks the 57 months (April 2020 to December 2024), so a dashboard filtered on
that column agrees with the Checkpoint 2 report exactly, and one that is not can
still show the holdout. Default the filter to the 57.

**`v_annual` excludes 2025 outright.** Two months of 2025 would produce a
revenue-per-month figure that looks comparable to a full year and is not. This
is the same class of mistake as the Checkpoint 1 correction, and the view is
built so it cannot be made.

`scripts/build_dashboard_data.py` verifies ten figures against the published
reports before it writes anything — row count, total revenue, the analysis
window, each year's revenue per month, the Printer collapse, the state count —
and exits non-zero if any has drifted. Run it before every rebuild.

---

## 2. Measure definitions

Every number on the dashboard, with its formula and its value today. A measure
not on this list does not belong on the dashboard.

| Measure | Definition | Current value |
| --- | --- | --- |
| **Orders per month** | `transaction_lines ÷ months_covered` | **20.0** (2024) |
| **Revenue per month** | `SUM(amount) ÷ months_covered` | **100,206.50** (2024) |
| **Margin %** | `SUM(profit) ÷ SUM(amount) × 100` | **25.64%** (2024) |
| **Average line value** | `SUM(amount) ÷ COUNT(lines)` | **5,010.33** (2024) |
| **Peak-to-current gap** | 2022 revenue/month − 2024 revenue/month | **−21,441.42**, −17.6% |
| **Order gap** | 2022 orders/month − 2024 orders/month | **4.0 orders** |
| **Gap value** | Order gap × regression slope (5,224.25) × 12 | **~250,000 a year** |
| **Revenue per customer** | `SUM(amount) ÷ COUNT(DISTINCT customer)` | Per city, in `v_geography` |

Measure the trend **per month**, never per year. 2020 holds nine months. Every
per-year total in this project is divided by `months_covered` for that reason,
and the dashboard must do the same.

---

## 3. Which KPI goes at the top, and why

Checkpoint 2 settled this, and it is the single most defensible design decision
on the dashboard.

**Order count is the primary KPI, not revenue.** Order count explains 85% of the
month-to-month variation in revenue (r = 0.9227, R² = 0.8514, p = 1.98 × 10⁻²⁴),
it is the leading indicator, and it is the thing the business can act on.
Revenue is what happens as a result.

**Segment on margin, not revenue.** Only about 46% of profit variation tracks
revenue (r = 0.6753), and profit is far more variable than revenue (CV 82.9%
against 54.2%). A dashboard that ranks anything by revenue alone will point
management at the wrong accounts — Checkpoint 1's Q1 found lines returning 414
and 4,339 profit on near-identical revenue.

**Do not put a single blended seasonality curve on the dashboard.** Electronics
peaks in Q2 at 30.79% of its annual revenue; Furniture and Office Supplies peak
in Q4 at 30.84% and 32.16%. One curve is wrong for all three. Seasonality
visuals must be split by category or not shown.

---

## 4. Dashboard layout

Four pages, each answering something specific. The business question each one
serves is named, because a visual that answers no question does not earn its
space.

### Page 1 — Executive summary

*Answers: is the company still growing?*

- **KPI row**, five tiles: orders per month, revenue per month, margin %,
  average line value, and the peak-to-current gap. Each against the 2022 peak,
  not against last month
- **The trend line**, revenue per month across the 57-month window, with the two
  regimes marked — growth to the late-2022 peak, then the plateau. This is the
  headline visual of the whole project
- **Year summary table** from `v_annual`, showing `months_covered` as a column
  so nobody compares a nine-month 2020 against a full year

### Page 2 — Product mix

*Answers: which categories and sub-categories drive the trend?*

- **Sub-category change, 2023 against 2024**, sorted by absolute change. Printers
  at −136,865 and Paper at +85,689 are the two ends
- **Category revenue over time**, three lines, so the opposite trends are visible
  rather than averaged away
- **Margin by sub-category**, since the ranking here differs from the revenue
  ranking and that difference is the point
- Filters: category, sub-category, year

### Page 3 — Seasonality

*Answers: when does demand concentrate, and is the pattern the same everywhere?*

- **Quarter share by category**, a small-multiple or grouped bar — one panel per
  category, never one blended line
- **Monthly seasonal index**, January 0.679 to December 1.273
- **Orders against average line value by month**, which shows that the Q4 peak is
  a throughput problem rather than a basket-size one: December records the most
  lines of any month at 133, on an average line value of 4,928 — below the annual
  range

### Page 4 — Geography and the negative results

*Answers: what did we rule out?*

- **State and city revenue**, showing the 28% spread that makes geography a
  non-factor. Include it so a viewer can verify the claim rather than take it
- **Quantity against amount scatter**, r = 0.0446, p = 0.123 — the "sell more
  units" strategy that the data does not support
- **The forecast and its holdout**, with the seasonal model's 22.7% mean absolute
  error against the flat average's 14.9% shown honestly

A dashboard that only shows what worked is a sales deck. Page 4 is what makes it
analysis.

---

## 5. What is still open

**The tool.** Power BI, Tableau and Looker Studio all read `data/dashboard/*.csv`
directly, and all three connect to MySQL if the brief prefers a live connection.
The data layer does not change; only the build does. Confirm what the brief or
the instructor requires.

**The brief's Task 3.x list.** See the assumption at the top of this document.

**Screenshots and interpretations.** As with both earlier checkpoints, Section
3.2 requires the written interpretation of every visual to be the group's own
words, and Section 3.1 requires numbered, captioned figures.
