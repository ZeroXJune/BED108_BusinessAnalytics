"""
Builds the charts used in the Checkpoint 1 report from the populated
warehouse. Output: docs/figures/*.png

Run:  python3 scripts/make_figures.py
"""

import os
import sqlite3

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "sales_trend.db")
FIG_DIR = os.path.join(ROOT, "docs", "figures")

INK = "#1f2933"
MUTED = "#7b8794"
ACCENT = "#2f6f9f"
WARM = "#c96f3f"
SERIES = ["#2f6f9f", "#c96f3f", "#5c9e73"]

thousands = FuncFormatter(lambda v, _: f"{v/1000:,.0f}k")


def style(ax):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.grid(axis="y", color="#e4e7eb", linewidth=0.8)
    ax.set_axisbelow(True)


def save(fig, name):
    path = os.path.join(FIG_DIR, name)
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", path)


def fig_annual_trend(con):
    # Per month, not per year: 2020 holds only nine complete months, so raw
    # annual totals would overstate the growth out of 2020.
    rows = con.execute("""
        SELECT d.year_number,
               SUM(f.amount) / COUNT(DISTINCT d.year_month),
               SUM(f.profit) / COUNT(DISTINCT d.year_month)
        FROM sales f JOIN dates d ON d.order_date = f.order_date
        WHERE d.is_complete_year = 1 AND d.is_complete_month = 1
        GROUP BY d.year_number ORDER BY d.year_number
    """).fetchall()
    years = [str(r[0]) for r in rows]
    revenue = [r[1] for r in rows]
    profit = [r[2] for r in rows]

    fig, ax = plt.subplots(figsize=(7.5, 4))

    # The same two regimes marked on the Checkpoint 2 forecast chart: growth
    # to the 2022 peak, then a plateau. 2022 is the boundary, so it belongs to
    # both and the bands meet at its centre.
    peak = years.index("2022")
    ax.axvspan(-0.5, peak, color=ACCENT, alpha=0.06)
    ax.axvspan(peak, len(years) - 0.5, color=WARM, alpha=0.06)

    ax.bar(years, revenue, color=ACCENT, width=0.6, label="Revenue")
    ax.bar(years, profit, color="#9fc3dd", width=0.6, label="Profit")
    for x, v in zip(years, revenue):
        label = f"{v/1000:,.0f}k" + ("*" if x == "2020" else "")
        ax.text(x, v + 2500, label, ha="center", fontsize=9, color=INK)
    growth = 100 * (revenue[peak] / revenue[0] - 1)
    plateau = 100 * (revenue[-1] / revenue[peak] - 1)
    ax.text((peak - 0.5) / 2, max(revenue) * 1.09, f"GROWTH  +{growth:.1f}%",
            ha="center", fontsize=9, color=ACCENT, fontweight="bold")
    ax.text((peak + len(years) - 0.5) / 2, max(revenue) * 1.09,
            f"PLATEAU  \u2212{abs(plateau):.1f}%", ha="center", fontsize=9,
            color=WARM, fontweight="bold")

    style(ax)
    ax.yaxis.set_major_formatter(thousands)
    ax.set_ylim(0, max(revenue) * 1.18)
    ax.set_xlim(-0.5, len(years) - 0.5)
    ax.set_title("The trend in two regimes: growth to 2022, then plateau",
                 color=INK, fontsize=12, fontweight="bold", loc="left")
    ax.set_ylabel("Revenue per month", color=MUTED, fontsize=9)
    ax.text(0, -0.27, "* 2020 covers nine complete months (the file starts "
                      "22 March 2020), so all years are shown per month.",
            transform=ax.transAxes, fontsize=8, color=MUTED)
    ax.legend(frameon=False, fontsize=9, labelcolor=MUTED, ncol=2,
              loc="upper center", bbox_to_anchor=(0.5, -0.10))
    save(fig, "fig1_annual_trend.png")


def fig_monthly_seasonality(con):
    rows = con.execute("""
        SELECT d.month_number, d.month_name, SUM(f.amount)
        FROM sales f JOIN dates d ON d.order_date = f.order_date
        WHERE d.is_complete_year = 1 AND d.is_complete_month = 1
        GROUP BY d.month_number, d.month_name ORDER BY d.month_number
    """).fetchall()
    labels = [r[1][:3] for r in rows]
    values = [r[2] for r in rows]
    mean = sum(values) / len(values)

    fig, ax = plt.subplots(figsize=(7.5, 4))
    colors = [ACCENT if v >= mean else "#c3cbd3" for v in values]
    ax.bar(labels, values, color=colors, width=0.65)
    ax.axhline(mean, color=MUTED, linestyle="--", linewidth=1)
    ax.text(11.4, mean * 1.03, "5-year average", ha="right",
            fontsize=8, color=MUTED)
    style(ax)
    ax.yaxis.set_major_formatter(thousands)
    ax.set_title("Demand concentrates in October and December",
                 color=INK, fontsize=12, fontweight="bold", loc="left")
    ax.set_ylabel("Revenue, 2020–2024 pooled", color=MUTED, fontsize=9)
    save(fig, "fig2_monthly_seasonality.png")


def fig_category_trend(con):
    rows = con.execute("""
        SELECT c.category_name, d.year_number, SUM(f.amount)
        FROM sales f
        JOIN dates d ON d.order_date = f.order_date
        JOIN sub_categories s ON s.sub_category_id = f.sub_category_id
        JOIN categories c ON c.category_id = s.category_id
        WHERE d.is_complete_year = 1
        GROUP BY c.category_name, d.year_number
        ORDER BY c.category_name, d.year_number
    """).fetchall()
    cats = sorted({r[0] for r in rows})
    years = sorted({r[1] for r in rows})

    fig, ax = plt.subplots(figsize=(7.5, 4))
    for i, cat in enumerate(cats):
        vals = [next(r[2] for r in rows if r[0] == cat and r[1] == y)
                for y in years]
        ax.plot(years, vals, marker="o", color=SERIES[i], linewidth=2,
                markersize=5, label=cat)
        ax.text(years[-1] + 0.08, vals[-1], cat, color=SERIES[i],
                fontsize=9, va="center")
    style(ax)
    ax.yaxis.set_major_formatter(thousands)
    ax.set_xticks(years)
    ax.set_xlim(years[0] - 0.15, years[-1] + 1.15)
    ax.set_title("Electronics reversed in 2024 while Office Supplies rebounded",
                 color=INK, fontsize=12, fontweight="bold", loc="left")
    ax.set_ylabel("Revenue", color=MUTED, fontsize=9)
    save(fig, "fig3_category_trend.png")


def main():
    os.makedirs(FIG_DIR, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    fig_annual_trend(con)
    fig_monthly_seasonality(con)
    fig_category_trend(con)
    con.close()


if __name__ == "__main__":
    main()
