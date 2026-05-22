"""Join tier_1 from rules_reason_result.json with change_type from file_diffs (aligned by id); write one summary CSV."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
RQ22_DIR = SCRIPT_DIR.parent.parent
RULES_JSON = RQ22_DIR / "rules_reason_result.json"
FILE_DIFFS_DIR = RQ22_DIR.parent / "rq2_1_evolved_rules" / "file_diffs"

OUT_CSV = SCRIPT_DIR / "tier1_change_type.csv"

# Row order: top to bottom
TIER1_ROW_ORDER = [
    "Expansion",
    "Context Enrichment",
    "Synchronization",
    "Refinement",
    "Correction",
    "Pruning",
]

# Column order: left to right added → modified → deleted
CHANGE_TYPE_COL_ORDER = ["added", "modified", "deleted"]


def load_change_type_by_id(rule_ids: set[str]) -> dict[str, str]:
    """Load change_type from file_diffs only; ensure each id has at most one change_type in the 504 subset."""
    variants: dict[str, set[str]] = defaultdict(set)
    for path in FILE_DIFFS_DIR.rglob("*.diff.json"):
        rows = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(rows, list):
            continue
        for row in rows:
            if not isinstance(row, dict):
                continue
            rid = row.get("id")
            ct = row.get("change_type")
            if rid not in rule_ids or ct is None:
                continue
            variants[rid].add(str(ct))

    ambiguous = {k: sorted(v) for k, v in variants.items() if len(v) > 1}
    if ambiguous:
        raise ValueError(f"id(s) with multiple change_type values in file_diffs: {ambiguous}")

    return {k: next(iter(v)) for k, v in variants.items()}


def main() -> None:
    rules: list[dict] = json.loads(RULES_JSON.read_text(encoding="utf-8"))
    rule_ids = {str(r["rule_id"]) for r in rules if r.get("rule_id")}
    if len(rule_ids) != len(rules):
        raise ValueError("Duplicate rule_id in rules_reason_504.json")

    id_to_ct = load_change_type_by_id(rule_ids)
    missing = sorted(rule_ids - id_to_ct.keys())
    if missing:
        raise ValueError(
            f"rule_id(s) not found in file_diffs: {missing[:20]}…" if len(missing) > 20 else f"{missing}"
        )

    pair_counts: Counter[tuple[str, str]] = Counter()
    tier1_totals: Counter[str] = Counter()
    for r in rules:
        t1 = str(r["tier_1"])
        rid = str(r["rule_id"])
        ct = id_to_ct[rid]
        pair_counts[(t1, ct)] += 1
        tier1_totals[t1] += 1

    header = ["tier_1", "n_tier_1"]
    for ct in CHANGE_TYPE_COL_ORDER:
        header.append(f"{ct}_count")
        header.append(f"{ct}_pct")

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for t1 in TIER1_ROW_ORDER:
            if t1 not in tier1_totals:
                raise ValueError(f"Missing tier_1 in data: {t1!r}")
            n_t = tier1_totals[t1]
            row: list = [t1, n_t]
            for ct in CHANGE_TYPE_COL_ORDER:
                c = pair_counts.get((t1, ct), 0)
                row.append(c)
                row.append(f"{100.0 * c / n_t:.2f}" if n_t else "0.00")
            w.writerow(row)

    print(f"Wrote: {OUT_CSV}")


if __name__ == "__main__":
    main()
