# Checkpoint 3 — BI Dashboard Development

**BED 106 Business Analytics — Mini Capstone Project**
Semi-Final Period · Weeks 10–13 · 100 Points

Everything for Checkpoint 3 that can be prepared before Power BI is opened: the
Task 3.1 blueprint, the data the dashboard reads, the Task 3.3 segmentation
already computed and validated, the DAX for every measure, and a page-by-page
build order.

What only the group can do is build the visuals, export the `.pbix` and the PDF,
write the interpretations in your own words, and present. Those are marked at
each step below.

---

## Task 3.1 — Dashboard Design Blueprint

The brief asks for a wireframe showing the layout of each page, the title and
purpose of each, the visual types planned, and at least two interactive
elements. All four are on the blueprint below.

Caption: Dashboard blueprint. Three pages, their visuals, and the slicers acting on each.

![](docs/figures/cp3_fig3_wireframe.png)

| Page | Title | Purpose — the question it answers |
| --- | --- | --- |
| 1 | Executive Summary | Is the company still growing, and by how much has it slipped? |
| 2 | Trend & Comparison | Which categories and sub-categories drive the trend? |
| 3 | Deep Dive & Segmentation | Who are the customers and what are the product segments? |

**Visual types planned**

| Page | Visual | Type | Shows |
| --- | --- | --- | --- |
| 1 | Four KPI cards | Card | Orders/month, revenue/month, margin %, gap to peak |
| 1 | Revenue per month | Line | The 57-month series with the two regimes |
| 1 | Year summary | Table | Per-year figures with `months_covered` |
| 2 | Revenue by category | Line | Three categories over time |
| 2 | Sub-category change | Bar | 2023 against 2024, sorted |
| 2 | Quarter share by category | Column, small multiples | Seasonality, split by category |
| 2 | Margin by sub-category | Bar | Ranks differently from revenue |
| 3 | Sub-category segments | Scatter, bubble | k-means clusters, Task 3.3 |
| 3 | Customer segments | Scatter | k-means clusters, Task 3.3 |
| 3 | Segment profile | Table | n, revenue and margin per segment |
| 3 | State revenue | Map | The 28% spread — geography is not a driver |
| 3 | Quantity against amount | Scatter | r = 0.045, the negative result |

**Interactive elements** — the brief asks for at least two:

- **Slicers on three dimensions** — period (year and month), category and
  sub-category, and geography (state). Page 3 adds a **segment** slicer, which
  is that page's spine: selecting a segment refilters every visual on it
- **Drill-through from Page 2 to Page 3** — right-clicking any sub-category bar
  opens Page 3 filtered to that sub-category
- **Cross-filtering** between visuals on the same page, left on by default

---

## Task 3.2 — The data the dashboard reads

Five views in `sql/06_dashboard_views.sql`, exported to CSV in
`data/dashboard/` by `scripts/build_dashboard_data.py`. Connect Power BI to
MySQL and use the views, or load the CSVs — they are the same rows.

| View / file | Grain | Rows | Used by |
| --- | --- | --- | --- |
| `v_sales_detail` · `sales_detail.csv` | One transaction line, labelled | 1,194 | Page 3 scatter, anything ad hoc |
| `v_monthly` · `monthly.csv` | One complete calendar month | 59 | Page 1 line chart, KPI cards |
| `v_category_month` · `category_month.csv` | Month × sub-category | 562 | All of Page 2 |
| `v_geography` · `geography.csv` | State × city | 18 | Page 3 map |
| `v_annual` · `annual.csv` | One year in the analysis window | 5 | Page 1 table |
| `customer_segments.csv` | One customer | 807 | Page 3, from `build_segments.py` |
| `subcategory_segments.csv` | One sub-category | 12 | Page 3, from `build_segments.py` |

**Two things in the data layer are deliberate, and both are defensible.**

`v_monthly` returns 59 rows, not 57. `is_complete_month` admits January and
February 2025 — whole months that sit outside the window the Checkpoint 2
regression was fitted on, and which are the two holdout months the forecast was
tested against. The `in_analysis_window` column marks the 57 months from April
2020 to December 2024. **Default every trend visual to that filter**, or the
dashboard will disagree with the Checkpoint 2 report.

`v_annual` excludes 2025 outright, because two months of it would produce a
revenue-per-month figure that looks comparable to a full year. That is the same
class of mistake as the Checkpoint 1 correction, and the view is built so it
cannot be made.

`scripts/build_dashboard_data.py` verifies ten published figures before writing
anything and exits non-zero if any has drifted. Run it before every rebuild.

### The measures, as DAX

Load `monthly.csv` as `Monthly`, `category_month.csv` as `CategoryMonth`,
`annual.csv` as `Annual`, `sales_detail.csv` as `Sales`, and the two segment
files as `CustomerSegments` and `SubcategorySegments`.

```
Revenue          = SUM ( Sales[amount] )
Profit           = SUM ( Sales[profit] )
Orders           = COUNTROWS ( Sales )
Margin %         = DIVIDE ( [Profit], [Revenue] ) * 100
Avg Line Value   = DIVIDE ( [Revenue], [Orders] )

Months Covered   = DISTINCTCOUNT ( Monthly[year_month] )
Revenue / Month  = DIVIDE ( [Revenue], [Months Covered] )
Orders / Month   = DIVIDE ( [Orders], [Months Covered] )

Peak Rev / Month =
    CALCULATE ( [Revenue / Month], Annual[year_number] = 2022 )
Gap to Peak %    =
    DIVIDE ( [Revenue / Month] - [Peak Rev / Month], [Peak Rev / Month] ) * 100

-- The Checkpoint 2 regression slope, as a constant. Changing it means
-- refitting the model, not editing this line.
Gap Value / Year =
    ( [Peak Rev / Month] - [Revenue / Month] ) / 5224.25 * 5224.25 * 12
```

Always divide by `Months Covered`, never by 12. 2020 holds nine months.

**Expected values, to check the KPI cards against** — if a card disagrees with
this table, the model is wrong, not the table:

| Measure | 2024 | 2022 peak |
| --- | --- | --- |
| Orders per month | 20.0 | 24.0 |
| Revenue per month | 100,206.50 | 121,647.92 |
| Margin % | 25.64 | 26.93 |
| Average line value | 5,010.33 | 5,068.66 |
| Gap to peak | −17.6% | — |

**ACTION for the group:** build the three pages, title and label every visual,
add a source note ("Source: sales_trend database, 1,194 transaction lines,
March 2020 – March 2025"), export the `.pbix` and a PDF of all pages.

---

## Task 3.3 — Clustering and segmentation

Two k-means segmentations, both reproducible from a fixed seed by
`scripts/build_segments.py`. The brief allows Excel, Python or the built-in
Power BI clustering; this uses Python.

**How k was chosen.** Silhouette score across k = 2 to 6, then selected within
the 2–3 the brief asks for. The full scan is printed by the script rather than
hidden:

| k | Customers | Sub-categories |
| --- | --- | --- |
| 2 | 0.240 | 0.120 |
| **3** | **0.277** | **0.155** |
| 4 | 0.281 | 0.175 |
| 5 | 0.295 | 0.326 |
| 6 | 0.280 | 0.362 |

Be ready to defend this. On customers, k=5 scores 0.295 against k=3's 0.277 — a
difference too small to buy back the interpretability of five segments, two of
which came out with the same profile. On twelve sub-categories, k=6 leaves two
members per cluster, which is a partition rather than a segmentation.

### Customer segments — 807 customers

Clustered on total revenue, margin and recency, each standardised.

Caption: Customer segments. Value separates one cluster; margin separates the other two.

![](docs/figures/cp3_fig1_customer_segments.png)

| Segment | n | % of customers | % of revenue | % of profit | Margin |
| --- | --- | --- | --- | --- | --- |
| **High-Value Accounts** | 146 | 18.1% | 38.4% | 38.7% | 26.2% |
| **High-Margin Buyers** | 311 | 38.5% | 28.9% | **42.6%** | 38.5% |
| **Thin-Margin Buyers** | 350 | 43.4% | 32.7% | **18.7%** | 14.9% |

**The business significance, and it is the finding of Checkpoint 3.** Thin-Margin
Buyers are the largest group — 43% of customers and a third of revenue — and
they return **19% of the profit**. High-Margin Buyers are a smaller group
producing **43% of profit from less revenue**. A sales effort aimed at revenue
would chase the wrong group of the two. This is the customer-level form of the
Checkpoint 2 finding that revenue is a poor proxy for profit, and it converts
that statistic into a list of named accounts.

**Two honest notes to carry into the defence.** Recency separated nothing — every
cluster centre sits within 0.11 standard deviations of the mean on it — so there
are no "lapsed" or "active" segments to claim. And purchase frequency spans only
1 to 4 lines (510 customers bought once), too little spread to carry a segment
boundary, which is why it was not clustered on. Both are consequences of the
synthetic dataset documented in Checkpoint 1.

### Sub-category segments — 12 sub-categories

Clustered on total revenue, 2023-to-2024 growth, and margin.

Caption: Sub-category segments. Growth separates the two ends; the middle cluster is defined by margin.

![](docs/figures/cp3_fig2_subcategory_segments.png)

| Segment | Members | 2023 → 2024 |
| --- | --- | --- |
| **Growth Engines** | Markers, Paper, Pens, Sofas, Tables | 452,521 → 634,777, **+40.3%** |
| **Low-Margin Niche** | Binders, Phones | 180,351 → 187,537, +4.0% |
| **Declining Lines** | Bookcases, Chairs, Electronic Games, Laptops, Printers | 596,851 → 380,164, **−36.3%** |

The segmentation recovers Checkpoint 1's central finding without being told it:
the two large clusters move in opposite directions, +40.3% against −36.3%, and
the company-wide figure is their average. Printers sit at the far edge of
Declining Lines at −71.0%.

The middle cluster is named for margin, not growth: Binders grew 36.6% and
Phones fell 14.1%, so "stable" would be wrong. What its two members share is
low margin and small scale.

**ACTION for the group:** put both scatter plots on Page 3, add the segment
slicer, and write the business significance of each segment in your own words.

---

## Task 3.4 — Presentation

Ten minutes, during Weeks 12–13. The brief requires all three pages walked
through, at least one interactive feature demonstrated live, at least two
questions answered, and **every member speaking**.

`docs/discussion_script.md` already covers the project's findings across three
speakers and can be cut down for this. The live demonstration should be the
**segment slicer on Page 3** — selecting Thin-Margin Buyers and showing the
profit share collapse is the most persuasive thing on the dashboard.

Questions to expect: why order count rather than revenue as the headline KPI;
why three clusters and not five; whether the segments would hold on real data.
The answers to the first two are above; the answer to the third is no, and
saying so is better than pretending otherwise.

---

## Rubric map

| Criterion | Points | Where |
| --- | --- | --- |
| Dashboard Design & Usability | 30 | Blueprint above; **ACTION: build it** |
| Data Accuracy | 25 | Views verified against ten published figures; DAX and expected KPI values above |
| Insights & Storytelling | 25 | Page purposes above; **ACTION: the narrative in your own words** |
| Documentation | 20 | This document is the written report's spine; **ACTION: wireframe printed, `.pbix` and PDF exported** |

### Submission checklist

- Printed report: blueprint wireframe plus the discussion of insights and segmentation
- Dashboard file: `.pbix`, submitted digitally
- Exported PDF of all three dashboard pages
- Updated signed Individual Contribution Form — `reports/Form_A_Individual_Contribution.docx`
- Live presentation, Week 12 or 13
- Deadline: beginning of Week 14

### And the standing constraint

Section 3.2 still applies. The interpretation of every visual must be the
group's own words. The segmentation numbers above are computed output and the
DAX is tooling; what has to be yours is the reading of them.
