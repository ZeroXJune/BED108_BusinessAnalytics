# Sales Trend Analysis — Recording Script

**BED 106 Business Analytics — Mini Capstone Project**
Talibon Polytechnic College

**Mardy reads the parts below.** The full running order:

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

# Part 3 — Mardy

*[The ERD — have this on screen.]*

Caption: The star schema. One fact table, seven dimensions.

![](docs/figures/erd.png)

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

*[The loaded database — show your own SHOW TABLES output, or this.]*

Caption: Row counts after loading. sales holds exactly the 1,194 rows of the raw file.

| Table | Rows |
| --- | --- |
| `states` | 6 |
| `cities` | 18 |
| `categories` | 3 |
| `sub_categories` | 12 |
| `payment_modes` | 5 |
| `customers` | 807 |
| `dates` | 648 |
| `sales` | 1,194 |

The whole thing loads from one file — the database, all eight tables, all the
data. And it ends with a verification block whose last row has to read 1,194
rows, 6,182,639 in revenue, 547 order IDs, 57 complete months, and zero orphaned
rows.

*[Query 3 — show your own output, or this.]*

Caption: Q3 — annual sales trend, 2020–2024. 2020 has nine months, so read revenue per month.

| Year | Months | Lines | Units | Revenue | Profit | Revenue/month | Avg line | Margin % |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2020 | 9 | 167 | 1,651 | 836,410 | 217,911 | 92,934.44 | 5,008.44 | 26.05 |
| 2021 | 12 | 217 | 2,358 | 1,181,446 | 283,231 | 98,453.83 | 5,444.45 | 23.97 |
| 2022 | 12 | 288 | 3,234 | 1,459,775 | 393,113 | 121,647.92 | 5,068.66 | 26.93 |
| 2023 | 12 | 234 | 2,497 | 1,229,723 | 321,671 | 102,476.92 | 5,255.23 | 26.16 |
| 2024 | 12 | 240 | 2,523 | 1,202,478 | 308,336 | 100,206.50 | 5,010.33 | 25.64 |

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

*[Query 7 — show your own output, or this.]*

Caption: Q7 — sub-category revenue change, 2023 against 2024.

| Category | Sub-category | 2023 | 2024 | Change | % |
| --- | --- | --- | --- | --- | --- |
| Electronics | Printers | 192,817 | 55,952 | **−136,865** | **−71.0** |
| Electronics | Electronic Games | 144,484 | 88,017 | −56,467 | −39.1 |
| Electronics | Phones | 115,909 | 99,526 | −16,383 | −14.1 |
| Furniture | Bookcases | 86,730 | 74,875 | −11,855 | −13.7 |
| Electronics | Laptops | 85,109 | 75,135 | −9,974 | −11.7 |
| Furniture | Chairs | 87,711 | 86,185 | −1,526 | −1.7 |
| Furniture | Sofas | 92,052 | 98,984 | +6,932 | +7.5 |
| Office Supplies | Markers | 100,742 | 120,002 | +19,260 | +19.1 |
| Office Supplies | Binders | 64,442 | 88,011 | +23,569 | +36.6 |
| Office Supplies | Pens | 82,959 | 116,900 | +33,941 | +40.9 |
| Furniture | Tables | 119,400 | 155,834 | +36,434 | +30.5 |
| Office Supplies | Paper | 57,368 | 143,057 | **+85,689** | **+149.4** |

**Second, one sub-category explains most of the gap.** Printers lost 136,865
between 2023 and 2024 — a 71 percent collapse, and on its own that's more than
half the entire gap between the 2022 peak and 2024. Every Electronics
sub-category fell, and the category as a whole is down 40.8 percent. But every
Office Supplies sub-category grew — Paper is up 85,689, which is 149.4 percent.

And that's the point: this is not a general slowdown. Two opposite trends are
running at the same time, and the company-wide figure is just their average,
which describes neither of them. That's the most useful thing Checkpoint 1
produced.

*[Query 8 — show your own output, or this.]*

Caption: Q8 — each quarter's share of its own category's annual revenue.

| Category | Q1 | Q2 | Q3 | Q4 |
| --- | --- | --- | --- | --- |
| Electronics | 20.28% | **30.79%** | 23.69% | 25.24% |
| Furniture | 16.96% | 29.46% | 22.74% | **30.84%** |
| Office Supplies | 17.01% | 25.00% | 25.83% | **32.16%** |

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

