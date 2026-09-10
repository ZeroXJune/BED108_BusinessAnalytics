"""
Exports the Checkpoint 3 dashboard datasets.

Creates the five views from sql/06_dashboard_views.sql against the SQLite
build, exports each to CSV, and verifies the totals against the figures
published in the Checkpoint 1 and Checkpoint 2 reports. Exits non-zero if any
of them disagree, so a dashboard is never built on numbers that have drifted
from the reports.

Power BI, Tableau and Looker Studio all read these CSVs directly; connecting a
BI tool to MySQL and using the views is equivalent.

Run:  python3 scripts/build_dashboard_data.py
"""

import csv
import os
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "data", "sales_trend.db")
VIEWS = os.path.join(ROOT, "sql", "06_dashboard_views.sql")
OUTDIR = os.path.join(ROOT, "data", "dashboard")

EXPORTS = [
    ("v_sales_detail", "sales_detail.csv", "sale_id"),
    ("v_monthly", "monthly.csv", "year_month"),
    ("v_category_month", "category_month.csv",
     "year_month, category_name, sub_category_name"),
    ("v_geography", "geography.csv", "revenue DESC"),
    ("v_annual", "annual.csv", "year_number"),
]

# Every figure here is quoted in a report; if one moves, the report is wrong.
CHECKS = [
    ("detail rows", "SELECT COUNT(*) FROM v_sales_detail", 1194),
    ("total revenue", "SELECT SUM(amount) FROM v_sales_detail", 6182639),
    ("complete months", "SELECT COUNT(*) FROM v_monthly", 59),
    ("analysis months",
     "SELECT COUNT(*) FROM v_monthly WHERE in_analysis_window = 1", 57),
    ("years in window", "SELECT COUNT(*) FROM v_annual", 5),
    ("2022 revenue/month",
     "SELECT revenue_per_month FROM v_annual WHERE year_number = 2022",
     121647.92),
    ("2024 revenue/month",
     "SELECT revenue_per_month FROM v_annual WHERE year_number = 2024",
     100206.50),
    ("2020 months covered",
     "SELECT months_covered FROM v_annual WHERE year_number = 2020", 9),
    ("Printers 2024",
     "SELECT SUM(revenue) FROM v_category_month "
     "WHERE sub_category_name = 'Printers' AND year_number = 2024", 55952),
    ("states", "SELECT COUNT(DISTINCT state_name) FROM v_geography", 6),
]


def main():
    conn = sqlite3.connect(DB)
    conn.executescript(open(VIEWS).read())

    failures = []
    for label, sql, expected in CHECKS:
        got = conn.execute(sql).fetchone()[0]
        ok = abs(got - expected) < 0.005
        print("  %-22s %-14s %s" % (label, got, "ok" if ok else
                                    "MISMATCH, expected %s" % expected))
        if not ok:
            failures.append(label)
    if failures:
        sys.exit("verification failed: %s" % ", ".join(failures))

    os.makedirs(OUTDIR, exist_ok=True)
    for view, filename, order in EXPORTS:
        cur = conn.execute("SELECT * FROM %s ORDER BY %s" % (view, order))
        path = os.path.join(OUTDIR, filename)
        with open(path, "w", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow([d[0] for d in cur.description])
            rows = cur.fetchall()
            writer.writerows(rows)
        print("  wrote %-22s %5d rows" % (filename, len(rows)))
    conn.close()


if __name__ == "__main__":
    main()
