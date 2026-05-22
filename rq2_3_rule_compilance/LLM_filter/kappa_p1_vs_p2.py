"""
Compute Cohen's Kappa on can_detect between sampled_284_p1.json
and sampled_284_p2.csv.

Align by rule_id; can_detect is True/False only (case-insensitive).
JSON list order defines item index; use RANGE_START / RANGE_END below for a 1-based
closed interval sub-range; both None uses all data.
If PRINT_MISMATCH_DETAILS is True, print can_detect mismatches in JSON order after stats.
"""

import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ==================== Range slice (1-based, closed interval) ====================
# e.g. items 151–284 -> RANGE_START = 151, RANGE_END = 284
# Both None: use all JSON entries in file order.
RANGE_START: Optional[int] = None
RANGE_END: Optional[int] = None
# ================================================================

# If True, list can_detect mismatches in JSON order after Kappa stats (fields mostly from JSON)
PRINT_MISMATCH_DETAILS: bool = True

BASE_DIR = Path(__file__).parent
RECONCILED_JSON = BASE_DIR / "sampled_284_p1.json"
LABELING_CSV = BASE_DIR / "sampled_284_p2.csv"


def parse_can_detect(value: Any) -> Optional[bool]:
    """Normalize can_detect to bool; return None if unparseable."""
    if isinstance(value, bool):
        return value
    if value is None:
        return None
    s = str(value).strip().lower()
    if s in ("true", "1", "yes", "y"):
        return True
    if s in ("false", "0", "no", "n"):
        return False
    return None


def load_reconciled(path: Path) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"{path} must be a JSON array")
    return data


def load_csv_can_detect(path: Path) -> Dict[str, bool]:
    """rule_id -> can_detect from CSV can_detect column."""
    out: Dict[str, bool] = {}
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None or "rule_id" not in reader.fieldnames:
            raise ValueError("CSV missing rule_id column")
        if "can_detect" not in reader.fieldnames:
            raise ValueError("CSV missing can_detect column")
        for row in reader:
            rid = (row.get("rule_id") or "").strip()
            if not rid:
                continue
            cd = parse_can_detect(row.get("can_detect"))
            if cd is None:
                continue
            out[rid] = cd
    return out


def apply_range_slice(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Slice by RANGE_START / RANGE_END (1-based closed); None means start or end."""
    n = len(items)
    start_1 = 1 if RANGE_START is None else RANGE_START
    end_1 = n if RANGE_END is None else RANGE_END
    if start_1 < 1 or end_1 < start_1:
        raise ValueError(f"Invalid range: RANGE_START={RANGE_START}, RANGE_END={RANGE_END}, n={n}")
    if end_1 > n:
        raise ValueError(f"RANGE_END={RANGE_END} exceeds data length n={n}")
    # 1-based closed [start_1, end_1] -> 0-based slice [start_1 - 1 : end_1]
    return items[start_1 - 1 : end_1]


def calculate_cohen_kappa_manual(
    y1: List[bool], y2: List[bool]
) -> Tuple[float, Dict[str, Any]]:
    if len(y1) != len(y2):
        raise ValueError("Both lists must have the same length")
    n = len(y1)
    if n == 0:
        raise ValueError("No valid samples; cannot compute Kappa")

    unique_labels = sorted(set(y1 + y2))
    confusion: Dict[Tuple[bool, bool], int] = {}
    for a in unique_labels:
        for b in unique_labels:
            confusion[(a, b)] = 0
    for i in range(n):
        confusion[(y1[i], y2[i])] += 1

    po = sum(confusion.get((lb, lb), 0) for lb in unique_labels) / n
    p1 = {lb: sum(1 for y in y1 if y == lb) / n for lb in unique_labels}
    p2 = {lb: sum(1 for y in y2 if y == lb) / n for lb in unique_labels}
    pe = sum(p1[lb] * p2[lb] for lb in unique_labels)

    if pe >= 1.0:
        kappa = 1.0 if po >= 1.0 else float("nan")
    else:
        kappa = (po - pe) / (1 - pe)

    agree = sum(confusion.get((lb, lb), 0) for lb in unique_labels)
    stats = {
        "n": n,
        "po": po,
        "pe": pe,
        "kappa": kappa,
        "confusion_matrix": confusion,
        "agreement_count": agree,
        "disagreement_count": n - agree,
    }
    return kappa, stats


def _str_field(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def print_mismatches_in_order(
    rows: List[Tuple[Dict[str, Any], bool, bool]],
) -> None:
    """Print can_detect mismatches in order (fields from JSON)."""
    if not rows:
        return
    print("-" * 60)
    print(f"Mismatches ({len(rows)} rows, same order as JSON in current range)")
    print("-" * 60)
    for idx, (rec, jcd, _ccd) in enumerate(rows, start=1):
        print(f"\n--- [{idx}/{len(rows)}] ---")
        print(f"rule_id: {_str_field(rec.get('rule_id'))}")
        if jcd is True:
            print(f"detection_targets:\n{_str_field(rec.get('detection_targets'))}")
            print(f"detection_logic:\n{_str_field(rec.get('detection_logic'))}")
        else:
            print(f"reason_for_false:\n{_str_field(rec.get('reason_for_false'))}")
    print("-" * 60)


def main() -> None:
    rules = load_reconciled(RECONCILED_JSON)
    csv_map = load_csv_can_detect(LABELING_CSV)

    sliced = apply_range_slice(rules)
    range_desc = "all data"
    if RANGE_START is not None or RANGE_END is not None:
        range_desc = f"items {RANGE_START or 1}–{RANGE_END or len(rules)} ({len(sliced)} total)"

    y_json: List[bool] = []
    y_csv: List[bool] = []
    rule_ids: List[str] = []
    missing_csv: List[str] = []
    bad_json: List[str] = []
    mismatch_rows: List[Tuple[Dict[str, Any], bool, bool]] = []

    for rec in sliced:
        rid = rec.get("rule_id")
        if not rid:
            continue
        rid = str(rid).strip()
        jcd = parse_can_detect(rec.get("can_detect"))
        if jcd is None:
            bad_json.append(rid)
            continue
        if rid not in csv_map:
            missing_csv.append(rid)
            continue
        ccd = csv_map[rid]
        rule_ids.append(rid)
        y_json.append(jcd)
        y_csv.append(ccd)
        if jcd != ccd:
            mismatch_rows.append((rec, jcd, ccd))

    print("=" * 60)
    print("Cohen's Kappa: reconciled JSON vs manual CSV labels (can_detect)")
    print("=" * 60)
    print(f"Range: {range_desc}")
    print(f"JSON path: {RECONCILED_JSON.name}")
    print(f"CSV path: {LABELING_CSV.name}")
    print(f"JSON rows in range: {len(sliced)}")
    print(f"Aligned (valid can_detect on both sides): {len(y_json)}")
    if missing_csv:
        print(f"rule_ids missing in CSV: {len(missing_csv)}")
    if bad_json:
        print(f"rule_ids with unparseable can_detect in JSON: {len(bad_json)}")

    if len(y_json) == 0:
        print("No usable samples; exiting.")
        return

    kappa, stats = calculate_cohen_kappa_manual(y_json, y_csv)
    print("-" * 60)
    print(f"Cohen's κ = {stats['kappa']:.6f}")
    print(f"Observed agreement Po = {stats['po']:.6f}")
    print(f"Expected agreement Pe = {stats['pe']:.6f}")
    print(f"Agreements: {stats['agreement_count']} / {stats['n']}")
    print("Confusion (JSON rows, CSV cols) True/False:")
    for a in (False, True):
        row_parts = []
        for b in (False, True):
            row_parts.append(str(stats["confusion_matrix"].get((a, b), 0)))
        print(f"  JSON={a!s:5} -> CSV F={row_parts[0]:>4}  T={row_parts[1]:>4}")
    print("=" * 60)
    if PRINT_MISMATCH_DETAILS:
        print_mismatches_in_order(mismatch_rows)


if __name__ == "__main__":
    main()
