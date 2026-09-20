/*
 * Builds the Checkpoint 4 final defense slide deck.
 *
 * Structure follows Task 4.4 of the BED 106 brief exactly: seven segments
 * across 20-25 minutes, with the live dashboard demo in the middle.
 *
 * Every figure on these slides is verified against reports/ — the charts are
 * built from the same numbers the reports publish, not retyped from memory.
 *
 * Run:  node scripts/build_deck.js   ->  reports/Capstone_Defense_Deck.pptx
 */

const fs = require("fs");
const path = require("path");
const PptxGenJS = require("pptxgenjs");

const ROOT = path.dirname(__dirname);
const FIG = path.join(ROOT, "docs", "figures");
const OUT = path.join(ROOT, "reports", "Capstone_Defense_Deck.pptx");

/* The project's own figure palette, so slides and embedded charts match. */
const INK = "1F2933";
const BLUE = "2F6F9F";
const RED = "C1666B";
const GREEN = "5B8C5A";
const AMBER = "D09B3E";
const MUTED = "7B8994";
const PALE = "EEF3F7";
const WHITE = "FFFFFF";

const HEAD = "Cambria";
const BODY = "Calibri";

const W = 13.333;
const H = 7.5;
const M = 0.7;                 /* side margin */

const pres = new PptxGenJS();
pres.layout = "LAYOUT_WIDE";
pres.author = "BED 106 Capstone Group";
pres.title = "Sales Trend Analysis — Final Defense";

/* ------------------------------------------------------------------ parts */

function darkSlide() {
  const s = pres.addSlide();
  s.background = { color: INK };
  return s;
}

function lightSlide(title, kicker) {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  if (kicker) {
    s.addText(kicker.toUpperCase(), {
      x: M, y: 0.42, w: W - 2 * M, h: 0.28, isTextBox: true, margin: 0,
      fontFace: BODY, fontSize: 11, bold: true, color: BLUE, charSpacing: 1.6
    });
  }
  s.addText(title, {
    x: M, y: kicker ? 0.72 : 0.55, w: W - 2 * M, h: 0.78, isTextBox: true,
    margin: 0, fontFace: HEAD, fontSize: 32, bold: true, color: INK
  });
  return s;
}

/* A big number with a label under it. */
function stat(s, x, y, value, label, color, w) {
  s.addText(value, {
    x, y, w: w || 3.0, h: 0.85, isTextBox: true, margin: 0,
    fontFace: HEAD, fontSize: 40, bold: true, color: color || INK
  });
  s.addText(label, {
    x, y: y + 0.82, w: w || 3.0, h: 0.44, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 12, color: MUTED
  });
}

/* A tinted card. No edge stripes - a background tint sets it apart. */
function card(s, x, y, w, h, fill) {
  s.addShape(pres.ShapeType.roundRect, {
    x, y, w, h, rectRadius: 0.08,
    fill: { color: fill || PALE }, line: { color: fill || PALE, width: 0 }
  });
}

/* A numbered chip, the deck's one repeated motif. */
function chip(s, x, y, n, color) {
  s.addShape(pres.ShapeType.ellipse, {
    x, y, w: 0.46, h: 0.46,
    fill: { color: color || BLUE }, line: { color: color || BLUE, width: 0 }
  });
  s.addText(String(n), {
    x, y, w: 0.46, h: 0.46, isTextBox: true, margin: 0,
    align: "center", valign: "middle",
    fontFace: HEAD, fontSize: 16, bold: true, color: WHITE
  });
}

function source(s, text) {
  s.addText(text, {
    x: M, y: H - 0.62, w: W - 2 * M, h: 0.3, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 9, italic: true, color: MUTED
  });
}

const CHART_BASE = () => ({
  chartColors: [BLUE, RED, GREEN, AMBER],
  showLegend: false,
  catAxisLabelColor: MUTED, valAxisLabelColor: MUTED,
  catAxisLabelFontFace: BODY, valAxisLabelFontFace: BODY,
  catAxisLabelFontSize: 11, valAxisLabelFontSize: 11,
  valGridLine: { color: "E4EAEF", size: 1 },
  catGridLine: { style: "none" },
  dataLabelFontFace: BODY, dataLabelFontSize: 10, dataLabelColor: INK
});

/* ----------------------------------------------------------------- slides */

/* 1 — title */
{
  const s = darkSlide();
  s.addText("Sales Trend Analysis", {
    x: M, y: 2.25, w: 9.6, h: 1.0, isTextBox: true, margin: 0,
    fontFace: HEAD, fontSize: 48, bold: true, color: WHITE
  });
  s.addText("Why a growing retailer stopped growing — and what the data says to do about it", {
    x: M, y: 3.32, w: 9.6, h: 0.7, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 17, color: "CADCFC"
  });
  s.addText([
    { text: "BED 106 — Business Analytics · Mini Capstone Project", options: { breakLine: true } },
    { text: "Talibon Polytechnic College · A.Y. 2026–2027, 1st Semester", options: { breakLine: true } },
    { text: "Alber · Julebeth · Mardy", options: {} }
  ], {
    x: M, y: 4.6, w: 9.6, h: 1.1, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 13, color: MUTED, lineSpacing: 20
  });
  s.addText("Final Defense", {
    x: W - M - 2.6, y: 6.25, w: 2.6, h: 0.4, isTextBox: true, margin: 0,
    align: "right", fontFace: BODY, fontSize: 12, bold: true, color: AMBER
  });
  s.addNotes("Good day. We are presenting our BED 106 mini capstone on sales trend analysis. Introduce the three of you by name, then go straight into the problem.");
}

/* 2 — agenda */
{
  const s = lightSlide("What we will cover", "Agenda · 20–25 minutes");
  const items = [
    ["Introduction & business context", "2–3 min"],
    ["Data & SQL overview", "3–4 min"],
    ["Statistical insights", "3–4 min"],
    ["Live dashboard demo", "5–6 min"],
    ["Predictive analytics & recommendations", "4–5 min"],
    ["Ethics & governance", "1–2 min"],
    ["Open defense / Q&A", "5 min"]
  ];
  items.forEach(([label, mins], i) => {
    const y = 1.82 + i * 0.68;
    chip(s, M, y, i + 1, i === 3 ? AMBER : BLUE);
    s.addText(label, {
      x: M + 0.72, y: y + 0.02, w: 7.0, h: 0.42, isTextBox: true, margin: 0,
      valign: "middle", fontFace: BODY, fontSize: 15,
      bold: i === 3, color: INK
    });
    s.addText(mins, {
      x: M + 7.8, y: y + 0.02, w: 1.0, h: 0.42, isTextBox: true, margin: 0,
      valign: "middle", fontFace: BODY, fontSize: 12, color: MUTED
    });
  });
  card(s, W - M - 2.9, 1.82, 2.9, 4.4, PALE);
  s.addText([
    { text: "Two checkpoints of analysis\n", options: { bold: true, breakLine: true } },
    { text: "1,194 transaction lines\nMarch 2020 – March 2025\n8 tables · 8 SQL queries\n57 months modelled", options: {} }
  ], {
    x: W - M - 2.55, y: 2.15, w: 2.2, h: 2.4, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 12.5, color: INK, lineSpacing: 22
  });
  s.addNotes("Keep this short — name the seven segments, flag that segment four is a live demo, and move on.");
}

/* 3 — the problem */
{
  const s = lightSlide("The company grew, then stopped", "1 · Business context");
  s.addText([
    { text: "A multi-category retailer — electronics, furniture, office supplies — trading across six US states.", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "On a like-for-like monthly basis revenue rose to a 2022 peak, then fell two years running.", options: {} }
  ], {
    x: M, y: 1.75, w: 5.6, h: 1.5, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 14.5, color: INK, lineSpacing: 22
  });

  stat(s, M, 3.4, "+30.9%", "2020 → 2022 peak", GREEN, 2.6);
  stat(s, M + 2.9, 3.4, "−17.6%", "2022 peak → 2024", RED, 2.6);

  card(s, 6.9, 1.68, W - M - 6.9, 3.9, PALE);
  s.addText("So why does a falling sales figure need a database?", {
    x: 7.25, y: 1.98, w: 5.1, h: 0.85, isTextBox: true, margin: 0,
    fontFace: HEAD, fontSize: 17, bold: true, color: INK
  });
  s.addText([
    { text: "Because of what didn't move.", options: { bold: true, breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "Margin held between 23.97% and 26.93% for five years. Average order value stayed between 5,008 and 5,444.", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "Had margin collapsed, the answer would be \"we discounted too hard\". It didn't. The company is writing fewer orders, not worse ones.", options: {} }
  ], {
    x: 7.25, y: 2.95, w: 5.1, h: 2.5, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 13.5, color: INK, lineSpacing: 21
  });
  source(s, "Source: sales_trend database, Query 3. Synthetic dataset — see Checkpoint 1.");
  s.addNotes("This is the slide that frames everything. Stress the margin point: it is what turns 'sales fell' into a question worth a database.");
}

/* 4 — three questions */
{
  const s = lightSlide("Three questions, and every deliverable maps to one", "1 · Business context");
  const qs = [
    ["How have revenue and profit trended, and is the company still growing?", "Query 3 · CP2 regression"],
    ["Which categories and sub-categories drive the trend?", "Queries 5 and 7"],
    ["When does demand concentrate, and is it the same for every category?", "Queries 4 and 8"]
  ];
  qs.forEach(([q, src], i) => {
    const y = 1.95 + i * 1.5;
    card(s, M, y, W - 2 * M, 1.22, PALE);
    chip(s, M + 0.35, y + 0.38, i + 1, BLUE);
    s.addText(q, {
      x: M + 1.05, y: y + 0.22, w: 8.2, h: 0.5, isTextBox: true, margin: 0,
      fontFace: BODY, fontSize: 15, bold: true, color: INK
    });
    s.addText("Answered by " + src, {
      x: M + 1.05, y: y + 0.7, w: 8.2, h: 0.35, isTextBox: true, margin: 0,
      fontFace: BODY, fontSize: 11.5, color: MUTED
    });
  });
  s.addText("What hangs on them: what to stock, when to stock it, where to put the sales effort.", {
    x: M, y: 6.45, w: W - 2 * M, h: 0.4, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 13, italic: true, color: INK
  });
  s.addNotes("Read the three questions, then the one-line consequence. Do not linger.");
}

/* 5 — divider */
{
  const s = darkSlide();
  chip(s, M, 2.9, 2, AMBER);
  s.addText("Data & SQL", {
    x: M, y: 3.5, w: 9, h: 0.95, isTextBox: true, margin: 0,
    fontFace: HEAD, fontSize: 40, bold: true, color: WHITE
  });
  s.addText("What the raw file was, what was wrong with it, and what the database found", {
    x: M, y: 4.45, w: 9.5, h: 0.5, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 15, color: "CADCFC"
  });
  s.addNotes("Hand over to whoever takes the data segment.");
}

/* 6 — dataset and defects */
{
  const s = lightSlide("Five things were wrong with the raw file", "2 · Data & SQL");
  const defects = [
    ["Order ID is not a primary key", "1,194 rows, 547 distinct IDs — repeats span different dates and customers"],
    ["Customer name is not an identifier", "807 customers from 802 names; five names appear in two cities"],
    ["Year-Month is redundant", "Derivable from the date — rebuilt in a dates table"],
    ["Both ends of the file are partial", "Starts 22 March 2020, stops 15 March 2025"],
    ["The dataset is synthetic", "Five machine-checked signals — we say so rather than bury it"]
  ];
  defects.forEach(([t, d], i) => {
    const y = 1.78 + i * 0.94;
    chip(s, M, y, i + 1, i === 4 ? RED : BLUE);
    s.addText(t, {
      x: M + 0.72, y: y - 0.02, w: 5.9, h: 0.38, isTextBox: true, margin: 0,
      fontFace: BODY, fontSize: 14.5, bold: true, color: INK
    });
    s.addText(d, {
      x: M + 0.72, y: y + 0.34, w: 6.1, h: 0.42, isTextBox: true, margin: 0,
      fontFace: BODY, fontSize: 11.5, color: MUTED
    });
  });
  card(s, 8.3, 1.72, W - M - 8.3, 4.5, PALE);
  s.addText("We fixed none of it.", {
    x: 8.65, y: 2.05, w: 3.6, h: 0.45, isTextBox: true, margin: 0,
    fontFace: HEAD, fontSize: 18, bold: true, color: RED
  });
  s.addText([
    { text: "Repairing Order ID means deciding which of two conflicting rows is real, with no evidence for the decision.", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "That is data fabrication, which the brief says is grounds for a failing mark.", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "So we documented every defect and worked around it. The method is unaffected.", options: {} }
  ], {
    x: 8.65, y: 2.65, w: 3.6, h: 3.3, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 12.5, color: INK, lineSpacing: 19
  });
  s.addNotes("The synthetic-data point must be said out loud here, before anyone asks. Five signals: no loss-making line in five years; 22 names with credential suffixes; US cities with Indian payment rails; near-uniform payment mix; a flat amount histogram.");
}

/* 7 — the database */
{
  const s = lightSlide("A star schema, eight tables", "2 · Data & SQL");
  s.addImage({ path: path.join(FIG, "erd.png"), x: M, y: 1.68, w: 8.0, h: 4.4, sizing: { type: "contain", w: 8.0, h: 4.4 } });
  card(s, 9.0, 1.68, W - M - 9.0, 4.4, PALE);
  s.addText([
    { text: "8 tables\n", options: { bold: true, breakLine: true } },
    { text: "1 fact, 7 dimensions\n\n", options: { breakLine: true } },
    { text: "8 primary keys\n7 foreign keys\n6 unique constraints\n4 check constraints\n\n", options: { breakLine: true } },
    { text: "Tested to reject bad rows, not assumed to.", options: { italic: true } }
  ], {
    x: 9.3, y: 2.0, w: 3.3, h: 3.6, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 13, color: INK, lineSpacing: 20
  });
  source(s, "Figure: Entity-Relationship Diagram of the sales_trend database.");
  s.addNotes("Three reasons for the star: consistency, the brief asks for it, and the queries need category and date on the same row as the amount. Mention the reserved-word trap: year_month broke CREATE TABLE in MySQL until backticked.");
}

/* 8 — finding 1 */
{
  const s = lightSlide("Growth stopped in 2022 — and in a specific way", "2 · Data & SQL · Finding 1");
  const opts = Object.assign(CHART_BASE(), {
    showTitle: false, showValue: true, dataLabelPosition: "outEnd",
    dataLabelFormatCode: "#,##0", valAxisMaxVal: 140000, barGapWidthPct: 60
  });
  s.addChart(pres.ChartType.bar, [{
    name: "Revenue per month",
    labels: ["2020", "2021", "2022", "2023", "2024"],
    values: [92934, 98454, 121648, 102477, 100207]
  }], Object.assign(opts, { x: M, y: 1.75, w: 7.5, h: 4.1 }));

  card(s, 8.6, 1.75, W - M - 8.6, 4.1, PALE);
  s.addText("Measured per month", {
    x: 8.95, y: 2.05, w: 3.4, h: 0.4, isTextBox: true, margin: 0,
    fontFace: HEAD, fontSize: 16, bold: true, color: INK
  });
  s.addText([
    { text: "2020 holds nine months. Comparing its part-year total against a full 2021 was the one real error we made, and corrected.", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "Margin never left 24–27%. Average order value never left 5,008–5,444.", options: { bold: true, breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "Fewer orders — not cheaper ones. That points at demand generation, not pricing.", options: {} }
  ], {
    x: 8.95, y: 2.55, w: 3.4, h: 3.1, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 12.5, color: INK, lineSpacing: 19
  });
  source(s, "Source: Query 3, revenue per month by year. 2020 = 9 complete months.");
  s.addNotes("The correction belongs here: we reported 69.9% growth in Checkpoint 1 and the like-for-like figure is 30.9%. Volunteer it.");
}

/* 9 — finding 2 */
{
  const s = lightSlide("One sub-category explains most of the gap", "2 · Data & SQL · Finding 2");
  const labels = ["Printers", "Elec. Games", "Phones", "Bookcases", "Laptops", "Chairs",
                  "Sofas", "Markers", "Binders", "Pens", "Tables", "Paper"];
  const values = [-136865, -56467, -16383, -11855, -9974, -1526,
                  6932, 19260, 23569, 33941, 36434, 85689];
  s.addChart(pres.ChartType.bar, [{
    name: "Change 2023 → 2024", labels, values
  }], Object.assign(CHART_BASE(), {
    x: M, y: 1.72, w: 8.1, h: 4.35,
    barDir: "bar", showTitle: false, showValue: true,
    dataLabelPosition: "outEnd", dataLabelFormatCode: "#,##0",
    dataLabelFontSize: 9, chartColors: [RED], invertedColors: [GREEN],
    barGapWidthPct: 40, catAxisLabelFontSize: 10
  }));
  card(s, 9.1, 1.72, W - M - 9.1, 4.35, PALE);
  stat(s, 9.4, 2.0, "−71%", "Printers, 2023 → 2024", RED, 3.0);
  s.addText([
    { text: "136,865 lost on one line item — over half the entire peak-to-2024 gap.", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "Every Electronics sub-category fell. Every Office Supplies sub-category grew.", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "This is not a slowdown. Two opposite trends are running at once, and the company-wide figure is their average — which describes neither.", options: { bold: true } }
  ], {
    x: 9.4, y: 3.35, w: 3.0, h: 2.5, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 11.5, color: INK, lineSpacing: 17
  });
  source(s, "Source: Query 7, sub-category revenue change 2023 against 2024.");
  s.addNotes("This is the most useful thing Checkpoint 1 produced. Let the chart do the work — the red block at the top and the green at the bottom.");
}

/* 10 — finding 3 */
{
  const s = lightSlide("Seasonality is category-specific", "2 · Data & SQL · Finding 3");
  s.addChart(pres.ChartType.bar, [
    { name: "Electronics", labels: ["Q1", "Q2", "Q3", "Q4"], values: [20.28, 30.79, 23.69, 25.24] },
    { name: "Furniture", labels: ["Q1", "Q2", "Q3", "Q4"], values: [16.96, 29.46, 22.74, 30.84] },
    { name: "Office Supplies", labels: ["Q1", "Q2", "Q3", "Q4"], values: [17.01, 25.00, 25.83, 32.16] }
  ], Object.assign(CHART_BASE(), {
    x: M, y: 1.75, w: 7.9, h: 4.1,
    showTitle: false, showValue: true, dataLabelPosition: "outEnd",
    dataLabelFormatCode: '0.0"%"', dataLabelFontSize: 9,
    showLegend: true, legendPos: "b", legendFontFace: BODY, legendFontSize: 11,
    valAxisMaxVal: 38, barGapWidthPct: 40
  }));
  card(s, 8.9, 1.75, W - M - 8.9, 4.1, PALE);
  s.addText("The blended curve is wrong for all three", {
    x: 9.2, y: 2.05, w: 3.2, h: 0.75, isTextBox: true, margin: 0,
    fontFace: HEAD, fontSize: 16, bold: true, color: INK
  });
  s.addText([
    { text: "Electronics peaks in Q2 at 30.79% of its own annual revenue.", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "Furniture and Office Supplies peak in Q4.", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "A single company-wide planning curve over-stocks Electronics in Q4 and under-stocks it in Q2.", options: {} }
  ], {
    x: 9.2, y: 2.95, w: 3.2, h: 2.7, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 12.5, color: INK, lineSpacing: 19
  });
  source(s, "Source: Query 8, each quarter's share of its own category's annual revenue.");
  s.addNotes("If asked why it matters: inventory and staffing are planned on the blended curve, so they are mistimed for a third of the business.");
}

/* 11 — divider */
{
  const s = darkSlide();
  chip(s, M, 2.9, 3, AMBER);
  s.addText("Statistical Insights", {
    x: M, y: 3.5, w: 9.5, h: 0.95, isTextBox: true, margin: 0,
    fontFace: HEAD, fontSize: 40, bold: true, color: WHITE
  });
  s.addText("How strong is the evidence, and what can be predicted", {
    x: M, y: 4.45, w: 9.5, h: 0.5, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 15, color: "CADCFC"
  });
  s.addNotes("Checkpoint 2 takes the same dataset into Excel.");
}

/* 12 — descriptive statistics */
{
  const s = lightSlide("The histogram is itself a finding", "3 · Statistics");
  s.addImage({ path: path.join(FIG, "cp2_fig1_histogram.png"), x: M, y: 1.7, w: 7.5, h: 4.2, sizing: { type: "contain", w: 7.5, h: 4.2 } });
  stat(s, 8.6, 1.85, "54.2%", "Amount — coefficient of variation", INK, 3.9);
  stat(s, 8.6, 3.15, "82.9%", "Profit — far less predictable, skew +0.94", RED, 3.9);
  s.addText([
    { text: "A revenue target does not manage profit. ", options: { bold: true } },
    { text: "And a flat distribution is what a random number generator produces — our own descriptive statistics confirm the data is synthetic.", options: {} }
  ], {
    x: 8.6, y: 4.6, w: 3.9, h: 1.5, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 12.5, color: INK, lineSpacing: 19
  });
  source(s, "Source: Checkpoint 2, Task 2.2. n = 1,194 transaction lines, ten bins of 1,000.");
  s.addNotes("Two points only: profit is less predictable than revenue, and the flat shape is evidence the data is generated.");
}

/* 13 — correlation */
{
  const s = lightSlide("One driver, and one strategy the data kills", "3 · Statistics");
  card(s, M, 1.8, 5.8, 3.9, PALE);
  stat(s, M + 0.4, 2.15, "r = 0.923", "Monthly orders → monthly revenue", BLUE, 5.0);
  s.addText([
    { text: "Order count explains about 85% of the variation in monthly revenue.", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "Checkpoint 1 inferred this. Checkpoint 2 measures it.", options: { bold: true } }
  ], {
    x: M + 0.4, y: 3.5, w: 5.0, h: 1.9, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 13, color: INK, lineSpacing: 20
  });

  card(s, 6.85, 1.8, 5.78, 3.9, "FBF0F0");
  stat(s, 7.25, 2.15, "r = 0.045", "Units sold → order value · p = 0.123", RED, 5.0);
  s.addText([
    { text: "No relationship, and not statistically significant.", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "A negative result we are keeping: a \"sell more units\" target would not move revenue in this business.", options: { bold: true } }
  ], {
    x: 7.25, y: 3.5, w: 5.0, h: 1.9, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 13, color: INK, lineSpacing: 20
  });
  s.addText("Correlation is not causation — the association is strong and consistent over 57 months, which is not the same as one causing the other.", {
    x: M, y: 5.95, w: W - 2 * M, h: 0.5, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 12.5, italic: true, color: MUTED
  });
  source(s, "Source: Checkpoint 2, Task 2.3. n = 57 months and 1,194 lines respectively.");
  s.addNotes("Say the caveat out loud. The negative result on the right is the one worth pausing on.");
}

/* 14 — regression */
{
  const s = lightSlide("Order count drives revenue — measured, not inferred", "3 · Statistics");
  card(s, M, 1.75, W - 2 * M, 1.12, INK);
  s.addText("Monthly Revenue  =  −1,353.65  +  5,224.25 × Orders", {
    x: M, y: 1.75, w: W - 2 * M, h: 1.12, isTextBox: true, margin: 0,
    align: "center", valign: "middle",
    fontFace: HEAD, fontSize: 25, bold: true, color: WHITE
  });
  const cells = [
    ["R² = 0.8514", "85% of month-to-month variation", BLUE],
    ["t = 17.75", "55 degrees of freedom", BLUE],
    ["p = 1.98 × 10⁻²⁴", "The slope is not zero", GREEN],
    ["5,178.09", "The actual mean order value", AMBER]
  ];
  cells.forEach(([big, small, col], i) => {
    const x = M + i * 3.06;
    card(s, x, 3.2, 2.86, 1.5, PALE);
    s.addText(big, {
      x: x + 0.2, y: 3.38, w: 2.5, h: 0.5, isTextBox: true, margin: 0,
      fontFace: HEAD, fontSize: 19, bold: true, color: col
    });
    s.addText(small, {
      x: x + 0.2, y: 3.9, w: 2.5, h: 0.65, isTextBox: true, margin: 0,
      fontFace: BODY, fontSize: 11, color: MUTED
    });
  });
  s.addText([
    { text: "The check that makes this convincing: ", options: { bold: true } },
    { text: "the slope lands within 0.9% of the plain mean order value. The regression rediscovered it without being told.", options: {} }
  ], {
    x: M, y: 5.0, w: W - 2 * M, h: 0.5, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 14, color: INK
  });
  s.addText([
    { text: "Four orders a month below the 2022 level ≈ 250,000 a year. ", options: { bold: true } },
    { text: "Checkpoint 1 reached 257,297 by summing category shortfalls — two independent methods within 3%.", options: {} }
  ], {
    x: M, y: 5.6, w: W - 2 * M, h: 0.6, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 14, color: INK
  });
  source(s, "Source: Checkpoint 2, Task 2.4. n = 57 complete months, April 2020 – December 2024.");
  s.addNotes("The 250,000 corroboration is the strongest single piece of evidence in the project. Say that sentence deliberately.");
}

/* 15 — trend and the honest forecast */
{
  const s = lightSlide("Two regimes — and a forecast that lost", "3 · Statistics");
  s.addImage({ path: path.join(FIG, "cp2_fig4_forecast.png"), x: M, y: 1.7, w: 7.8, h: 4.1, sizing: { type: "contain", w: 7.8, h: 4.1 } });
  card(s, 8.9, 1.7, W - M - 8.9, 4.1, PALE);
  s.addText("Why no growth rate?", {
    x: 9.2, y: 1.98, w: 3.2, h: 0.4, isTextBox: true, margin: 0,
    fontFace: HEAD, fontSize: 16, bold: true, color: INK
  });
  s.addText([
    { text: "A straight line across all 57 months explains under 1% — R² = 0.0078, p = 0.515.", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "That is not \"no trend\". It is that no single line fits both regimes — the up-slope and the flat cancel out.", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "So the forecast uses level and seasonality, not a growth rate we cannot demonstrate.", options: {} }
  ], {
    x: 9.2, y: 2.48, w: 3.2, h: 3.1, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 12, color: INK, lineSpacing: 18
  });
  card(s, M, 5.95, W - 2 * M, 0.72, "FBF0F0");
  s.addText([
    { text: "Tested honestly: our seasonal forecast lost to a flat average. ", options: { bold: true } },
    { text: "22.7% mean absolute error against 14.9%. We report it and keep the method, because choosing on two observations is overfitting the holdout.", options: {} }
  ], {
    x: M + 0.3, y: 5.95, w: W - 2 * M - 0.6, h: 0.72, isTextBox: true, margin: 0,
    valign: "middle", fontFace: BODY, fontSize: 12.5, color: INK
  });
  source(s, "Source: Checkpoint 2, Task 2.5. Holdout: January and February 2025.");
  s.addNotes("January 2025 came in at 112,906 against a prediction of 68,853. January's index says it is the weakest month; this one was not.");
}

/* 16 — dashboard divider with demo cues */
{
  const s = darkSlide();
  chip(s, M, 1.5, 4, AMBER);
  s.addText("Live Dashboard Demo", {
    x: M, y: 2.1, w: 8.5, h: 0.9, isTextBox: true, margin: 0,
    fontFace: HEAD, fontSize: 38, bold: true, color: WHITE
  });
  s.addText("Three pages, built in Power BI on the same database", {
    x: M, y: 3.0, w: 8.5, h: 0.45, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 15, color: "CADCFC"
  });
  const cues = [
    "Page 1 — Executive Summary: four KPI cards, the 57-month trend",
    "Page 2 — Trend & Comparison: category lines, sub-category change",
    "Page 3 — Deep Dive: the customer and product segments",
    "Demonstrate live: the segment slicer on Page 3"
  ];
  cues.forEach((c, i) => {
    s.addText(c, {
      x: M + 0.1, y: 3.85 + i * 0.52, w: 9.0, h: 0.42, isTextBox: true, margin: 0,
      fontFace: BODY, fontSize: 14,
      bold: i === 3, color: i === 3 ? AMBER : WHITE, bullet: true
    });
  });
  s.addImage({ path: path.join(FIG, "cp3_fig3_wireframe.png"), x: 10.0, y: 1.3, w: 2.6, h: 5.0, sizing: { type: "contain", w: 2.6, h: 5.0 } });
  s.addNotes("Switch to Power BI here. Select Thin-Margin Buyers on the Page 3 slicer and show the profit share collapse — that is the most persuasive single interaction on the dashboard. Replace the wireframe on this slide with a screenshot of the finished dashboard before the defense.");
}

/* 17 — segmentation */
{
  const s = lightSlide("The largest customer group returns the least profit", "4 · Dashboard · Segmentation");
  s.addChart(pres.ChartType.bar, [
    { name: "% of customers", labels: ["High-Value Accounts", "High-Margin Buyers", "Thin-Margin Buyers"], values: [18.1, 38.5, 43.4] },
    { name: "% of revenue", labels: ["High-Value Accounts", "High-Margin Buyers", "Thin-Margin Buyers"], values: [38.4, 28.9, 32.7] },
    { name: "% of profit", labels: ["High-Value Accounts", "High-Margin Buyers", "Thin-Margin Buyers"], values: [38.7, 42.6, 18.7] }
  ], Object.assign(CHART_BASE(), {
    x: M, y: 1.75, w: 7.9, h: 4.1,
    showTitle: false, showValue: true, dataLabelPosition: "outEnd",
    dataLabelFormatCode: '0.0"%"', dataLabelFontSize: 9,
    showLegend: true, legendPos: "b", legendFontFace: BODY, legendFontSize: 11,
    chartColors: [MUTED, BLUE, GREEN], valAxisMaxVal: 50, barGapWidthPct: 40
  }));
  card(s, 8.9, 1.75, W - M - 8.9, 4.1, PALE);
  s.addText("k-means, k = 3", {
    x: 9.2, y: 2.0, w: 3.2, h: 0.35, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 11, bold: true, color: MUTED
  });
  s.addText([
    { text: "807 customers clustered on value, margin and recency. k chosen by silhouette.", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "Thin-Margin Buyers: 43% of customers, a third of revenue — and 19% of the profit.", options: { bold: true, breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "High-Margin Buyers turn less revenue into 43% of it. A sales push aimed at revenue would chase the wrong group.", options: {} }
  ], {
    x: 9.2, y: 2.45, w: 3.2, h: 3.2, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 12, color: INK, lineSpacing: 18
  });
  source(s, "Source: Checkpoint 3, Task 3.3. Recency separated nothing; frequency spans 1–4 lines only.");
  s.addNotes("If asked why three clusters and not five: k=5 scores 0.295 against 0.277, but two of its five came out with the same profile, and the brief asks for two or three.");
}

/* 18 — divider */
{
  const s = darkSlide();
  chip(s, M, 2.9, 5, AMBER);
  s.addText("Predictive Analytics", {
    x: M, y: 3.5, w: 9.5, h: 0.95, isTextBox: true, margin: 0,
    fontFace: HEAD, fontSize: 40, bold: true, color: WHITE
  });
  s.addText("Extending the regression — and what happened when we tested it",  {
    x: M, y: 4.45, w: 9.5, h: 0.5, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 15, color: "CADCFC"
  });
  s.addNotes("Checkpoint 4, Task 4.1.");
}

/* 19 — the multiple regression */
{
  const s = lightSlide("We extended the model. The simple one still wins.", "5 · Predictive analytics");
  s.addImage({ path: path.join(FIG, "cp4_fig1_actual_vs_predicted.png"), x: M, y: 1.72, w: 7.6, h: 3.5, sizing: { type: "contain", w: 7.6, h: 3.5 } });

  card(s, 8.7, 1.72, W - M - 8.7, 3.5, PALE);
  s.addText("Holdout — six unseen months", {
    x: 9.0, y: 1.98, w: 3.4, h: 0.35, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 11, bold: true, color: MUTED
  });
  stat(s, 9.0, 2.4, "9.3%", "Orders only — the CP2 baseline", GREEN, 3.4);
  stat(s, 9.0, 3.75, "9.8%", "Multiple regression, five predictors", RED, 3.4);

  card(s, M, 5.42, W - 2 * M, 1.25, PALE);
  s.addText([
    { text: "So why present it? Because the value is diagnostic. ", options: { bold: true } },
    { text: "Units sold (p = 0.79), customer count (p = 0.27), product mix (p = 0.48) and elapsed time (p = 0.55) were each given a fair chance alongside order count. None explained anything — which is the evidence behind building the dashboard on order count.", options: {} }
  ], {
    x: M + 0.3, y: 5.42, w: W - 2 * M - 0.6, h: 1.25, isTextBox: true, margin: 0,
    valign: "middle", fontFace: BODY, fontSize: 12.5, color: INK, lineSpacing: 18
  });
  source(s, "Source: Checkpoint 4, Task 4.1. Trained on 51 months, six held out. R² = 0.8647, adjusted R² = 0.8514.");
  s.addNotes("Two problems handled rather than ignored: severe multicollinearity — orders, units and customers are 0.81 to 0.92 correlated, VIF 13.67 — and Breusch-Pagan rejecting constant variance at p = 0.0023, so robust standard errors are reported.");
}

/* 20 — recommendations */
{
  const s = lightSlide("Five recommendations, each tied to a measurement", "5 · Recommendations");
  const recs = [
    ["Track order count, not revenue", "r = 0.923 · the only predictor that survives"],
    ["Investigate Printers first", "136,865 lost — over half the entire gap"],
    ["Plan seasonality by category", "Electronics peaks Q2; the others Q4"],
    ["Segment on margin, not revenue", "43% of customers return 19% of profit"],
    ["Drop volume and acquisition targets", "Units and customer count predict nothing"]
  ];
  recs.forEach(([t, d], i) => {
    const y = 1.85 + i * 0.95;
    chip(s, M, y, i + 1, GREEN);
    s.addText(t, {
      x: M + 0.75, y: y - 0.02, w: 6.4, h: 0.4, isTextBox: true, margin: 0,
      fontFace: BODY, fontSize: 15.5, bold: true, color: INK
    });
    s.addText(d, {
      x: M + 0.75, y: y + 0.36, w: 6.4, h: 0.36, isTextBox: true, margin: 0,
      fontFace: BODY, fontSize: 11.5, color: MUTED
    });
  });
  card(s, 8.3, 1.8, W - M - 8.3, 4.5, INK);
  s.addText("What we would stand behind", {
    x: 8.65, y: 2.1, w: 3.6, h: 0.45, isTextBox: true, margin: 0,
    fontFace: HEAD, fontSize: 16, bold: true, color: WHITE
  });
  s.addText([
    { text: "A dataset whose defects are documented rather than hidden.", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "A normalised schema with constraints that are enforced and tested.", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "Queries verified on two database engines.", options: { breakLine: true } },
    { text: "", options: { breakLine: true } },
    { text: "Statistics tested for significance rather than eyeballed — with the negative results reported alongside the positive.", options: {} }
  ], {
    x: 8.65, y: 2.7, w: 3.6, h: 3.4, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 12, color: "CADCFC", lineSpacing: 18
  });
  s.addNotes("These are the answer to 'so what'. Each one names the measurement behind it.");
}

/* 21 — ethics */
{
  const s = lightSlide("Ethics, privacy and governance", "6 · Ethics & governance");
  const blocks = [
    ["Privacy", "The names are synthetic, so there is no data subject and R.A. 10173 is not engaged. Not because the file is public — public availability is not consent.", BLUE],
    ["Ethics", "Our own segmentation is the risk. Labelling 350 customers \"Thin-Margin\" is accurate, and on real data it is a mechanism by which poorer customers get served worse.", RED],
    ["Governance", "A named owner for the customer dimension, analysts on pseudonymised views, a retention rule, and reproducible lineage.", GREEN],
    ["Regulation", "R.A. 10173 on proportionality, purpose and the right to object. GDPR Article 22 on automated decisions — a line our clustering is closer to than it looks.", AMBER]
  ];
  blocks.forEach(([t, d, col], i) => {
    const x = M + (i % 2) * 6.1;
    const y = 1.85 + Math.floor(i / 2) * 2.35;
    card(s, x, y, 5.85, 2.05, PALE);
    s.addShape(pres.ShapeType.ellipse, {
      x: x + 0.32, y: y + 0.3, w: 0.32, h: 0.32,
      fill: { color: col }, line: { color: col, width: 0 }
    });
    s.addText(t, {
      x: x + 0.78, y: y + 0.24, w: 4.7, h: 0.42, isTextBox: true, margin: 0,
      valign: "middle", fontFace: HEAD, fontSize: 17, bold: true, color: INK
    });
    s.addText(d, {
      x: x + 0.35, y: y + 0.78, w: 5.15, h: 1.1, isTextBox: true, margin: 0,
      fontFace: BODY, fontSize: 12, color: INK, lineSpacing: 18
    });
  });
  source(s, "Full reflection: Checkpoint 4, Task 4.2 — 1,153 words against a 500-word minimum.");
  s.addNotes("Ninety seconds. The one point to land is that public availability is not consent, and that the ethical risk comes from our own segmentation rather than from the data.");
}

/* 22 — limitations */
{
  const s = lightSlide("What we would not claim", "Limitations");
  const lims = [
    ["The data is synthetic", "These figures illustrate a method; they do not describe a real company. We proved it with five signals and did not invent corrections."],
    ["The forecast is weak", "22.7% mean absolute error against a flat average's 14.9%. We measured our own error rather than dropping the test."],
    ["Correlation is not causation", "Order count and revenue move together over 57 months. That is not proof one causes the other."]
  ];
  lims.forEach(([t, d], i) => {
    const y = 1.95 + i * 1.5;
    card(s, M, y, W - 2 * M, 1.25, PALE);
    s.addText(t, {
      x: M + 0.4, y: y + 0.18, w: 11.0, h: 0.42, isTextBox: true, margin: 0,
      fontFace: HEAD, fontSize: 18, bold: true, color: INK
    });
    s.addText(d, {
      x: M + 0.4, y: y + 0.63, w: 11.0, h: 0.5, isTextBox: true, margin: 0,
      fontFace: BODY, fontSize: 13, color: MUTED
    });
  });
  s.addText("A project that only reports what worked is a sales deck. These three are why this one is analysis.", {
    x: M, y: 6.5, w: W - 2 * M, h: 0.45, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 13.5, italic: true, color: INK
  });
  s.addNotes("Say all three before Q&A. Volunteering them is worth more than defending them under questioning.");
}

/* 23 — Q&A */
{
  const s = darkSlide();
  s.addText("Questions", {
    x: M, y: 1.4, w: 9, h: 0.95, isTextBox: true, margin: 0,
    fontFace: HEAD, fontSize: 42, bold: true, color: WHITE
  });
  s.addText("Any member can answer on any part of the project.", {
    x: M, y: 2.35, w: 9, h: 0.45, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 15, color: "CADCFC"
  });
  const qa = [
    ["Your dataset is fake — what is the project worth?", "The figures illustrate a method. Every query, statistic and model would run identically on a real export."],
    ["Your multiple regression performed worse. Why present it?", "Its value is diagnostic: it rules out units, customers, mix and time as drivers."],
    ["Why three clusters and not five?", "k=5 scores higher, but two of its five had the same profile — and the brief asks for two or three."],
    ["What would you do differently?", "Check the completeness of both ends of the date range first. That caused our one real error."]
  ];
  qa.forEach(([q, a], i) => {
    const y = 3.15 + i * 0.88;
    s.addText(q, {
      x: M, y, w: 11.9, h: 0.38, isTextBox: true, margin: 0,
      fontFace: BODY, fontSize: 14, bold: true, color: AMBER
    });
    s.addText(a, {
      x: M, y: y + 0.36, w: 11.9, h: 0.42, isTextBox: true, margin: 0,
      fontFace: BODY, fontSize: 12, color: "CADCFC"
    });
  });
  s.addText("Thank you.", {
    x: M, y: H - 0.72, w: 5, h: 0.4, isTextBox: true, margin: 0,
    fontFace: HEAD, fontSize: 15, bold: true, color: WHITE
  });
  s.addNotes("Do not read this slide out. It is a prompt for whoever is fielding the question.");
}

pres.writeFile({ fileName: OUT }).then(() => {
  console.log("wrote " + path.relative(ROOT, OUT));
  console.log("  " + pres.slides.length + " slides");
});
