"""
Compute Cohen's Kappa on tier_1 (Unclear vs non-Unclear):

1) reason_results_sampled_308_reconciled.json vs each LLM JSON file and vs their majority.
2) rule_data_labeling - rule_reason_check.csv (human) vs same files and vs majority.

Human CSV binarization matches kappa_p1_v1_p2.py: only Clear/clear -> non-Unclear (0);
any other non-empty tier_1 -> Unclear (1). Rows with empty tier_1 are skipped.

Model JSON: tier_1 == "Unclear" -> 1, else -> 0.
"""

import csv
import json
from pathlib import Path
from typing import Optional


def cohen_kappa_score(y1: list, y2: list) -> float:
    """Cohen's kappa for two binary (0/1) label lists. (P_o - P_e) / (1 - P_e)."""
    n = len(y1)
    if n != len(y2) or n == 0:
        raise ValueError("Lengths must match and be > 0")
    P_o = sum(1 for a, b in zip(y1, y2) if a == b) / n
    n1_0, n1_1 = sum(1 for a in y1 if a == 0), sum(1 for a in y1 if a == 1)
    n2_0, n2_1 = sum(1 for a in y2 if a == 0), sum(1 for a in y2 if a == 1)
    P_e = (n1_0 * n2_0 + n1_1 * n2_1) / (n * n)
    if P_e >= 1.0:
        return 1.0
    return (P_o - P_e) / (1.0 - P_e)


# ---------------------------------------------------------------------------
# Paths (relative to script dir)
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
LLM_FILTER_DIR = SCRIPT_DIR / "LLM_filter"
SAMPLED_FILE = "sampled_308_p1.json"
LABELING_CSV = "sampled_308_p2.csv"
# You can put 3, 5, or any number (>=1) of model result files here.
MODEL_FILES = [
    "reason_results_gemini-3-flash-preview.json",
    "reason_results_glm-5.json",
    "reason_results_qwen3-max.json",
]


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def binarize_model_tier1(tier_1: str) -> int:
    """Model JSON: Unclear -> 1, otherwise -> 0."""
    return 1 if tier_1 == "Unclear" else 0


def binarize_human_csv_tier1(raw: str) -> Optional[int]:
    """Human CSV: Clear/clear -> 0; other non-empty -> 1; empty -> None (skip)."""
    s = (raw or "").strip()
    if not s:
        return None
    if s.lower() == "clear":
        return 0
    return 1


def build_rule_id_to_tier1(data: list) -> dict:
    """From list of rule objects, build rule_id -> binarized tier_1 (model)."""
    out = {}
    for obj in data:
        rid = obj.get("rule_id")
        if rid is None:
            continue
        out[rid] = binarize_model_tier1(obj.get("tier_1", ""))
    return out


def build_rule_id_to_tier1_raw(data: list) -> dict:
    """From list of rule objects, build rule_id -> raw tier_1 string."""
    out = {}
    for obj in data:
        rid = obj.get("rule_id")
        if rid is None:
            continue
        out[rid] = obj.get("tier_1", "") or ""
    return out


def load_labeling_csv(path: Path) -> tuple[list[str], dict[str, int], dict[str, str]]:
    """First occurrence per rule_id; skip empty tier_1. Returns ordered rule_ids, bin, raw."""
    order: list[str] = []
    bin_out: dict[str, int] = {}
    raw_out: dict[str, str] = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rid = (row.get("rule_id") or "").strip()
            if not rid or rid in bin_out:
                continue
            raw = row.get("tier_1") or ""
            b = binarize_human_csv_tier1(raw)
            if b is None:
                continue
            bin_out[rid] = b
            raw_out[rid] = raw.strip()
            order.append(rid)
    return order, bin_out, raw_out


def majority_vote(values: list[int]) -> int:
    """Majority vote for binary 0/1 list. Tie-break: 0 (non-Unclear)."""
    if not values:
        raise ValueError("majority_vote requires at least one value")
    s = sum(values)
    return 1 if s > (len(values) / 2) else 0


def interpret_kappa(kappa: float) -> str:
    if kappa < 0:
        return "Poor"
    elif kappa < 0.20:
        return "Slight"
    elif kappa < 0.40:
        return "Fair"
    elif kappa < 0.60:
        return "Moderate"
    elif kappa < 0.80:
        return "Substantial"
    else:
        return "Almost Perfect"


def load_model_file_maps():
    file_to_tier1 = {}
    file_to_tier1_raw = {}
    for filename in MODEL_FILES:
        path = LLM_FILTER_DIR / filename
        if not path.exists():
            raise FileNotFoundError(filename)
        data = load_json(path)
        file_to_tier1[filename] = build_rule_id_to_tier1(data)
        file_to_tier1_raw[filename] = build_rule_id_to_tier1_raw(data)
    return file_to_tier1, file_to_tier1_raw


def align_with_models(
    rule_ids: list[str],
    y_ref: list[int],
    file_to_tier1: dict,
) -> tuple[list[str], list[int], dict[str, list[int]]]:
    """Filter to rule_ids present in all model files; return aligned lists per file."""
    rule_ids_ok = []
    y_ok = []
    aligned_by_file = {filename: [] for filename in MODEL_FILES}
    for rid, y in zip(rule_ids, y_ref):
        values = []
        missing = False
        for filename in MODEL_FILES:
            v = file_to_tier1[filename].get(rid)
            if v is None:
                missing = True
                break
            values.append(v)
        if missing:
            continue
        rule_ids_ok.append(rid)
        y_ok.append(y)
        for filename, v in zip(MODEL_FILES, values):
            aligned_by_file[filename].append(v)
    return rule_ids_ok, y_ok, aligned_by_file


def report_kappa_block(
    title: str,
    ref_name: str,
    y_ref: list[int],
    rule_ids_ok: list[str],
    aligned_by_file: dict[str, list[int]],
    majority_list: list[int],
    ref_raw_by_rid: dict[str, str],
    file_to_tier1_raw: dict,
    print_disagree_vs_majority: bool,
) -> tuple[dict[str, float], float]:
    n = len(y_ref)
    print("=" * 70)
    print(title)
    print("=" * 70)
    print(f"Using {n} rules (all present in {ref_name} + {len(MODEL_FILES)} LLM files).")

    def report(name: str, y_other: list):
        assert len(y_ref) == len(y_other)
        k = cohen_kappa_score(y_ref, y_other)
        agree = sum(1 for a, b in zip(y_ref, y_other) if a == b)
        print(f"  Kappa = {k:.4f}  ({interpret_kappa(k)})  Agreement = {agree}/{n} ({100 * agree / n:.1f}%)")
        return k

    print(f"\n--- {ref_name} vs each model file ({len(MODEL_FILES)} files) ---")
    per_file_kappa = {}
    for filename in MODEL_FILES:
        per_file_kappa[filename] = report(filename, aligned_by_file[filename])

    print(f"\n--- {ref_name} vs majority of the {len(MODEL_FILES)} files ---")
    k_majority = report("majority", majority_list)

    if print_disagree_vs_majority:
        disagree_idx = [i for i in range(n) if y_ref[i] != majority_list[i]]
        if disagree_idx:
            print(f"\n--- Differing rule_ids ({ref_name} vs majority): {len(disagree_idx)} rules ---")
            short_names = [f.replace("reason_results_", "").replace(".json", "") for f in MODEL_FILES]
            labels = ["rule_id", ref_name] + short_names
            w_id = max(10, max(len(rid) for rid in rule_ids_ok))
            w_col = 28
            widths = [w_id] + [w_col] * (len(labels) - 1)
            header = "  ".join(labels[j].ljust(widths[j]) for j in range(len(labels)))
            print(header)
            print("-" * len(header))
            for i in disagree_idx:
                rid = rule_ids_ok[i]
                cells = [ref_raw_by_rid.get(rid, "")]
                for filename in MODEL_FILES:
                    cells.append(file_to_tier1_raw[filename].get(rid, ""))
                cells = [str(c)[:w_col] + ("..." if len(str(c)) > w_col else "") for c in cells]
                line = rid.ljust(widths[0]) + "  " + "  ".join(c.ljust(w_col) for c in cells)
                print(line)
        else:
            print(f"\n--- Differing rule_ids ({ref_name} vs majority): 0 rules (full agreement) ---")

    return per_file_kappa, k_majority


def main():
    if len(MODEL_FILES) == 0:
        print("Error: MODEL_FILES is empty.")
        return

    file_to_tier1, file_to_tier1_raw = load_model_file_maps()
    for filename in MODEL_FILES:
        print(f"Loaded {filename}: {len(file_to_tier1[filename])} rules by rule_id")

    # ----- Block 1: reconciled sampled JSON -----
    sampled_path = SCRIPT_DIR / SAMPLED_FILE
    sampled_data = load_json(sampled_path)
    if not isinstance(sampled_data, list):
        print(f"Error: {SAMPLED_FILE} is not a JSON array")
        return
    rule_ids = [obj["rule_id"] for obj in sampled_data if obj.get("rule_id") is not None]
    sampled_tier1 = [
        binarize_model_tier1(obj.get("tier_1", ""))
        for obj in sampled_data
        if obj.get("rule_id") is not None
    ]
    n0 = len(rule_ids)
    print(f"\nLoaded {SAMPLED_FILE}: {n0} rules")
    if n0 == 0:
        print("No rules found. Abort.")
        return

    sampled_rule_id_to_tier1_raw = build_rule_id_to_tier1_raw(sampled_data)
    rule_ids_ok, y_ref, aligned = align_with_models(
        rule_ids, sampled_tier1, file_to_tier1
    )
    n_skip = n0 - len(rule_ids_ok)
    if n_skip > 0:
        print(f"Skipped {n_skip} rule_ids not present in all {len(MODEL_FILES)} LLM files (sampled block).")
    majority_list = [
        majority_vote([aligned[filename][i] for filename in MODEL_FILES])
        for i in range(len(rule_ids_ok))
    ]

    sampled_per_file_kappa, k_gm = report_kappa_block(
        f"Kappa: {SAMPLED_FILE} vs {len(MODEL_FILES)} LLM files (tier_1: Unclear vs non-Unclear)",
        "Sampled_308",
        y_ref,
        rule_ids_ok,
        aligned,
        majority_list,
        sampled_rule_id_to_tier1_raw,
        file_to_tier1_raw,
        print_disagree_vs_majority=True,
    )

    # ----- Block 2: labeling CSV -----
    csv_path = SCRIPT_DIR / LABELING_CSV
    if not csv_path.exists():
        print(f"\nError: file not found: {LABELING_CSV}")
        return
    csv_rule_ids, csv_bin, csv_raw = load_labeling_csv(csv_path)
    csv_y = [csv_bin[rid] for rid in csv_rule_ids]
    n_csv0 = len(csv_rule_ids)
    print(f"\nLoaded {LABELING_CSV}: {n_csv0} rules with non-empty tier_1 (first occurrence per rule_id)")

    rule_ids_ok2, y_ref2, aligned2 = align_with_models(csv_rule_ids, csv_y, file_to_tier1)
    n_skip2 = n_csv0 - len(rule_ids_ok2)
    if n_skip2 > 0:
        print(f"Skipped {n_skip2} CSV rule_ids not present in all {len(MODEL_FILES)} LLM files.")
    if len(rule_ids_ok2) == 0:
        print(f"No overlapping rules between CSV and {len(MODEL_FILES)} LLM files. Abort CSV block.")
    else:
        maj2 = [
            majority_vote([aligned2[filename][i] for filename in MODEL_FILES])
            for i in range(len(rule_ids_ok2))
        ]
        csv_per_file_kappa, k_cm = report_kappa_block(
            f"Kappa: {LABELING_CSV} vs {len(MODEL_FILES)} LLM files (human: Clear vs other; model: Unclear vs other)",
            "CSV_human",
            y_ref2,
            rule_ids_ok2,
            aligned2,
            maj2,
            csv_raw,
            file_to_tier1_raw,
            print_disagree_vs_majority=True,
        )

    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"[{SAMPLED_FILE}]")
    for filename in MODEL_FILES:
        print(f"  vs {filename}: {sampled_per_file_kappa[filename]:.4f}")
    print(f"  vs majority ({len(MODEL_FILES)} files): {k_gm:.4f}")
    if len(rule_ids_ok2) > 0:
        print(f"[{LABELING_CSV}]")
        for filename in MODEL_FILES:
            print(f"  vs {filename}: {csv_per_file_kappa[filename]:.4f}")
        print(f"  vs majority ({len(MODEL_FILES)} files): {k_cm:.4f}")


if __name__ == "__main__":
    main()
