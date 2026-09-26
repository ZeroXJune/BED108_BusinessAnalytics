"""
Generates a Power BI project (.pbip) for Checkpoint 3.

A .pbix cannot be written here: its DataModel part is a binary produced by the
Analysis Services engine, which only Power BI Desktop has. A .pbip is the same
artifact in Microsoft's plain-text project format — TMDL for the semantic
model, JSON for the report — so it can be generated. Power BI Desktop opens
the folder, and File > Save as > .pbix produces the file the brief asks for.

What this builds:
  * the semantic model — seven tables plus a date table, typed columns,
    five relationships, and all twenty measures
  * page 1 of the report, with the four KPI cards and the trend chart
  * pages 2 and 3, named and empty, to be filled per the build guide

Run:  python3 scripts/build_pbip.py
"""

import csv
import json
import os
import shutil
import uuid

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "dashboard")
OUT = os.path.join(ROOT, "powerbi", "Checkpoint3_Dashboard")
NAME = "Checkpoint3_Dashboard"

# Column name -> TMDL data type. Anything unlisted falls back to string.
TYPES = {
    "int64": {"sale_id", "customer_id", "year_number", "quarter_number",
              "month_number", "transaction_lines", "units_sold", "quantity",
              "months_covered", "customers", "recency_days", "cluster",
              "is_complete_month", "is_complete_year", "in_analysis_window"},
    "double": {"revenue", "profit", "amount", "margin_pct", "avg_line_value",
               "revenue_per_month", "revenue_per_customer", "revenue_total",
               "revenue_2023", "revenue_2024", "growth_pct"},
    "dateTime": {"order_date", "month_start"},
}

TABLES = [
    ("Monthly", "monthly.csv"),
    ("CategoryMonth", "category_month.csv"),
    ("Sales", "sales_detail.csv"),
    ("Geography", "geography.csv"),
    ("Annual", "annual.csv"),
    ("CustomerSegments", "customer_segments.csv"),
    ("SubcategorySegments", "subcategory_segments.csv"),
]

# From the many side to the one side. The one-side column must be unique, so
# Monthly and CategoryMonth are deliberately NOT related to DateTable:
# DateTable is daily, its MonthStart repeats about thirty times a month, and a
# relationship onto it would be built backwards or refused. Those two tables
# carry their own month_start and are used directly as a visual's axis.
RELATIONSHIPS = [
    ("Sales", "customer_id", "CustomerSegments", "customer_id"),
    ("Sales", "sub_category_name", "SubcategorySegments", "sub_category_name"),
    ("Sales", "order_date", "DateTable", "Date"),
]

MEASURES = [
    ("Sales", "Revenue", "SUM ( Sales[amount] )", "#,0"),
    ("Sales", "Profit", "SUM ( Sales[profit] )", "#,0"),
    ("Sales", "Orders", "COUNTROWS ( Sales )", "#,0"),
    ("Sales", "Units", "SUM ( Sales[quantity] )", "#,0"),
    ("Sales", "Customers", "DISTINCTCOUNT ( Sales[customer_id] )", "#,0"),
    ("Sales", "Margin %", "DIVIDE ( [Profit], [Revenue] ) * 100", "#,0.00"),
    ("Sales", "Avg Line Value", "DIVIDE ( [Revenue], [Orders] )", "#,0.00"),
    ("Sales", "Months Covered", "DISTINCTCOUNT ( Sales[year_month] )", "#,0"),
    ("Sales", "Revenue per Month", "DIVIDE ( [Revenue], [Months Covered] )", "#,0.00"),
    ("Sales", "Orders per Month", "DIVIDE ( [Orders], [Months Covered] )", "#,0.0"),
    ("Sales", "Peak Revenue per Month",
     "CALCULATE ( [Revenue per Month], ALL ( Sales ), Sales[year_number] = 2022 )", "#,0.00"),
    ("Sales", "Peak Orders per Month",
     "CALCULATE ( [Orders per Month], ALL ( Sales ), Sales[year_number] = 2022 )", "#,0.0"),
    ("Sales", "Gap to Peak %",
     "DIVIDE ( [Revenue per Month] - [Peak Revenue per Month], [Peak Revenue per Month] ) * 100", "#,0.0"),
    ("Sales", "Order Gap", "[Peak Orders per Month] - [Orders per Month]", "#,0.0"),
    ("Sales", "Gap Value per Year", "[Order Gap] * 5224.25 * 12", "#,0"),
    ("CustomerSegments", "Segment Customers", "COUNTROWS ( CustomerSegments )", "#,0"),
    ("CustomerSegments", "Segment Revenue", "SUM ( CustomerSegments[revenue] )", "#,0"),
    ("CustomerSegments", "Segment Profit", "SUM ( CustomerSegments[profit] )", "#,0"),
    ("CustomerSegments", "Segment Margin %",
     "DIVIDE ( [Segment Profit], [Segment Revenue] ) * 100", "#,0.00"),
    ("CustomerSegments", "Segment % of Customers",
     "DIVIDE ( [Segment Customers], CALCULATE ( [Segment Customers], ALL ( CustomerSegments ) ) ) * 100", "#,0.0"),
    ("CustomerSegments", "Segment % of Revenue",
     "DIVIDE ( [Segment Revenue], CALCULATE ( [Segment Revenue], ALL ( CustomerSegments ) ) ) * 100", "#,0.0"),
    ("CustomerSegments", "Segment % of Profit",
     "DIVIDE ( [Segment Profit], CALCULATE ( [Segment Profit], ALL ( CustomerSegments ) ) ) * 100", "#,0.0"),
]


def gid():
    return str(uuid.uuid4())


def dtype(col):
    for t, names in TYPES.items():
        if col in names:
            return t
    return "string"


def headers(path):
    with open(path) as fh:
        return next(csv.reader(fh))


def write(path, text, encoding="utf-8"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding=encoding, newline="\n") as fh:
        fh.write(text)


# ------------------------------------------------------------ semantic model

def table_tmdl(name, filename):
    cols = headers(os.path.join(DATA, filename))
    lines = ["table %s" % name, "\tlineageTag: %s" % gid(), ""]
    for c in cols:
        t = dtype(c)
        lines += [
            "\tcolumn %s" % c,
            "\t\tdataType: %s" % t,
            "\t\tlineageTag: %s" % gid(),
            "\t\tsummarizeBy: %s" % ("sum" if t in ("int64", "double") else "none"),
            "\t\tsourceColumn: %s" % c,
        ]
        if t == "dateTime":
            lines.append('\t\tformatString: yyyy-mm-dd')
        lines.append("")
    for tbl, mname, expr, fmt in MEASURES:
        if tbl != name:
            continue
        lines += [
            "\tmeasure '%s' = %s" % (mname, expr),
            "\t\tformatString: %s" % fmt,
            "\t\tlineageTag: %s" % gid(),
            "",
        ]
    # The M partition. Csv.Document with the delimiter and a UTF-8 encoding,
    # then the same type mapping as the columns above.
    transforms = ", ".join(
        '{"%s", %s}' % (c, {"int64": "Int64.Type", "double": "type number",
                            "dateTime": "type date"}.get(dtype(c), "type text"))
        for c in cols)
    lines += [
        "\tpartition %s = m" % name,
        "\t\tmode: import",
        "\t\tsource =",
        "\t\t\t\tlet",
        '\t\t\t\t    Source = Csv.Document(File.Contents(FolderPath & "%s"),'
        % filename,
        "\t\t\t\t        [Delimiter = \",\", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),",
        "\t\t\t\t    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),",
        "\t\t\t\t    Typed = Table.TransformColumnTypes(Promoted, {%s})" % transforms,
        "\t\t\t\tin",
        "\t\t\t\t    Typed",
        "",
    ]
    return "\n".join(lines)


def datetable_tmdl():
    """A calculated date table, so it cannot drift from the data."""
    cols = [
        ("Date", "dateTime", "[Date]"),
        ("Year", "int64", "YEAR ( [Date] )"),
        ("Quarter", "string", '"Q" & FORMAT ( QUARTER ( [Date] ), "0" )'),
        ("MonthNumber", "int64", "MONTH ( [Date] )"),
        ("MonthName", "string", 'FORMAT ( [Date], "MMMM" )'),
        ("MonthStart", "dateTime", "EOMONTH ( [Date], -1 ) + 1"),
        ("YearMonth", "string", 'FORMAT ( [Date], "YYYY-MM" )'),
    ]
    lines = ["table DateTable", "\tlineageTag: %s" % gid(),
             "\tdataCategory: Time", ""]
    for name, t, expr in cols:
        lines += [
            "\tcolumn %s = %s" % (name, expr),
            "\t\tdataType: %s" % t,
            "\t\tlineageTag: %s" % gid(),
            "\t\tsummarizeBy: none",
        ]
        if name == "Date":
            lines.append("\t\tisKey")
        if t == "dateTime":
            lines.append("\t\tformatString: yyyy-mm-dd")
        lines.append("")
    lines += [
        "\tpartition DateTable = calculated",
        "\t\tmode: import",
        "\t\tsource = CALENDAR ( DATE ( 2020, 3, 1 ), DATE ( 2025, 3, 31 ) )",
        "",
    ]
    return "\n".join(lines)


def build_model(dest):
    defn = os.path.join(dest, "definition")
    write(os.path.join(dest, "definition.pbism"),
          json.dumps({"version": "4.2", "settings": {}}, indent=2))
    write(os.path.join(defn, "database.tmdl"),
          "database\n\tcompatibilityLevel: 1567\n")

    names = [n for n, _ in TABLES] + ["DateTable"]
    model = [
        "model Model",
        "\tculture: en-US",
        "\tdefaultPowerBIDataSourceVersion: powerBI_V3",
        "\tsourceQueryCulture: en-US",
        "",
        '\tannotation PBI_QueryOrder = %s' % json.dumps(names),
        "",
    ]
    model += ["ref table %s" % n for n in names]
    model += ["", "ref cultureInfo en-US", ""]
    write(os.path.join(defn, "model.tmdl"), "\n".join(model))

    write(os.path.join(defn, "cultureInfos", "en-US.tmdl"),
          "cultureInfo en-US\n")

    # FolderPath is a parameter, so opening the project prompts for it.
    write(os.path.join(defn, "expressions.tmdl"),
          'expression FolderPath = "C:\\Users\\YourName\\Documents\\BED106\\'
          'data\\dashboard\\" meta [IsParameterQuery=true, Type="Text", '
          'IsParameterQueryRequired=true]\n'
          "\tlineageTag: %s\n\n"
          "\tannotation PBI_ResultType = Text\n" % gid())

    for name, filename in TABLES:
        write(os.path.join(defn, "tables", "%s.tmdl" % name),
              table_tmdl(name, filename))
    write(os.path.join(defn, "tables", "DateTable.tmdl"), datetable_tmdl())

    rels = []
    for ft, fc, tt, tc in RELATIONSHIPS:
        rels += [
            "relationship %s" % gid(),
            "\tfromColumn: %s.%s" % (ft, fc),
            "\ttoColumn: %s.%s" % (tt, tc),
            "",
        ]
    write(os.path.join(defn, "relationships.tmdl"), "\n".join(rels))


# ------------------------------------------------------------------- report

def card_visual(x, y, w, h, measure, title, fmt=None):
    name = gid()
    cfg = {
        "name": name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": 0,
                                           "width": w, "height": h}}],
        "singleVisual": {
            "visualType": "card",
            "projections": {"Values": [{"queryRef": "Sales.%s" % measure}]},
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": "s", "Entity": "Sales", "Type": 0}],
                "Select": [{
                    "Measure": {"Expression": {"SourceRef": {"Source": "s"}},
                                "Property": measure},
                    "Name": "Sales.%s" % measure
                }]
            },
            "drillFilterOtherVisuals": True,
            "objects": {"labels": [{"properties": {
                "fontSize": {"expr": {"Literal": {"Value": "28D"}}}}}]},
            "vcObjects": {"title": [{"properties": {
                "show": {"expr": {"Literal": {"Value": "true"}}},
                "text": {"expr": {"Literal": {"Value": "'%s'" % title}}}
            }}]}
        }
    }
    return {"x": x, "y": y, "z": 0, "width": w, "height": h,
            "config": json.dumps(cfg)}


def line_visual(x, y, w, h):
    name = gid()
    cfg = {
        "name": name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": 1,
                                           "width": w, "height": h}}],
        "singleVisual": {
            "visualType": "lineChart",
            "projections": {
                "Category": [{"queryRef": "Monthly.month_start"}],
                "Y": [{"queryRef": "Sum(Monthly.revenue)"}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": "m", "Entity": "Monthly", "Type": 0}],
                "Select": [
                    {"Column": {"Expression": {"SourceRef": {"Source": "m"}},
                                "Property": "month_start"},
                     "Name": "Monthly.month_start"},
                    {"Aggregation": {"Expression": {"Column": {
                        "Expression": {"SourceRef": {"Source": "m"}},
                        "Property": "revenue"}}, "Function": 0},
                     "Name": "Sum(Monthly.revenue)"}
                ],
                "Where": [{"Condition": {"Comparison": {
                    "ComparisonKind": 0,
                    "Left": {"Column": {
                        "Expression": {"SourceRef": {"Source": "m"}},
                        "Property": "in_analysis_window"}},
                    "Right": {"Literal": {"Value": "1L"}}}}}]
            },
            "drillFilterOtherVisuals": True,
            "vcObjects": {"title": [{"properties": {
                "show": {"expr": {"Literal": {"Value": "true"}}},
                "text": {"expr": {"Literal": {"Value":
                    "'Revenue per month, April 2020 - December 2024'"}}}
            }}]}
        }
    }
    return {"x": x, "y": y, "z": 1, "width": w, "height": h,
            "config": json.dumps(cfg)}


def section(ordinal, display, visuals):
    return {
        "name": gid().replace("-", "")[:20],
        "displayName": display,
        "ordinal": ordinal,
        "width": 1280,
        "height": 720,
        "config": json.dumps({}),
        "filters": "[]",
        "visualContainers": visuals,
    }


def build_report(dest):
    write(os.path.join(dest, "definition.pbir"),
          json.dumps({"version": "1.0",
                      "datasetReference": {"byPath": {
                          "path": "../%s.SemanticModel" % NAME}}}, indent=2))

    kpis = [
        ("Orders per Month", "Orders per month  (2022 peak: 24.0)"),
        ("Revenue per Month", "Revenue per month  (2022 peak: 121,648)"),
        ("Margin %", "Margin %"),
        ("Gap to Peak %", "Gap to the 2022 peak"),
    ]
    visuals = []
    for i, (m, t) in enumerate(kpis):
        visuals.append(card_visual(24 + i * 310, 24, 296, 150, m, t))
    visuals.append(line_visual(24, 196, 916, 470))

    report = {
        "config": json.dumps({
            "version": "5.43",
            "themeCollection": {"baseTheme": {
                "name": "CY24SU10", "version": "5.51", "type": 2}},
            "activeSectionIndex": 0,
            "defaultDrillFilterOtherVisuals": True,
        }),
        "layoutOptimization": 0,
        "resourcePackages": [],
        "sections": [
            section(0, "1 Executive Summary", visuals),
            section(1, "2 Trend & Comparison", []),
            section(2, "3 Deep Dive & Segmentation", []),
        ],
    }
    write(os.path.join(dest, "report.json"),
          json.dumps(report, indent=2, ensure_ascii=False))


def main():
    base = os.path.dirname(OUT)
    model_dir = os.path.join(base, "%s.SemanticModel" % NAME)
    report_dir = os.path.join(base, "%s.Report" % NAME)
    for d in (model_dir, report_dir):
        if os.path.isdir(d):
            shutil.rmtree(d)

    build_model(model_dir)
    build_report(report_dir)
    write(os.path.join(base, "%s.pbip" % NAME), json.dumps({
        "version": "1.0",
        "artifacts": [{"report": {"path": "%s.Report" % NAME}}],
        "settings": {"enableAutoRecovery": True},
    }, indent=2))

    total = sum(len(f) for _, _, f in os.walk(base) if True)
    print("wrote powerbi/%s.pbip" % NAME)
    for root, _, files in sorted(os.walk(base)):
        for f in sorted(files):
            p = os.path.relpath(os.path.join(root, f), ROOT)
            if NAME in p:
                print("  " + p)


if __name__ == "__main__":
    main()
