# Checkpoint 2 — Excel Guide

Practical notes for working with `reports/Checkpoint_2_Workbook.xlsx`.

---

## 1. First thing to do: open it and check the Read Me sheet

The workbook was built on Linux with `openpyxl`, which writes formulas but
does not calculate them. **Excel recalculates everything the moment you open
the file.**

The **Read Me** sheet ends with a *Self-check* block of seven rows. Every one
must read **OK**:

| Check | Expected |
| --- | --- |
| Pivot 1 grand total equals SUM of all Amount | OK |
| Pivot 2 order count equals COUNT of all rows | OK |
| Pivot 2 revenue equals SUM of all Amount | OK |
| Pivot 3 order count equals COUNT of all rows | OK |
| Pivot 3 revenue equals SUM of all Amount | OK |
| Regression sample is 57 complete months | OK |
| Cleaned Data holds 1,194 transaction lines | OK |

Each one recomputes a total two independent ways and compares them. If any row
says **CHECK**, something did not evaluate — do not submit until it is
resolved.

Also scan for `#NAME?`, `#REF!` or `#VALUE!` anywhere. There should be none:
every formula uses functions available in Excel 2007 and later, and the
workbook deliberately avoids newer array functions such as `XLOOKUP`,
`FILTER` and `TEXTJOIN`, which do not survive this build path.

> **Why the workbook was not pre-calculated.** LibreOffice, the tool normally
> used to recalculate a generated workbook, cannot load documents in the build
> environment. The formula ranges were verified programmatically instead, and
> the self-check block was added so the workbook proves itself the first time
> it is opened in Excel.

---

## 2. PivotTables — both kinds are already in the workbook

The workbook now contains **both** forms, so whichever reading of the brief
your instructor takes is covered:

| Where | What | Why it is there |
| --- | --- | --- |
| **Pivot Analysis** | Four SUMIFS / COUNTIFS / AVERAGEIFS cross-tabs | Auditable cell by cell — click any cell and read the logic |
| **PivotTable 1–3** | Three native Excel PivotTable objects | The PivotTable object itself, with the Fields pane and drag-and-drop |

The three native PivotTables, each with a **PivotChart** beside it:

| Sheet | Rows | Columns | Values | Chart |
| --- | --- | --- | --- | --- |
| PivotTable 1 | Category | Year | Sum of Amount | Clustered column |
| PivotTable 2 | State | — | Average of Amount | Column |
| PivotTable 3 | YearMonth | — | Count of SaleID | Line |

A PivotChart is not an ordinary chart: it is bound to its PivotTable, refreshes
with it, and shows field buttons you can filter from.

All three read from `Cleaned Data!A1:S1195` through one shared pivot cache,
exactly as Excel does when you build several PivotTables from one range.

**They populate when you open the file.** The cache is marked *refresh on
load*, because the builder writes the PivotTable definition but cannot compute
its cached values outside Excel. If one ever looks empty, click inside it and
use **PivotTable Analyze → Refresh**.

> **Do not rename this file.** A PivotChart stores its source as
> `[filename]Sheet!PivotName`, so the three PivotCharts are tied to the name
> **`Checkpoint_2_Workbook.xlsx`**. If your group needs to submit under a
> different name, ask for the workbook to be regenerated under that name
> rather than renaming it afterwards. The PivotTables themselves and the four
> charts on *Pivot Charts* are unaffected by renaming.

> **Check this on first open.** The PivotTables and PivotCharts were written by
> a library, not by Excel, and could not be opened in Excel during the build.
> They should appear populated. If Excel instead offers to "repair" the file,
> say yes, tell me, and use the *Pivot Analysis* cross-tabs and the *Pivot
> Charts* sheet — both are unaffected and satisfy the same requirement.

### Building more of your own

If you want additional PivotTables, each takes about two minutes.

#### Example — total revenue by category

1. Click any cell in the **Cleaned Data** sheet.
2. **Insert → PivotTable → New Worksheet → OK**.
3. Drag **Category** to *Rows*.
4. Drag **Amount** to *Values*. It should read "Sum of Amount"; if it says
   "Count of", click it → *Value Field Settings* → **Sum**.
5. Drag **Year** to *Columns*.
6. Rename the sheet `PivotTable 1`.

#### Example — average order value by region

Same steps, then: **State** to *Rows*, **Amount** to *Values*, and set the
value field to **Average** rather than Sum.

#### Example — count of orders by period

**YearMonth** to *Rows*, **SaleID** to *Values*, value field set to **Count**.

#### Turning a PivotTable into a PivotChart

Click inside the PivotTable → **Insert → PivotChart** → choose Column for
categories or Line for the monthly series. Then add a chart title and axis
titles: **Chart Design → Add Chart Element**. The rubric explicitly asks for
titles, axis labels and business annotations, and it is the easiest place to
lose marks.

---

## 3. Running the regression through the Data Analysis ToolPak

The **Regression** sheet computes everything with individual functions
(`SLOPE`, `INTERCEPT`, `RSQ`, `STEYX`, `DEVSQ`, `TDIST`), which shows the
working. The brief mentions the ToolPak, so here is how to produce its output
as well.

**Enabling it:** *File → Options → Add-ins → Manage: Excel Add-ins → Go →*
tick **Analysis ToolPak**. On Mac: *Tools → Excel Add-ins*.

**Running it:**

1. **Data → Data Analysis → Regression**.
2. *Input Y Range*: the monthly revenue column on **Pivot Analysis**, rows 27
   to 83 (column C) — these are the 57 complete months.
3. *Input X Range*: the orders column, same rows (column B).
4. Tick **Labels** only if you include the header row — easier not to.
5. *Output Range*: any empty cell on a new sheet.
6. OK.

**Reading the output**, and where each number matches this workbook:

| ToolPak label | Value | Where it appears here |
| --- | --- | --- |
| Multiple R | 0.9227 | Correlation r |
| R Square | 0.8514 | R squared |
| Standard Error | 15,099.14 | Standard error of estimate |
| Observations | 57 | Sample size n |
| Intercept → Coefficient | −1,353.65 | Intercept (a) |
| X Variable 1 → Coefficient | 5,224.25 | Slope (b) |
| X Variable 1 → t Stat | 17.75 | t statistic |
| X Variable 1 → P-value | 1.98 × 10⁻²⁴ | p-value |

If your numbers differ, the usual cause is including rows 26 or 84–86 —
March 2020 and the 2025 months, which are partial and excluded by design.

---

## 4. Why the analysis uses 57 months, not 61

The file runs **22 March 2020 to 15 March 2025**. Three windows are excluded:

- **March 2020** — only 10 days of trading. A part-month in a monthly average
  drags that month's seasonal index down by 15%.
- **March 2025** — only 15 days, same problem.
- **April 2020 to December 2024** is therefore the analysis window: **57 whole
  months**.
- **January and February 2025** are complete months but fall in a partial year.
  They are deliberately held back and used only to check the forecast.

On Pivot 3, the helper columns (`t index`, `Month no`) start at row 27, not
row 26, for exactly this reason.

---

## 5. If you edit the data

Everything downstream is formula-driven, so edits flow through automatically —
with two exceptions to watch:

1. **Adding rows to Cleaned Data.** The named ranges (`Amount`, `Profit`,
   `Quantity`, `Category`, `State`, `Yr`, `YearMonth`, `SubCategory`,
   `PaymentMode`) are fixed at rows 2–1195. New rows below that are invisible
   to every formula. Extend the ranges via *Formulas → Name Manager*.
2. **Adding months.** The helper columns and the `Tindex`, `MonthNumber`,
   `MonthRevenue` and `MonthOrders` ranges cover rows 27–83. A new month needs
   those extended too, or the regression will silently ignore it.

The safer route is to change the source data and re-run
`python3 scripts/build_workbook.py`, which rebuilds the workbook with correct
ranges.
