"""
Merge rules with can_detect=true in all three filter result files with matching file_diffs entries;
write combined JSON objects to rule_judge.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Set, Optional

# Same three filter result files as in calculate_multi_kappa.py
FILTER_FILES = [
    "filter_results_gemini-3-flash-preview.json",
    "filter_results_qwen3-max.json",
    "filter_results_glm-5.json",
]

SCRIPT_DIR = Path(__file__).resolve().parent
FILE_DIFFS_DIR = SCRIPT_DIR.parent.parent / "rq2_1_evolved_rules" / "file_diffs"
RULE_JUDGE_DIR = SCRIPT_DIR.parent / "rule_judge"
OUTPUT_FILENAME = "detect_rules2.json"


def load_json_list(file_path: Path) -> List[Dict[str, Any]]:
    """Load JSON file; expected to be an array."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []
        return data
    except (json.JSONDecodeError, OSError) as e:
        print(f"Warning: could not load {file_path}: {e}")
        return []


def get_rule_ids_can_detect_all(
    filter_dir: Path, filenames: List[str]
) -> Set[str]:
    """rule_ids where can_detect is True in every filter file."""
    rule_id_to_flags: Dict[str, List[bool]] = {}

    for name in filenames:
        path = filter_dir / name
        if not path.is_file():
            print(f"Warning: file not found {path}")
            continue
        items = load_json_list(path)
        for item in items:
            rid = item.get("rule_id")
            if rid is None:
                continue
            if rid not in rule_id_to_flags:
                rule_id_to_flags[rid] = []
            rule_id_to_flags[rid].append(item.get("can_detect") is True)

    # rule_id present in every file with can_detect True in each
    result = set()
    n_files = len(filenames)
    for rid, flags in rule_id_to_flags.items():
        if len(flags) == n_files and all(flags):
            result.add(rid)
    return result


def build_filter_by_rule_id(
    filter_dir: Path, filenames: List[str], rule_ids: Set[str]
) -> Dict[str, Dict[str, Any]]:
    """First available filter file: rule_id -> full filter object (rule_ids only)."""
    for name in filenames:
        path = filter_dir / name
        if not path.is_file():
            continue
        items = load_json_list(path)
        by_id = {}
        for item in items:
            rid = item.get("rule_id")
            if rid in rule_ids:
                by_id[rid] = dict(item)
        if by_id:
            return by_id
    return {}


def collect_file_diffs_by_id(diffs_dir: Path) -> Dict[str, Dict[str, Any]]:
    """Scan all .json under file_diffs; collect by id (keep first occurrence)."""
    id_to_diff: Dict[str, Dict[str, Any]] = {}
    if not diffs_dir.is_dir():
        return id_to_diff
    for jpath in sorted(diffs_dir.rglob("*.json")):
        items = load_json_list(jpath)
        for item in items:
            rid = item.get("id")
            if rid is not None and rid not in id_to_diff:
                id_to_diff[rid] = dict(item)
    return id_to_diff


# Merged field order: rule_id, rule_content; diff fields; can_detect/detection_* last
DIFF_KEYS_ORDER = [
    "change_type", "project", "file", "commit_id",
    "first_level", "second_level", "constraint_degree",
]
TAIL_KEYS = ["can_detect", "detection_targets", "detection_logic"]


def merge_filter_and_diff(
    filter_obj: Dict[str, Any], diff_obj: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """Merge filter and file_diff: keep rule_id/rule_content; drop id/content/reason_for_false; detection fields last."""
    out: Dict[str, Any] = {}
    # 1. rule_id, rule_content
    out["rule_id"] = filter_obj.get("rule_id")
    out["rule_content"] = filter_obj.get("rule_content")
    # 2. file_diff fields (excluding id, content)
    for k in DIFF_KEYS_ORDER:
        if diff_obj and k in diff_obj:
            out[k] = diff_obj[k]
        else:
            out[k] = None
    # 3. trailing detection fields
    for k in TAIL_KEYS:
        out[k] = filter_obj.get(k)
    return out


def main() -> None:
    filter_dir = SCRIPT_DIR
    rule_ids = get_rule_ids_can_detect_all(filter_dir, FILTER_FILES)
    print(f"Rule IDs with can_detect=true in all 3 files: {len(rule_ids)}")

    filter_by_id = build_filter_by_rule_id(filter_dir, FILTER_FILES, rule_ids)
    print(f"Filter records for those IDs: {len(filter_by_id)}")

    diff_by_id = collect_file_diffs_by_id(FILE_DIFFS_DIR)
    print(f"File-diff entries (by id) total: {len(diff_by_id)}")

    merged: List[Dict[str, Any]] = []
    for rid in sorted(rule_ids):
        fobj = filter_by_id.get(rid)
        if not fobj:
            continue
        dobj = diff_by_id.get(rid)
        merged.append(merge_filter_and_diff(fobj, dobj))

    RULE_JUDGE_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RULE_JUDGE_DIR / OUTPUT_FILENAME
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    print(f"Written {len(merged)} merged objects to {out_path}")


if __name__ == "__main__":
    main()
