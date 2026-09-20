# Checkpoint 4 — Capstone Analytics Project & Final Defense

**BED 106 Business Analytics — Mini Capstone Project**
Final Period · Weeks 14–18 · 100 Points

---

# Task 4.1 — Predictive Analytics Application

**Technique:** multiple linear regression, extending the simple regression from
Checkpoint 2. Computed by `scripts/build_predictive_model.py`; full output in
`reports/predictive_model_results.md`.

## The model

**Output variable:** monthly revenue.

**Predictors tested:** order count, units sold, distinct customers, Electronics
share of lines, a time index, and quarter indicators for Q2, Q3 and Q4.

The Electronics share is computed from *line counts*, not from revenue. A
revenue share would be derived from the target and would leak it back into the
model — a mistake that inflates R² while predicting nothing.

Three models were fitted on the same 57-month window Checkpoint 2 used, trained
on the first 51 months with the last six held out and never fitted.

| Model | Specification | R² | Adjusted R² |
| --- | --- | --- | --- |
| A | `revenue ~ orders` — the Checkpoint 2 baseline | 0.8562 | 0.8533 |
| B | all eight predictors | 0.8746 | **0.8507** |
| C | `orders + Q2 + Q3 + Q4 + elec_line_share` | 0.8695 | **0.8550** |

**Model B is the instructive failure.** Adding every predictor raised R² and
*lowered* adjusted R² below the one-variable baseline — the classic sign of
predictors bought with degrees of freedom rather than information. Its variance
inflation factors show why: orders at **13.67**, units at 7.64, customers at
5.48. Order count, units sold and customer count are 0.81 to 0.92 correlated
with each other, because they all measure the same thing — how much trade
happened. Fitting them together makes each coefficient unstable and
uninterpretable. Dropping units and customers brings every VIF in Model C under
1.8.

## The reported model

Model C, refitted on all 57 months once the holdout had done its job of
choosing the specification:

> **Monthly Revenue = −12,275.79 + 5,219.51 × Orders + 11,382.65 × Q2
> + 9,624.56 × Q3 + 5,989.42 × Q4 + 12,091.77 × Electronics line share**

| Term | Coefficient | Robust SE | Robust p |
| --- | --- | --- | --- |
| Intercept | −12,275.79 | 9,775.60 | 0.215 |
| **Orders** | **5,219.51** | 388.49 | **2.21 × 10⁻¹⁸** |
| **Q2** | **11,382.65** | 5,484.91 | **0.043** |
| Q3 | 9,624.56 | 5,455.74 | 0.084 |
| Q4 | 5,989.42 | 6,199.18 | 0.339 |
| Electronics line share | 12,091.77 | 16,873.75 | 0.477 |

R² = 0.8647, adjusted R² = 0.8514, n = 57.

**On the standard errors.** The Breusch-Pagan test rejects constant variance
(p = 0.0023), so the classical standard errors are unreliable and
heteroscedasticity-consistent (HC1) errors are reported instead. This is not
cosmetic: under classical errors Q2 sits at p = 0.062 and is not significant;
under robust errors it is p = 0.043 and is. Both are close enough to 0.05 that
the honest statement is "Q2 is marginally significant", not "Q2 is significant".

**The slope is the same number three times over.** 5,219.51 here, 5,224.25 in
the Checkpoint 2 simple regression, and 5,178.09 as the plain mean order value
in the data. Three routes, agreeing within 0.8%.

## Model performance

Evaluated on six months the models never saw (July to December 2024):

| Model | Mean absolute percentage error |
| --- | --- |
| A — orders only | **9.3%** |
| C — reduced multiple | 9.8% |

**The multiple regression did not beat the simple one out of sample.** We are
reporting that rather than burying it, and it is the second time in this
project that a more elaborate method lost to a simpler one — the Checkpoint 2
seasonal forecast lost to a flat average by 22.7% against 14.9%.

Both models missed December 2024 badly, predicting about 130,000 against an
actual 98,879, a 32% error. Every earlier December in the window was strong;
this one was not. That single month accounts for most of the gap between the
two models' scores.

**What the extension is worth is diagnostic, not predictive.** Model C's real
output is the finding that **order count is the only driver that matters**.
Units sold, customer count, product mix and elapsed time were each given a
fair chance to explain monthly revenue alongside it, and none of them did.
That is exactly the evidence needed to justify the Checkpoint 3 dashboard's
central design decision.

## Business predictions

At the mean Electronics line share, holding everything else at the model:

| Orders per month | Q1 | Q2 | Q4 |
| --- | --- | --- | --- |
| 20 — the 2024 level | 96,027 | 107,410 | 102,017 |
| 22 | 106,466 | 117,849 | 112,456 |
| 24 — the 2022 peak level | 116,905 | **128,288** | 122,895 |

## Recommendations

**One — the only lever that moves revenue is order count, so target it
directly.** Each additional order in a month is worth about 5,220 in revenue
(robust p = 2.21 × 10⁻¹⁸). The company is running four orders per month below
its 2022 level; closing that gap is worth roughly **250,000 a year**, which
corroborates the 257,297 shortfall Checkpoint 1 measured by summing category
losses. Two independent methods, within 3% of each other.

**Two — stop setting volume and acquisition targets.** Units sold (p = 0.79)
and distinct customers (p = 0.27) add nothing once order count is in the model.
A "sell more units" or "sign more customers" incentive would not move revenue
in this business, and the data says so directly rather than by inference.

**Three — plan for a Q2 uplift, not only a Q4 one.** Q2 runs about 11,400 above
an equivalent Q1 month at the same order count, and it is the only quarter
indicator that reaches significance. This confirms from a second direction what
Checkpoint 1 found by category: Electronics peaks in Q2 at 30.79% of its annual
revenue while the blended company curve points at Q4. Staffing and inventory
planned on the blended curve are mistimed for a third of the business.

**Four — do not expect a forecast to do the work.** Neither model predicts
within better than 9% on unseen months, and both missed December 2024 by 32%.
Use the model to size the value of a decision, not to promise a number.

## Assumptions, limitations and conditions

| Assumption | Test | Result |
| --- | --- | --- |
| Linearity | Residuals against fitted | No pattern |
| Independence of errors | Durbin-Watson | 2.078 — no autocorrelation |
| Normality of residuals | Shapiro-Wilk | p = 0.86 — passes |
| Constant variance | Breusch-Pagan | **p = 0.0023 — fails**; robust SEs used |
| No multicollinearity | VIF | Fails in Model B (13.67); Model C all under 1.8 |

Six further conditions on any use of this model:

- **57 monthly observations is not many** for five predictors. Adjusted R² and
  the holdout are reported precisely because plain R² would flatter it.
- **Do not extrapolate beyond the observed range.** Order counts run from 9 to
  45 per month and revenue from 22,187 to 204,413. The model says nothing
  outside that.
- **The intercept is not meaningful.** Zero orders cannot produce −12,276 in
  revenue; it is where the plane crosses the axis, far outside the data.
- **Association, not causation.** Orders and revenue move together over 57
  months. Nothing here shows that generating an order causes the revenue, as
  opposed to both responding to demand we cannot observe.
- **The dataset is synthetic**, so these coefficients describe a generated
  file. The method transfers to real data; the numbers do not.
- **Transactions only.** The file records sales that happened, never a customer
  who considered a purchase and did not make one, so the model cannot see
  demand that was lost.

---

# Task 4.2 — Data Ethics, Privacy & Governance

Written up in full at `docs/checkpoint4_ethics.md` (`Checkpoint_4_Ethics.docx`),
1,153 words against the 500-word minimum, covering all four required areas.

The argument in brief:

- **Privacy.** The names are synthetic, so there is no data subject and R.A.
  10173 is not engaged. The reason matters: not that the file is public, but
  that the people in it do not exist. **Public availability is not consent.**
- **Ethics.** The sharpest issue is our own Checkpoint 3 segmentation. Labelling
  350 customers "Thin-Margin Buyers" is accurate and commercially useful, and
  on real data it is a mechanism by which poorer customers could be served
  worse. Also covered: survivorship bias, and why we documented the `Order ID`
  defect instead of fabricating a repair.
- **Governance.** Four requirements — a named owner for the customer dimension,
  analysts working against pseudonymised views, a retention rule (every finding
  except the customer segmentation survives deleting every name), and the
  lineage this project already has.
- **Regulation.** R.A. 10173 in detail, with proportionality, purpose
  specification and the right to object applied to this analysis; GDPR Article
  22 on automated decisions, and where our clustering would cross that line.

---

# Task 4.3 — Integrated Capstone Report

The brief specifies eleven sections. Most already exist.

| # | Section | Source | Status |
| --- | --- | --- | --- |
| 1 | Title page | Checkpoint reports | **ACTION: fill the blanks** |
| 2 | Executive summary | — | **ACTION: write, 1 page** |
| 3 | Business problem & data source | CP1 report, Tasks 1.1–1.2 | Ready, refine |
| 4 | Database design & SQL analysis | CP1 report, Tasks 1.3–1.4 | Ready — 8 tables, 8 queries, all results |
| 5 | Statistical analysis | CP2 report | Ready |
| 6 | BI dashboard summary | CP3 | **ACTION: screenshots once built** |
| 7 | Predictive analytics | Task 4.1 above | Ready |
| 8 | Ethics & governance | `checkpoint4_ethics.md` | Ready |
| 9 | Conclusions & recommendations | Below | Ready, 3–5 required |
| 10 | References | — | **ACTION: APA format** |
| 11 | Appendix | Form A, raw sample, Form B | Forms ready — **ACTION: sign them** |

### The 3–5 actionable recommendations for section 9

1. **Track order count as the primary KPI.** It explains 85% of revenue
   variation and is the only predictor that survives a multiple regression.
2. **Investigate Printers first.** One sub-category lost 136,865 between 2023
   and 2024 — over half the entire peak-to-2024 gap.
3. **Plan seasonality by category.** Electronics peaks in Q2, Furniture and
   Office Supplies in Q4; the blended curve is wrong for all three.
4. **Segment on margin, not revenue.** Thin-Margin Buyers are 43% of customers
   and a third of revenue, and return 19% of profit.
5. **Do not set volume or acquisition targets.** Units sold and customer count
   add nothing to revenue prediction once orders are accounted for.

---

# Task 4.4 — Final Presentation & Defense

20–25 minutes, Weeks 16–18, all members speaking.

| Segment | Time | Material |
| --- | --- | --- |
| Introduction & business context | 2–3 min | Discussion script, Part 1 |
| Data & SQL overview | 3–4 min | ERD, plus Q3, Q7 and Q8 |
| Statistical insights | 3–4 min | CP2 descriptive stats and regression |
| Live dashboard demo | 5–6 min | **ACTION: the .pbix, with the segment slicer** |
| Predictive analytics & recommendations | 4–5 min | Task 4.1 above |
| Ethics & governance | 1–2 min | Task 4.2 summary |
| Open defense / Q&A | 5 min | Defence questions in `project_explained.md`, Part 5 |

`docs/discussion_script.md` already covers the first three segments and the
recommendations as spoken lines and can be extended for the last three.

**The deck is built**: `reports/Capstone_Defense_Deck.pptx`, 23 slides mapped
to the seven segments, with speaker notes on every slide. Two things to do to
it before the defense — replace the wireframe on the demo slide with a
screenshot of the finished dashboard, and fill the group number on the title
slide. Rebuild with `node scripts/build_deck.js` after editing the generator
rather than editing the file by hand, or the two will drift.

### The four questions most likely to be asked

**"Your multiple regression performed worse than your simple one. Why present
it?"** Because that is the result. Its value is diagnostic: it rules out units,
customers, mix and time as drivers, which is what justifies building the
dashboard on order count.

**"Your dataset is fake. What is the project worth?"** The figures illustrate a
method rather than describe a company. Every query, statistic and model would
run identically on a real export. We proved the file was synthetic rather than
discovering it late, and we did not fabricate corrections.

**"Why three clusters and not five?"** k=5 does score higher on silhouette,
0.295 against 0.277. Two of its five clusters came out with the same profile,
and the brief asks for two or three. The full scan is in the Checkpoint 3 spec.

**"What would you do differently?"** Check the completeness of both ends of the
date range before building on it. That is what caused the one real error in
this project — treating a nine-month 2020 as a full year, which overstated
growth as 69.9% when it is 30.9%.

---

## Rubric map

| Criterion | Points | Where |
| --- | --- | --- |
| Business problem & scope | 15 | CP1 Task 1.1, carried consistently through every checkpoint |
| Analysis & predictive technique | 25 | Task 4.1 above, with model evaluation, VIF, robust SEs and diagnostics; ethics in Task 4.2 |
| Dashboard / report quality | 25 | **ACTION: integrate the 11 sections; dashboard screenshots** |
| Presentation & defense | 20 | **ACTION: present** |
| Documentation & peer eval | 15 | Form A ready; **ACTION: peer evaluation forms, APA references** |

### Submission checklist

Taken from the brief's Checkpoint 4 submission requirements, in its order.

| Deliverable | Status |
| --- | --- |
| Final capstone report — spiral-bound hardcopy **and** digital PDF | **ACTION: integrate the 11 sections** |
| All digital files in one organised folder: SQL, Excel, Power BI, datasets | Everything exists except the `.pbix` — see below |
| Presentation slide deck, `.pptx` or `.pdf` | `reports/Capstone_Defense_Deck.pptx` — 23 slides, **ACTION: swap the wireframe on the demo slide for a dashboard screenshot** |
| Peer Evaluation Forms, one per member, signed | `reports/Form_B_Peer_Evaluation.docx` — three copies, **ACTION: sign** |
| Individual Contribution Forms for **all four** checkpoints | `reports/Form_A_Individual_Contribution.docx` — twelve copies, **ACTION: sign** |
| Due: beginning of Week 16, before defense schedules begin | — |

**What goes in the digital folder.** The brief asks for one organised folder
containing the SQL, the Excel, the Power BI file and the datasets:

| Folder | From this repository |
| --- | --- |
| `sql/` | `01_schema_mysql.sql`, `02_mysql_full_import.sql`, `04_queries.sql`, `06_dashboard_views.sql` |
| `excel/` | `reports/Checkpoint_2_Workbook.xlsx` — the Checkpoint 2 deliverable, unchanged |
| `powerbi/` | `Checkpoint_3_Dashboard.pbix` and its exported PDF — **ACTION** |
| `data/` | `data/raw/sales_dataset_raw.csv` and `data/dashboard/*.csv` |
| `reports/` | All four checkpoint reports as PDF |

The Excel workbook is Checkpoint 2's and needs no changes for Checkpoint 4 —
it is included because the brief asks for all digital files together, not
because anything new is required of it.

- Defense scheduled, Weeks 16–18

### And the standing constraint

Section 3.2 still applies to every word of the integrated report. The model
output, the diagnostics and the coefficients are computed; the reading of them
must be the group's own.
