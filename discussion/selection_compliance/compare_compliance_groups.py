"""Compare the 160-rule and 30-rule groups on compliance and compliance change.

Run: /opt/anaconda3/bin/python discussion/rule_selection_compliance/compare_compliance_groups.py
The primary comparison is after-minus-before; the other three are secondary.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from importlib.metadata import version
from pathlib import Path


HERE = Path(__file__).resolve().parent
BEFORE, CURRENT, AFTER, CHANGE = "before5%", "current%", "after5%", "after5%-before5%"
METRICS = [(CHANGE, "after_minus_before", "primary"),
           (BEFORE, "before", "secondary"), (CURRENT, "current", "secondary"),
           (AFTER, "after", "secondary")]


def rate(text):
    text = text.strip()
    if text in ("", "-"):
        return None
    value = Decimal(text[:-1]) / 100 if text.endswith("%") else Decimal(text)
    if not value.is_finite() or not 0 <= value <= 1:
        raise ValueError(f"Invalid rate: {text!r}")
    return value


def load_group(path, expected, label):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not {"rule_id", BEFORE, CURRENT, AFTER}.issubset(reader.fieldnames or []):
            raise ValueError(f"Missing required columns: {path}")
        records = list(reader)
    ids = [r["rule_id"].strip() for r in records]
    if len(records) != expected or len(set(ids)) != expected or any(not rid for rid in ids):
        raise ValueError(f"Expected {expected} unique nonempty rule IDs: {path}")
    rows = []
    for record, rid in zip(records, ids):
        values = {field: rate(record[field]) for field in (BEFORE, CURRENT, AFTER)}
        # Decimal prevents binary subtraction noise from splitting genuine tied changes.
        values[CHANGE] = (values[AFTER] - values[BEFORE]
                          if values[AFTER] is not None and values[BEFORE] is not None else None)
        rows.append({"rule_id": rid, "group": label, "values": values, "original": record})
    return rows


def compare(groups, alpha):
    import numpy as np
    from scipy.stats import mannwhitneyu
    from statsmodels.stats.multitest import multipletests

    results = []
    for field, metric, role in METRICS:
        samples = [[float(r["values"][field]) for r in group if r["values"][field] is not None]
                   for group in groups]
        x, y = samples
        if not x or not y:
            raise ValueError(f"No valid observations for {metric}")
        test = mannwhitneyu(x, y, alternative="two-sided", method="asymptotic",
                            use_continuity=True, nan_policy="raise")
        u, p = float(test.statistic), float(test.pvalue)
        result = {"metric": metric, "source_column": field, "role": role,
                  "n_160": len(x), "n_30": len(y),
                  "missing_160": len(groups[0]) - len(x), "missing_30": len(groups[1]) - len(y)}
        for label, values in (("160", x), ("30", y)):
            result[f"mean_{label}"] = float(np.mean(values))
            result[f"median_{label}"] = float(np.median(values))
        result.update({"U_160": u, "p_value": p, "significant_raw": p < alpha,
                       "cliffs_delta_160_minus_30": 2 * u / (len(x) * len(y)) - 1})
        results.append(result)
    adjusted = multipletests([r["p_value"] for r in results], method="holm")[1]
    for result, p_holm in zip(results, adjusted):
        result["p_holm_all_four"] = float(p_holm)
        result["significant_holm"] = bool(p_holm < alpha)
    return results


def write_csv(path, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--group-160", type=Path, default=HERE / "stats_rule_compliance_matrix_160.csv")
    parser.add_argument("--group-30", type=Path, default=HERE / "stats_rule_compliance_matrix_30.csv")
    parser.add_argument("--output-dir", type=Path, default=HERE / "results")
    parser.add_argument("--alpha", type=float, default=0.05)
    args = parser.parse_args()
    if not 0 < args.alpha < 1:
        parser.error("Require 0 < alpha < 1")
    groups = [load_group(args.group_160, 160, "retained_160"),
              load_group(args.group_30, 30, "sampled_filtered_30")]
    overlap = {r["rule_id"] for r in groups[0]} & {r["rule_id"] for r in groups[1]}
    if overlap:
        raise ValueError(f"Groups overlap: {sorted(overlap)}")
    results = compare(groups, args.alpha)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    augmented = []
    for group in groups:
        for row in group:
            change = row["values"][CHANGE]
            augmented.append({"group": row["group"], **row["original"],
                              CHANGE: str(change) if change is not None else ""})
    write_csv(args.output_dir / "rule_data_with_change.csv", augmented)
    write_csv(args.output_dir / "mann_whitney_results.csv", results)
    lines = [
        "Rule selection and compliance: 160 retained versus 30 sampled filtered rules", "",
        "Primary comparison: after-minus-before compliance change. Before, current and after are secondary comparisons.",
        "Method: two-sided Mann-Whitney U; asymptotic normal p values with tie and continuity corrections.",
        "Change = after - before for each rule, computed at source precision before any rounding.",
        "Rates are on the 0-1 scale; a change of 0.10 means an increase of 10 percentage points.",
        "Missing rates are excluded only for the affected comparison; they are never replaced with zero.",
        f"Single-comparison significance: unrounded raw p < {args.alpha}.",
        f"Also reported: Holm correction over all four tests, with adjusted p < {args.alpha}.",
        "Cliff's delta = 2*U_160/(n_160*n_30)-1; positive means the 160-rule group tends to have higher values.",
        "For change, positive delta means greater improvement in the 160-rule group.", "",
        "Metric\tN160\tN30\tMean160\tMean30\tMedian160\tMedian30\tU160\tRaw p\tRaw significant\tHolm p\tHolm significant\tCliff delta",
    ]
    for r in results:
        lines.append(f"{r['metric']}\t{r['n_160']}\t{r['n_30']}\t"
                     f"{r['mean_160']:.4f}\t{r['mean_30']:.4f}\t"
                     f"{r['median_160']:.4f}\t{r['median_30']:.4f}\t{r['U_160']:.2f}\t"
                     f"{r['p_value']:.8g}\t{r['significant_raw']}\t"
                     f"{r['p_holm_all_four']:.8g}\t{r['significant_holm']}\t"
                     f"{r['cliffs_delta_160_minus_30']:.4f}")
    lines += ["", "Notes:",
              "These are independent-group comparisons. The change comparison uses each rule's paired after-before difference, then compares differences across groups.",
              "The rank test does not directly test arithmetic means. Non-significance does not establish equivalence.",
              "Rules may cluster within projects; clustering and selection effects are not adjusted for. Differences do not establish causation.",
              f"Input 160: {args.group_160.resolve()}", f"Input 30: {args.group_30.resolve()}",
              f"Versions: scipy={version('scipy')}, statsmodels={version('statsmodels')}",
              f"Generated (UTC): {datetime.now(timezone.utc).isoformat()}",
              "Method: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html"]
    summary = "\n".join(lines) + "\n"
    (args.output_dir / "summary.txt").write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, ImportError, InvalidOperation) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
