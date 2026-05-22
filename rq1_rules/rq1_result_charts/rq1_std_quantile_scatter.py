"""
1) Scatter plot of rule_count vs mean_score; color = OLS studentized residual of mean_score on rule_count
2) Quantile view: assign quartiles to rule_count and mean_score across n subcategories and list quadrants;
   optional CSV output

std_score vs mean_score correlation is in std_score_mean_score_correlation.py.

Requires: matplotlib.

Subcategory labels default above each point (offset points). If names overlap, set (dx, dy) in
LABEL_OFFSET_POINTS for the subcategory.

Examples:
  python3 rq1_std_quantile_scatter.py
  python3 rq1_std_quantile_scatter.py --out fig.pdf --dpi 300
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path
from typing import List, Sequence, Tuple

import os

_mpl_cache = Path(__file__).resolve().parent / ".matplotlib-cache"
_mpl_cache.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_mpl_cache))

# Optional: label offset per subcategory string from CSV (points, relative to data point).
# Default (0, 12) is directly above. E.g.: {"Workflow Conventions": (40, 8)}
LABEL_OFFSET_POINTS: dict[str, tuple[float, float]] = {
    "Workflow Conventions": (-20, 8),
    "Logging Standards": (-15, -20),
    "Code Review": (30,10),
    "Environment Configuration": (0, -20),
    "System Architecture": (0, 8),
    "AI Context Management": (0, -20),
    "Business Logic": (0, -20),
    "Security Practices": (60, -7),
    "Language Features": (-65, -7),
    "Error & Exception Handling": (0, -20),
    "AI Behavior & Decision Strategies": (40, -20),
    "Framework Usage": (-20,8),
    "Project Documentation": (-70,-7),
    "Design Principles & Patterns": (0,8)
}
DEFAULT_LABEL_OFFSET: tuple[float, float] = (0, 10)


def _configure_matplotlib_fonts(plt_mod) -> None:
    import platform

    if platform.system() == "Darwin":
        plt_mod.rcParams["font.sans-serif"] = [
            "PingFang SC",
            "Heiti SC",
            "Arial Unicode MS",
            "DejaVu Sans",
        ]
    else:
        plt_mod.rcParams["font.sans-serif"] = [
            "Noto Sans CJK SC",
            "WenQuanYi Zen Hei",
            "DejaVu Sans",
        ]
    plt_mod.rcParams["axes.unicode_minus"] = False


def _apply_publication_style(plt_mod) -> None:
    plt_mod.rcParams.update(
        {
            "font.size": 13,
            "axes.labelsize": 17,
            "axes.titlesize": 14,
            "xtick.labelsize": 13,
            "ytick.labelsize": 13,
            "axes.spines.top": True,
            "axes.spines.right": True,
            "figure.facecolor": "white",
            "axes.facecolor": "#fafafa",
            "axes.edgecolor": "#2a2a2a",
            "axes.linewidth": 1.05,
            "xtick.direction": "out",
            "ytick.direction": "out",
            "xtick.major.width": 1.0,
            "ytick.major.width": 1.0,
            "lines.linewidth": 1.2,
        }
    )


def quantile_linear(sorted_vals: List[float], p: float) -> float:
    m = len(sorted_vals)
    if m == 0:
        return float("nan")
    if m == 1:
        return sorted_vals[0]
    pos = (m - 1) * p
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    t = pos - lo
    return sorted_vals[lo] * (1 - t) + sorted_vals[hi] * t


def quartile_label(v: float, q25: float, q50: float, q75: float) -> int:
    if v <= q25:
        return 1
    if v <= q50:
        return 2
    if v <= q75:
        return 3
    return 4


def ols_studentized(
    x: Sequence[float], y: Sequence[float]
) -> Tuple[float, float, List[float], List[float], List[float], float]:
    n = len(x)
    if n < 3:
        raise ValueError("n must be at least 3")
    xbar = sum(x) / n
    ybar = sum(y) / n
    sxx = sum((xi - xbar) ** 2 for xi in x)
    if sxx <= 0:
        raise ValueError("x has no variation")
    sxy = sum((x[i] - xbar) * (y[i] - ybar) for i in range(n))
    beta1 = sxy / sxx
    beta0 = ybar - beta1 * xbar
    fitted = [beta0 + beta1 * x[i] for i in range(n)]
    residual = [y[i] - fitted[i] for i in range(n)]
    sse = sum(r * r for r in residual)
    mse = sse / (n - 2)
    leverage = [1.0 / n + (x[i] - xbar) ** 2 / sxx for i in range(n)]
    return beta0, beta1, fitted, residual, leverage, mse


def studentized_internal(residual: Sequence[float], leverage: Sequence[float], mse: float) -> List[float]:
    out: List[float] = []
    for i in range(len(residual)):
        denom = mse * (1.0 - leverage[i])
        if denom <= 0:
            out.append(float("nan"))
        else:
            out.append(residual[i] / math.sqrt(denom))
    return out


def load_records(csv_path: Path) -> List[dict]:
    rows: List[dict] = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, skipinitialspace=True)
        if reader.fieldnames is None:
            raise ValueError("CSV has no header row")
        for raw in reader:
            if not any((v or "").strip() for v in raw.values()):
                continue
            row = {k.strip(): (v or "").strip() for k, v in raw.items()}
            for k in ("rule_count", "mean_score", "std_score", "major_category", "subcategory"):
                if k not in row:
                    raise ValueError(f"Missing column: {k}")
            ms = row["mean_score"].replace(" ", "")
            ss = row["std_score"].replace(" ", "")
            try:
                rc = float(row["rule_count"])
                msf = float(ms)
                stf = float(ss)
            except ValueError:
                continue
            rows.append(
                {
                    "major_category": row["major_category"],
                    "subcategory": row["subcategory"],
                    "rule_count": rc,
                    "mean_score": msf,
                    "std_score": stf,
                }
            )
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "csv",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parent / "rq1_rule_survey_distribution_table_data.csv",
    )
    ap.add_argument(
        "--out",
        type=Path,
        dest="out_fig",
        default=Path(__file__).resolve().parent / "scatter_rule_count_mean_score_residual.pdf",
        help="Scatter plot output path (default PDF; use .png etc. for raster)",
    )
    ap.add_argument("--out-quant", type=Path, default=None, help="Optional: write quartile annotation CSV")
    ap.add_argument("--dpi", type=int, default=220)
    args = ap.parse_args()

    if not args.csv.is_file():
        print(f"File not found: {args.csv}", file=sys.stderr)
        return 1

    rec = load_records(args.csv)
    n = len(rec)
    if n < 3:
        print("Insufficient valid rows", file=sys.stderr)
        return 1

    mean_s = [r["mean_score"] for r in rec]
    rule_c = [r["rule_count"] for r in rec]

    _, _, _, resid, lev, mse = ols_studentized(rule_c, mean_s)
    stud = studentized_internal(resid, lev, mse)

    # --- Quartiles ---
    src = sorted(rule_c)
    sm = sorted(mean_s)
    qrc = [quantile_linear(src, p) for p in (0.25, 0.5, 0.75)]
    qms = [quantile_linear(sm, p) for p in (0.25, 0.5, 0.75)]
    rc25, rc50, rc75 = qrc
    ms25, ms50, ms75 = qms

    print("=== Quartiles (empirical quartiles over n subcategories) ===")
    print(f"n = {n}")
    print(f"rule_count: Q1≤{rc25:.1f} <Q2≤{rc50:.1f} <Q3≤{rc75:.1f} <Q4")
    print(f"mean_score: Q1≤{ms25:.3f} <Q2≤{ms50:.3f} <Q3≤{ms75:.3f} <Q4")
    print()

    enriched = []
    for i, r in enumerate(rec):
        rq = quartile_label(r["rule_count"], rc25, rc50, rc75)
        mq = quartile_label(r["mean_score"], ms25, ms50, ms75)
        enriched.append(
            {
                **r,
                "rule_quartile": rq,
                "mean_quartile": mq,
                "studentized_residual": stud[i],
            }
        )

    hi_rule_lo_score = [e for e in enriched if e["rule_quartile"] >= 4 and e["mean_quartile"] <= 1]
    lo_rule_hi_score = [e for e in enriched if e["rule_quartile"] <= 1 and e["mean_quartile"] >= 4]
    hi_rule_lo_score_relax = [e for e in enriched if e["rule_quartile"] >= 3 and e["mean_quartile"] <= 2]
    lo_rule_hi_score_relax = [e for e in enriched if e["rule_quartile"] <= 2 and e["mean_quartile"] >= 3]

    def _lines(label: str, xs: List[dict]) -> None:
        print(f"--- {label} (n={len(xs)}) ---")
        if not xs:
            print("  (none)")
            return
        for e in sorted(xs, key=lambda z: -z["rule_count"]):
            print(
                f"  {e['subcategory'][:48]:48} | RC={e['rule_count']:.0f} Q{e['rule_quartile']} | "
                f"mean={e['mean_score']:.3f} Q{e['mean_quartile']} | std={e['std_score']:.3f}"
            )

    _lines("Strict quadrant: rule Q4 and mean Q1", hi_rule_lo_score)
    print()
    _lines("Strict quadrant: rule Q1 and mean Q4", lo_rule_hi_score)
    print()
    _lines("Relaxed: rule≥Q3 and mean≤Q2 (high rules, low scores)", hi_rule_lo_score_relax)
    print()
    _lines("Relaxed: rule≤Q2 and mean≥Q3 (low rules, high scores)", lo_rule_hi_score_relax)
    print()

    if args.out_quant:
        with args.out_quant.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(
                [
                    "major_category",
                    "subcategory",
                    "rule_count",
                    "mean_score",
                    "std_score",
                    "rule_quartile",
                    "mean_quartile",
                    "studentized_residual",
                ]
            )
            for e in sorted(enriched, key=lambda z: (-z["rule_count"], z["subcategory"])):
                w.writerow(
                    [
                        e["major_category"],
                        e["subcategory"],
                        e["rule_count"],
                        e["mean_score"],
                        e["std_score"],
                        e["rule_quartile"],
                        e["mean_quartile"],
                        round(e["studentized_residual"], 6),
                    ]
                )
        print(f"Wrote quartile table: {args.out_quant}")

    # --- Scatter plot ---
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    _configure_matplotlib_fonts(plt)
    _apply_publication_style(plt)

    fig, ax = plt.subplots(figsize=(12, 7.5))

    s_valid = [s for s in stud if not math.isnan(s)]
    s_min = min(s_valid)
    s_max = max(s_valid)
    if s_max - s_min < 1e-9:
        s_max = s_min + 1e-6

    sc = ax.scatter(
        rule_c,
        mean_s,
        c=stud,
        cmap="viridis",
        vmin=s_min,
        vmax=s_max,
        s=140,
        alpha=0.92,
        edgecolors="none",
        linewidths=0,
        zorder=3,
    )
    cb = fig.colorbar(sc, ax=ax, shrink=0.82, pad=0.02)
    cb.set_label("Studentized Residual", fontsize=16, fontweight="medium")
    cb.ax.tick_params(labelsize=12)

    for e in enriched:
        dx, dy = LABEL_OFFSET_POINTS.get(e["subcategory"], DEFAULT_LABEL_OFFSET)
        ax.annotate(
            e["subcategory"],
            (e["rule_count"], e["mean_score"]),
            xytext=(dx, dy),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=12.5,  # Subcategory label size beside each point; adjust as needed
            color="#1a1a1a",
            alpha=0.95,
            zorder=4,
            clip_on=False,
        )

    ax.axvline(rc25, color="#9e9e9e", linestyle="--", linewidth=1.0, zorder=1, alpha=0.85)
    ax.axvline(rc50, color="#9e9e9e", linestyle="--", linewidth=1.0, zorder=1, alpha=0.85)
    ax.axvline(rc75, color="#9e9e9e", linestyle="--", linewidth=1.0, zorder=1, alpha=0.85)
    ax.axhline(ms25, color="#757575", linestyle=":", linewidth=1.05, zorder=1, alpha=0.9)
    ax.axhline(ms50, color="#757575", linestyle=":", linewidth=1.05, zorder=1, alpha=0.9)
    ax.axhline(ms75, color="#757575", linestyle=":", linewidth=1.05, zorder=1, alpha=0.9)

    ax.set_xlabel("Rule Count", fontweight="medium")
    ax.set_ylabel("Importance Mean Score", fontweight="medium")
    # No main grid; keep quartile reference lines only (axvline / axhline)
    ax.grid(False)
    ax.set_axisbelow(True)

    fig.tight_layout()
    args.out_fig.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out_fig, dpi=args.dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved scatter plot: {args.out_fig}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
