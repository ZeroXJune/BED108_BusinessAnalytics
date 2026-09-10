"""
Checkpoint 3, Task 3.1 — dashboard blueprint wireframe.

Draws the three dashboard pages as a labelled layout sketch: what sits where,
which visual type each block is, and which interactive elements act on it.
The brief accepts a hand-drawn or digital wireframe; this is the digital one.

Run:  python3 scripts/make_wireframe.py   →  docs/figures/cp3_fig3_wireframe.png
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "figures", "cp3_fig3_wireframe.png")

INK, MUTED = "#1f2933", "#7b8994"
FILL, EDGE = "#eef3f7", "#2f6f9f"
SLICER_FILL, SLICER_EDGE = "#fdf3e7", "#d09b3e"

# (x, y, w, h, title, subtitle, kind)
PAGES = [
    ("Page 1 — Executive Summary",
     "Is the company still growing?",
     [(0.00, 0.72, 0.235, 0.16, "KPI: Orders/month", "20.0 vs 24.0 peak", "kpi"),
      (0.255, 0.72, 0.235, 0.16, "KPI: Revenue/month", "100,206 vs 121,648", "kpi"),
      (0.510, 0.72, 0.235, 0.16, "KPI: Margin %", "25.64%", "kpi"),
      (0.765, 0.72, 0.235, 0.16, "KPI: Gap to peak", "−17.6%", "kpi"),
      (0.00, 0.20, 0.66, 0.46, "Line chart — revenue per month",
       "57-month series, two regimes shaded", "visual"),
      (0.68, 0.20, 0.32, 0.46, "Table — year summary",
       "months_covered shown", "visual"),
      (0.00, 0.02, 1.00, 0.12, "Slicers:  Year  ·  Category",
       "act on every visual on this page", "slicer")]),

    ("Page 2 — Trend & Comparison",
     "Which categories drive the trend?",
     [(0.00, 0.56, 0.49, 0.36, "Line chart — revenue by category",
       "three lines, monthly", "visual"),
      (0.51, 0.56, 0.49, 0.36, "Bar chart — sub-category change",
       "2023 vs 2024, sorted", "visual"),
      (0.00, 0.18, 0.49, 0.32, "Column chart — quarter share by category",
       "small multiples, one per category", "visual"),
      (0.51, 0.18, 0.49, 0.32, "Bar chart — margin by sub-category",
       "ranks differently from revenue", "visual"),
      (0.00, 0.02, 1.00, 0.12, "Slicers:  Year  ·  Category  ·  State",
       "drill-through to Page 3 on any bar", "slicer")]),

    ("Page 3 — Deep Dive & Segmentation",
     "Who and what are the segments?",
     [(0.00, 0.56, 0.55, 0.36, "Scatter — sub-category segments",
       "k-means, 3 clusters, bubble = revenue", "visual"),
      (0.57, 0.56, 0.43, 0.36, "Scatter — customer segments",
       "k-means, 3 clusters, n = 807", "visual"),
      (0.00, 0.18, 0.32, 0.32, "Table — segment profile",
       "n, revenue, margin per segment", "visual"),
      (0.34, 0.18, 0.32, 0.32, "Map — state revenue",
       "28% spread: not a driver", "visual"),
      (0.68, 0.18, 0.32, 0.32, "Scatter — quantity vs amount",
       "r = 0.045: the negative result", "visual"),
      (0.00, 0.02, 1.00, 0.12, "Slicers:  Segment  ·  Category  ·  Year",
       "segment slicer is the page's spine", "slicer")]),
]


def draw_page(ax, title, purpose, blocks):
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.06)
    ax.axis("off")
    ax.text(0, 1.02, title, fontsize=12, fontweight="bold", color=INK, va="top")
    ax.text(0, 0.955, purpose, fontsize=9, color=MUTED, va="top", style="italic")

    for x, y, w, h, label, sub, kind in blocks:
        fill, edge = (SLICER_FILL, SLICER_EDGE) if kind == "slicer" else (FILL, EDGE)
        style = "round,pad=0,rounding_size=0.012"
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=style,
                                    linewidth=1.2, edgecolor=edge,
                                    facecolor=fill,
                                    linestyle="--" if kind == "slicer" else "-"))
        ax.text(x + w / 2, y + h / 2 + (0.022 if sub else 0), label,
                ha="center", va="center", fontsize=8.4,
                fontweight="bold" if kind == "kpi" else "normal", color=INK)
        if sub:
            ax.text(x + w / 2, y + h / 2 - 0.028, sub, ha="center", va="center",
                    fontsize=7.2, color=MUTED)


def main():
    fig, axes = plt.subplots(3, 1, figsize=(9.5, 13.5))
    for ax, (title, purpose, blocks) in zip(axes, PAGES):
        draw_page(ax, title, purpose, blocks)
    fig.suptitle("Checkpoint 3 — Dashboard Blueprint (Task 3.1)",
                 fontsize=14, fontweight="bold", color=INK, y=0.995)
    fig.tight_layout(rect=(0, 0, 1, 0.985))
    fig.savefig(OUT, dpi=160)
    plt.close(fig)
    print("wrote", os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()
