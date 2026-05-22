"""
Spearman rank correlation between rule_count and mean_score in
rq1_rule_survey_distribution_table_data.csv.

- Spearman ρ: equivalent to Pearson correlation on average ranks of both columns.
- p-value: if scipy is installed, uses scipy.stats.spearmanr (asymptotic test with tie
  correction); otherwise uses a permutation test based on Spearman ρ (tests independence,
  no scipy required).

Runs with the standard library only; optional: pip install scipy (compare with permutation p).
"""

from __future__ import annotations

import argparse
import csv
import math
import random
import sys
from pathlib import Path
from typing import List, Sequence, Tuple

try:
    from scipy import stats as scipy_stats
except ImportError:
    scipy_stats = None


def rankdata_average(values: Sequence[float]) -> List[float]:
    """Average ranks (1..n), consistent with SciPy / R average ties."""
    n = len(values)
    idx = sorted(range(n), key=lambda i: values[i])
    ranks = [0.0] * n
    pos = 0
    while pos < n:
        start = pos
        v = values[idx[pos]]
        while pos < n and values[idx[pos]] == v:
            pos += 1
        # 1-based ranks for sorted positions start .. pos-1
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


def permutation_pvalue_spearman(
    x: List[float],
    y: List[float],
    rho_obs: float,
    n_perm: int = 20000,
    seed: int = 42,
) -> float:
    """Two-sided permutation p: shuffle y under H0 (independence) to build empirical ρ distribution."""
    rng = random.Random(seed)
    y_work = y.copy()
    ge = 1  # include the observed statistic
    for _ in range(n_perm):
        rng.shuffle(y_work)
        r = spearman_rho(x, y_work)
        if math.isnan(r):
            continue
        if abs(r) >= abs(rho_obs) - 1e-15:
            ge += 1
    return ge / (n_perm + 1)


def load_rows(csv_path: Path) -> Tuple[List[float], List[float]]:
    rule_counts: List[float] = []
    mean_scores: List[float] = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, skipinitialspace=True)
        if reader.fieldnames is None:
            raise ValueError("CSV has no header row")
        # Strip keys (headers may contain alignment spaces)
        for raw in reader:
            if not any((v or "").strip() for v in raw.values()):
                continue
            row = {k.strip(): (v or "").strip() for k, v in raw.items()}
            if "rule_count" not in row or "mean_score" not in row:
                continue
            ms = row["mean_score"].replace(" ", "")
            try:
                rc = float(row["rule_count"])
                msf = float(ms)
            except ValueError:
                continue
            rule_counts.append(rc)
            mean_scores.append(msf)
    return rule_counts, mean_scores


def main() -> int:
    parser = argparse.ArgumentParser(description="Spearman: rule_count vs mean_score")
    parser.add_argument(
        "csv",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parent / "rq1_rule_survey_distribution_table_data.csv",
        help="Path to CSV file",
    )
    parser.add_argument(
        "--n-perm",
        type=int,
        default=20000,
        help="Number of permutation replicates (default 20000; independent of scipy)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for permutation test",
    )
    args = parser.parse_args()
    csv_path: Path = args.csv

    if not csv_path.is_file():
        print(f"File not found: {csv_path}", file=sys.stderr)
        return 1

    x, y = load_rows(csv_path)
    n = len(x)
    if n < 3:
        print("Insufficient valid rows (need at least 3)", file=sys.stderr)
        return 1

    rho = spearman_rho(x, y)

    print(f"Data file: {csv_path}")
    print(f"Valid rows n = {n}")
    print()
    print(f"Spearman rank correlation ρ = {rho:.4f}")
    print()

    if scipy_stats is not None:
        rho_sp, p_scipy = scipy_stats.spearmanr(x, y)
        print("scipy.stats.spearmanr (asymptotic / exact algorithm with tie correction):")
        print(f"  ρ = {rho_sp:.4f}")
        print(f"  two-sided p-value = {p_scipy:.6g}")
        print()

    p_perm = permutation_pvalue_spearman(x, y, rho, n_perm=args.n_perm, seed=args.seed)
    print(f"Permutation test (two-sided, independence H0; n_perm={args.n_perm}, seed={args.seed}):")
    print(f"  p-value ≈ {p_perm:.6g}")
    print()

    p_main = p_scipy if scipy_stats is not None else p_perm
    sig = p_main < 0.05

    print("Direction and significance:")
    if rho > 0.05:
        trend = "positive rank association (higher rule_count tends to go with higher mean_score)"
    elif rho < -0.05:
        trend = "negative rank association (higher rule_count tends to go with lower mean_score)"
    else:
        trend = "|ρ| near 0, almost no monotonic rank relationship"
    print(f"  {trend}.")
    if sig:
        print(f"  At α=0.05, p={p_main:.4g}: reject independence (statistical association detected).")
    else:
        print(f"  At α=0.05, p={p_main:.4g}: cannot reject independence (no significant association).")
    print()
    print("Note: correlation ≠ causation; with non-independent subcategories, treat p-values as exploratory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
