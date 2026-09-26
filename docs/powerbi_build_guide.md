# Building the Checkpoint 3 dashboard in Power BI

**BED 106 Business Analytics — Mini Capstone Project**

A `.pbix` cannot be generated outside Power BI Desktop: its data model is a
binary written by the Analysis Services engine, which ships only with the
Windows application. But Power BI also has a **plain-text project format**,
`.pbip`, and that *can* be generated — so there are two routes below.

## Route A — open the generated project (try this first)

`powerbi/Checkpoint3_Dashboard.pbip` is a complete Power BI project: the
semantic model with all eight tables, their column types, three relationships
and all twenty-two measures, plus page 1 of the report with the four KPI cards
and the trend chart already placed.

**To use it:**

1. Power BI Desktop → File → Options and settings → Options → Preview features
   → tick **Power BI Project (.pbip) save format** if it is not already on, and
   restart
2. File → Open → browse to `Checkpoint3_Dashboard.pbip`
3. It will prompt for **FolderPath** — give it the full path to your
   `data\dashboard\` folder, with a trailing backslash
4. Refresh. Then File → **Save as** → `Checkpoint3_Dashboard.pbix`

That leaves you pages 2 and 3 to build, which is Steps 6 and 7 below.

> **This has not been opened in Power BI Desktop.** There is no Power BI in the
> environment it was generated in, so it has been checked structurally — every
> file parses, every relationship points at a real column, the model references
> all eight tables — but not opened. If Power BI rejects it, do not fight it:
> use Route B, which is all hand-operated and cannot fail for the same reason.
> Tell me what the error says and I will fix the generator.

## Route B — build it by hand (the reliable route)

Everything from Step 1 onward. The data is shaped and typed, the measures are
written, and the visuals are specified field by field; what remains is loading,
pasting and dragging.

Budget about **90 minutes** for the first build if nobody in the group has used
Power BI before, and about 30 if someone has.

---

## Step 1 — Get the files

From the repository you need the folder `data/dashboard/`, which holds seven
CSVs:

```
monthly.csv              59 rows    the trend series
category_month.csv      562 rows    page 2
sales_detail.csv      1,194 rows    page 3 scatter
geography.csv            18 rows    the map
annual.csv                5 rows    the year table
customer_segments.csv   807 rows    page 3, Task 3.3
subcategory_segments.csv 12 rows    page 3, Task 3.3
```

If they are stale, regenerate with `python3 scripts/build_dashboard_data.py`
and `python3 scripts/build_segments.py`. The first verifies ten published
figures before it writes and fails loudly if any has drifted.

## Step 2 — Load the tables

**The simple way.** Home → Get data → Text/CSV, once per file. Power BI detects
the types. Check two things afterwards: `month_start` and `order_date` must be
**Date**, not Text, and `revenue`, `profit`, `margin_pct` must be **Decimal
number**.

**The tidy way.** Use `powerbi/load_tables.m`, which types every column
explicitly so you never have to fix a wrong axis later. Home → Transform data →
New Source → Blank query → Advanced Editor → paste the file → change
`FolderPath` at the top to your own path.

Rename the queries to exactly: `Monthly`, `CategoryMonth`, `Sales`,
`Geography`, `Annual`, `CustomerSegments`, `SubcategorySegments`, `DateTable`.
The measures refer to these names.

## Step 3 — Model view: relationships

Model view, then drag to create these. All are one-to-many, single direction,
from the one side to the many.

| From | To | On |
| --- | --- | --- |
| `DateTable[Date]` | `Sales[order_date]` | mark `DateTable` as the date table |
| `DateTable[MonthStart]` | `Monthly[month_start]` | one-to-one is fine here |
| `DateTable[MonthStart]` | `CategoryMonth[month_start]` | |
| `CustomerSegments[customer_id]` | `Sales[customer_id]` | **not** `customer_name` — see below |
| `SubcategorySegments[sub_category_name]` | `Sales[sub_category_name]` | |

Right-click `DateTable` → **Mark as date table** → `Date`. Without this, a
continuous axis and any time logic will misbehave.

**Use `customer_id`, never `customer_name`.** 802 distinct names resolve to 807
customers, because five names — Jacqueline Harris, Michael Rodriguez, Megan
Williams, Christian Jones and Kimberly Fuller — each appear in two different
cities. A relationship on the name would silently merge those five pairs and
quietly corrupt the segment figures. This is the same defect Checkpoint 1
documented, surfacing again in a different tool.

Do **not** relate `Annual` or `Geography` to anything. They are standalone
summary tables and a relationship would double-count them.

## Step 4 — The measures

Twenty measures are written out in `powerbi/measures.dax`. Add them by hand
(Modeling → New measure, about fifteen minutes), or paste the C# block at the
bottom of that file into Tabular Editor 2 and create all twenty at once.

**Verify before building anything on them.** Drop a card on a blank page, put
`Revenue per Month` on it, and filter to 2024. It must read **100,206.50**. If
it does not, the model is wrong and every visual built on it will be wrong too.

| Measure | 2024 | 2022 |
| --- | --- | --- |
| Orders per Month | 20.0 | 24.0 |
| Revenue per Month | 100,206.50 | 121,647.92 |
| Margin % | 25.64 | 26.93 |
| Avg Line Value | 5,010.33 | 5,068.66 |
| Gap to Peak % | −17.6 | 0.0 |

---

## Step 5 — Page 1: Executive Summary

*Task 3.2 requires at least four KPI cards on this page.*

**Four cards**, across the top. Visual → Card, one measure each:
`Orders per Month`, `Revenue per Month`, `Margin %`, `Gap to Peak %`.
Give each a title naming the comparison, for example "Orders per month — 20.0
against a 2022 peak of 24.0".

**Line chart** — revenue per month, the headline visual of the project.

- X axis: `Monthly[month_start]`, set to **Continuous**, not Categorical
- Y axis: `Monthly[revenue]`
- Filter: `Monthly[in_analysis_window]` is 1 — **this one matters.** Without it
  the chart shows 59 months and stops agreeing with the Checkpoint 2 report,
  which used 57
- Title: "Revenue per month, April 2020 – December 2024"
- Add two shaded regions or a reference line at 2022-12 to mark where growth
  ends and the plateau begins

**Table** — the year summary. Fields from `Annual`: `year_number`,
`months_covered`, `revenue_per_month`, `margin_pct`, `avg_line_value`.

Keep `months_covered` visible. It is what stops a reader comparing a
nine-month 2020 against a full year, and it is the visible trace of the
correction the group found and fixed.

**Slicers**: `Annual[year_number]` and `Sales[category_name]`.

## Step 6 — Page 2: Trend & Comparison

*Task 3.2 requires at least two different chart types here. This page has
three.*

**Line chart** — revenue by category over time.
X: `CategoryMonth[month_start]` continuous · Y: `revenue` ·
Legend: `category_name`. Three lines, and the point is that they diverge.

**Bar chart** — sub-category change, 2023 against 2024.
Y axis: `SubcategorySegments[sub_category_name]` ·
X axis: a quick measure or calculated column `revenue_2024 − revenue_2023` ·
sort descending. Printers at −136,865 and Paper at +85,689 are the two ends.

**Column chart, small multiples** — quarter share by category.
X: `CategoryMonth[quarter_number]` · Y: `revenue` ·
Small multiples: `category_name`. Three panels.

Never put a single blended seasonality line on this page. Electronics peaks in
Q2 at 30.79% of its own annual revenue while the other two peak in Q4; one line
is wrong for all three.

**Bar chart** — margin by sub-category, using `margin_pct`. The ranking differs
from the revenue ranking, and that difference is the reason the visual is here.

**Slicers**: year, category, state — three dimensions, against the two the
brief asks for.

**Drill-through**: on Page 3, drag `sub_category_name` into the Drill through
well. Right-clicking any bar on Page 2 then opens Page 3 filtered to it. That
is your second interactive element for Task 3.1.

## Step 7 — Page 3: Deep Dive & Segmentation

*Task 3.2 requires at least one visual from the clustering work. This page has
three.*

**Scatter** — sub-category segments.
X: `growth_pct` · Y: `margin_pct` · Size: `revenue_total` ·
Legend: `segment` · Details: `sub_category_name`.
Three clusters: Growth Engines, Low-Margin Niche, Declining Lines.

**Scatter** — customer segments.
X: `CustomerSegments[revenue]` · Y: `margin_pct` · Legend: `segment`.
807 points in three clusters.

**Table** — the segment profile, and the most persuasive object on the
dashboard. Rows: `CustomerSegments[segment]`. Values: `Segment Customers`,
`Segment % of Customers`, `Segment % of Revenue`, `Segment % of Profit`,
`Segment Margin %`.

It should read:

| Segment | n | % customers | % revenue | % profit | Margin |
| --- | --- | --- | --- | --- | --- |
| High-Value Accounts | 146 | 18.1 | 38.4 | 38.7 | 26.2 |
| High-Margin Buyers | 311 | 38.5 | 28.9 | 42.6 | 38.5 |
| Thin-Margin Buyers | 350 | 43.4 | 32.7 | 18.7 | 14.9 |

**Map** — `Geography[state_name]`, sized by `revenue`. Six states, a 28%
spread. It is here so a viewer can confirm that geography is not a driver
rather than take the claim on trust.

**Scatter** — `Sales[quantity]` against `Sales[amount]`, the negative result.
r = 0.045, p = 0.123. Add a trend line from the Analytics pane; its flatness is
the finding.

**Slicers**: `CustomerSegments[segment]`, category, year. The segment slicer is
this page's spine — selecting Thin-Margin Buyers and watching the profit share
collapse is the live demonstration for Task 3.4.

---

## Step 8 — Finish

**Every visual needs a title, axis labels and a source note.** Task 3.2 asks
for it explicitly and the rubric gives 30 points for design and usability. Put
one text box on each page: *"Source: sales_trend database, 1,194 transaction
lines, March 2020 – March 2025. Synthetic dataset — see Checkpoint 1."*

Keep one colour per category across all three pages. A reader should not have
to relearn the palette on each page.

**Then:**

- File → Save as → `Checkpoint_3_Dashboard.pbix`
- File → Export → PDF, for all three pages
- Check every KPI against the table in Step 4 one final time

## If a number disagrees

In order of likelihood:

**The line chart shows 59 months.** The `in_analysis_window = 1` filter is
missing from the visual.

**Revenue per Month is wrong by a factor.** `Months Covered` is counting the
wrong thing — it must be `DISTINCTCOUNT(Sales[year_month])`, not a hard 12.

**A date axis sorts oddly or will not go continuous.** `month_start` imported
as Text. Fix the type in Power Query, not in the visual.

**Segment percentages do not sum to 100.** The `ALL()` in the share measures
was dropped, so the denominator is being filtered along with the numerator.

**Everything is doubled.** `Annual` or `Geography` got related to `Sales`. They
are summary tables; remove the relationship.

**The segment table shows 802 customers, not 807.** The relationship was built
on `customer_name` instead of `customer_id`.
