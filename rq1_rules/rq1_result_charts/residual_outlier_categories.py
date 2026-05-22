"""
Identify subcategories with mean_score unusually high/low relative to the overall
linear trend of mean_score on rule_count, using OLS studentized residuals
(regression diagnostics / residual analysis).

Intuition:
- Residual = observed mean_score − score predicted from the linear rule_count trend.
- Large negative residual: at a given rule_count level, mean_score is unusually low
  → may correspond to "many rules but relatively low score" when x is also large.
- Large positive residual: mean_score is above the trend (may correspond to "few rules but high score").

Standard library only. Use --out to write a CSV for tables.

"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Sequence, Tuple


def _t_crit_two_sided(alpha: float, df: int) -> float:
    """Approximate two-sided t critical value (Newton on normal tail + Cornish-Fisher); df>=1."""
    if df < 1:
        return float("inf")
    # Wilson-Hilferty cube-root normal approx to chi2, then invert; simplified scipy-free lookup
    # For df>=5, common-value interpolation is enough for paper reproduction
    target = 1.0 - alpha / 2.0
    # bisection on normal inverse via rational approximation not worth it — use hardcoded common df
    table = {
        1: 12.706,
        2: 4.303,
        3: 3.182,
        4: 2.776,
        5: 2.571,
        6: 2.447,
        7: 2.365,
        8: 2.306,
        9: 2.262,
        10: 2.228,
        15: 2.131,
        20: 2.086,
        23: 2.069,
        24: 2.064,
        25: 2.060,
        30: 2.042,
        40: 2.021,
        60: 2.000,
        120: 1.980,
    }
    if df in table:
        return table[df]
    # Linear interpolation between bracketing keys
    keys = sorted(table)
    if df < keys[0]:
        return table[keys[0]]
    if df > keys[-1]:
        return 1.96  # asymptotic normal
    for a, b in zip(keys, keys[1:]):
        if a <= df <= b:
            return table[a] + (table[b] - table[a]) * (df - a) / (b - a)
    return 2.0


@dataclass
class RowOut:
    major_category: str
    subcategory: str
    rule_count: float
    mean_score: float
    fitted: float
    residual: float
    leverage: float
    studentized: float


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
            for k in ("rule_count", "mean_score", "major_category", "subcategory"):
                if k not in row:
                    raise ValueError(f"Missing column: {k}")
            ms = row["mean_score"].replace(" ", "")
            try:
                rc = float(row["rule_count"])
                msf = float(ms)
            except ValueError:
                continue
            rows.append(
                {
                    "major_category": row["major_category"],
                    "subcategory": row["subcategory"],
                    "rule_count": rc,
                    "mean_score": msf,
                }
            )
    return rows


def ols_studentized(
    x: Sequence[float], y: Sequence[float]
) -> Tuple[float, float, List[float], List[float], List[float], float]:
    """Return beta0, beta1, fitted, residual, leverage, MSE."""
    n = len(x)
    if n < 3:
        raise ValueError("n must be at least 3")
    xbar = sum(x) / n
    ybar = sum(y) / n
    sxx = sum((xi - xbar) ** 2 for xi in x)
    if sxx <= 0:
        raise ValueError("rule_count has no variation")
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


def analyze(
    records: List[dict],
    x_transform: Callable[[float], float],
) -> Tuple[List[RowOut], float, float, float]:
    x = [x_transform(r["rule_count"]) for r in records]
    y = [r["mean_score"] for r in records]
    beta0, beta1, fitted, resid, lev, mse = ols_studentized(x, y)
    stud = studentized_internal(resid, lev, mse)
    outs = [
        RowOut(
            major_category=r["major_category"],
            subcategory=r["subcategory"],
            rule_count=r["rule_count"],
            mean_score=r["mean_score"],
            fitted=fitted[i],
            residual=resid[i],
            leverage=lev[i],
            studentized=stud[i],
        )
        for i, r in enumerate(records)
    ]
    return outs, beta0, beta1, mse


def main() -> int:
    p = argparse.ArgumentParser(
        description="Find subcategories deviating from trend via regression studentized residuals"
    )
    p.add_argument(
        "csv",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parent / "rq1_rule_survey_distribution_table_data.csv",
    )
    p.add_argument(
        "--x-log",
        action="store_true",
        help="Regress on log(x+1) of rule_count (common for right-skewed counts)",
    )
    p.add_argument(
        "--z",
        type=float,
        default=2.0,
        help="|studentized| above this threshold is flagged (default 2; use Bonferroni for formal tests)",
    )
    p.add_argument("--out", type=Path, default=None, help="Write full results CSV")
    args = p.parse_args()

    if not args.csv.is_file():
        print(f"File not found: {args.csv}", file=sys.stderr)
        return 1

    records = load_records(args.csv)
    n = len(records)
    if n < 3:
        print("Insufficient valid rows", file=sys.stderr)
        return 1

    if args.x_log:
        x_tf: Callable[[float], float] = lambda v: math.log(v + 1.0)
        x_label = "log(rule_count+1)"
    else:
        x_tf = lambda v: v
        x_label = "rule_count"

    outs, b0, b1, mse = analyze(records, x_tf)
    df = n - 2
    t_bonf = _t_crit_two_sided(0.05 / n, df)  # pointwise two-sided, Bonferroni

    print(f"Data: {args.csv}  (n={n})")
    print(f"Model: mean_score ~ {x_label}  (OLS linear regression)")
    print(f"Fit: mean_score ≈ {b0:.4f} + {b1:.4f} * ({x_label})")
    print(f"MSE = {mse:.6f}")
    print()
    print("Interpretation (paper-ready wording):")
    print("  Studentized residual measures how far mean_score deviates from the overall linear trend")
    print("  at a given rule_count level; large negative ≈ 'many rules but relatively low score';")
    print("  large positive ≈ 'few rules but relatively high score'.")
    print()
    print(f"Heuristic threshold |studentized| > {args.z:g} (~95% normal rule; residuals not independent, exploratory)")
    print(f"Bonferroni (n={n} pointwise tests, family-wise α=0.05) two-sided critical ≈ |t| > {t_bonf:.3f}")
    print()

    flagged = [o for o in outs if abs(o.studentized) > args.z]
    flagged.sort(key=lambda o: o.studentized)

    print("=== Large negative residuals (below trend: relatively low scores) ===")
    neg = sorted([o for o in outs if o.studentized < 0], key=lambda o: o.studentized)
    for o in neg[:8]:
        print(
            f"  t*={o.studentized:+.2f}  rule_count={o.rule_count:.0f}  mean_score={o.mean_score:.3f}  "
            f"fitted={o.fitted:.3f}  | {o.major_category} / {o.subcategory}"
        )
    print()
    print("=== Large positive residuals (above trend: relatively high scores) ===")
    pos = sorted([o for o in outs if o.studentized > 0], key=lambda o: -o.studentized)
    for o in pos[:8]:
        print(
            f"  t*={o.studentized:+.2f}  rule_count={o.rule_count:.0f}  mean_score={o.mean_score:.3f}  "
            f"fitted={o.fitted:.3f}  | {o.major_category} / {o.subcategory}"
        )
    print()
    print(f"=== Subcategories with |t*|>{args.z:g} (n={len(flagged)}) ===")
    for o in sorted(flagged, key=lambda o: -abs(o.studentized)):
        print(
            f"  t*={o.studentized:+.2f}  rule_count={o.rule_count:.0f}  mean_score={o.mean_score:.3f}  "
            f"| {o.major_category} / {o.subcategory}"
        )

    if args.out:
        with args.out.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(
                [
                    "major_category",
                    "subcategory",
                    "rule_count",
                    "mean_score",
                    "fitted",
                    "residual",
                    "leverage",
                    "studentized_residual",
                ]
            )
            for o in sorted(outs, key=lambda r: -abs(r.studentized)):
                w.writerow(
                    [
                        o.major_category,
                        o.subcategory,
                        o.rule_count,
                        o.mean_score,
                        round(o.fitted, 6),
                        round(o.residual, 6),
                        round(o.leverage, 6),
                        round(o.studentized, 6),
                    ]
                )
        print()
        print(f"Wrote: {args.out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
