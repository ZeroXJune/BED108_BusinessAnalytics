"""
Checkpoint 4, Task 4.1 — predictive analytics.

Extends the Checkpoint 2 simple regression to a multiple regression on the
same 57-month window, then tests whether the extension was worth making.

Three models are fitted and compared:

  A  revenue ~ orders                      the Checkpoint 2 baseline
  B  every candidate predictor             to expose the multicollinearity
  C  the reduced model, chosen on          what is actually reported
     adjusted R² and significance

Reports coefficients with standard errors, t and p; R² and adjusted R²; the
overall F test; VIF for every predictor; and residual diagnostics
(Durbin-Watson, Shapiro-Wilk, a Breusch-Pagan style check). Validates on a
six-month holdout the models never see.

Run:  python3 scripts/build_predictive_model.py
      → docs/figures/cp4_fig1_actual_vs_predicted.png
      → docs/figures/cp4_fig2_residuals.png
      → reports/predictive_model_results.md
"""

import os
import sqlite3

import numpy as np
from scipy import stats

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "data", "sales_trend.db")
VIEWS = os.path.join(ROOT, "sql", "06_dashboard_views.sql")
FIGDIR = os.path.join(ROOT, "docs", "figures")
OUT = os.path.join(ROOT, "reports", "predictive_model_results.md")

HOLDOUT = 6                      # last six months of the window, never fitted
INK, GRID = "#1f2933", "#d9e0e6"
BLUE, RED, GREEN = "#2f6f9f", "#c1666b", "#5b8c5a"


# --------------------------------------------------------------------- data

def load():
    conn = sqlite3.connect(DB)
    conn.executescript(open(VIEWS).read())
    rows = conn.execute("""
        SELECT m.year_month, m.quarter_number, m.transaction_lines,
               m.units_sold, m.revenue,
               (SELECT COUNT(DISTINCT s.customer_id) FROM sales s
                  JOIN dates d ON d.order_date = s.order_date
                 WHERE d.year_month = m.year_month)            AS customers,
               (SELECT COUNT(*) FROM sales s
                  JOIN dates d ON d.order_date = s.order_date
                  JOIN sub_categories sc
                    ON sc.sub_category_id = s.sub_category_id
                  JOIN categories cat ON cat.category_id = sc.category_id
                 WHERE d.year_month = m.year_month
                   AND cat.category_name = 'Electronics')      AS elec_lines
        FROM v_monthly m
        WHERE m.in_analysis_window = 1
        ORDER BY m.year_month
    """).fetchall()
    conn.close()

    months = [r[0] for r in rows]
    quarter = np.array([r[1] for r in rows])
    orders = np.array([r[2] for r in rows], float)
    units = np.array([r[3] for r in rows], float)
    revenue = np.array([r[4] for r in rows], float)
    customers = np.array([r[5] for r in rows], float)
    # Share of *lines*, not of revenue: a revenue share would be computed from
    # the target and leak it back into the model.
    elec_share = np.array([r[6] for r in rows], float) / orders
    time_idx = np.arange(len(rows), dtype=float)

    feats = {
        "orders": orders,
        "units": units,
        "customers": customers,
        "elec_line_share": elec_share,
        "time_index": time_idx,
        "Q2": (quarter == 2).astype(float),
        "Q3": (quarter == 3).astype(float),
        "Q4": (quarter == 4).astype(float),
    }
    return months, revenue, feats


# ------------------------------------------------------------------ fitting

class OLS:
    """Ordinary least squares with the inference the brief asks to report."""

    def __init__(self, y, X, names):
        self.names = ["intercept"] + list(names)
        self.X = np.column_stack([np.ones(len(y)), X])
        self.y = y
        n, p = self.X.shape
        self.n, self.p = n, p
        xtx_inv = np.linalg.inv(self.X.T @ self.X)
        self.beta = xtx_inv @ self.X.T @ y
        self.fitted = self.X @ self.beta
        self.resid = y - self.fitted
        rss = float(self.resid @ self.resid)
        tss = float(((y - y.mean()) ** 2).sum())
        self.df = n - p
        self.sigma2 = rss / self.df
        self.se = np.sqrt(np.diag(self.sigma2 * xtx_inv))
        self.t = self.beta / self.se
        self.pvals = 2 * stats.t.sf(np.abs(self.t), self.df)

        # Heteroscedasticity-consistent (HC1) standard errors. The
        # Breusch-Pagan test on this data rejects constant variance, which
        # makes the classical standard errors above unreliable; these do not
        # assume it. The coefficients are unchanged — only their precision is.
        meat = self.X.T @ np.diag(self.resid ** 2) @ self.X
        hc1 = xtx_inv @ meat @ xtx_inv * (n / self.df)
        self.se_robust = np.sqrt(np.diag(hc1))
        self.t_robust = self.beta / self.se_robust
        self.p_robust = 2 * stats.t.sf(np.abs(self.t_robust), self.df)
        self.r2 = 1 - rss / tss
        self.adj_r2 = 1 - (1 - self.r2) * (n - 1) / self.df
        self.f = (tss - rss) / (p - 1) / self.sigma2
        self.f_p = stats.f.sf(self.f, p - 1, self.df)
        self.rss = rss

    def predict(self, X):
        return np.column_stack([np.ones(len(X)), X]) @ self.beta

    def table(self):
        out = []
        for i, nm in enumerate(self.names):
            out.append((nm, self.beta[i], self.se[i], self.t[i], self.pvals[i],
                        self.se_robust[i], self.p_robust[i]))
        return out


def vif(X, names):
    """Variance inflation factor: how far each predictor is explained by the rest."""
    out = []
    for i in range(X.shape[1]):
        others = np.delete(X, i, axis=1)
        m = OLS(X[:, i], others, [f"x{j}" for j in range(others.shape[1])])
        out.append((names[i], 1 / max(1 - m.r2, 1e-12)))
    return out


def durbin_watson(e):
    return float(((np.diff(e)) ** 2).sum() / (e ** 2).sum())


def breusch_pagan(model):
    """Regress squared residuals on the fitted values; a significant slope
    means the error variance moves with the prediction."""
    m = OLS(model.resid ** 2, model.fitted.reshape(-1, 1), ["fitted"])
    return m.pvals[1]


def report(model, label):
    print("\n%s" % label)
    print("  %-18s %12s %10s %8s %10s %10s %10s"
          % ("term", "coef", "std err", "t", "p", "robust se", "robust p"))
    for nm, b, se, t, p, rse, rp in model.table():
        star = "  *" if rp < 0.05 else ""
        print("  %-18s %12.2f %10.2f %8.2f %10.4g %10.2f %10.4g%s"
              % (nm, b, se, t, p, rse, rp, star))
    print("  n=%d  df=%d  R²=%.4f  adj R²=%.4f  F=%.2f (p=%.3g)"
          % (model.n, model.df, model.r2, model.adj_r2, model.f, model.f_p))


# --------------------------------------------------------------------- main

def main():
    months, revenue, feats = load()
    n = len(months)
    split = n - HOLDOUT
    print("57-month window: %s to %s; training on %d, holding out %d (%s to %s)"
          % (months[0], months[-1], split, HOLDOUT, months[split], months[-1]))

    full_names = ["orders", "units", "customers", "elec_line_share",
                  "time_index", "Q2", "Q3", "Q4"]
    Xfull = np.column_stack([feats[k] for k in full_names])

    # --- Model A: the Checkpoint 2 baseline, refitted on the training window
    a_names = ["orders"]
    Xa = np.column_stack([feats[k] for k in a_names])
    A = OLS(revenue[:split], Xa[:split], a_names)
    report(A, "Model A — the Checkpoint 2 baseline, revenue ~ orders")

    # --- Model B: everything, to show why everything is the wrong answer
    B = OLS(revenue[:split], Xfull[:split], full_names)
    report(B, "Model B — all eight candidate predictors")
    print("\n  variance inflation factors (>5 is a problem, >10 is severe):")
    for nm, v in vif(Xfull[:split], full_names):
        flag = "  SEVERE" if v > 10 else ("  high" if v > 5 else "")
        print("    %-18s %6.2f%s" % (nm, v, flag))

    # --- Model C: reduced. Drop the collinear counts, keep calendar structure.
    c_names = ["orders", "Q2", "Q3", "Q4", "elec_line_share"]
    Xc = np.column_stack([feats[k] for k in c_names])
    C = OLS(revenue[:split], Xc[:split], c_names)
    report(C, "Model C — reduced: orders, quarter, category mix")
    print("\n  VIF after reduction:")
    for nm, v in vif(Xc[:split], c_names):
        print("    %-18s %6.2f" % (nm, v))

    print("\nResidual diagnostics (Model C, training window)")
    dw = durbin_watson(C.resid)
    sw_p = stats.shapiro(C.resid).pvalue
    bp_p = breusch_pagan(C)
    print("  Durbin-Watson        %.3f   (2.0 = no autocorrelation)" % dw)
    print("  Shapiro-Wilk p       %.4f  (>0.05 = residuals pass as normal)" % sw_p)
    print("  Breusch-Pagan p      %.4f  (>0.05 = constant variance holds)" % bp_p)

    print("\nHoldout — six months never fitted")
    print("  %-9s %11s %11s %11s %11s" % ("month", "actual", "A pred", "C pred", "C error"))
    errs = {"A": [], "C": []}
    for i in range(split, n):
        act = revenue[i]
        pa = float(A.predict(Xa[i:i + 1])[0])
        pc = float(C.predict(Xc[i:i + 1])[0])
        errs["A"].append(abs(pa - act) / act)
        errs["C"].append(abs(pc - act) / act)
        print("  %-9s %11.0f %11.0f %11.0f %10.1f%%"
              % (months[i], act, pa, pc, 100 * (pc - act) / act))
    mape = {k: 100 * float(np.mean(v)) for k, v in errs.items()}
    print("  MAPE   Model A %.1f%%   Model C %.1f%%" % (mape["A"], mape["C"]))
    print("  %s" % ("Model C is the better predictor." if mape["C"] < mape["A"]
                    else "Model A wins: the extra predictors did not pay for themselves."))

    write_outputs(months, revenue, split, A, C, Xa, Xc, mape, dw, sw_p, bp_p,
                  vif(Xfull[:split], full_names), B)


def write_outputs(months, revenue, split, A, C, Xa, Xc, mape, dw, sw_p, bp_p,
                  vifs, B):
    n = len(months)
    pred_c = np.concatenate([C.fitted, C.predict(Xc[split:])])

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(n)
    ax.plot(x, revenue, color=INK, linewidth=1.8, label="Actual")
    ax.plot(x[:split], C.fitted, color=BLUE, linewidth=1.5, label="Model C, fitted")
    ax.plot(x[split:], pred_c[split:], color=RED, linewidth=1.8,
            linestyle="--", marker="o", markersize=4, label="Model C, holdout")
    ax.axvline(split - 0.5, color=GREEN, linewidth=1.0, linestyle=":")
    ax.text(split - 0.3, ax.get_ylim()[1] * 0.97, " holdout begins",
            fontsize=8, color=GREEN, va="top")
    step = 6
    ax.set_xticks(x[::step])
    ax.set_xticklabels([months[i] for i in range(0, n, step)], fontsize=8)
    ax.set_ylabel("Monthly revenue")
    ax.set_title("Multiple regression: actual against predicted monthly revenue\n"
                 "trained on %d months, six held out" % split, color=INK)
    ax.grid(color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "cp4_fig1_actual_vs_predicted.png"), dpi=160)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].scatter(C.fitted, C.resid, s=22, color=BLUE, alpha=0.8,
                    edgecolors="none")
    axes[0].axhline(0, color=INK, linewidth=0.8)
    axes[0].set_xlabel("Fitted value")
    axes[0].set_ylabel("Residual")
    axes[0].set_title("Residuals against fitted", color=INK)
    stats.probplot(C.resid, dist="norm", plot=axes[1])
    axes[1].set_title("Normal Q-Q plot of residuals", color=INK)
    axes[1].get_lines()[0].set_color(BLUE)
    axes[1].get_lines()[0].set_markersize(4)
    axes[1].get_lines()[1].set_color(RED)
    for ax in axes:
        ax.grid(color=GRID, linewidth=0.6)
        ax.set_axisbelow(True)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "cp4_fig2_residuals.png"), dpi=160)
    plt.close(fig)

    def rows(model):
        return "\n".join(
            "| `%s` | %s | %s | %.2f | %s | %s | %s |"
            % (nm, format(round(b, 2), ","), format(round(se, 2), ","), t,
               "%.3g" % p, format(round(rse, 2), ","),
               ("%.3g" % rp) + (" **" if rp < 0.05 else ""))
            for nm, b, se, t, p, rse, rp in model.table())

    with open(OUT, "w") as fh:
        fh.write("""# Checkpoint 4, Task 4.1 — predictive model results

Generated by `scripts/build_predictive_model.py`. Every figure here is
computed; nothing is transcribed by hand.

Window: %s to %s, the same 57 complete months the Checkpoint 2 regression
used. Trained on the first %d, with the last %d held out and never fitted.

## Model A — the Checkpoint 2 baseline

`revenue ~ orders`

| Term | Coefficient | Std error | t | p | Robust SE | Robust p |
| --- | --- | --- | --- | --- | --- | --- |
%s

R² = %.4f, adjusted R² = %.4f, F = %.2f (p = %.3g), n = %d.

## Model B — all eight candidates

Fitted to show why it is not the model reported. R² = %.4f, adjusted
R² = %.4f.

| Term | Coefficient | Std error | t | p | Robust SE | Robust p |
| --- | --- | --- | --- | --- | --- | --- |
%s

### Variance inflation factors

| Predictor | VIF | Reading |
| --- | --- | --- |
%s

## Model C — the reported model

`revenue ~ orders + Q2 + Q3 + Q4 + elec_line_share`

| Term | Coefficient | Std error | t | p | Robust SE | Robust p |
| --- | --- | --- | --- | --- | --- | --- |
%s

R² = %.4f, adjusted R² = %.4f, F = %.2f (p = %.3g), n = %d, df = %d.

## Residual diagnostics

| Test | Statistic | Reading |
| --- | --- | --- |
| Durbin-Watson | %.3f | 2.0 means no autocorrelation |
| Shapiro-Wilk | p = %.4f | above 0.05, residuals pass as normal |
| Breusch-Pagan | p = %.4f | above 0.05, constant variance holds |

## Holdout performance

Mean absolute percentage error over the six held-out months:

| Model | MAPE |
| --- | --- |
| A — orders only | %.1f%% |
| C — reduced multiple | %.1f%% |
""" % (months[0], months[-1], split, n - split,
       rows(A), A.r2, A.adj_r2, A.f, A.f_p, A.n,
       B.r2, B.adj_r2, rows(B),
       "\n".join("| `%s` | %.2f | %s |"
                 % (nm, v, "severe" if v > 10 else
                    ("high" if v > 5 else "acceptable"))
                 for nm, v in vifs),
       rows(C), C.r2, C.adj_r2, C.f, C.f_p, C.n, C.df,
       dw, sw_p, bp_p, mape["A"], mape["C"]))
    print("\nwrote %s" % os.path.relpath(OUT, ROOT))
    print("wrote docs/figures/cp4_fig1_actual_vs_predicted.png")
    print("wrote docs/figures/cp4_fig2_residuals.png")


if __name__ == "__main__":
    main()
