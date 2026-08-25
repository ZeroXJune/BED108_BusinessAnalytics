"""
BED 106 Business Analytics - Mini Capstone: Sales Trend Analysis
Checkpoint 1, Task 1.2 / 1.3

Cleans the raw Kaggle-style sales export and loads it into a normalised
star schema. Produces:
    data/processed/*.csv   one file per table, ready for MySQL LOAD DATA
    sql/03_insert_data.sql portable INSERT statements (MySQL / SQLite)
    data/sales_trend.db    a populated SQLite database used to run the
                           Task 1.4 queries and capture real results
    reports/data_quality_report.md

Run:  python3 scripts/clean_and_load.py
"""

import csv
import os
import re
import sqlite3
from collections import Counter, defaultdict
from datetime import date, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw", "sales_dataset_raw.csv")
PROCESSED = os.path.join(ROOT, "data", "processed")
DB_PATH = os.path.join(ROOT, "data", "sales_trend.db")
SCHEMA_SQL = os.path.join(ROOT, "sql", "01_schema_sqlite.sql")
INSERT_SQL = os.path.join(ROOT, "sql", "03_insert_data.sql")
QUALITY_MD = os.path.join(ROOT, "reports", "data_quality_report.md")

# The raw file ends mid-March 2025, so the final year is incomplete. Trend
# work reports it separately instead of reading the drop as a real decline.
LAST_COMPLETE_YEAR = 2024

MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"]


def titlecase(value):
    """Collapse whitespace and normalise casing on free-text labels."""
    return re.sub(r"\s+", " ", value).strip().title()


def read_raw():
    with open(RAW, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def profile(rows):
    """Collect the evidence quoted in the Task 1.2 quality assessment."""
    issues = {}
    cols = list(rows[0].keys())

    issues["row_count"] = len(rows)
    issues["column_count"] = len(cols)
    issues["missing"] = {
        c: sum(1 for r in rows if r[c] is None or not r[c].strip()) for c in cols
    }

    exact = Counter(tuple(r[c] for c in cols) for r in rows)
    issues["exact_duplicates"] = sum(n - 1 for n in exact.values() if n > 1)

    line_key = Counter(
        (r["Order ID"], r["Order Date"], r["CustomerName"], r["Sub-Category"])
        for r in rows
    )
    issues["near_duplicates"] = sum(n - 1 for n in line_key.values() if n > 1)

    by_order = defaultdict(list)
    for r in rows:
        by_order[r["Order ID"]].append(r)
    issues["order_ids"] = len(by_order)
    issues["order_ids_reused"] = sum(
        1 for g in by_order.values()
        if len({r["Order Date"] for r in g}) > 1
        or len({r["CustomerName"] for r in g}) > 1
    )

    issues["ym_mismatch"] = sum(
        1 for r in rows if r["Order Date"][:7] != r["Year-Month"]
    )

    names = defaultdict(set)
    for r in rows:
        names[r["CustomerName"]].add((r["State"], r["City"]))
    issues["customer_names"] = len(names)
    issues["names_in_multiple_cities"] = sum(1 for v in names.values() if len(v) > 1)

    dates = sorted(r["Order Date"] for r in rows)
    issues["date_min"], issues["date_max"] = dates[0], dates[-1]
    issues["rows_per_year"] = dict(sorted(Counter(d[:4] for d in dates).items()))

    issues["negative_amount"] = sum(1 for r in rows if int(r["Amount"]) < 0)
    issues["negative_profit"] = sum(1 for r in rows if int(r["Profit"]) < 0)
    issues["profit_gt_amount"] = sum(
        1 for r in rows if int(r["Profit"]) > int(r["Amount"])
    )
    issues["quantity_non_positive"] = sum(1 for r in rows if int(r["Quantity"]) < 1)
    return issues


def build_tables(rows):
    """Turn the flat file into the six tables of the star schema."""
    states, cities, categories, subcats, payments, customers, dates_seen = (
        {}, {}, {}, {}, {}, {}, {},
    )
    facts = []

    for r in rows:
        state = titlecase(r["State"])
        city = titlecase(r["City"])
        category = titlecase(r["Category"])
        subcat = titlecase(r["Sub-Category"])
        payment = r["PaymentMode"].strip()
        customer = titlecase(r["CustomerName"])
        order_date = r["Order Date"].strip()

        states.setdefault(state, len(states) + 1)
        # A city is only unique within its state, so key on the pair.
        cities.setdefault((city, state), len(cities) + 1)
        categories.setdefault(category, len(categories) + 1)
        subcats.setdefault((subcat, category), len(subcats) + 1)
        payments.setdefault(payment, len(payments) + 1)
        # CustomerName repeats across cities, so the business key is name+city.
        customers.setdefault((customer, city, state), len(customers) + 1)

        d = datetime.strptime(order_date, "%Y-%m-%d").date()
        dates_seen.setdefault(order_date, d)

        facts.append({
            "order_ref": r["Order ID"].strip(),
            "order_date": order_date,
            "customer_id": customers[(customer, city, state)],
            "sub_category_id": subcats[(subcat, category)],
            "payment_mode_id": payments[payment],
            "quantity": int(r["Quantity"]),
            "amount": int(r["Amount"]),
            "profit": int(r["Profit"]),
        })

    tables = {}

    tables["dim_state"] = (
        ["state_id", "state_name"],
        [[sid, name] for name, sid in sorted(states.items(), key=lambda x: x[1])],
    )
    tables["dim_city"] = (
        ["city_id", "city_name", "state_id"],
        [[cid, city, states[state]]
         for (city, state), cid in sorted(cities.items(), key=lambda x: x[1])],
    )
    tables["dim_category"] = (
        ["category_id", "category_name"],
        [[cid, name] for name, cid in sorted(categories.items(), key=lambda x: x[1])],
    )
    tables["dim_sub_category"] = (
        ["sub_category_id", "sub_category_name", "category_id"],
        [[sid, sub, categories[cat]]
         for (sub, cat), sid in sorted(subcats.items(), key=lambda x: x[1])],
    )
    tables["dim_payment_mode"] = (
        ["payment_mode_id", "payment_mode_name"],
        [[pid, name] for name, pid in sorted(payments.items(), key=lambda x: x[1])],
    )
    tables["dim_customer"] = (
        ["customer_id", "customer_name", "city_id"],
        [[cid, name, cities[(city, state)]]
         for (name, city, state), cid in sorted(customers.items(), key=lambda x: x[1])],
    )

    date_rows = []
    for iso, d in sorted(dates_seen.items()):
        date_rows.append([
            iso, d.year, (d.month - 1) // 3 + 1, d.month, MONTH_NAMES[d.month - 1],
            f"{d.year:04d}-{d.month:02d}",
            1 if d.year <= LAST_COMPLETE_YEAR else 0,
        ])
    tables["dim_date"] = (
        ["order_date", "year_number", "quarter_number", "month_number",
         "month_name", "year_month", "is_complete_year"],
        date_rows,
    )

    fact_rows = []
    for i, f in enumerate(sorted(facts, key=lambda x: (x["order_date"], x["order_ref"])), 1):
        fact_rows.append([
            i, f["order_ref"], f["order_date"], f["customer_id"],
            f["sub_category_id"], f["payment_mode_id"],
            f["quantity"], f["amount"], f["profit"],
        ])
    tables["fact_sales"] = (
        ["sale_id", "order_ref", "order_date", "customer_id", "sub_category_id",
         "payment_mode_id", "quantity", "amount", "profit"],
        fact_rows,
    )
    return tables


LOAD_ORDER = ["dim_state", "dim_city", "dim_category", "dim_sub_category",
              "dim_payment_mode", "dim_customer", "dim_date", "fact_sales"]


def write_csvs(tables):
    os.makedirs(PROCESSED, exist_ok=True)
    for name in LOAD_ORDER:
        header, rows = tables[name]
        with open(os.path.join(PROCESSED, f"{name}.csv"), "w", newline="",
                  encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(header)
            w.writerows(rows)


def sql_literal(v):
    if isinstance(v, int):
        return str(v)
    return "'" + str(v).replace("'", "''") + "'"


def write_inserts(tables):
    with open(INSERT_SQL, "w", encoding="utf-8") as fh:
        fh.write("-- BED 106 Mini Capstone: Sales Trend Analysis\n")
        fh.write("-- Task 1.3 - populate the schema. Generated by "
                 "scripts/clean_and_load.py; do not edit by hand.\n")
        fh.write("-- Runs on MySQL 8 and SQLite 3.\n\n")
        for name in LOAD_ORDER:
            header, rows = tables[name]
            fh.write(f"-- {name}: {len(rows)} rows\n")
            cols = ", ".join(header)
            for i in range(0, len(rows), 100):
                chunk = rows[i:i + 100]
                values = ",\n    ".join(
                    "(" + ", ".join(sql_literal(v) for v in row) + ")" for row in chunk
                )
                fh.write(f"INSERT INTO {name} ({cols}) VALUES\n    {values};\n")
            fh.write("\n")


def build_sqlite(tables):
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON")
    with open(SCHEMA_SQL, encoding="utf-8") as fh:
        con.executescript(fh.read())
    for name in LOAD_ORDER:
        header, rows = tables[name]
        placeholders = ", ".join("?" * len(header))
        con.executemany(
            f"INSERT INTO {name} ({', '.join(header)}) VALUES ({placeholders})", rows
        )
    con.commit()

    # Referential integrity must hold before any Task 1.4 query is trusted.
    violations = con.execute("PRAGMA foreign_key_check").fetchall()
    if violations:
        raise SystemExit(f"Foreign key violations found: {violations[:5]}")
    con.close()


def write_quality_report(issues, tables):
    lines = [
        "# Preliminary Data Quality Assessment",
        "",
        "Generated by `scripts/clean_and_load.py` from "
        "`data/raw/sales_dataset_raw.csv`. Supports Checkpoint 1, Task 1.2.",
        "",
        "## 1. Shape and coverage",
        "",
        "| Measure | Value |",
        "| --- | --- |",
        f"| Rows in raw file | {issues['row_count']:,} |",
        f"| Columns in raw file | {issues['column_count']} |",
        f"| Earliest order date | {issues['date_min']} |",
        f"| Latest order date | {issues['date_max']} |",
        f"| Distinct Order ID values | {issues['order_ids']:,} |",
        f"| Distinct customer names | {issues['customer_names']:,} |",
        "",
        "Rows per calendar year:",
        "",
        "| Year | Rows |",
        "| --- | --- |",
    ]
    for y, n in issues["rows_per_year"].items():
        note = " (partial - ends 15 March)" if y == "2025" else ""
        lines.append(f"| {y} | {n:,}{note} |")

    lines += [
        "",
        "## 2. Missing values",
        "",
        "| Column | Null or blank |",
        "| --- | --- |",
    ]
    for col, n in issues["missing"].items():
        lines.append(f"| {col} | {n} |")
    lines += [
        "",
        "No column contains a null or blank value, so no imputation was needed.",
        "",
        "## 3. Duplicates",
        "",
        f"- Fully identical rows: **{issues['exact_duplicates']}**.",
        f"- Rows repeating the same (Order ID, Order Date, CustomerName, "
        f"Sub-Category) combination: **{issues['near_duplicates']}**. These are "
        "kept as separate transaction lines, since a customer can legitimately "
        "buy the same sub-category twice on one order.",
        f"- `Order ID` is **not** unique: {issues['order_ids']:,} distinct values "
        f"cover {issues['row_count']:,} rows, and "
        f"**{issues['order_ids_reused']}** of them appear against more than one "
        "order date or customer. It is therefore treated as a non-unique "
        "reference label (`order_ref`), not a primary key.",
        "",
        "## 4. Inconsistencies",
        "",
        f"- `Year-Month` is fully derivable from `Order Date` "
        f"({issues['ym_mismatch']} mismatches), so it is redundant and is "
        "recomputed in `dim_date` rather than stored twice.",
        f"- `CustomerName` is not a reliable identifier: "
        f"{issues['names_in_multiple_cities']} names appear in more than one "
        "city, so the customer key is (name, city).",
        f"- Negative `Amount` values: {issues['negative_amount']}; negative "
        f"`Profit` values: {issues['negative_profit']}; rows where profit "
        f"exceeds amount: {issues['profit_gt_amount']}; non-positive "
        f"`Quantity`: {issues['quantity_non_positive']}. The measures are "
        "internally consistent, but note that a dataset with zero loss-making "
        "orders across five years is unusual for real retail and points to a "
        "synthetic or pre-filtered source.",
        "- The 2025 rows stop on 15 March. Any year-on-year trend statement "
        "must exclude 2025 or label it as a partial year; `dim_date."
        "is_complete_year` flags this.",
        "",
        "## 5. Cleaning steps applied",
        "",
        "1. Trimmed surrounding whitespace and normalised casing on all text "
        "labels (`State`, `City`, `Category`, `Sub-Category`, `CustomerName`).",
        "2. Cast `Amount`, `Profit` and `Quantity` to integers and `Order Date` "
        "to a true date type.",
        "3. Dropped the redundant `Year-Month` column and rebuilt the calendar "
        "attributes in `dim_date`.",
        "4. Replaced the unreliable `Order ID` key with a surrogate primary key "
        "`sale_id`, retaining the original value as `order_ref`.",
        "5. Split the flat file into six dimension tables and one fact table, "
        "assigning surrogate keys and enforcing foreign keys.",
        "6. Verified referential integrity with `PRAGMA foreign_key_check` "
        "after load; the build fails if any violation is found.",
        "",
        "## 6. Loaded row counts",
        "",
        "| Table | Rows |",
        "| --- | --- |",
    ]
    for name in LOAD_ORDER:
        lines.append(f"| `{name}` | {len(tables[name][1]):,} |")
    lines.append("")

    with open(QUALITY_MD, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def main():
    rows = read_raw()
    issues = profile(rows)
    tables = build_tables(rows)
    write_csvs(tables)
    write_inserts(tables)
    build_sqlite(tables)
    write_quality_report(issues, tables)

    print(f"Read {issues['row_count']:,} raw rows.")
    for name in LOAD_ORDER:
        print(f"  {name:20s} {len(tables[name][1]):>6,} rows")
    print(f"SQLite database written to {DB_PATH}")


if __name__ == "__main__":
    main()
