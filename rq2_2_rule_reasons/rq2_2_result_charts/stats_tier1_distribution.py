"""Compute tier_1 distribution in rq2_2_rule_reasons/rules_reason_result.json."""

import csv
import json
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
INPUT_JSON = REPO_ROOT / "rq2_2_rule_reasons" / "rules_reason_result.json"
OUTPUT_CSV = SCRIPT_DIR / "tier1_distribution.csv"


def main() -> None:
    with INPUT_JSON.open(encoding="utf-8") as f:
        records = json.load(f)

    if not isinstance(records, list):
        raise TypeError("Expected JSON root to be an array")

    tier1_values: list[str] = []
    missing = 0
    for i, row in enumerate(records):
        if not isinstance(row, dict):
            raise TypeError(f"Record {i} is not an object")
        v = row.get("tier_1")
        if v is None or v == "":
            missing += 1
            tier1_values.append("(missing)")
        else:
            tier1_values.append(str(v))

    total = len(tier1_values)
    counts = Counter(tier1_values)

    # Sort by count descending; put missing last if present
    ordered = sorted(counts.items(), key=lambda x: (-x[1], x[0]))

    print(f"File: {INPUT_JSON}")
    print(f"Total records: {total}")
    if missing:
        print(f"tier_1 missing or empty: {missing}")
    print()
    print(f"{'tier_1':<40} {'count':>8} {'pct':>10}")
    print("-" * 60)
    for label, c in ordered:
        pct = 100.0 * c / total if total else 0.0
        print(f"{label:<40} {c:>8} {pct:>9.2f}%")

    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["tier_1", "count", "proportion"])
        for label, c in ordered:
            prop = c / total if total else 0.0
            w.writerow([label, c, f"{prop:.6f}"])

    print()
    print(f"Wrote: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
