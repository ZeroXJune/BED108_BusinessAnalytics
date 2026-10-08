# Building the Checkpoint 3 dashboard in Power BI

**BED 106 Business Analytics — Mini Capstone Project**
Complete build instructions, from installing Power BI to exporting the `.pbix`.

Written for someone who has never opened Power BI. Every field well, every
format setting, every click. Follow it in order — later steps assume the
earlier ones are done.

**Time:** about 90 minutes the first time, 30 if someone in the group has used
Power BI before.

---

## Contents

| Part | What it covers |
| --- | --- |
| 0 | Before you start — install, files |
| A | The shortcut: open the generated project |
| 1 | Load the seven tables |
| 2 | Fix the column types |
| 3 | Build the relationships |
| 4 | Create the 22 measures |
| 5 | Verify the model before building anything |
| 6 | Set the theme |
| 7 | Page 1 — Executive Summary |
| 8 | Page 2 — Trend & Comparison |
| 9 | Page 3 — Deep Dive & Segmentation |
| 10 | Slicers and drill-through |
| 11 | Titles, labels and source notes |
| 12 | Export the `.pbix` and the PDF |
| 13 | Troubleshooting |
| 14 | Final checklist against the rubric |

---

# Part 0 — Before you start

## 0.1 Install Power BI Desktop

Free, Windows only. Either:

- **Microsoft Store** — search "Power BI Desktop", Install. This version updates
  itself, which is the easier option.
- **Download** from powerbi.microsoft.com → Products → Power BI Desktop →
  Download free.

A Microsoft account is **not** needed to build and save a `.pbix`. You only
need to sign in to publish to the Power BI Service, which this project does not
require.

**If nobody in the group has Windows:** Tableau Public is free and runs on Mac,
and the brief accepts `.twbx` instead. The data and the measures below transfer;
the click-paths do not. Decide this before anyone starts building.

## 0.2 Get the data files

You need the folder `data/dashboard/` from the repository. It holds seven CSVs:

| File | Rows | Used on |
| --- | --- | --- |
| `monthly.csv` | 59 | Page 1 trend chart, KPI cards |
| `category_month.csv` | 562 | All of Page 2 |
| `sales_detail.csv` | 1,194 | Page 3 scatter |
| `geography.csv` | 18 | Page 3 map |
| `annual.csv` | 5 | Page 1 table |
| `customer_segments.csv` | 807 | Page 3 segments |
| `subcategory_segments.csv` | 12 | Page 2 and 3 segments |

Put the folder somewhere with a short path and **no OneDrive sync**, for example
`C:\BED106\data\dashboard\`. OneDrive paths change under you and break the
refresh.

If the files look stale, regenerate them:

```
python3 scripts/build_dashboard_data.py
python3 scripts/build_segments.py
```

The first verifies ten published figures before it writes anything and fails
loudly if any has drifted from the reports.

---

# Part A — The shortcut

`powerbi/Checkpoint3_Dashboard.pbip` is a ready-made Power BI project: the whole
semantic model (eight tables, typed columns, three relationships, all 22
measures) plus Page 1 with the four KPI cards and the trend chart already
placed.

1. Power BI Desktop → **File → Options and settings → Options → Preview
   features** → tick **Power BI Project (.pbip) save format** → OK → restart
2. **File → Open** → browse to `Checkpoint3_Dashboard.pbip`
3. It prompts for **FolderPath** — type the full path to your `data\dashboard\`
   folder **with a trailing backslash**, e.g. `C:\BED106\data\dashboard\`
4. **Home → Refresh**
5. **File → Save as** → `Checkpoint3_Dashboard.pbix`

Then skip to **Part 8** and build pages 2 and 3.

> **This project has never been opened in Power BI Desktop.** There is no Power
> BI in the environment that generated it, so it has been checked structurally
> — every file parses, every relationship points at a real column — but not
> actually opened. If it errors, don't fight it: start at Part 1 and build by
> hand. Send me the error text and I will fix the generator.

Everything from here is the hand-built route.

---

# Part 1 — Load the seven tables

**Home → Get data → Text/CSV** → pick a file → **Open** → a preview appears →
click **Load** (not Transform data yet).

Repeat for all seven files.

Power BI names each table after its file. **Rename them now** — the measures
below refer to these exact names. Right-click each table in the Data pane →
**Rename**:

| File loaded as | Rename to |
| --- | --- |
| `monthly` | `Monthly` |
| `category_month` | `CategoryMonth` |
| `sales_detail` | `Sales` |
| `geography` | `Geography` |
| `annual` | `Annual` |
| `customer_segments` | `CustomerSegments` |
| `subcategory_segments` | `SubcategorySegments` |

**Faster alternative.** `powerbi/load_tables.m` loads all seven with every
column typed correctly in one go. Home → **Transform data** → **New Source →
Blank query** → **Advanced Editor** → delete what is there, paste the file,
change `FolderPath` at the top to your path → **Done** → **Close & Apply**.
If you use this, Part 2 is already done.

---

# Part 2 — Fix the column types

Power BI guesses types on import and gets two of them wrong in a way that
breaks charts later. Check these before going further.

**Home → Transform data** to open Power Query. For each table, click the small
type icon to the left of the column name and set:

| Table | Column | Must be |
| --- | --- | --- |
| `Monthly` | `month_start` | **Date** |
| `Monthly` | `revenue`, `profit`, `avg_line_value`, `margin_pct` | **Decimal number** |
| `Monthly` | `in_analysis_window` | **Whole number** |
| `CategoryMonth` | `month_start` | **Date** |
| `CategoryMonth` | `revenue`, `profit`, `margin_pct` | **Decimal number** |
| `Sales` | `order_date`, `month_start` | **Date** |
| `Sales` | `amount`, `profit` | **Decimal number** |
| `Sales` | `customer_id`, `quantity` | **Whole number** |
| `CustomerSegments` | `revenue`, `profit`, `margin_pct` | **Decimal number** |
| `CustomerSegments` | `customer_id` | **Whole number** |
| `SubcategorySegments` | `revenue_total`, `revenue_2023`, `revenue_2024`, `growth_pct`, `margin_pct` | **Decimal number** |
| `Geography`, `Annual` | every numeric column | **Decimal number** |

**Close & Apply** when done.

**Why `month_start` matters.** `year_month` is text like `"2024-01"`. A text
column cannot go on a continuous axis and cannot drive any date logic, so the
trend chart would plot categories instead of time. `month_start` is the real
date — use it on every axis.

---

# Part 3 — Build the relationships

Switch to **Model view** (the third icon down the left edge).

Drag from the **first** column named to the **second**. Direction matters:
you always drag from the *many* side to the *one* side.

| Drag from | Drag to | Cardinality |
| --- | --- | --- |
| `Sales[customer_id]` | `CustomerSegments[customer_id]` | Many to one (\*:1) |
| `Sales[sub_category_name]` | `SubcategorySegments[sub_category_name]` | Many to one (\*:1) |

Double-click each new relationship line and confirm **Cross filter direction:
Single** and **Make this relationship active** is ticked.

**That is all three tables that need relating. Three things must NOT be
related:**

**Never relate on `customer_name`.** 802 distinct names resolve to 807
customers, because five names — Jacqueline Harris, Michael Rodriguez, Megan
Williams, Christian Jones and Kimberly Fuller — each appear in two different
cities. A relationship on the name would silently merge those five pairs and
corrupt every segment figure on Page 3. Use `customer_id`. This is the same
defect Checkpoint 1 documented in `Order ID`, reappearing in a different tool.

**Do not relate `Annual` or `Geography` to anything.** They are pre-aggregated
summary tables. Relating them to `Sales` double-counts every value on the page.

**Do not build a date table.** You do not need one. `Monthly` and
`CategoryMonth` each carry their own `month_start` at month grain, and those
columns go straight onto the axis. A daily date table cannot be related to them
anyway — its month-start column repeats about thirty times per month, so it
cannot be the "one" side of a relationship. Power BI would either refuse it or
build it backwards and your trend visuals would filter wrongly.

---

# Part 4 — Create the 22 measures

**Modeling → New measure** opens a formula bar. Type the name, `=`, then the
expression. Press Enter. Repeat.

Click the **`Sales` table first** so the measure lands there — the first fifteen
belong on `Sales`, the last seven on `CustomerSegments`.

## On the `Sales` table

```
Revenue = SUM ( Sales[amount] )

Profit = SUM ( Sales[profit] )

Orders = COUNTROWS ( Sales )

Units = SUM ( Sales[quantity] )

Customers = DISTINCTCOUNT ( Sales[customer_id] )

Margin % = DIVIDE ( [Profit], [Revenue] ) * 100

Avg Line Value = DIVIDE ( [Revenue], [Orders] )

Months Covered = DISTINCTCOUNT ( Sales[year_month] )

Revenue per Month = DIVIDE ( [Revenue], [Months Covered] )

Orders per Month = DIVIDE ( [Orders], [Months Covered] )

Peak Revenue per Month =
CALCULATE ( [Revenue per Month], ALL ( Sales ), Sales[year_number] = 2022 )

Peak Orders per Month =
CALCULATE ( [Orders per Month], ALL ( Sales ), Sales[year_number] = 2022 )

Gap to Peak % =
DIVIDE ( [Revenue per Month] - [Peak Revenue per Month],
         [Peak Revenue per Month] ) * 100

Order Gap = [Peak Orders per Month] - [Orders per Month]

Gap Value per Year = [Order Gap] * 5224.25 * 12
```

## On the `CustomerSegments` table

```
Segment Customers = COUNTROWS ( CustomerSegments )

Segment Revenue = SUM ( CustomerSegments[revenue] )

Segment Profit = SUM ( CustomerSegments[profit] )

Segment Margin % = DIVIDE ( [Segment Profit], [Segment Revenue] ) * 100

Segment % of Customers =
DIVIDE ( [Segment Customers],
         CALCULATE ( [Segment Customers], ALL ( CustomerSegments ) ) ) * 100

Segment % of Revenue =
DIVIDE ( [Segment Revenue],
         CALCULATE ( [Segment Revenue], ALL ( CustomerSegments ) ) ) * 100

Segment % of Profit =
DIVIDE ( [Segment Profit],
         CALCULATE ( [Segment Profit], ALL ( CustomerSegments ) ) ) * 100
```

## Three things to be able to explain

**Why divide by `Months Covered` and never by 12.** 2020 holds nine months of
trading, because the file starts on 22 March 2020. Dividing a nine-month year by
twelve understates it by a quarter. This is exactly the error Checkpoint 2
caught in Checkpoint 1, and every per-month measure here is written so it cannot
recur.

**Why `ALL ( Sales )` is in the peak measures.** It clears the page's year
slicer, so the 2022 peak stays the peak whichever year the viewer selects.
Without it, selecting 2024 would make the "peak" 2024 and `Gap to Peak %` would
always read zero.

**Why 5224.25 is hard-coded.** It is the slope of the Checkpoint 2 regression —
one more order in a month is worth about 5,224 in revenue. It is a constant on
purpose: changing it means refitting the model, not editing a measure.

**Faster alternative.** Install Tabular Editor 2 (free, tabulareditor.com) →
**External Tools → Tabular Editor → Advanced Scripting** → paste the C# block
at the bottom of `powerbi/measures.dax` → F5 → back in Power BI, **Refresh
now**. All 22 appear at once with their number formats set.

---

# Part 5 — Verify before you build anything

**Do this now.** Every visual you build from here inherits whatever is wrong in
the model, and a wrong KPI is worth more lost marks than a plain-looking page.

On a blank page, drop a **Card** visual, put `Revenue per Month` in it, then add
a **Slicer** with `Sales[year_number]` and select 2024.

It must read **100,206.50**. Check all five:

| Measure | 2024 | 2022 |
| --- | --- | --- |
| Orders per Month | 20.0 | 24.0 |
| Revenue per Month | 100,206.50 | 121,647.92 |
| Margin % | 25.64 | 26.93 |
| Avg Line Value | 5,010.33 | 5,068.66 |
| Gap to Peak % | −17.6 | 0.0 |

If any disagrees, stop and go to **Part 13** before building. Delete this test
page when the numbers check out.

---

# Part 6 — Set the theme

**View → Themes → Customize current theme.**

Under **Name and colours**, set the eight theme colours to these, so the
dashboard matches the figures in your written reports:

| Slot | Hex |
| --- | --- |
| Colour 1 | `2F6F9F` (blue — the main series) |
| Colour 2 | `C1666B` (red — decline) |
| Colour 3 | `5B8C5A` (green — growth) |
| Colour 4 | `D09B3E` (amber — highlight) |
| Colour 5 | `7B8994` (grey — context) |
| Colour 6 | `1F2933` (ink — text) |
| Colour 7 | `A7C4DC` |
| Colour 8 | `E4EAEF` |

Under **Text**, set the general font to **Segoe UI**, size 10.

This matters for marks: "consistent colours" is named in the 30-point Design &
Usability criterion, and one colour per category across all three pages is the
easiest way to earn it.

**Name your pages now.** Right-click each page tab at the bottom → Rename:
`1 Executive Summary`, `2 Trend & Comparison`, `3 Deep Dive`. Add pages with the
`+` at the bottom.

---

# Part 7 — Page 1: Executive Summary

The brief requires **at least four KPI cards** on this page.

## 7.1 The four KPI cards

**Visualizations pane → Card.** Drag one measure into **Fields** per card.

| Card | Measure | Title to type |
| --- | --- | --- |
| 1 | `Orders per Month` | Orders per month (2022 peak: 24.0) |
| 2 | `Revenue per Month` | Revenue per month (2022 peak: 121,648) |
| 3 | `Margin %` | Margin % |
| 4 | `Gap to Peak %` | Gap to the 2022 peak |

For each card, open the **Format** pane (the paint-roller icon):

- **Callout value** → Font size **28**, Colour → `1F2933`. On card 4 set the
  colour to `C1666B`, since it reports a shortfall
- **Category label** → Off (the title says it already)
- **Title** → On → type the text above → Font size 11 → Colour `7B8994`
- **Effects → Background** → On → Colour `E4EAEF`, Transparency 0
- **Effects → Visual border** → On → Rounded corners 8

Position them in a row across the top: each about **3.0 in wide × 1.4 in high**,
starting 0.5 in from the left and top edges, 0.2 in apart. Use **Format →
General → Properties → Size and position** to type exact numbers rather than
dragging — it is the only way to get them aligned.

## 7.2 The trend line chart

**Visualizations → Line chart.**

| Well | Field |
| --- | --- |
| X-axis | `Monthly[month_start]` |
| Y-axis | `Monthly[revenue]` |

**This next step is the one people miss.** In the **Filters** pane, under
*Filters on this visual*, drag in `Monthly[in_analysis_window]` → Filter type
**Basic filtering** → tick **1** → Apply filter.

Without it the chart shows 59 months and stops agreeing with the Checkpoint 2
report, which used 57. The two extra months are January and February 2025 —
whole months, but outside the window the regression was fitted on, and the ones
the forecast was tested against.

Format:

- **X-axis** → Type **Continuous** (not Categorical). If this option is missing,
  `month_start` is still Text — go back to Part 2
- **Y-axis** → Display units **Thousands**, Value decimal places 0
- **Title** → "Revenue per month, April 2020 – December 2024"
- **Lines** → Stroke width 3, Colour `2F6F9F`
- **Gridlines** → Horizontal on, Colour `E4EAEF`; Vertical off

**Mark the two regimes.** Format → **Analytics** pane → **Constant line** →
Add → Value `121648` → Colour `C1666B` → Line style Dashed → Data label On →
Name it "2022 peak". That single line turns a wiggly chart into the project's
argument.

Size it about **8.0 in wide × 3.6 in high**, under the cards.

## 7.3 The year summary table

**Visualizations → Table.** Drag in, from `Annual`, in this order:

`year_number`, `months_covered`, `revenue_per_month`, `margin_pct`,
`avg_line_value`

Format:

- **Title** → "Revenue per month by year"
- **Values** → Font size 11
- **Specific column** → `months_covered` → Background colour `E4EAEF`

**Keep `months_covered` visible.** It shows 2020 at nine months, which is what
stops a reader comparing it against a full year. It is the visible trace of the
correction your group found and fixed, and it is worth a sentence in the
defense.

Place it to the right of the line chart, about **3.6 in wide × 3.6 in high**.

## 7.4 Page 1 slicers

**Visualizations → Slicer**, two of them, along the bottom:

| Slicer | Field | Format |
| --- | --- | --- |
| Year | `Annual[year_number]` | Style **Tile**, horizontal |
| Category | `Sales[category_name]` | Style **Tile**, horizontal |

Set both: Format → **Slicer settings → Options → Style: Tile**, and
**Selection → Multi-select with Ctrl** on.

---

# Part 8 — Page 2: Trend & Comparison

The brief requires **at least two different chart types** here. This page has
three.

## 8.1 Revenue by category over time — line chart

| Well | Field |
| --- | --- |
| X-axis | `CategoryMonth[month_start]` (Continuous) |
| Y-axis | `CategoryMonth[revenue]` |
| Legend | `CategoryMonth[category_name]` |

Title: "Revenue by category, monthly". Legend → Position **Top centre**.

The point of this visual is that the three lines **diverge** — say so when you
present it.

Top-left quadrant, about **5.8 in × 3.0 in**.

## 8.2 Sub-category change — bar chart

First make the measure. Click `SubcategorySegments` → **New measure**:

```
Revenue Change 23 to 24 =
SUM ( SubcategorySegments[revenue_2024] ) - SUM ( SubcategorySegments[revenue_2023] )
```

**Visualizations → Clustered bar chart** (horizontal bars):

| Well | Field |
| --- | --- |
| Y-axis | `SubcategorySegments[sub_category_name]` |
| X-axis | `Revenue Change 23 to 24` |

Format:

- Click the **⋯** on the visual → **Sort axis** → `Revenue Change 23 to 24` →
  **Sort ascending**, so Printers sits at one end and Paper at the other
- **Data labels** → On, Display units None, Decimal places 0
- **Bars → Colour → Conditional formatting (fx)** → Format style **Rules** →
  Based on `Revenue Change 23 to 24` → Rule: *if value < 0* → `C1666B`;
  *if value ≥ 0* → `5B8C5A`
- Title: "Sub-category revenue change, 2023 to 2024"

Red at one end, green at the other, Printers at −136,865 and Paper at +85,689.

Top-right quadrant, about **5.8 in × 3.0 in**.

## 8.3 Quarter share by category — column chart with small multiples

**Visualizations → Clustered column chart:**

| Well | Field |
| --- | --- |
| X-axis | `CategoryMonth[quarter_number]` |
| Y-axis | `CategoryMonth[revenue]` |
| Small multiples | `CategoryMonth[category_name]` |

Format → **Small multiples** → Layout 3 columns × 1 row.

Title: "Quarterly revenue by category".

**Never replace this with one blended seasonality line.** Electronics peaks in
Q2 at 30.79% of its own annual revenue; Furniture and Office Supplies peak in Q4
at 30.84% and 32.16%. A single curve is wrong for all three, and saying so is
one of your findings.

Bottom-left, about **5.8 in × 2.6 in**.

## 8.4 Margin by sub-category — bar chart

| Well | Field |
| --- | --- |
| Y-axis | `SubcategorySegments[sub_category_name]` |
| X-axis | `SubcategorySegments[margin_pct]` (set to **Average**, not Sum) |

To change it: click the arrow next to the field in the well → **Average**.

Sort descending by margin. Title: "Margin % by sub-category".

This visual earns its place because the ranking here **differs** from the
revenue ranking — that difference is the point.

Bottom-right, about **5.8 in × 2.6 in**.

---

# Part 9 — Page 3: Deep Dive & Segmentation

The brief requires **at least one visual from the clustering work**. This page
has three.

## 9.1 Sub-category segments — scatter

**Visualizations → Scatter chart:**

| Well | Field |
| --- | --- |
| X-axis | `SubcategorySegments[growth_pct]` (Average) |
| Y-axis | `SubcategorySegments[margin_pct]` (Average) |
| Size | `SubcategorySegments[revenue_total]` (Sum) |
| Legend | `SubcategorySegments[segment]` |
| Values | `SubcategorySegments[sub_category_name]` |

Three clusters appear: **Growth Engines**, **Low-Margin Niche**, **Declining
Lines**.

Format → **Category labels** → On, so each bubble is named. Title:
"Sub-category segments (k-means, k = 3)".

Top-left, about **5.5 in × 3.0 in**.

## 9.2 Customer segments — scatter

| Well | Field |
| --- | --- |
| X-axis | `CustomerSegments[revenue]` (Sum, **not** Average) |
| Y-axis | `CustomerSegments[margin_pct]` (Average) |
| Legend | `CustomerSegments[segment]` |
| Values | `CustomerSegments[customer_name]` |

807 points in three clusters. Title: "Customer segments (k-means, n = 807)".

Top-right, about **5.5 in × 3.0 in**.

## 9.3 The segment profile table — the most persuasive object on the dashboard

**Visualizations → Table:**

| Well | Field |
| --- | --- |
| Rows | `CustomerSegments[segment]` |
| Values | `Segment Customers`, `Segment % of Customers`, `Segment % of Revenue`, `Segment % of Profit`, `Segment Margin %` |

It must read exactly this:

| Segment | n | % customers | % revenue | % profit | Margin |
| --- | --- | --- | --- | --- | --- |
| High-Value Accounts | 146 | 18.1 | 38.4 | 38.7 | 26.2 |
| High-Margin Buyers | 311 | 38.5 | 28.9 | 42.6 | 38.5 |
| Thin-Margin Buyers | 350 | 43.4 | 32.7 | 18.7 | 14.9 |

If it shows 802 customers instead of 807, the relationship is on `customer_name`
— go back to Part 3.

Format → **Cell elements** → `Segment % of Profit` → **Background colour** → On
→ Conditional formatting, so the 18.7 reads red and the 42.6 green. That one
touch makes the finding visible without a word of explanation.

Bottom-left, about **4.4 in × 2.6 in**.

## 9.4 State revenue — map

**Visualizations → Map** (the filled map also works):

| Well | Field |
| --- | --- |
| Location | `Geography[state_name]` |
| Bubble size | `Geography[revenue]` |

If Power BI asks about map services, accept. Title: "Revenue by state".

This is here so a viewer can confirm for themselves that geography is **not** a
driver — the spread across five years is only 28%. Negative results earn marks
under Insights & Storytelling.

Bottom-middle, about **3.8 in × 2.6 in**.

## 9.5 Quantity against amount — the negative result

**Visualizations → Scatter chart:**

| Well | Field |
| --- | --- |
| X-axis | `Sales[quantity]` (do **not** aggregate — set to "Don't summarize") |
| Y-axis | `Sales[amount]` ("Don't summarize") |
| Values | `Sales[sale_id]` |

Then **Analytics pane → Trend line → Add**, Colour `C1666B`, Style Dashed.

Title: "Units sold against order value — r = 0.045, p = 0.123".

The trend line comes out flat. That flatness **is** the finding: a "sell more
units" target would not move revenue in this business.

Bottom-right, about **3.8 in × 2.6 in**.

---

# Part 10 — Slicers and drill-through

The brief requires **slicers on at least two dimensions** and names
drill-through as an interactive element. This gives you three dimensions plus
drill-through.

## 10.1 Page slicers

| Page | Slicers |
| --- | --- |
| 1 | `Annual[year_number]`, `Sales[category_name]` |
| 2 | `Sales[year_number]`, `Sales[category_name]`, `Sales[state_name]` |
| 3 | `CustomerSegments[segment]`, `Sales[category_name]`, `Sales[year_number]` |

Style them all the same: Format → **Slicer settings → Style: Tile**, horizontal,
along the bottom of each page.

**The segment slicer on Page 3 is your live demonstration.** Selecting
*Thin-Margin Buyers* and watching the profit share collapse to 18.7% is the most
persuasive single interaction on the dashboard — Task 3.4 asks you to
demonstrate one live, and this is it.

## 10.2 Drill-through from Page 2 to Page 3

On **Page 3**, in the Visualizations pane, find the **Drill through** well at
the bottom. Drag `SubcategorySegments[sub_category_name]` into it.

Power BI adds a back-arrow button to Page 3 automatically.

Now right-click any bar on Page 2's sub-category chart → **Drill through → 3
Deep Dive**, and Page 3 opens filtered to that sub-category.

Test it on Printers before the defense. "Right-click Printers, drill through,
and here is everything about the sub-category that lost 136,865" is a strong
thirty seconds.

## 10.3 Cross-filtering

Leave it on — it is the default. Clicking a category in one visual filters the
others on the page. Mention it as an interactive element; it costs nothing.

---

# Part 11 — Titles, labels and source notes

The brief says *"All visuals must be properly titled, labeled, and sourced."*
This is part of the 30-point Design & Usability criterion, so do not skip it.

**Every visual needs a title.** Format → General → Title → On. Write what the
visual *shows*, not what it is: "Revenue per month by year", not "Bar chart".

**Axis labels on.** Format → X-axis → Title → On, same for Y-axis.

**One source note per page.** Insert → **Text box**, place it bottom-left, 9pt,
colour `7B8994`:

> Source: sales_trend database, 1,194 transaction lines, March 2020 – March 2025.
> Synthetic dataset — see Checkpoint 1.

**One page header per page.** Insert → Text box, top-left, 16pt bold, colour
`1F2933`, with the page name. Keeps the three pages looking like one artefact.

**Consistency check before you finish.** Same colour for Electronics on every
page. Same font everywhere. Same slicer style. A reader should not have to
relearn the layout on each page.

---

# Part 12 — Export

1. **File → Save as** → `Checkpoint_3_Dashboard.pbix` — this is the digital
   deliverable
2. **File → Export → Export to PDF** → all three pages — this is the printed
   deliverable
3. Take **screenshots of each page** for the written report and for the
   Checkpoint 4 integrated report, section 6
4. Walk the three pages once and check every KPI against the table in **Part 5**
   one final time

---

# Part 13 — Troubleshooting

In order of how often each happens.

**The line chart shows 59 months instead of 57.**
The `in_analysis_window = 1` filter is missing from that visual. Part 7.2.

**`Revenue per Month` is wrong by roughly a factor of 1.3.**
`Months Covered` is counting the wrong thing. It must be
`DISTINCTCOUNT(Sales[year_month])`, never a hard-coded 12.

**The date axis will not switch to Continuous.**
`month_start` imported as Text. Fix the type in Power Query (Part 2), not in the
visual.

**The segment table shows 802 customers, not 807.**
The relationship is on `customer_name`. Change it to `customer_id`. Part 3.

**Segment percentages do not add up to 100.**
The `ALL()` was dropped from the share measures, so the denominator is being
filtered along with the numerator. Part 4.

**Every number is several times too large.**
`Annual` or `Geography` got related to `Sales`. Delete the relationship — they
are pre-aggregated summary tables.

**`Gap to Peak %` always reads 0.**
`ALL ( Sales )` is missing from `Peak Revenue per Month`, so the year slicer is
moving the peak along with the current value.

**A visual says "can't determine relationships between fields".**
You have mixed fields from two unrelated tables in one visual. Either use one
table's fields, or relate them properly.

**The scatter on Page 3 shows one dot.**
`quantity` and `amount` are being aggregated. Set both to "Don't summarize" and
put `sale_id` in Values.

---

# Part 14 — Final checklist

Against the Checkpoint 3 rubric.

**Dashboard Design & Usability — 30 pts**

- Three pages, named and in order
- Every visual titled; axes labelled
- One colour per category, the same on all three pages
- Slicers work and are styled consistently
- Drill-through from Page 2 to Page 3 tested

**Data Accuracy — 25 pts**

- All five KPIs match the Part 5 table
- The trend chart is filtered to the 57-month window
- The segment table reads 146 / 311 / 350 and totals 807
- `months_covered` is visible in the year table

**Insights & Storytelling — 25 pts**

- Each page answers a stated question
- The negative results are on the dashboard, not hidden: geography at 28%
  spread, quantity against amount at r = 0.045
- The written discussion is **in the group's own words** — Section 3.2 of the
  brief, and worth saying twice

**Documentation — 20 pts**

- Blueprint wireframe printed (`docs/figures/cp3_fig3_wireframe.png`)
- Written report covering design decisions, insights and segmentation findings
- `.pbix` submitted digitally
- PDF of all three pages
- Signed Individual Contribution Form

## The standing constraint

Section 3.2 has not gone away. The measures, the segmentation and the figures in
this guide are computed output and tooling. **The reading of them has to be
yours** — every sentence of interpretation in the written report and every word
you say over the dashboard in the live presentation.
