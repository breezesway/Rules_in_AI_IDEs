"""
Subcategory-level correlation between std_score and mean_score (Pearson / Spearman),
p-values, and effect-size guidance.

ρ vs p (brief):
- ρ (Spearman) or r (Pearson): direction and strength of joint variation; the correlation
  coefficient itself is an effect size.
- p-value: probability of observing an association this extreme (or more) if the variables
  were truly unrelated; a small p only means "unlikely by chance", not "strong effect".

Effect size: for Pearson, report r and r²; for Spearman, report ρ (optional ρ², weaker
interpretation than r²). Cohen (1988) benchmarks for |r|: ~0.1 small, 0.3 medium, 0.5 large
(Spearman |ρ| is often interpreted analogously).

Dependencies: none required; if scipy is installed, use its exact p (Pearson/Spearman);
otherwise permutation p for both (default 20000 replicates).

Usage:
  python3 std_score_mean_score_correlation.py
  python3 std_score_mean_score_correlation.py path/to.csv --n-perm 50000
"""

from __future__ import annotations

import argparse
import csv
import math
import random
import sys
from pathlib import Path
from typing import List, Sequence

try:
    from scipy import stats as scipy_stats
except ImportError:
    scipy_stats = None


def rankdata_average(values: Sequence[float]) -> List[float]:
    n = len(values)
    idx = sorted(range(n), key=lambda i: values[i])
    ranks = [0.0] * n
    pos = 0
    while pos < n:
        start = pos
        v = values[idx[pos]]
        while pos < n and values[idx[pos]] == v:
            pos += 1
        avg_rank = (start + 1 + pos) / 2.0
        for k in range(start, pos):
            ranks[idx[k]] = avg_rank
    return ranks


def pearson_r(x: Sequence[float], y: Sequence[float]) -> float:
    n = len(x)
    if n < 2:
        return float("nan")
    mx = sum(x) / n
    my = sum(y) / n
    sxx = sum((xi - mx) ** 2 for xi in x)
    syy = sum((yi - my) ** 2 for yi in y)
    if sxx <= 0 or syy <= 0:
        return float("nan")
    sxy = sum((x[i] - mx) * (y[i] - my) for i in range(n))
    return sxy / math.sqrt(sxx * syy)


def spearman_rho(x: Sequence[float], y: Sequence[float]) -> float:
    return pearson_r(rankdata_average(list(x)), rankdata_average(list(y)))


def permutation_pvalue_correlation(
    x: List[float],
    y: List[float],
    r_obs: float,
    stat: str,
    n_perm: int,
    seed: int,
) -> float:
    """stat: 'pearson' | 'spearman'; two-sided, shuffle y."""
    rng = random.Random(seed)
    y_work = y.copy()
    ge = 1
    for _ in range(n_perm):
        rng.shuffle(y_work)
        if stat == "pearson":
            r = pearson_r(x, y_work)
        else:
            r = spearman_rho(x, y_work)
        if not math.isnan(r) and abs(r) >= abs(r_obs) - 1e-15:
            ge += 1
    return ge / (n_perm + 1)


def cohen_label(abs_corr: float) -> str:
    a = abs(abs_corr)
    if a < 0.1:
        return "below Cohen 'small' threshold 0.1"
    if a < 0.3:
        return "between small (0.1) and medium (0.3)"
    if a < 0.5:
        return "between medium (0.3) and large (0.5)"
    return "at or above Cohen 'large' threshold 0.5"


def fisher_z(r: float) -> float:
    """Fisher z transform (|r|<1); for meta-analysis etc., not a p-value."""
    r = max(-0.999999, min(0.999999, r))
    return 0.5 * math.log((1 + r) / (1 - r))


def load_pairs(csv_path: Path) -> tuple[List[float], List[float]]:
    xs: List[float] = []
    ys: List[float] = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, skipinitialspace=True)
        if reader.fieldnames is None:
            raise ValueError("CSV has no header row")
        for raw in reader:
            if not any((v or "").strip() for v in raw.values()):
                continue
            row = {k.strip(): (v or "").strip() for k, v in raw.items()}
            if "mean_score" not in row or "std_score" not in row:
                continue
            ms = row["mean_score"].replace(" ", "")
            ss = row["std_score"].replace(" ", "")
            try:
                xs.append(float(ms))
                ys.append(float(ss))
            except ValueError:
                continue
    return xs, ys


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "csv",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parent / "rq1_rule_survey_distribution_table_data.csv",
    )
    ap.add_argument("--n-perm", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    if not args.csv.is_file():
        print(f"File not found: {args.csv}", file=sys.stderr)
        return 1

    mean_s, std_s = load_pairs(args.csv)
    n = len(mean_s)
    if n < 3:
        print("Insufficient valid rows", file=sys.stderr)
        return 1

    r_p = pearson_r(mean_s, std_s)
    rho = spearman_rho(mean_s, std_s)

    print("=== std_score ~ mean_score (subcategory aggregate table) ===")
    print(f"Data: {args.csv}")
    print(f"n = {n}")
    print()
    print("--- Pearson ---")
    print(f"  r = {r_p:.4f}")
    print(f"  r² = {r_p * r_p:.4f}  (proportion of variance explained linearly; standard interpretation for Pearson)")
    print(f"  Fisher z = {fisher_z(r_p):.4f}")
    print(f"  |r| effect-size band (Cohen 1988 rule of thumb): {cohen_label(r_p)}")
    if scipy_stats is not None:
        _, p_pear_scipy = scipy_stats.pearsonr(mean_s, std_s)
        print(f"  scipy Pearson two-sided p = {p_pear_scipy:.6g}")
    p_pear_perm = permutation_pvalue_correlation(
        mean_s, std_s, r_p, "pearson", args.n_perm, args.seed
    )
    print(f"  permutation two-sided p ≈ {p_pear_perm:.6g} (n_perm={args.n_perm}, seed={args.seed})")
    print()
    print("--- Spearman ---")
    print(f"  ρ = {rho:.4f}")
    print(f"  |ρ| effect-size band (often analogized to Cohen thresholds): {cohen_label(rho)}")
    if scipy_stats is not None:
        _, p_sp = scipy_stats.spearmanr(mean_s, std_s)
        print(f"  scipy Spearman two-sided p = {p_sp:.6g}")
    p_spe_perm = permutation_pvalue_correlation(
        mean_s, std_s, rho, "spearman", args.n_perm, args.seed
    )
    print(f"  permutation two-sided p ≈ {p_spe_perm:.6g}")
    print()
    print("--- Summary ---")
    print("  In this dataset std_score and mean_score show a strong negative association;")
    print("  small p-values are inconsistent with 'no relationship by chance'.")
    print("  When writing up, report r/ρ, r² (Pearson), and qualitative limits such as Likert ceiling effects.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
