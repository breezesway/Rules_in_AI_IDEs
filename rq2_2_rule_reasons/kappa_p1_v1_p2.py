"""
Human tier_1 (labeling CSV): only Clear/clear -> Clear; all other non-empty
values -> Unclear.

Model tier_1 (reason JSON): Unclear -> Unclear; any other value -> Clear.

Binary agreement for Cohen's kappa uses two labels: Unclear and Clear.
  Unclear = human non-Clear bucket; model Unclear.
  Clear   = human Clear; model non-Unclear (specific tier).

Row scope: set LABEL_ROW_START / LABEL_ROW_END (1-based, inclusive, below) to
restrict which labeling CSV rows are summarized and used for kappa; both None
uses the full table.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

try:
    from sklearn.metrics import cohen_kappa_score as _sk_kappa
except ImportError:
    _sk_kappa = None  # type: ignore


def cohen_kappa(human: list[str], model: list[str], labels: list[str]) -> float:
    """Cohen's kappa; pure Python fallback if sklearn missing."""
    if _sk_kappa is not None:
        return float(_sk_kappa(human, model, labels=labels))
    n = len(human)
    if n == 0:
        return 0.0
    p_o = sum(1 for a, b in zip(human, model) if a == b) / n
    ch = Counter(human)
    cm = Counter(model)
    p_e = sum((ch[c] / n) * (cm[c] / n) for c in labels)
    if p_e >= 1.0 - 1e-15:
        return 1.0 if p_o >= 1.0 - 1e-15 else 0.0
    return (p_o - p_e) / (1.0 - p_e)


DIR = Path(__file__).resolve().parent
LABELING_CSV = DIR / "sampled_308_p2.csv"
REASON_JSON = DIR / "sampled_308_p1.json"

# Labeling CSV (LABELING_CSV) row range: 1-based inclusive [START, END], relative to the first data row.
# When both are None, tier_1 stats and Kappa use all data rows; otherwise only rows in range.
LABEL_ROW_START: int | None = None
LABEL_ROW_END: int | None = None

# Binary labels: Unclear vs Clear
BIN_UNCLEAR = "Unclear"
BIN_CLEAR = "Clear"


def human_tier_to_binary(raw: str) -> str:
    """Clear / clear -> Clear; anything else non-empty -> Unclear."""
    s = (raw or "").strip()
    if not s:
        return ""
    if s.lower() == "clear":
        return BIN_CLEAR
    return BIN_UNCLEAR


def human_to_kappa_label(raw: str) -> str:
    """Clear/clear -> Clear; anything else non-empty -> Unclear."""
    s = (raw or "").strip()
    if not s:
        return ""
    if s.lower() == "clear":
        return BIN_CLEAR
    return BIN_UNCLEAR


def model_to_kappa_label(raw: str) -> str:
    """Model: Unclear -> Unclear; else -> Clear."""
    s = (raw or "").strip()
    if not s:
        return ""
    if s.lower() == "unclear":
        return BIN_UNCLEAR
    return BIN_CLEAR


def row_key(d: dict) -> tuple:
    return (d.get("rule_id", ""), d.get("file", ""), d.get("change_type", ""))


def load_csv_rows(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def slice_labeling_rows(
    rows: list[dict],
    start_1based: int | None,
    end_1based_inclusive: int | None,
) -> tuple[list[dict], str]:
    """Return a 1-based inclusive slice; when start and end are both None, return the full table."""
    n = len(rows)
    if start_1based is None and end_1based_inclusive is None:
        return rows, f"all data rows (1–{n})"
    lo = 1 if start_1based is None else start_1based
    hi = n if end_1based_inclusive is None else end_1based_inclusive
    lo = max(1, min(lo, n))
    hi = max(1, min(hi, n))
    if lo > hi:
        return [], f"invalid range (start {lo} > end {hi})"
    out = rows[lo - 1 : hi]
    return out, f"rows {lo}–{hi} ({len(out)} row(s), relative to first data row)"


def main() -> None:
    labeling = load_csv_rows(LABELING_CSV)
    labeling_scope, scope_desc = slice_labeling_rows(
        labeling, LABEL_ROW_START, LABEL_ROW_END
    )

    if not REASON_JSON.exists():
        print(f"Missing model result file: {REASON_JSON}")
        return

    reason_by_key: dict[tuple, dict] = {}
    with open(REASON_JSON, encoding="utf-8") as f:
        jrows = json.load(f)
    for r in jrows:
        reason_by_key[row_key(r)] = r

    n = len(labeling_scope)
    tier1_raw = [(row.get("tier_1") or "").strip() for row in labeling_scope]
    n_empty = sum(1 for t in tier1_raw if not t)
    n_filled = n - n_empty

    # Human coarse: Clear vs Unclear (all non-Clear)
    n_human_clear = sum(1 for t in tier1_raw if t and human_tier_to_binary(t) == "Clear")
    n_human_unclear_bucket = sum(1 for t in tier1_raw if t and human_tier_to_binary(t) == "Unclear")

    filled_counter = Counter(t for t in tier1_raw if t)

    print("=" * 60)
    print("rule_data_labeling - rule_reason_check.csv  —  tier_1 coarse labels")
    print("=" * 60)
    print(f"Scope: {scope_desc} (full table: {len(labeling)} rows)")
    print("Rule: Clear / clear -> Clear; any other non-empty value -> Unclear")
    print(f"Rows in scope: {n}")
    print(f"tier_1 filled: {n_filled}; empty: {n_empty}")
    print(f"  mapped to Clear: {n_human_clear}")
    print(f"  mapped to Unclear (incl. UnClear, Partial, Parial, etc.): {n_human_unclear_bucket}")
    print("\nRaw tier_1 value distribution (non-empty samples):")
    for k, v in sorted(filled_counter.items(), key=lambda x: (-x[1], x[0])):
        print(f"  {k!r}: {v}")

    y_human: list[str] = []
    y_model: list[str] = []
    # In labeling order: (rule_id, human_tier_1_raw, model_tier_1_raw, reasoning)
    paired_detail: list[tuple[str, str, str, str]] = []
    skip_no_row = 0
    skip_empty_model = 0

    for row in labeling_scope:
        human_raw = (row.get("tier_1") or "").strip()
        h = human_to_kappa_label(human_raw)
        if not h:
            continue
        k = row_key(row)
        rrow = reason_by_key.get(k)
        if not rrow:
            skip_no_row += 1
            continue
        m_raw = (rrow.get("tier_1") or "").strip()
        m = model_to_kappa_label(m_raw)
        if not m:
            skip_empty_model += 1
            continue
        reasoning = (rrow.get("reasoning") or "").strip()
        rule_id = row.get("rule_id", "")
        paired_detail.append((rule_id, human_raw, m_raw, reasoning))
        y_human.append(h)
        y_model.append(m)

    n_model_unclear = sum(1 for x in y_model if x == BIN_UNCLEAR)
    n_model_clear = len(y_model) - n_model_unclear

    print("\n" + "=" * 60)
    print("reason_results_sampled_308_reconciled.json (aligned to labeled samples) — model coarse labels")
    print("=" * 60)
    print("Rule: tier_1 == Unclear -> Unclear; otherwise -> Clear")
    print(f"Valid samples: {len(y_model)}")
    print(f"  model Unclear: {n_model_unclear}")
    print(f"  model Clear (specific tier, etc.): {n_model_clear}")

    print("\n" + "=" * 60)
    print("Kappa encoding (binary: Unclear vs Clear)")
    print("=" * 60)
    print("  Unclear: human=non-Clear bucket; model=Unclear")
    print("  Clear:   human=Clear; model=non-Unclear (specific tier)")

    if skip_no_row:
        print(f"\nSkipped (no matching reason row): {skip_no_row}")
    if skip_empty_model:
        print(f"Skipped (empty model tier_1): {skip_empty_model}")

    if len(y_human) < 2:
        print("\nToo few valid pairs to compute Kappa.")
        return

    labels = [BIN_UNCLEAR, BIN_CLEAR]
    kappa = cohen_kappa(y_human, y_model, labels)
    print("\n" + "=" * 60)
    print("Cohen's Kappa (binary: Unclear vs Clear)")
    print("=" * 60)
    print(f"Kappa = {kappa:.4f}")

    agree = sum(1 for a, b in zip(y_human, y_model) if a == b)
    print(f"Agreement: {agree} / {len(y_human)} ({100 * agree / len(y_human):.1f}%)")

    print("\nCross-tabulation (human=rows, model=columns):")
    w = 12
    print(f"{'':{w}}" f"{BIN_UNCLEAR:>{w}}" f"{BIN_CLEAR:>{w}}")
    for hcat in labels:
        line = f"{hcat:>{w}}"
        for mcat in labels:
            c = sum(1 for a, b in zip(y_human, y_model) if a == hcat and b == mcat)
            line += f"{c:>{w}}"
        print(line)

    # Output disagreeing rules in labeling CSV order
    disagree = [
        (i, paired_detail[i])
        for i in range(len(y_human))
        if y_human[i] != y_model[i]
    ]
    print("\n" + "=" * 60)
    print("Rules with disagreeing labels (rule_data_labeling order within scope)")
    print("=" * 60)
    print(f"Total: {len(disagree)}\n")
    for _idx, (rule_id, human_tier, model_tier, reasoning) in disagree:
        print(f"rule_id: {rule_id}")
        print(f"  human tier_1: {human_tier}")
        print(f"  model tier_1: {model_tier}")
        print(f"  reasoning: {reasoning}")
        print()


if __name__ == "__main__":
    main()
