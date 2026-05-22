"""Align tier_1 with second_level via rule_id ↔ id; output two row-percentage tables (count in col 2, then percentages)."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
RQ22_DIR = SCRIPT_DIR.parent.parent
RULES_JSON = RQ22_DIR / "rules_reason_result.json"
FILE_DIFFS_DIR = RQ22_DIR.parent / "rq2_1_evolved_rules" / "file_diffs"

# Per change reason: share of each second_level within that reason (rows sum to 100%)
OUT_TIER1_ROWS = SCRIPT_DIR / "pct_second_level_within_tier1.csv"
# Per second_level: share of each change reason within that category (rows sum to 100%)
OUT_SECOND_LEVEL_ROWS = SCRIPT_DIR / "pct_tier1_within_second_level.csv"

TIER1_ORDER = [
    "Expansion",
    "Context Enrichment",
    "Synchronization",
    "Refinement",
    "Correction",
    "Pruning",
]


def load_category_by_id(rule_ids: set[str]) -> dict[str, dict[str, str]]:
    """Load id -> first_level, second_level, etc. from file_diffs."""
    variants: dict[str, list[dict[str, str]]] = defaultdict(list)
    for path in FILE_DIFFS_DIR.rglob("*.diff.json"):
        rows = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(rows, list):
            continue
        for row in rows:
            if not isinstance(row, dict):
                continue
            rid = row.get("id")
            if rid not in rule_ids:
                continue
            variants[str(rid)].append(
                {
                    "first_level": str(row.get("first_level") or ""),
                    "second_level": str(row.get("second_level") or ""),
                    "change_type": str(row.get("change_type") or ""),
                    "file": str(row.get("file") or ""),
                    "project": str(row.get("project") or ""),
                    "source_json": str(path.relative_to(FILE_DIFFS_DIR)),
                }
            )

    def _cat_key(d: dict[str, str]) -> tuple[str, str, str]:
        return (d["first_level"], d["second_level"], d["change_type"])

    ambiguous = {k: v for k, v in variants.items() if len({_cat_key(d) for d in v}) > 1}
    if ambiguous:
        sample = {k: v[:2] for k, v in list(ambiguous.items())[:5]}
        raise ValueError(f"Inconsistent category fields in file_diffs for id(s) (sample): {sample}")

    out: dict[str, dict[str, str]] = {}
    for rid, lst in variants.items():
        out[rid] = lst[0] if lst else {}
    return out


def main() -> None:
    rules: list[dict] = json.loads(RULES_JSON.read_text(encoding="utf-8"))
    rule_ids = {str(r["rule_id"]) for r in rules if r.get("rule_id")}
    if len(rule_ids) != len(rules):
        raise ValueError("Duplicate rule_id in rules_reason_504.json")

    id_to_cat = load_category_by_id(rule_ids)
    missing = sorted(rule_ids - id_to_cat.keys())
    if missing:
        raise ValueError(
            f"rule_id(s) not found in file_diffs: {missing[:30]}"
            + ("…" if len(missing) > 30 else "")
        )

    pair_sl: Counter[tuple[str, str]] = Counter()
    tier1_totals: Counter[str] = Counter()
    sl_totals: Counter[str] = Counter()

    for r in rules:
        t1 = str(r["tier_1"])
        rid = str(r["rule_id"])
        sl = id_to_cat[rid]["second_level"]
        pair_sl[(t1, sl)] += 1
        tier1_totals[t1] += 1
        sl_totals[sl] += 1

    second_levels = sorted({sl for (_, sl) in pair_sl})

    with OUT_TIER1_ROWS.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["tier_1", "总数", *second_levels])
        for t1 in TIER1_ORDER:
            n_row = tier1_totals[t1]
            pcts = [
                round(100.0 * pair_sl[(t1, sl)] / n_row, 2) if n_row else 0.0
                for sl in second_levels
            ]
            w.writerow([t1, n_row, *pcts])

    with OUT_SECOND_LEVEL_ROWS.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["second_level", "总数", *TIER1_ORDER])
        for sl in second_levels:
            n_col = sl_totals[sl]
            pcts = [
                round(100.0 * pair_sl[(t1, sl)] / n_col, 2) if n_col else 0.0
                for t1 in TIER1_ORDER
            ]
            w.writerow([sl, n_col, *pcts])

    print(f"Wrote {OUT_TIER1_ROWS} ({len(second_levels)} second_level columns)")
    print(f"Wrote {OUT_SECOND_LEVEL_ROWS}")


if __name__ == "__main__":
    main()
