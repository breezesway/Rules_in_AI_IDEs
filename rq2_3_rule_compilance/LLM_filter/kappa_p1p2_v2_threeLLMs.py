"""
Compute Cohen's Kappa on can_detect:

1) sampled_284_p1.json vs
   majority vote of [gemini-3-flash-preview, glm-5, qwen3-max]

2) sampled_284_p2.csv vs
   majority vote of [gemini-3-flash-preview, glm-5, qwen3-max]
"""

import csv
import json
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent

SAMPLED_FILE = "sampled_284_p1.json"
LABELING_CSV = "sampled_284_p2.csv"
THREE_FILES = [
    "filter_results_gemini-3-flash-preview.json",
    "filter_results_glm-5.json",
    "filter_results_qwen3-max.json",
]


def parse_bool(value):
    """Parse bool/string/number to 0 or 1; return None if unparseable."""
    if isinstance(value, bool):
        return 1 if value else 0
    if value is None:
        return None
    if isinstance(value, (int, float)):
        if value == 1:
            return 1
        if value == 0:
            return 0
        return None

    s = str(value).strip().lower()
    true_set = {"true", "t", "1", "yes", "y"}
    false_set = {"false", "f", "0", "no", "n"}
    if s in true_set:
        return 1
    if s in false_set:
        return 0
    return None


def cohen_kappa_score(y1, y2):
    """Cohen's kappa for binary labels."""
    n = len(y1)
    if n != len(y2) or n == 0:
        raise ValueError("Lengths must match and be > 0")

    p_o = sum(1 for a, b in zip(y1, y2) if a == b) / n
    n1_0, n1_1 = sum(1 for a in y1 if a == 0), sum(1 for a in y1 if a == 1)
    n2_0, n2_1 = sum(1 for a in y2 if a == 0), sum(1 for a in y2 if a == 1)
    p_e = (n1_0 * n2_0 + n1_1 * n2_1) / (n * n)
    if p_e >= 1.0:
        return 1.0
    return (p_o - p_e) / (1.0 - p_e)


def interpret_kappa(kappa):
    if kappa < 0:
        return "Poor"
    if kappa < 0.20:
        return "Slight"
    if kappa < 0.40:
        return "Fair"
    if kappa < 0.60:
        return "Moderate"
    if kappa < 0.80:
        return "Substantial"
    return "Almost Perfect"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"{path.name} is not a JSON array")
    return data


def build_rule_id_to_can_detect_from_json(data):
    out = {}
    for obj in data:
        rid = obj.get("rule_id")
        if rid is None:
            continue
        val = parse_bool(obj.get("can_detect"))
        if val is None:
            continue
        out[rid] = val
    return out


def load_labeling_csv(path):
    """
    CSV: first occurrence per rule_id with parseable can_detect.
    Returns:
      rule_ids: order preserved
      by_id: rule_id -> 0/1
    """
    rule_ids = []
    by_id = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rid = (row.get("rule_id") or "").strip()
            if not rid or rid in by_id:
                continue
            val = parse_bool(row.get("can_detect"))
            if val is None:
                continue
            by_id[rid] = val
            rule_ids.append(rid)
    return rule_ids, by_id


def majority_of_three(a, b, c):
    return 1 if (a + b + c) >= 2 else 0


def load_three_model_maps():
    model_maps = {}
    for filename in THREE_FILES:
        data = load_json(SCRIPT_DIR / filename)
        model_maps[filename] = build_rule_id_to_can_detect_from_json(data)
    return model_maps


def align_and_build_majority(rule_ids, ref_by_id, model_maps):
    aligned_ids = []
    y_ref = []
    y_majority = []
    for rid in rule_ids:
        ref_val = ref_by_id.get(rid)
        if ref_val is None:
            continue
        g = model_maps[THREE_FILES[0]].get(rid)
        m = model_maps[THREE_FILES[1]].get(rid)
        q = model_maps[THREE_FILES[2]].get(rid)
        if g is None or m is None or q is None:
            continue
        aligned_ids.append(rid)
        y_ref.append(ref_val)
        y_majority.append(majority_of_three(g, m, q))
    return aligned_ids, y_ref, y_majority


def report_block(title, ref_name, y_ref, y_majority):
    n = len(y_ref)
    if n == 0:
        print("=" * 72)
        print(title)
        print("=" * 72)
        print("No comparable samples (0 rows).")
        return None

    kappa = cohen_kappa_score(y_ref, y_majority)
    agree = sum(1 for a, b in zip(y_ref, y_majority) if a == b)
    disagree = n - agree
    print("=" * 72)
    print(title)
    print("=" * 72)
    print(f"Comparison: {ref_name} vs 3-model majority")
    print(f"Sample count: {n}")
    print(f"Agreement: {agree}/{n} ({100 * agree / n:.1f}%)")
    print(f"Disagreement: {disagree}/{n} ({100 * disagree / n:.1f}%)")
    print(f"Cohen's Kappa: {kappa:.4f} ({interpret_kappa(kappa)})")
    return kappa


def main():
    model_maps = load_three_model_maps()
    for filename in THREE_FILES:
        print(f"Loaded {filename}: {len(model_maps[filename])} rules with can_detect")

    # Block 1: sampled reconciled JSON vs majority(3)
    sampled_data = load_json(SCRIPT_DIR / SAMPLED_FILE)
    sampled_rule_ids = [obj["rule_id"] for obj in sampled_data if obj.get("rule_id") is not None]
    sampled_by_id = build_rule_id_to_can_detect_from_json(sampled_data)
    sampled_aligned_ids, sampled_y, sampled_maj = align_and_build_majority(
        sampled_rule_ids, sampled_by_id, model_maps
    )
    skipped_sampled = len(sampled_rule_ids) - len(sampled_aligned_ids)
    if skipped_sampled > 0:
        print(f"Skipped sampled rule_ids not in all 3 models: {skipped_sampled}")
    kappa_sampled = report_block(
        f"Kappa: {SAMPLED_FILE} vs majority({', '.join(THREE_FILES)})",
        "sampled_reconciled",
        sampled_y,
        sampled_maj,
    )

    # Block 2: CSV vs majority(3)
    csv_rule_ids, csv_by_id = load_labeling_csv(SCRIPT_DIR / LABELING_CSV)
    csv_aligned_ids, csv_y, csv_maj = align_and_build_majority(
        csv_rule_ids, csv_by_id, model_maps
    )
    skipped_csv = len(csv_rule_ids) - len(csv_aligned_ids)
    if skipped_csv > 0:
        print(f"Skipped CSV rule_ids not in all 3 models: {skipped_csv}")
    kappa_csv = report_block(
        f"Kappa: {LABELING_CSV} vs majority({', '.join(THREE_FILES)})",
        "csv_labeling",
        csv_y,
        csv_maj,
    )

    print("\n" + "=" * 72)
    print("Summary")
    print("=" * 72)
    if kappa_sampled is not None:
        print(f"[{SAMPLED_FILE}] vs majority(3): {kappa_sampled:.4f}")
    else:
        print(f"[{SAMPLED_FILE}] vs majority(3): N/A")
    if kappa_csv is not None:
        print(f"[{LABELING_CSV}] vs majority(3): {kappa_csv:.4f}")
    else:
        print(f"[{LABELING_CSV}] vs majority(3): N/A")


if __name__ == "__main__":
    main()
