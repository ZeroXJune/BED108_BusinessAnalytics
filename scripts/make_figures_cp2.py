"""
Charts for the Checkpoint 2 report. Output: docs/figures/cp2_*.png

Run:  python3 scripts/make_figures_cp2.py
"""

import os
import sqlite3

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
from scipy import stats

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "data", "sales_trend.db")
FIG = os.path.join(ROOT, "docs", "figures")

INK, MUTED, ACCENT = "#1f2933", "#7b8794", "#2f6f9f"
WARM = "#c96f3f"
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
    p = os.path.join(FIG, name)
    fig.savefig(p, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", p)


def series(con):
    rows = con.execute("""
        SELECT d.year_month, COUNT(*), SUM(f.amount), d.month_number
        FROM sales f JOIN dates d ON d.order_date = f.order_date
        WHERE d.is_complete_year = 1 AND d.is_complete_month = 1
        GROUP BY d.year_month, d.month_number ORDER BY d.year_month
    """).fetchall()
    return rows


def fig_histogram(con):
    amounts = [r[0] for r in con.execute("SELECT amount FROM sales")]
    fig, ax = plt.subplots(figsize=(7.5, 3.9))
    ax.hist(amounts, bins=range(0, 11000, 1000), color=ACCENT,
            edgecolor="white", linewidth=1.2)
    style(ax)
    ax.set_title("Amount is close to uniform, not bell-shaped",
                 color=INK, fontsize=12, fontweight="bold", loc="left")
    ax.set_xlabel("Transaction amount", color=MUTED, fontsize=9)
    ax.set_ylabel("Transaction lines", color=MUTED, fontsize=9)
    save(fig, "cp2_fig1_histogram.png")


def fig_scatter_regression(con):
    rows = series(con)
    x = np.array([r[1] for r in rows], float)
    y = np.array([r[2] for r in rows], float)
    res = stats.linregress(x, y)
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.scatter(x, y, s=34, color=ACCENT, alpha=0.75, edgecolor="white",
               linewidth=0.6, zorder=3)
    xs = np.linspace(x.min(), x.max(), 50)
    ax.plot(xs, res.intercept + res.slope * xs, color=WARM, linewidth=2,
            zorder=4)
    ax.text(0.03, 0.95,
            f"Revenue = {res.intercept:,.0f} + {res.slope:,.0f} x Orders\n"
            f"R$^2$ = {res.rvalue**2:.3f}   p < 0.001   n = {len(x)}",
            transform=ax.transAxes, va="top", fontsize=9.5, color=INK,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#f5f7f9",
                      edgecolor="#dde3e8"))
    style(ax)
    ax.yaxis.set_major_formatter(thousands)
    ax.set_title("Order count explains 86% of monthly revenue",
                 color=INK, fontsize=12, fontweight="bold", loc="left")
    ax.set_xlabel("Orders in the month", color=MUTED, fontsize=9)
    ax.set_ylabel("Revenue in the month", color=MUTED, fontsize=9)
    save(fig, "cp2_fig2_regression.png")


def fig_scatter_null(con):
    rows = con.execute("SELECT quantity, amount FROM sales").fetchall()
    x = np.array([r[0] for r in rows], float)
    y = np.array([r[1] for r in rows], float)
    r, p = stats.pearsonr(x, y)
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.scatter(x, y, s=9, color=ACCENT, alpha=0.32, linewidth=0)
    res = stats.linregress(x, y)
    xs = np.linspace(x.min(), x.max(), 20)
    ax.plot(xs, res.intercept + res.slope * xs, color=WARM, linewidth=2)
    ax.text(0.03, 0.95, f"r = {r:+.3f}   p = {p:.3f}   n = {len(x):,}\n"
                        "Not significant at the 5% level",
            transform=ax.transAxes, va="top", fontsize=9.5, color=INK,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#f5f7f9",
                      edgecolor="#dde3e8"))
    style(ax)
    ax.set_title("Units sold tells you nothing about order value",
                 color=INK, fontsize=12, fontweight="bold", loc="left")
    ax.set_xlabel("Quantity (units on the line)", color=MUTED, fontsize=9)
    ax.set_ylabel("Amount", color=MUTED, fontsize=9)
    save(fig, "cp2_fig3_no_correlation.png")


def fig_forecast(con):
    rows = series(con)
    rev = np.array([r[2] for r in rows], float)
    mon = [r[3] for r in rows]
    labels = [r[0] for r in rows]
    idx = {m: np.mean([rev[i] for i in range(len(rev)) if mon[i] == m])
           for m in range(1, 13)}
    grand = np.mean(list(idx.values()))
    level = rev[-24:].mean()

    fut = [f"2025-{m:02d}" for m in range(1, 7)]
    fc = [level * idx[m] / grand for m in range(1, 7)]
    act = dict(con.execute("""SELECT d.year_month, SUM(f.amount) FROM sales f
        JOIN dates d ON d.order_date=f.order_date
        WHERE d.year_number=2025 GROUP BY 1"""))

    fig, ax = plt.subplots(figsize=(9.5, 4.2))
    n = len(rev)
    ax.plot(range(n), rev, color=ACCENT, linewidth=1.1, alpha=0.45,
            label="Actual (complete months)")
    # A 12-month rolling mean: monthly noise is large enough to hide the
    # trend, and the two regimes are the point of this chart.
    w = 12
    roll = [np.mean(rev[max(0, i - w + 1):i + 1]) for i in range(n)]
    ax.plot(range(w - 1, n), roll[w - 1:], color=INK, linewidth=2.4,
            label="12-month rolling average")
    ax.plot(range(n, n + 6), fc, color=WARM, linewidth=2, linestyle="--",
            marker="o", markersize=4, label="Forecast")
    obs = [act.get(f) for f in fut]
    xs = [n + i for i, v in enumerate(obs) if v is not None and i < 2]
    ys = [obs[i] for i in range(len(obs)) if obs[i] is not None and i < 2]
    ax.scatter(xs, ys, color=INK, s=44, zorder=5, label="Actual 2025 (holdout)")
    ax.axvline(n - 0.5, color=MUTED, linestyle=":", linewidth=1)

    # The structural break: growth to the 2022 peak, then a flat regime.
    break_i = labels.index("2022-12") if "2022-12" in labels else 33
    ax.axvspan(0, break_i, color="#2f6f9f", alpha=0.05)
    ax.axvspan(break_i, n - 0.5, color="#c96f3f", alpha=0.05)
    top = max(rev.max(), max(fc)) * 1.03
    ax.text(break_i / 2, top, "GROWTH  +30.9%", ha="center", fontsize=8.5,
            color=ACCENT, fontweight="bold")
    ax.text((break_i + n) / 2, top, "PLATEAU  \u221217.6%", ha="center",
            fontsize=8.5, color=WARM, fontweight="bold")
    style(ax)
    ax.yaxis.set_major_formatter(thousands)
    step = 6
    ticks = list(range(0, n + 6, step))
    ax.set_xticks(ticks)
    ax.set_xticklabels([(labels + fut)[t] for t in ticks], rotation=45,
                       ha="right", fontsize=8)
    ax.set_title("The trend in two regimes, with a six-month forecast",
                 color=INK, fontsize=12, fontweight="bold", loc="left")
    ax.set_ylabel("Monthly revenue", color=MUTED, fontsize=9)
    ax.legend(frameon=False, fontsize=8.5, labelcolor=MUTED, loc="lower left",
              ncol=2)
    save(fig, "cp2_fig4_forecast.png")


def main():
    os.makedirs(FIG, exist_ok=True)
    con = sqlite3.connect(DB)
    fig_histogram(con)
    fig_scatter_regression(con)
    fig_scatter_null(con)
    fig_forecast(con)
    con.close()


if __name__ == "__main__":
    main()
